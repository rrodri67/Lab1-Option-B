#Raul Rodriguez
#Lab 1

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import praw

reddit = praw.Reddit(client_id= 'Wd-WRix4MLXfBQ',
                     client_secret= 'cHqEazflu9bUk_Pi8CjaF1SwTh8',
                     user_agent= 'utepcstest'
                     )


nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()


def get_text_negative_proba(text):
    return sid.polarity_scores(text)['neg']


def get_text_neutral_proba(text):
    return sid.polarity_scores(text)['neu']


def get_text_positive_proba(text):
    return sid.polarity_scores(text)['pos']


def get_submission_comments(url):
    submission = reddit.submission(url=url)
    submission.comments.replace_more()

    return submission.comments

       

def process_comments(comments):

    replies_list = []
    topCommentBody = ''
    commentLVL = 0
    
    if comments._comments[commentLVL].depth == 0:
        replies_list, _ =process_comments(comments._comments[commentLVL].replies)
        topCommentBody = comments._comments[commentLVL].body
    
    if comments._comments[0].depth == 0:
        for i in comments._comments:
            replies_list.append(i.body)
            print(i.body)
    
    return replies_list, topCommentBody
 

def main():
  
    comments = get_submission_comments('https://www.reddit.com/r/learnprogramming/comments/5w50g5/eli5_what_is_recursion/')
    replies_list, topCommentBody = process_comments(comments)
    for i in replies_list:
        negRank = get_text_negative_proba(i)
        posRank = get_text_positive_proba(i)
        neuRank = get_text_neutral_proba(i)
        
        rankList = [negRank, posRank, neuRank]
        
        maximum = max(rankList)
        
        if maximum == negRank:
            commOverallAttitude = 'Negative'
        elif maximum == posRank:
            commOverallAttitude = 'Positive'
        else:
            commOverallAttitude = 'Neutral'
            
        print('Reply had highest ' + commOverallAttitude + ' score of: ' + str(maximum))
            
    
 

main()
