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

class StreamListener(threading.Thread, tweepy.Cursor):

    count = 1
    data_since = strftime("%Y-%m-%d_%H:%M:%S", gmtime())
    result_dict ={data_since:[]}
    file_name = data_since[:10]+'.json'
    start_time = time.perf_counter()
 

    # initialize
    def __init__(self, api_key, api_key_secret, access_token, access_token_secret, keywords,datetime_until,key_val,thread_name):
        threading.Thread.__init__(self)
        auth = tweepy.OAuthHandler(api_key, api_key_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth,wait_on_rate_limit=True)
        tweepy.Cursor.__init__(self, api.search_tweets, q=keywords['track'], geocode=keywords['locations'],lang = keywords['languages'], count=1000, until = datetime_until, tweet_mode='extended')
        self.key_val = key_val
        self.thread_name = thread_name



    # Override Thread
    def run(self):

        dataset = self.items(100000)
        
        for data in dataset:
            try:
                # read the data
                data_raw = data._json
                place = data_raw['place']

                json_data = {"id":data_raw['id'],"doc":data_raw}
                # print(self.key_val)
                if  place != None:
                    # store data to db
                    db_load_data.store_to_new_data_backup_db(json_data)
                    # print(self.key_val)
                    # count the number
                    self.count+=1
                    print('\r' + self.thread_name + ' get ' + str(self.count) + ' tweets by search now.')

            except KeyError as e:
                # escapse the escapse
                return True

            except BaseException as e:
                print("----------Exception made. Data printed below----------")
                print(data)
                print(e)
                print("------------------------------------------------------\n")
        time.sleep(10)
        return True






