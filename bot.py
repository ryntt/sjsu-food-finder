"""
Implements code to connect bot to Discord and start pattern matching.

The program will initiate the Discord client with the proper intents.
It will notify the user when it is online on Discord, and it will send
back messages to a user on Discord when specific prompts are entered.

When an argument is entered in Discord, the code will check whether
the first string passed is "$sjsufood". If it is, then it will
evaluate the rest of the strings. If the rest of the strings are either
"help" or blank, the bot will return help documentation. If the rest of
the strings follow the pattern "find: (restaurant name)", the bot will
do a search for a designated restaurant with Yelp's API and return
some essential information. Otherwise, the bot will retrieve essential
arguments from the rest of the strings and pass them through Yelp's
API to return a string representation of the best results.
"""

import discord
import os
from dotenv import load_dotenv
import yelp_read as yelp
import re
from help_doc import HELP_DOC

# intents to basically give permissions
intents = discord.Intents.all()
client = discord.Client(intents=intents)


def main():
    # lets user know when the bot is up and running
    @client.event
    async def on_ready():
        print(f'{client.user} is currently online!')

    # when a message is passed, the bot checks that it isn't calling
    # itself. then, it lowers the message, splits it, and checks the
    # arguments
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        txt = message.content.lower()
        starting_pattern = re.compile(r'\$sjsufood')
        find_pattern = re.compile(r'find:\s*(\S+)')
        category_pattern = re.compile(r'([A-Za-z][A-Za-z,]*[A-Za-z])')
        num_pattern = re.compile(r'n(10|[1-9])')
        rating_pattern = re.compile(r'r([0-5]\.?[0-5]?)')
        price_pattern = re.compile(r'p([1-4])')

        # if the first string is $sjsufood, then...
        if starting_pattern.match(txt) and txt is not None:
            formatted_txt = txt.replace('$sjsufood', '').strip()
            if formatted_txt == 'help' or formatted_txt == '':
                await message.channel.send(HELP_DOC)
            elif find_pattern.match(formatted_txt):
                await message.channel.send(yelp.return_details(
                    find_pattern.match(formatted_txt).group(1)))
            else:
                category = category_pattern.search(formatted_txt).group(1) \
                    if category_pattern.search(formatted_txt) else \
                    yelp.DEFAULT_CATEGORY
                num = int(num_pattern.search(formatted_txt).group(1) if
                          num_pattern.search(formatted_txt) else
                          yelp.DEFAULT_LIMIT)
                rating = float(rating_pattern.search(formatted_txt).group(1) if
                               rating_pattern.search(formatted_txt) else
                               yelp.DEFAULT_RATING)
                price = int(price_pattern.search(formatted_txt).group(1) if
                            price_pattern.search(
                                formatted_txt) else yelp.DEFAULT_PRICE)
                price_arr = [i for i in range(1, 5) if i <= price]
                try:
                    await message.channel.send(yelp.eatery_list_string
                        (yelp.return_best_results(
                        category, num, rating, price_arr)))
                except Exception as e:
                    print(f'An exception has occurred: {e}')

    load_dotenv('.env')
    client.run(os.getenv('TOKEN'))


if __name__ == '__main__':
    main()
