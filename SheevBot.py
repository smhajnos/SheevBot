# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 14:11:39 2022

@author: sam
"""



import nextcord
from nextcord import SlashOption
from nextcord.ext import commands, tasks
import sheevsecrets
import asyncio
import selectors
import praw
import sqlite3

selector = selectors.SelectSelector()
loop = asyncio.SelectorEventLoop(selector)
asyncio.set_event_loop(loop)
asyncio.new_event_loop()


mod_server = 429365222461931522
servers = [mod_server]

channels = {
    "log":1098770267372789832,
    "modposts":895323724260188191
    }

sheev_color = 0xfc036f

intents = nextcord.Intents.all()
#intents.members = True


dataWarehouse = sqlite3.connect("datawarehouse.db")
cursor = dataWarehouse.cursor()

bot = commands.Bot(command_prefix='$', intents=intents)




#  _                 _       
# | |               (_)      
# | |     ___   __ _ _ _ __  
# | |    / _ \ / _` | | '_ \ 
# | |___| (_) | (_| | | | | |
# |______\___/ \__, |_|_| |_|
#               __/ |        
#              |___/         
username = "SheevBot"

reddit = praw.Reddit(client_id=sheevsecrets.REDDIT_CLIENT_ID,
                     client_secret=sheevsecrets.REDDIT_SECRET,
                     password=sheevsecrets.REDDIT_PASSWORD,
                     user_agent='SheevBot, the /r/PrequelMemes mod bot',
                     username=username)  
subreddit_names = ["PrequelMemes", "PrequelMemesTest"]
subreddits = []
for s in subreddit_names:
    subreddits.append(reddit.subreddit(s))
test_subreddit = reddit.subreddit("PrequelMemesTest")


 #   _____ _               _        
 #  / ____| |             | |       
 # | |    | |__   ___  ___| | _____ 
 # | |    | '_ \ / _ \/ __| |/ / __|
 # | |____| | | |  __/ (__|   <\__ \
 #  \_____|_| |_|\___|\___|_|\_\___/
#async def admin_command(ctx):
#    return ctx.guild.id == bot_server




 #   _____                                          _     
 #  / ____|                                        | |    
 # | |     ___  _ __ ___  _ __ ___   __ _ _ __   __| |___ 
 # | |    / _ \| '_ ` _ \| '_ ` _ \ / _` | '_ \ / _` / __|
 # | |___| (_) | | | | | | | | | | | (_| | | | | (_| \__ \
 #  \_____\___/|_| |_| |_|_| |_| |_|\__,_|_| |_|\__,_|___/
                                                        


 #  _______          _                 _____                           _                 
 # |__   __|        | |       ___     / ____|                         | |                
 #    | | ___   ___ | |___   ( _ )   | |  __  ___ _ __   ___ _ __ __ _| |_ ___  _ __ ___ 
 #    | |/ _ \ / _ \| / __|  / _ \/\ | | |_ |/ _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__/ __|
 #    | | (_) | (_) | \__ \ | (_>  < | |__| |  __/ | | |  __/ | | (_| | || (_) | |  \__ \
 #    |_|\___/ \___/|_|___/  \___/\/  \_____|\___|_| |_|\___|_|  \__,_|\__\___/|_|  |___/
                                                                                       
def commit():
    dataWarehouse.commit()
    #backup to cloud?                                                                                     
    
    
    
def getconfig(param):
    cursor.execute("SELECT COUNT(*) FROM config WHERE param = ?",(param,))
    res = cursor.fetchone()
    if res[0] > 0:
        cursor.execute("SELECT val FROM config WHERE param = ?",(param,))
        res = cursor.fetchone()
        return res[0]
    else:
        return None

def setconfig(param, val):
    cursor.execute("SELECT COUNT(*) FROM config WHERE param = ?",(param,))
    res = cursor.fetchone()
    if res[0] > 0:
            cursor.execute("DELETE FROM config WHERE param = ?",(param,))
    cursor.execute("INSERT INTO config (param, val) VALUES (?,?)",(param,val,))
    commit()
    
    

 #  _______        _       
 # |__   __|      | |      
 #    | | ___  ___| |_ ___ 
 #    | |/ _ \/ __| __/ __|
 #    | |  __/\__ \ |_\__ \
 #    |_|\___||___/\__|___/
                         
                         
# nothin here rn
                                                                                  
             

 #   _____      _              _       _          _   _______        _        
 #  / ____|    | |            | |     | |        | | |__   __|      | |       
 # | (___   ___| |__   ___  __| |_   _| | ___  __| |    | | __ _ ___| | _____ 
 #  \___ \ / __| '_ \ / _ \/ _` | | | | |/ _ \/ _` |    | |/ _` / __| |/ / __|
 #  ____) | (__| | | |  __/ (_| | |_| | |  __/ (_| |    | | (_| \__ \   <\__ \
 # |_____/ \___|_| |_|\___|\__,_|\__,_|_|\___|\__,_|    |_|\__,_|___/_|\_\___/
                                                                            
@tasks.loop(seconds=60)
async def redditcheck():                                                                            
    for subreddit in subreddits:
        for i in [1,2]:
            print("getting sticky #{}".format(i))
            try:
                submission = subreddit.sticky(number=i)
            except:
                submission = None
            if submission:
                cursor.execute("SELECT COUNT(*) FROM modposts WHERE post = ?",(submission.id,))
                res = cursor.fetchone()
                if res[0] == 0 and submission.title != "Free Talk Friday":
                    ch = bot.get_channel(channels["modposts"])
                    await ch.send("New Modpost by /u/{}:\r\n\r\nhttps://www.reddit.com{}".format(submission.author.name, submission.permalink))
                    cursor.execute("INSERT INTO modposts (post) VALUES (?)",(submission.id,))
                    commit()
            else:
                print("No sticky #{} found".format(i))
                                                                              
                                                                                       
                                                                                       
                                                                                       




 #  _    _ _   _ _ _ _   _           
 # | |  | | | (_) (_) | (_)          
 # | |  | | |_ _| |_| |_ _  ___  ___ 
 # | |  | | __| | | | __| |/ _ \/ __|
 # | |__| | |_| | | | |_| |  __/\__ \
 #  \____/ \__|_|_|_|\__|_|\___||___/
                                   
async def log(s):
    lc = bot.get_channel(channels["log"])
    await lc.send(s)    
    
    
    


 #  _______ _            __  __       _         ______               _   
 # |__   __| |          |  \/  |     (_)       |  ____|             | |  
 #    | |  | |__   ___  | \  / | __ _ _ _ __   | |____   _____ _ __ | |_ 
 #    | |  | '_ \ / _ \ | |\/| |/ _` | | '_ \  |  __\ \ / / _ \ '_ \| __|
 #    | |  | | | |  __/ | |  | | (_| | | | | | | |___\ V /  __/ | | | |_ 
 #    |_|  |_| |_|\___| |_|  |_|\__,_|_|_| |_| |______\_/ \___|_| |_|\__|
                                                                       
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}') 
    main_channel = bot.get_channel(channels["log"])
    await main_channel.send("Starting")
    if not redditcheck.is_running():
        redditcheck.start()
    
print("Starting bot")
bot.run(sheevsecrets.DISCORD_TOKEN)