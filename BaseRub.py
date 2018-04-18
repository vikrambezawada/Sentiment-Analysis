from flask import Flask,render_template,request,session,jsonify
import jinja2
import pymongo
from DEM_files.Git_Ali_Copy import SentimentAnalysis
from Sentiment_Analysis.Common.DataBase import Database
import sys,tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt



app=Flask(__name__)
app.secret_key="Vikram"
client=pymongo.MongoClient()
db=client["TweetBase"]
collection=db["USERS"]
api=0

"""sent_object = SentimentAnalysis()
sent_object.DownloadData()
tweets=sent_object.tweets"""
search_tweet=0
tweets=0


def return_query(name):
    return {

        "id":1,
        "query":name
    }
def insert_query(item):
    Database.insert(collection="Queries",data=return_query(item))



@app.route('/')
def main_page():

    return render_template('real_base.html')



@app.route('/base_html', methods=['POST','GET'])
def search_query():
    store_item=request.form['search_item']
    session['search_item']=store_item
    global search_tweet
    search_tweet=session['search_item']
    insert_query(search_tweet)

    td = Database.find_one(collection='USERS', query={'query': search_tweet})

    return render_template('Show_table.html', tweet_name=td['query'],np=td['negative'],pp=td['positive'],nep=td['neutral'],Gt=td['General Report'])

"""@app.route('/tweets')
def queries(search_tweet):

    data=Database.find(collection="USERS",query={'query':search_tweet})
    return render_template('print_tweets.html',tweetsy=data)"""


"""@app.route('/show_pers')
def show_perst():
    tweet_data= Database.find_one(collection='USERS',query={'query':'Virat Kohli'})

    return render_template("show_per.html",tweet_name=tweet_data['query'])"""








if __name__ == "__main__":

    app.run(debug=True)