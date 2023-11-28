"""
Author: Wei Ge - 1074198
        Han Wang - 1041260 
        YanBei Jiang - 1087029
        Yiwen Zhang - 1002781
        Zening Zhang - 1078374
"""
import configparser
import io
import json
import datetime
import schedule
import tweepy_search_crawler
import tweepy_stream_crawler
import db_load_data
import read_data
from pytz import utc

old_data_bacup_line = 0

def set_configuration():
    '''
    Set the configuration for crawlers
    '''
    # get the key words for each crawler to search
    keywords_file = 'search_keywords_search.json'
    # read the json with key words
    keywords = []
    with io.open(keywords_file,'r') as f:
        keywords = json.load(f)

    # get the configuration of crawler
    config_file = 'crawler_config.ini'
    # read the configuration
    try:
        # read the configuration file
        config = configparser.ConfigParser()
        config.read(config_file)
        # curr_key_words records each crawler's key words from keywords list
        curr_key_words = 0
    
        # initilize each crawler followed by assigning key searching word to it
        for i in config.sections():
            # set the configuration
            api_key = config[i]['api_key']
            api_key_secret = config[i]['api_key_secret']

            access_token = config[i]['access_token']
            access_token_secret = config[i]['access_token_secret']
            datetime_until  = (datetime.datetime.now().astimezone(utc) - datetime.timedelta(days = 6)).strftime("%Y-%m-%d")
            globals()['listener_search_'+i] = tweepy_search_crawler.StreamListener(
                                                                            api_key, api_key_secret, access_token, access_token_secret, 
                                                                            (keywords[list(keywords.keys())[curr_key_words]]),
                                                                            datetime_until,
                                                                            (list(keywords.keys())[curr_key_words]),
                                                                            "Thread_"+str(curr_key_words))
            # move to the next key words should be searched
            curr_key_words+=1
        print("Initialize the Crawlers Successfully.\n")

    except KeyError:
        print('\nSet Search Crawler: Missing the key of Api or Access, please check the file')
        exit(1)



def start_crawlers_search():
    '''
    Start the crawlers to manipulate the data through search
    '''
    # initialize the crawlers
    print("Initialize the Search Crawlers")
    set_configuration()

    # start the crawlers
    print("Start Search Crawlers")
    listener_search_account_1.start()
    listener_search_account_2.start()
    listener_search_account_3.start()
    print("Start Three Search Crawlers Successfully\n")
    
    # assign the work to re-start all thread each 15 minutes
    #schedule.every(15).minutes.do(restart_crawlers)

    # while (True):
    #     schedule.run_pending()
        

def initialize_db():
    '''
    Provide the API to initialize the couch db
    '''
    db_load_data.initialize_couchdb()



def set_configuration_stream():
    '''
    Set the configuration for crawlers
    '''
    # get the key words for each crawler to search
    keywords_stream_file = 'search_keywords_stream.json'
    # read the json with key words
    keywords_stream = []
    with io.open(keywords_stream_file,'r') as f:
        keywords_stream = json.load(f)

    # get the configuration of crawler
    config_stream_file = 'crawler_config.ini'
    # read the configuration
    try:
        # read the configuration file
        config = configparser.ConfigParser()
        config.read(config_stream_file)
        # curr_key_words records each crawler's key words from keywords list
        curr_key_words = 0
    
        # initilize each crawler followed by assigning key searching word to it
        for i in config.sections():
            # set the configuration
            api_key = config[i]['api_key']
            api_key_secret = config[i]['api_key_secret']
            access_token = config[i]['access_token']
            access_token_secret = config[i]['access_token_secret']
            globals()['listener_stream_'+i] = tweepy_stream_crawler.StreamListener(
                                                    api_key, api_key_secret, access_token, access_token_secret, 
                                                    (keywords_stream[list(keywords_stream.keys())[curr_key_words]]),
                                                    (list(keywords_stream.keys())[curr_key_words]),
                                                    "Thread_"+str(curr_key_words))
            
            # move to the next key words should be searched
            curr_key_words +=1
        print("Initialize the Stream Crawlers Successfully.\n")

    except KeyError:
        print('\nSet Stream Crawler: Missing the key of Api or Access, please check the file')
        exit(1)


def start_crawlers_stream():
    '''
    Start the crawlers to manipulate the data through stream
    '''
    # initialize the crawlers
    print("Initialize the Stream Crawlers")
    set_configuration_stream()

    # start the crawlers
    print("Start Crawlers")
    listener_stream_account_1.start()
    listener_stream_account_2.start()
    listener_stream_account_3.start()
    print("Start Three Stream Crawlers Successfully\n")
    
    # assign the work to re-start all thread each 15 minutes
    #schedule.every(15).minutes.do(restart_crawlers)

    # while (True):
    #     schedule.run_pending()


def initialize_backup():
    '''
    Get the backup information from file
    '''
    global old_data_bacup_line

    # get the configuration of backup
    config_stream_file = 'db_backup.ini'
    # read the configuration
    try:
        config = configparser.ConfigParser()
        config.read(config_stream_file)
        old_data_bacup_line = int(config['old_data']['end'])

    except KeyError:
        print('\nBackup: Missing the key of Api or Access, please check the file')
        exit(1)



# initialize the db
initialize_db()

# initialize back-up set
initialize_backup()

#start reading the old data
old_data_reader = read_data.OldDataRead(old_data_bacup_line, "./twitter-melb.json")
old_data_reader.start()

# # start crawlers
start_crawlers_stream()

# daily search
schedule.every().day.at("16:15").do(start_crawlers_search)
# daily stream
schedule.every().day.at("17:00").do(start_crawlers_stream)
# start the schedule
while(True):
    schedule.run_pending()
