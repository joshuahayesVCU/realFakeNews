# Author: Joshua Hayes
import copy
import random

# The web scraping tool used to gather headlines and links for the guessing game
# Utilizes the Reddit API to gather data
# tutorial from https://medium.com/geekculture/how-to-extract-reddit-posts-for-an-nlp-project-56d121b260b4

import praw

# Creating a scraper instance using the Reddit class inside praw's library

# Define user agent and create a reddit class
user_agent = "praw_scraper"
reddit = praw.Reddit(client_id="kJ7QyvYqKCvHNOg3gV59cA", client_secret="hI7CLLMKjD7Lq2IZu_XkWRehd3saqQ", user_agent=user_agent)

# List to store future article objects
notTheOnion = []
theOnion = []


# Article class to store headlines and urls from scraped post
class Article:

    def __init__(self, headline, url, isReal):
        self.headline = headline
        self.url = url
        self.isReal = isReal

    def get_headline(self):
        return self.headline

    def get_url(self):
        return self.url

# Method to scrape subreddit post
def scrape(article_list, subreddit_name, postRange, realNews):

    # Subreddit to scrape from
    subreddit = reddit.subreddit(subreddit_name)

    # Fills given list from top post to range (if not fake)
    if realNews:
        for submission in subreddit.hot(limit=(postRange - 1)):
            article_list.append(Article(submission.title, submission.url, True))
    else:
        for submission in subreddit.hot(limit=(postRange - 1)):
            article_list.append(Article(submission.title, submission.url, False))


def game(fake_news, real_news):

    # Bool for main game loop, score tracker
    active_game = True
    current_score = 0

    # Scraping the articles from reddit
    scrape(theOnion, "TheOnion", 50, True)
    scrape(notTheOnion, "notTheOnion", 50, False)

    # main game loop
    while active_game:
        print("=-=-=-=-= REAL FAKE NEWS =-=-=-=-=")
        print("Two of these news articles are real, one is fake. Can you spot the impostor?")
        print("Current score: " + str(current_score))

        # TODO: Make this not have duplicates / put in its own function
        # Creates a new list to store 3 random articles
        choice_list = []
        # deep copies 3 articles from scraped article list
        article1 = copy.deepcopy(notTheOnion[random.randint(0, 49)])
        article2 = copy.deepcopy(notTheOnion[random.randint(0, 49)])
        article3 = copy.deepcopy(theOnion[random.randint(0, 49)])
        # Adds deep copies to list of choices
        choice_list.append(article1)
        choice_list.append(article2)
        choice_list.append(article3)
        # Shuffle list to ensure randomness of choices
        random.shuffle(choice_list)

        print("1." + choice_list[0].headline)
        print("2." + choice_list[1].headline)
        print("3." + choice_list[2].headline)

        answer = int(input("Type the number you think is fake: "))

        # Handling of invalid input
        while answer <= 0 or answer >= 4:
            print("ERROR: Invalid choice. Please choice a number between 1 and 3")
            answer = int(input("Type the number you think is fake: "))

        # If the choice is fake
        if not choice_list[answer-1].isReal:
            print("That's right!")
            print("Read the article here: " + choice_list[answer-1].url)
            current_score += 1

        # If the choice is real
        else:
            print("That's not right")
            print("But you can read your article choice here: " + choice_list[answer-1].url)
        print()

        # Continue or exit loop
        keep_playing = input("Do you want to play again? Y / N ")
        if not keep_playing.lower() == "y":
            active_game = False

    print("=-=-=-=-= Thanks for playing! =-=-=-=-=")
    print("Total score: " + str(current_score))


game(notTheOnion, theOnion)




