"""
Author: Wei Ge - 1074198
        Han Wang - 1041260 
        YanBei Jiang - 1087029
        Yiwen Zhang - 1002781
        Zening Zhang - 1078374
"""
import io
import time
import json
from time import gmtime, strftime
import tweepy
import threading
import configparser
import os.path
import db_load_data
import datetime

class StreamListener(threading.Thread, tweepy.Stream):

    count = 1
    data_since = strftime("%Y-%m-%d_%H:%M:%S", gmtime())
    result_dict ={data_since:[]}
    file_name = data_since[:10]+'.json'
    start_time = time.perf_counter()


    # initialize
    def __init__(self, api_key, api_key_secret, access_token, access_token_secret, keywords, key_val,thread_name):
        threading.Thread.__init__(self)
        tweepy.Stream.__init__(self, api_key, api_key_secret, access_token, access_token_secret)
        self.keywords = keywords
        self.thread_name = thread_name
        self.key_val = key_val


    # Override Tweepy.Stream
    def on_data(self, data):
        now_time = int(datetime.datetime.now().now().strftime('%H%M'))
        if now_time > 1600 and now_time < 1602:
            print("Disconnect one Stream Crawler.\n")
            self.disconnect()
        # dur_for_sleep = time.perf_counter() - self.start_time
        # if dur_for_sleep>14*60:
        #     print('\nHave runned %d second' %dur_for_sleep)
        #     print('I have to sleep')
        #     time.sleep(15*60)
        try:
            # read the data
            data_raw = json.loads(data)
            place = data_raw['place']
            json_data = {"id":data_raw['id'],"doc":data_raw}
            if  place != None:
                # store data to db
                db_load_data.store_to_new_data_backup_db(json_data)
                # count the number
                self.count+=1
                print('\r' + self.thread_name + ' get ' + str(self.count) + ' tweets by stream now.')
                # print(data_label)
                # store to file
                # if os.path.isfile(self.file_name):
                #     with io.open(self.file_name, 'r') as f:
                #         content = json.load(f) 
                #     content.update(json_data)
                #     with io.open(self.file_name,'w') as f:
                #         json.dump(content,f,indent = 2)
                # else:
                #     with io.open(self.file_name,'w') as f:
                #         json.dump(json_data,f,indent = 2)
                # show the processing
                # i = self.count%10
                # a = '*' * i
                # b = '.' * (10-i)
                # c = (i/10)*100
                # dur = time.perf_counter()-self.start_time
                # if (self.thread_name == "Thread_0"):
                #     print('\n'+self.thread_name + ': {:^3.0f}%[{}->{}]{:.2f}s'.format(c,a,b,dur),end='')
                # elif (self.thread_name == "Thread_1"):
                #     print('\n'+self.thread_name + ': {:^3.0f}%[{}->{}]{:.2f}s'.format(c,a,b,dur),end='')
                # else:
                #     print('\n'+self.thread_name + ': {:^3.0f}%[{}->{}]{:.2f}s'.format(c,a,b,dur),end='')

                # if self.count %10 == 0:
                #     print('\nHave crawled %d twitter' %self.count)
                
                # print(self.count)

                # if self.count == 10:
                #     self.disconnect()

        except KeyError as e:
            # escapse the escapse
            return True

        except BaseException as e:
            print("----------Exception made. Data printed below----------")
            print(data)
            print(e)
            print("------------------------------------------------------\n")
        # time.sleep(0.5)
        return True


    # Override Stream
    def on_error(self, status_code):
        
        if status_code == 420:
            self.wait()
            print(self.thread_name + ' suspends because of 420.')
        elif status_code == 429:
            self.wait()
            print(self.thread_name + ' suspends because of 429.')
        else:
            self.wait()
            print('Unknown error during calling Tweet API')


    # Override Thread
    def run(self):
        # get the searching key words
        language_val = self.keywords['languages']
        track_val = self.keywords['track']
        locations_val = self.keywords['locations']

        # start filter
        self.filter(languages=language_val, track=track_val, locations=locations_val)


    """
    def on_status(self, status):
        if status.retweeted:
            return
    """




