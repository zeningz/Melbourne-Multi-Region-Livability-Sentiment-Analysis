"""
Author: Wei Ge - 1074198
        Han Wang - 1041260 
        YanBei Jiang - 1087029
        Yiwen Zhang - 1002781
        Zening Zhang - 1078374
"""
import mmap
import json
from time import sleep
import db_load_data as db
import threading

class OldDataRead(threading.Thread):

    backup_end_line = 0
    twitter_file = ""

    def __init__(self, backup_end_line, twitter_file):
        threading.Thread.__init__(self)
        self.backup_end_line = backup_end_line
        self.twitter_file = twitter_file

    def read_data_file(self):

        # read the file
        with open(self.twitter_file, "r") as f:
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            # count line
            curr_line = -1

            # filter the twitter data to match grid
            for line in iter(mm.readline, b""):
                # count how many lines be read
                curr_line += 1

                # does not store until touch the backup line
                if (curr_line <= self.backup_end_line):
                    continue

                # get the information from the current line
                line_json = self.get_row_language_info(line)

                # store the json format line into old data backup database
                if (line_json != False):
                    db.store_to_old_data_backup_db(line_json)
            
            mm.close()
        f.close()


    def get_row_language_info(self, line):
            '''
            Capture grid id and language from twitter file's line

            :param line: row from twitter file
            :return boolean / the line in json format
            '''

            # convert current line from byte to string format
            line = line.decode('utf8')
            # remove useless element and convert current line to json format
            line = line.replace('"location":"melbourne"}},', '"location":"melbourne"}}')
            line = line.replace('"location":"melbourne"}}]}', '"location":"melbourne"}}')

            # convert current line from string to json format 
            try:
                line = json.loads(line) 
            except:
                #print(line)
                return False
            
            return line
    
    def run(self):
        self.read_data_file()
