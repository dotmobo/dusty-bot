#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
from openai import OpenAI
import tweepy

def load_config():
    """
    Load configuration from config.ini file.
    
    :return: Dictionary with configuration values
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    return {
        'grok_key': config.get('DEFAULT', 'grok_key'),
        'api_key': config.get('DEFAULT', 'api_key'),
        'api_secret_key': config.get('DEFAULT', 'api_secret_key'),
        'access_token': config.get('DEFAULT', 'access_token'),
        'access_token_secret': config.get('DEFAULT', 'access_token_secret')
    }

def get_grok_response(client, system_content, user_content):
    """
    Fetch a response from Grok using the provided system and user content.
    
    :param client: OpenAI client instance
    :param system_content: System role message content
    :param user_content: User role message content
    :return: The response from Grok
    """
    completion = client.chat.completions.create(
        model="grok-2-1212",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
        ],
    )
    return completion.choices[0].message.content

def create_tweet(client):
    """
    Create a tweet about the Dusty Bones project and Shadow Lands game.
    
    :param client: OpenAI client instance
    :return: A tweet string
    """
    system_content = """You are Dusty, the mascot of the Shadow Lands game from the Dusty Bones community. Your role is to provide information and tweet about the project with enthusiasm and flair. Here's what you should know:

    - **Dusty Bones**: An NFT community on MultiversX, focusing on art and community, with 90% of rewards distributed to holders.
    - **Project Details**: 
      - Explores MultiverseX, invests in Hatom protocol, manages DAO portfolio with xSafe.
      - Roadmap includes NFT collection launch, investment in Hatom Protocol farms, and the release of "Shadow Lands" game.
    - **Team**: 
      - Stan (Designer), Pentaxx (Social Manager), Mobo (Developer)
    - **Game Mechanics**: 
      - Players build mystical structures (Tavern, Bank, Laboratory, Crypt, Haunted House) on Dark Forest land for $DUST returns.
    - **Economics**:
      - Controlled NFT minting, liquidity pool strategies, regular holder rewards, snapshot for land and $DUST distribution.
      - Secondary market trades in $EGLD, $DUST, or other tokens.
      - Airdrop/tokenomics: rewards, staking, building purchases, SFT market, progress incentives with a total $DUST supply of 1 billion.
    - **Community Engagement**: 
      - Social media events like advertising competitions, social rankings.
    - **Legal**: 
      - The project holds copyright and IP rights over all content.

    Keep your tweets engaging, informative, and reflective of Dusty's vibrant personality!
    """

    user_content = "Create a cool and engaging tweet about the Dusty Bones project and the upcoming Shadow Lands game. The tweet must not exceed 280 characters."

    tweet = get_grok_response(client, system_content, user_content)
    return tweet

def post_tweet(tweet_text, config):
    """
    Post a tweet using the Twitter API through Tweepy.
    
    :param tweet_text: The text of the tweet to post
    :param config: Configuration dictionary with Twitter API credentials
    """
    # Create API object
    client = tweepy.Client(
        consumer_key=config['api_key'],
        consumer_secret=config['api_secret_key'],
        access_token=config['access_token'],
        access_token_secret=config['access_token_secret']
    )

    try:
        # Post the tweet
        client.create_tweet(text=tweet_text)
        print("Tweet posted successfully.")
    except Exception as e:
        print(f"Error posting tweet: {e}")

def main():
    # Load configuration
    config = load_config()

    # Initialize the OpenAI client with the Grok API key
    client = OpenAI(api_key=config['grok_key'], base_url="https://api.x.ai/v1")

    # Create a tweet
    tweet = create_tweet(client)
    
    # Truncate the tweet if it exceeds 280 characters
    if len(tweet) > 280:
        tweet = tweet[:280]

    print(f"Tweet: {tweet}")
    print(f"Character count: {len(tweet)}")

    # Post the tweet
    post_tweet(tweet, config)

if __name__ == "__main__":
    main()