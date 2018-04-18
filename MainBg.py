import sys,tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt
import matplotlib
from Sentiment_Analysis.Common.DataBase import Database
import pymongo


class SentimentAnalysis:
    Database.initialize()
    Pos_per = 0
    neg_per = 0
    neu_per = 0
    Poll_per = 0
    gen_report=0
    store_query=0

    def __init__(self):
        self.tweets = []
        self.tweetText = []
        self.search_query=0
        self.tweet_text=[]


    def DownloadData(self):
        # authenticating
        consumerKey = 'jhLraSRJGkttSvsyfgSB6iShM'
        consumerSecret = 'VJVFTzOxm8KHONC0NAPMFRvRhcKnZ26uHzFPwBhS1TUZtyWJs7'
        accessToken = '782676766158491649-giy0oVUWsPDIlt8CFXnuy0klhjF1juH'
        accessTokenSecret = 'xJeHzjPZMfbvUDS1aREbEndaIi6xW2Y3M1CROtlijkp2e'
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)

        global search_query
        global gen_report


        # input for term to be searched and how many tweets to search

        searchTerm =input("Enter Keyword/Tag to search about: ")m
        self.search_query=searchTerm
        NoOfTerms = int(input("Enter how many tweets to search: "))

        # searching for tweets
        self.tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)

        # Open/create a file to append data to
        csvFile = open('result.csv', 'a')
        # Use csv writer
        csvWriter = csv.writer(csvFile)


        # creating some variables to store info
        polarity = 0
        positive=0
        neutral=0
        negative=0


        # iterating through tweets fetched
        for tweet in self.tweets:


            #Append to temp so that we can store in csv later. I use encode UTF-8
            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
            # print (tweet.text.translate(non_bmp_map))    #print tweet's text
            self.tweet_text.append(tweet.text)



            analysis = TextBlob(tweet.text)
            # print(analysis.sentiment)  # print tweet's polarity
            analysis_sub=analysis.sentiment.polarity
            polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

            if (analysis_sub == 0):  # adding reaction of how people are reacting to find average later
                neutral += 1
            elif (analysis_sub > 0 and analysis_sub <= 1):
                positive += 1
            elif (analysis_sub > -1 and analysis_sub <= 0):
                negative += 1




        # Write to csv and close csv file
        csvWriter.writerow(self.tweetText)
        csvFile.close()


        # finding average of how people are reacting
        positive_num = self.percentage(positive, NoOfTerms)


        negative_num= self.percentage(negative, NoOfTerms)

        neutral_num = self.percentage(neutral, NoOfTerms)

       # global neg_per
        #global Pos_per
        #global neu_per
        #global Poll_per
        # finding average reaction
        polarity_num = polarity / NoOfTerms


        # printing out da
        print("How people are reacting on " + searchTerm + " by analyzing " + str(NoOfTerms) + " tweets.")
        print()
        print("General Report: ")

        if (polarity_num== 0):
            SentimentAnalysis.gen_report = "Neutral"
            print("Neutral")
        elif (polarity_num > 0 and polarity_num<= 0.3):
            SentimentAnalysis.gen_report = "Weakly Positive"
            print("Weakly Positive")
        elif (polarity_num > 0.3 and polarity_num <= 0.6):
            SentimentAnalysis.gen_report = "Positive"
            print("Positive")
        elif (polarity_num > 0.6 and polarity_num <= 1):
            SentimentAnalysis.gen_report = "Strongly Positive"
            print("Strongly Positive")
        elif (polarity_num > -0.3 and polarity_num <= 0):
            SentimentAnalysis.gen_report = "Weakly Negative"
            print("Weakly Negative")
        elif (polarity_num > -0.6 and polarity_num <= -0.3):
            SentimentAnalysis.gen_report = " Negative"
            print("Negative")
        elif (polarity_num > -1 and polarity_num <= -0.6):
            SentimentAnalysis.gen_report="Strongly Negative"
            print("Strongly Negative")

        print()
        print("Detailed Report: ")
        print(str(positive_num) + "% people thought it was positive")

        print(str(negative_num) + "% people thought it was negative")

        print(str(neutral_num) + "% people thought it was neutral")
        SentimentAnalysis.neg_per = negative_num
        SentimentAnalysis.Pos_per = positive_num
        SentimentAnalysis.neu_per = neutral_num
        SentimentAnalysis.Poll_per = polarity_num
        Database.insert(collection='USERS', data=self.json())

        self.plotPieChart(positive_num,  negative_num, neutral_num, searchTerm, NoOfTerms)



    def json(self):
        return {
        'query':self.search_query,
        'tweets':self.tweet_text,
        'negative':SentimentAnalysis.neg_per,
        'positive':SentimentAnalysis.Pos_per,
        'neutral':SentimentAnalysis.neu_per,
        'polarity':SentimentAnalysis.Poll_per,
        'General Report':SentimentAnalysis.gen_report

        }


    def retrieve(self,name):
        return Database.find(collection='USERS',query={'query':name})

    def cleanTweet(self, tweet):
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    # function to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def plotPieChart(self, positive, negative, neutral, searchTerm, noOfSearchTerms):
        labels = ['Positive [' + str(positive) + '%]',  'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]' ]
        sizes = [positive, neutral, negative]
        colors = ['yellowgreen','gold', 'red']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()
        plt.savefig("image")




if __name__== "__main__":
    sa = SentimentAnalysis()
    sa.DownloadData()

