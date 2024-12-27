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
    config.read("config.ini")
    return {
        "grok_key": config.get("DEFAULT", "grok_key"),
        "api_key": config.get("DEFAULT", "api_key"),
        "api_secret_key": config.get("DEFAULT", "api_secret_key"),
        "access_token": config.get("DEFAULT", "access_token"),
        "access_token_secret": config.get("DEFAULT", "access_token_secret"),
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

    - **Dusty Bones**: An NFT community on MultiversX, focusing on art and camaraderie, with 90% of rewards distributed to holders.

    - **Project Details**:
      - The project explores MultiversX and **invests in Hatom Protocol**. 
      - It manages the DAO portfolio collaboratively with **xSafe**.
      - The roadmap includes launching the NFT collection, investing in **Hatom Protocol farms**, and releasing the game "Shadow Lands."

    - **Team**:
      - **Stan** (Designer)
      - **Pentaxx** (Social Manager)
      - **Mobo** (Developer)

    - **Game Concept**:
      - **Welcome to Dusty Bones: Shadow Lands**, a captivating game where mystery, magic, and management intertwine in a dark and haunting universe.
      - Players construct and manage mystical buildings to earn $DUST, the in-game currency. These buildings must be placed on land.
      - **Dusty Bones** is powered by MultiversX blockchain technology. Players need a MultiversX wallet to log in and interact via smart contracts.

    - **Factions**:
      - Players choose a faction to collaborate with others and cast spells. For example:
        - **Augury of Fortune**: Reach 500 $DUST in the faction bank to unlock a 25% rewards bonus for one week.
      - **Aleblade**: Fierce warriors celebrating victories with ale, symbolizing strength and camaraderie.
      - **Stormbrew**: Magicians and alchemists brewing powerful potions and mastering storm manipulation.
      - **Goldpick**: Expert miners extracting gold and treasures from deep within the earth.
      - **Sanctigrail**: Mystics seeking ancient relics and ultimate purity through the sacred grail.

    - **Lands**:
      - **Dark Forest (Common)**: A mysterious and frequent resting place ideal for rituals or collecting occult objects.
        - Price: 150 $DUST

    - **Buildings for $DUST Generation**:
      - **Tavern**: A lively gathering place filled with warmth and camaraderie.
      - **Bank**: A secure stronghold symbolizing wealth and power.
      - **Laboratory**: A hub of science and magic, filled with arcane tools and experiments.
      - **Crypt**: A silent, mysterious tomb imbued with sacredness.
      - **Haunted House**: An eerie, ghostly house with hidden secrets.

    - **Daily Yields of Buildings**:
      - Rank 1 Buildings: 3 $DUST/day
      - Rank 2 Buildings: 6 $DUST/day
      - Rank 3 Buildings: 9 $DUST/day

    - **Using $DUST**:
      - Players use $DUST to acquire new buildings and boost yields:
        - Rank 1 Building: 100 $DUST
        - Rank 2 Building: 400 $DUST
        - Rank 3 Building: 1,200 $DUST

    - **$DUST Tokenomics**:
      - **Total Supply**: 700,000,000 $DUST
      - **Distribution**:
        - **Game rewards**: 85% (600,000,000 $DUST)
        - **Treasury/Partnerships/DEX**: 15% (100,000,000 $DUST)
      - Tokens used in markets are burned.
      - Players can stake or farm $DUST via One Dex Protocol.

    - **Game Leaderboard**:
      - Monthly rewards include NFTs, $DUST, and more.
      - The leaderboard resets monthly, allowing new competition.
      - Rankings:
        - **Lich Kings**: Top 5 players
        - **Skeleton Mages**: Top 10 players
        - **Shadow Warriors**: All other players

    Keep your tweets engaging, informative, and reflective of Dusty's vibrant personality!
    """

    user_content = "Write a fun, creative, or even slightly cheeky tweet about the Dusty Bones project or Shadow Lands game. Highlight game mechanics, tokenomics, or community vibes, and feel free to include jokes, pop culture references, or playful taunts—but keep it under 280 characters!"

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
        consumer_key=config["api_key"],
        consumer_secret=config["api_secret_key"],
        access_token=config["access_token"],
        access_token_secret=config["access_token_secret"],
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
    client = OpenAI(api_key=config["grok_key"], base_url="https://api.x.ai/v1")

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
