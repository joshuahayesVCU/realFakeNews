# Author: Joshua Hayes

# The web scraping tool used to gather headlines and links for the guessing game
# Utilizes the Reddit API to gather data
# tutorial from https://medium.com/geekculture/how-to-extract-reddit-posts-for-an-nlp-project-56d121b260b4

import praw

# Creating a scraper instance using the Reddit class inside praw's library

# Define user agent
# This is what access the data
user_agent = "praw_scraper"

# Create an instance of reddit class
reddit = praw.Reddit(client_id = "kJ7QyvYqKCvHNOg3gV59cA",
                     client_secret = "hI7CLLMKjD7Lq2IZu_XkWRehd3saqQ",
                     user_agent = user_agent)

# specifying the subreddit to scrape the data from
subreddit_name = "nottheonion"
subreddit = reddit.subreddit(subreddit_name)

print(subreddit.display_name)

# importing the pandas library and creating a data frame
import pandas as pd
df = pd.DataFrame()

# list to store details of scraped post
titles = []
url = []
scores = []

# accessing the new posts using a loop
for submission in subreddit.hot(limit=20):
    titles.append(submission.title)
    url.append(submission.url)
    scores.append(submission.score)

df['Title'] = titles
df['selfText'] = url
df['Upvotes'] = scores

print(df.shape)
print(df.head(10))