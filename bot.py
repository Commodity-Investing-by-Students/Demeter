# bot.py
import os
import random
from discord.ext import commands
from dotenv import load_dotenv
from goose3 import Goose
from sample import USDA 
from sample import summary

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

g = Goose()

#method for extracting text from url
def text(link):
    article = g.extract(url=link)
    return str(article.cleaned_text)

#bot command for summarizing from URL 
@bot.command(name='news', help='Summarize an article from a url')
async def scrape(ctx, url):
    await ctx.send(text(url)) 

#says pog
@bot.command(name='pog', help='says pog')
async def scrape(ctx):
    await ctx.send("pog") 

@bot.command(name='USDA', help='Summarizes last 3 USDA Press releases')
async def USDA_method(ctx):
    summarys = str() 
    links = USDA() 
    links.replace("'", "") 
    links = links.split()

    
    temp = links[0].replace("\'", "")
    summarys += summary(text(temp))
    
    await ctx.send(summary) 

bot.run(TOKEN)