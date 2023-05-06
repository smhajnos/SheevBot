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
import datetime
import json
import time

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
#subreddit_names = ["PrequelMemesTest"]
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

# no commands right now. More to come!

 #  _______          _                 _____                           _                 
 # |__   __|        | |       ___     / ____|                         | |                
 #    | | ___   ___ | |___   ( _ )   | |  __  ___ _ __   ___ _ __ __ _| |_ ___  _ __ ___ 
 #    | |/ _ \ / _ \| / __|  / _ \/\ | | |_ |/ _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__/ __|
 #    | | (_) | (_) | \__ \ | (_>  < | |__| |  __/ | | |  __/ | | (_| | || (_) | |  \__ \
 #    |_|\___/ \___/|_|___/  \___/\/  \_____|\___|_| |_|\___|_|  \__,_|\__\___/|_|  |___/
                                                                                       
def commit():
    dataWarehouse.commit()
    #backup to cloud?                                                                                     

async def validateconfig():
    cfg_str = reddit.subreddit("PrequelMemes").wiki["sheevbot"].content_md
    cfg = json.loads(cfg_str)
    cursor.execute("SELECT * FROM configparams")
    res = cursor.fetchall()
    retval = True
    for r in res:
        if r[0] in cfg:
            #print("Found parameter {}".format(r[0]))
            pass
        else:
            print("Didn't find parameter {}".format(r[0]))
            await log("Didn't find parameter {}".format(r[0]))
            retval = False
    return retval
    
    
def getconfig():
    cfg_str = reddit.subreddit("PrequelMemes").wiki["sheevbot"].content_md
    cfg = json.loads(cfg_str)
    return cfg
        
    
def setconfig(param,value,who="Unknown"):
    cfg_str = reddit.subreddit("PrequelMemes").wiki["sheevbot"].content_md
    cfg = json.loads(cfg_str)
    cfg[param] = value
    cfg_str = json.dumps(cfg, sort_keys=True, indent=4)
    reddit.subreddit("PrequelMemes").wiki["sheevbot"].edit(content=cfg_str,reason="Config updated by {0} by command.".format(who))
    
    
"""
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
"""    
    



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
            try:
                submission = subreddit.sticky(number=i)
            except:
                submission = None
            if submission:
                print("Found sticky #{} in {}".format(i,subreddit.display_name))
                cursor.execute("SELECT COUNT(*) FROM modposts WHERE post = ?",(submission.id,))
                res = cursor.fetchone()
                if res[0] == 0 and submission.title != "Free Talk Friday":
                    ch = bot.get_channel(channels["modposts"])
                    await ch.send("New Modpost by /u/{}:\r\n\r\nhttps://www.reddit.com{}".format(submission.author.name, submission.permalink))
                    cursor.execute("INSERT INTO modposts (post) VALUES (?)",(submission.id,))
                    commit()
            else:
                print("No sticky #{} found in {}".format(i,subreddit.display_name))
                                                                              
                                                                                       
@tasks.loop(seconds=180)
async def postchecktask():
    await post_checker()                                                                                       
                                                                                       




 #  _    _ _   _ _ _ _   _           
 # | |  | | | (_) (_) | (_)          
 # | |  | | |_ _| |_| |_ _  ___  ___ 
 # | |  | | __| | | | __| |/ _ \/ __|
 # | |__| | |_| | | | |_| |  __/\__ \
 #  \____/ \__|_|_|_|\__|_|\___||___/
                                   
async def log(s):
    lc = bot.get_channel(channels["log"])
    await lc.send(s)    


# __          __        _                 
# \ \        / /       | |                
#  \ \  /\  / /__  _ __| | _____ _ __ ___ 
#   \ \/  \/ / _ \| '__| |/ / _ \ '__/ __|
#    \  /\  / (_) | |  |   <  __/ |  \__ \
#     \/  \/ \___/|_|  |_|\_\___|_|  |___/
                                         
                                         
async def post_checker():
    #start_time = time.time()
    config_good = await validateconfig()
    if not config_good:
        return
    cfg = getconfig()
    repost_text = cfg["repost_text"]
    oc_text = cfg["oc_text"]
    repost_thanks = cfg["repost_thanks"]
    oc_thanks = cfg["oc_thanks"]
    repost_shame = cfg["repost_shame"]
    oc_shame = cfg["oc_shame"]
    time_to_reply = float(cfg["time_to_reply"])
    post_count = 0
    #check_subreddits = subreddits
    check_subreddits = [test_subreddit]
    for sub_to_check in check_subreddits:
        new_posts = sub_to_check.new(limit=100)
        for submission in new_posts:
            post_count += 1
            await asyncio.sleep(1) # prevents blocking
            op_provided_source = False # if this gets set to true, the comment will be edited thanking the user
            already_modded = False # if this gets set to true, the bot will not leave a comment
            is_repost = False
            is_oc = False
            if submission.link_flair_text:
                if "REPOST" in submission.link_flair_text.upper():
                    is_repost = True
                elif "OC" in submission.link_flair_text.upper():
                    is_oc = True
                for comment in submission.comments:
                    if comment.stickied and not comment.author.name == "SheevBot":
                        already_modded = True # modded by someone else, let the humans handle it
                        break # no need to keep looking for stickied comments
                    elif comment.stickied: # mod commment by the bot
                        already_modded = True # modded by the bot, no need for another comment
                        if comment.body in [repost_text, oc_text]: # the post was flaired as a repost at the time of the comment
                            c_replies = comment.replies
                            c_replies.replace_more()
                            for c_reply in c_replies: # look for a comment reply by OP
                                if c_reply.author.name == submission.author.name:
                                    if is_repost and "http" in c_reply.body:
                                        op_provided_source = True
                                        # do NOT break the loop, in case OP posted multiple comments and only one is the one with the link
                                    elif is_oc:
                                        op_provided_source = True
                            if op_provided_source and is_repost:
                                comment.edit(body=repost_thanks)
                            elif is_repost:
                                time_delta = datetime.datetime.now(datetime.timezone.utc).timestamp() - comment.created_utc
                                if time_delta > time_to_reply:
                                    comment.edit(body=repost_shame)
                                    submod = submission.mod()
                                    submod.remove(spam=False)
                            elif op_provided_source and is_oc:
                                comment.edit(body=oc_thanks)
                            elif is_oc:
                                time_delta = datetime.datetime.now(datetime.timezone.utc).timestamp() - comment.created_utc
                                if time_delta > time_to_reply:
                                    comment.edit(body=oc_shame)
                                    submod = submission.mod()
                                    submod.remove(spam=False)
                        break # no need to keep looking for stickied comments
                                
            if submission.approved_by:
                already_modded = True              
            if not already_modded and is_repost:
                comment = submission.reply(body=repost_text)
                comment.mod.distinguish(sticky=True)
            if not already_modded and is_oc:
                comment = submission.reply(body=oc_text)
                comment.mod.distinguish(sticky=True)
    #timed = time.time() - start_time
    #rv = "It took {0} seconds to check {1} posts".format(timed, post_count)
    #return rv

    
    


 #  _______ _            __  __       _         ______               _   
 # |__   __| |          |  \/  |     (_)       |  ____|             | |  
 #    | |  | |__   ___  | \  / | __ _ _ _ __   | |____   _____ _ __ | |_ 
 #    | |  | '_ \ / _ \ | |\/| |/ _` | | '_ \  |  __\ \ / / _ \ '_ \| __|
 #    | |  | | | |  __/ | |  | | (_| | | | | | | |___\ V /  __/ | | | |_ 
 #    |_|  |_| |_|\___| |_|  |_|\__,_|_|_| |_| |______\_/ \___|_| |_|\__|
                                                                       
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}') 
    #main_channel = bot.get_channel(channels["log"])
    #await main_channel.send("Starting")
    if not redditcheck.is_running():
        redditcheck.start()
    if not postchecktask.is_running():
        postchecktask.start()
    
print("Starting bot")
bot.run(sheevsecrets.DISCORD_TOKEN)