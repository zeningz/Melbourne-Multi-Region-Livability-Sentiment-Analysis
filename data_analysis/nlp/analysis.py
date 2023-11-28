"""
Author: Wei Ge - 1074198
        Han Wang - 1041260 
        YanBei Jiang - 1087029
        Yiwen Zhang - 1002781
        Zening Zhang - 1078374
"""
import json
from nlp.sentiment_polarity import *
#from topic_extraction import *

def old_tweet_analysis(tweet_obj):
    new_tweet_obj = {}
    for key in tweet_obj.keys():
        if key != "_id" and key != "_rev":
            new_tweet_obj[key] = tweet_obj[key]
    text = new_tweet_obj["doc"]["text"]
    if new_tweet_obj["doc"]["place"]:
        coordinates = new_tweet_obj["doc"]["place"]["bounding_box"]["coordinates"][0]
        area = filter_area(coordinates)
        new_tweet_obj["melbourne_area"] = area
    else: 
        new_tweet_obj["melbourne_area"] = "other"
    processed_text = preprocess(text)
    sentiment = sentiment_analysis(processed_text)
    new_tweet_obj["sentiment"] = sentiment
    polarity = polarity_analysis(processed_text)
    new_tweet_obj["polarity"] = polarity
    
    new_tweet_obj["education"] = is_education_topic(processed_text)
    new_tweet_obj["house"] = is_house_topic(processed_text)
    time_list = new_tweet_obj["doc"]["created_at"].split(" ")
    new_tweet_obj["week"] = time_list[0]
    new_tweet_obj["day"] = time_list[2]
    new_tweet_obj["month"] = time_list[1]
    new_tweet_obj["year"] = time_list[5]
    return new_tweet_obj


def new_tweet_analysis(tweet_obj):
    for key in tweet_obj.keys():
        # only look at the third key (i.e. "Hoppers_Crossing_1522304716188700672_stream")
        if key != "_id" and key != "_rev" and key !="id":
            new_tweet_obj = tweet_obj[key]
            if new_tweet_obj["place"]:
                coordinates = new_tweet_obj["place"]["bounding_box"]["coordinates"][0]
                area = filter_area(coordinates)
                new_tweet_obj["melbourne_area"] = area
            else:
                new_tweet_obj["melbourne_area"] = "other"
            if "extended_tweet" in tweet_obj[key].keys():
                text = tweet_obj[key]["extended_tweet"]["full_text"]
                break
            elif "text" in tweet_obj[key].keys():
                text = tweet_obj[key]["text"]
                break
            else:
                text = ""
                break

    processed_text = preprocess(text)
    sentiment = sentiment_analysis(processed_text)
    new_tweet_obj["sentiment"] = sentiment
    polarity = polarity_analysis(processed_text)
    new_tweet_obj["polarity"] = polarity
    new_tweet_obj["education"] = is_education_topic(processed_text)
    new_tweet_obj["house"] = is_house_topic(processed_text)

    time_list = new_tweet_obj["created_at"].split(" ")
    new_tweet_obj["week"] = time_list[0]
    new_tweet_obj["day"] = time_list[2]
    new_tweet_obj["month"] = time_list[1]
    new_tweet_obj["year"] = time_list[5]
    return new_tweet_obj


def filter_area(coordinates):
    melbourne_city = [144.913581,-37.839086,144.994266,-37.781922]
    melbourne_kew = [144.999392,-37.855040,145.141140,-37.786685]
    Hoppers_Crossing = [144.633666,-37.974500,144.913581,-37.694900]
    left_bound = coordinates[0][0]
    right_bound = coordinates[2][0]
    top_bound = coordinates[1][1]
    down_bound = coordinates[0][1]
    center = [(left_bound+right_bound)/2, (top_bound+down_bound)/2]
    coordinates.append(center)
    for coordinate in coordinates:
        if Hoppers_Crossing[0] <= coordinate[0] <= Hoppers_Crossing[2] and Hoppers_Crossing[1] <= coordinate[1] <= Hoppers_Crossing[3]:
            return "Hoppers_Crossing"
        elif melbourne_kew[0] <= coordinate[0] <= melbourne_kew[2] and melbourne_kew[1] <= coordinate[1] <= melbourne_kew[3]:
            return "melbourne_kew" 
        elif melbourne_city[0] <= coordinate[0] <= melbourne_city[2] and melbourne_city[1] <= coordinate[1] <= melbourne_city[3]:
            return "melbourne_city"

    return "other"


def is_education_topic(text):
    text = text.lower()
    related_words = ["education","teacher","professor","tutor","student","university","graduation","school","tuition","middle school","primary school","high school","diploma","undergraduate","graduate","phd"]
    for word in related_words:
        if word in text:
            return 1
    return 0


def is_house_topic(text):
    text = text.lower()
    related_words = ["house price", "rent","house","apartment","property","home","accommodation","real estate"]
    for word in related_words:
        if word in text:
            return 1
    return 0
               

def preprocess(text):
    new_text = []
    for t in text.split(" "):
        if not t.startswith('@') and not t.startswith('http'):
            new_text.append(t)
    
    return " ".join(new_text)





