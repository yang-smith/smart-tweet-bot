import tweepy
from dotenv import load_dotenv
import os

def tweet_post(content):
    load_dotenv()
    consumer_key = os.environ.get("API_KEY")
    consumer_secret = os.environ.get("API_KEY_SECRET")
    access_token = os.environ.get("access_token")
    access_token_secret = os.environ.get("access_token_secret")
    bearer_token = os.environ.get("Bearer_token")

    # auth = tweepy.OAuth1UserHandler(
    #     consumer_key, consumer_secret, access_token, access_token_secret
    # )
    client = tweepy.Client(bearer_token=bearer_token,
                        access_token=access_token,
                        access_token_secret=access_token_secret,
                        consumer_key=consumer_key,
                        consumer_secret=consumer_secret)
    client.create_tweet(text=content)

