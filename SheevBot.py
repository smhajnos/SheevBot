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
import sheevcloud
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw



selector = selectors.SelectSelector()
loop = asyncio.SelectorEventLoop(selector)
asyncio.set_event_loop(loop)
asyncio.new_event_loop()


#  _       _ 
# (_)     (_)
#  _ _ __  _ 
# | | '_ \| |
# | | | | | |
# |_|_| |_|_|


with open("bot_config.json","r") as f:
    bot_config = json.load(f)


mod_server = bot_config["server"] # Discord server ID
channels = bot_config["channels"] # Discord channel IDs
username = bot_config["username"] # Reddit username
user_agent = bot_config["user_agent"] # tbh not really sure what this is
subreddit_names = bot_config["subreddits"] # list of subreddits to monitor
admin_user = bot_config["admin_discord"] # Discord user ID of who to notify of critical errors
test_sub_name = bot_config["test_subreddit"]
sticky_check_frequency = bot_config["sticky_check_frequency"]
main_check_frequency = bot_config["main_check_frequency"]



intents = nextcord.Intents.all()
#intents.members = True


#dataWarehouse = sqlite3.connect("datawarehouse.db")
#cursor = dataWarehouse.cursor()
dataWarehouse = None
cursor = None


bot = commands.Bot(command_prefix='$', intents=intents)

     
            


#  _                 _       
# | |               (_)      
# | |     ___   __ _ _ _ __  
# | |    / _ \ / _` | | '_ \ 
# | |___| (_) | (_| | | | | |
# |______\___/ \__, |_|_| |_|
#               __/ |        
#              |___/         

reddit = praw.Reddit(client_id=sheevsecrets.REDDIT_CLIENT_ID,
                     client_secret=sheevsecrets.REDDIT_SECRET,
                     password=sheevsecrets.REDDIT_PASSWORD,
                     user_agent='SheevBot, the /r/PrequelMemes mod bot',
                     username=username)  
#subreddit_names = ["PrequelMemes", "PrequelMemesTest","SequelMemes"]
#subreddit_names = ["PrequelMemesTest"]
subreddits = []
for s in subreddit_names:
    subreddits.append(reddit.subreddit(s))
test_subreddit = reddit.subreddit(test_sub_name)


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

@bot.slash_command(name="ping",description="Check if the bot is working", guild_ids=[mod_server])
async def ping(ctx):
    await ctx.send("Pong!")
    
@bot.slash_command(name="download_sheevfiles",description="Please don't use this command if you don't know what you are doing.",guild_ids=[mod_server])
async def download_sheevfiles(ctx):
    sheevcloud.download_all()
    await ctx.send("Done!")

@bot.slash_command(name="upload_sheevfiles",description="Please don't use this command if you don't know what you are doing.",guild_ids=[mod_server])
async def upload_sheevfiles(ctx):
    sheevcloud.upload_all()
    await ctx.send("Done!")
    

@bot.slash_command(name="report",description="Generate a mod report for the previous month", guild_ids=[mod_server])
async def report(ctx):
    await ctx.send("Working on it...")
    reasons = ["removecomment","approvecomment","spamcomment","removelink","approvelink","removecomment","banuser","unbanuser"]
    row_header = ["mod","Xc","✓c","Sc","Xp","✓p","Sp","Xu","✓u","all","%"]
            
    # collect data
    tempdatadb = sqlite3.connect("tempdata/temp.db")
    tdcursor = tempdatadb.cursor()
    now = datetime.datetime.now()
    if now.month == 1:
        startdate = datetime.datetime(now.year - 1, 12, 1, 0, 0, 0)
        enddate = datetime.datetime(now.year      ,  1, 1, 0, 0, 0)
    else:
        startdate = datetime.datetime(now.year, now.month - 1, 1, 0, 0, 0)
        enddate = datetime.datetime(now.year, now.month    , 1, 0, 0, 0)
    
    print("Getting data between {} and {} ({} and {})".format(startdate, enddate, startdate.timestamp(), enddate.timestamp()))
    tdcursor.execute("DELETE FROM modactions")
    
    subs = ["PrequelMemes", "SequelMemes"]
    for tsub in subs:
        sub = reddit.subreddit(tsub)        
        modlog = sub.mod.log(limit=50000)
 
        
        for log in modlog: # results are returned most recent first
            if log.created_utc < enddate.timestamp() and log.action in reasons:
                tdcursor.execute("INSERT INTO modactions (mod, timestamp, action, subreddit) VALUES (?, ?, ?, ?)",(log._mod, log.created_utc, log.action, log.subreddit,))
            elif log.created_utc < startdate.timestamp():
                break
            
    tempdatadb.commit()
    
    
    # process data
    modlist = []
    tempdatadb = sqlite3.connect("tempdata/temp.db")
    tdcursor = tempdatadb.cursor()
    tdcursor.execute("SELECT DISTINCT mod FROM modactions ORDER BY mod")
    for row in tdcursor:
        modlist.append(row[0])
    actionmatrix = [row_header]
    
    for reason in reasons:
        totals = ["total"]
        for reason in reasons:
            tdcursor.execute("SELECT COUNT(*) FROM modactions WHERE action = ?", (reason,))
            res = tdcursor.fetchone()
            totals.append(res[0])
        tdcursor.execute("SELECT COUNT(*) FROM modactions")
        res = tdcursor.fetchone()
        total_actions = res[0]
        totals.append(total_actions)
        totals.append("100%")

    for mod in modlist:
        modactions = [mod]
        for reason in reasons:
            tdcursor.execute("SELECT COUNT(*) FROM modactions WHERE mod = ? AND action = ?", (mod, reason,))
            res = tdcursor.fetchone()
            modactions.append(res[0])
        tdcursor.execute("SELECT COUNT(*) FROM modactions WHERE mod = ?", (mod,))
        res = tdcursor.fetchone()
        modactions.append(res[0])
        modactions.append("{:.0f}%".format(res[0]*100/total_actions))
        actionmatrix.append(modactions)
        
    actionmatrix.append(totals)
    for row in actionmatrix:
        print(len(row),row)
            
    fig, ax = plt.subplots()
    
    grid = np.flip(np.array(actionmatrix),0)
    
    ax.set_xlim([-3,grid.shape[0]])
    ax.set_ylim([0,grid.shape[1]])
    
    
    ax.text(-5,0, "total", ha="center", va="center", fontweight="bold")
    for j in range(1, grid.shape[1]):
        ax.text(j*2,0, grid[0,j], ha="center", va="center", fontweight="bold")
    for i in range(1, grid.shape[0]-1):
        ax.text(-5,i, grid[i,0], ha="center", va="center")
        for j in range(1, grid.shape[1]):
            ax.text(j*2,i, grid[i,j], ha="center", va="center")
    i = grid.shape[0]-1
    ax.text(-5,i, grid[i,0], ha="center", va="center", fontweight="bold")
    for j in range(1, grid.shape[1]):
        ax.text(j*2,i, grid[i,j], ha="center", va="center", fontweight="bold")
            
    ax.axis("off")
    
    plt.savefig("tempdata/actionmatrix.png", bbox_inches='tight')
    
    ch = bot.get_channel(channels["scoreboard"])
    await ch.send(content=startdate.strftime("%B %Y"),file=nextcord.File("tempdata/actionmatrix.png",filename="actionmatrix.png"))

 #  _______          _                 _____                           _                 
 # |__   __|        | |       ___     / ____|                         | |                
 #    | | ___   ___ | |___   ( _ )   | |  __  ___ _ __   ___ _ __ __ _| |_ ___  _ __ ___ 
 #    | |/ _ \ / _ \| / __|  / _ \/\ | | |_ |/ _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__/ __|
 #    | | (_) | (_) | \__ \ | (_>  < | |__| |  __/ | | |  __/ | | (_| | || (_) | |  \__ \
 #    |_|\___/ \___/|_|___/  \___/\/  \_____|\___|_| |_|\___|_|  \__,_|\__\___/|_|  |___/
                                                                                       
def commit():
    dataWarehouse.commit()
    #backup to cloud? - no do this one a separate call to avoid extra writes                                                                                  

async def validateconfig(sub="PrequelMemes"):
    print("Validating config for subreddit {}".format(sub))
    cfg_str = reddit.subreddit(sub).wiki["sheevbot"].content_md
    cfg = json.loads(cfg_str)
    
    
    #params_str = reddit.subreddit("PrequelMemes").wiki["sheevbotparams"].content_md
    #params = json.loads(params_str)
    with open("sheevbotparams.json", "r") as f:
        params= json.load(f)
        
    
    retval = True
    
    try:
        for p in params: # p = parameter, t = type ("int" or "str")
            t = params[p]    
            if t == "int":
                try:
                    x = int(cfg[p])
                except:
                    await log("Type mismatch in subreddit {} parameter {}.".format(sub,p), emergent=True)
                    retval = False
            elif t == "str":
                if not isinstance(cfg[p], str):
                    await log("Type mismatch in subreddit {} parameter {}.".format(sub,p), emergent=True)
                    retval = False
            elif t == "list":
                if not isinstance(cfg[p], list):
                    await log("Type mismatch in subreddit {} parameter {}.".format(sub,p), emergent=True)
                    retval = False
            elif t == "list:str":
                if not isinstance(cfg[p], list):
                    await log("Type mismatch in subreddit {} parameter {}.".format(sub,p), emergent=True)
                    retval = False
                elif len(cfg[p]) > 0:
                    for i in cfg[p]:
                        if not isinstance(i, str):
                            retval = False
                    if not retval:
                        await log("Type mismatch in subreddit {} parameter {}.".format(sub,p), emergent=True)
            elif t == "list:int":
                if not isinstance(cfg[p], list):
                    await log("Type mismatch in subreddit {} parameter {}.".format(sub,p), emergent=True)
                    retval = False
                elif len(cfg[p]) > 0:
                    for i in cfg[p]:
                        try:
                            x = int(i)
                        except:
                            retval = False
                    if not retval:
                        await log("Type mismatch in subreddit {} parameter {}.".format(sub,p))
            else:
                await log("Bad type in sheevbotparams for parameter {}.".format(p), emergent=True)
                retval = False
    except:
        retval = False   
        await log("Something went wrong validating sheevbot paramters for subreddit {}".format(sub), emergent=True)
    return retval
    
    
def getconfig(sub):
    print("getting config from {}".format(sub))
    cfg_str = reddit.subreddit(sub).wiki["sheevbot"].content_md
    cfg = json.loads(cfg_str)
    return cfg
        



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
                                                                            
@tasks.loop(seconds=sticky_check_frequency)
async def redditcheck():                                                                            
    for subreddit in subreddits:
        for i in [1,2]:
            await asyncio.sleep(1) # prevents blocking
            try:
                submission = subreddit.sticky(number=i)
            except:
                submission = None
            if submission:
                print("Found sticky #{} in {}".format(i,subreddit.display_name))
                cursor.execute("SELECT COUNT(*) FROM modposts WHERE post = ?",(submission.id,))
                res = cursor.fetchone()
                if res[0] == 0:
                    ch = bot.get_channel(channels["modposts"])
                    await ch.send("New Modpost by /u/{}:\r\n\r\nhttps://www.reddit.com{}".format(submission.author.name, submission.permalink))
                    cursor.execute("INSERT INTO modposts (post) VALUES (?)",(submission.id,))
                    commit()
                    sheevcloud.upload_file("datawarehouse.db")
            else:
                print("No sticky #{} found in {}".format(i,subreddit.display_name))
                                                                              
                                                                                       
@tasks.loop(seconds=main_check_frequency)
async def postchecktask():
    await post_checker()                                                                                       
                                                                                       




 #  _    _ _   _ _ _ _   _           
 # | |  | | | (_) (_) | (_)          
 # | |  | | |_ _| |_| |_ _  ___  ___ 
 # | |  | | __| | | | __| |/ _ \/ __|
 # | |__| | |_| | | | |_| |  __/\__ \
 #  \____/ \__|_|_|_|\__|_|\___||___/
                                   
async def log(s, emergent=False):
    lc = bot.get_channel(channels["log"])
    print(s)
    if emergent:    
        await lc.send("<@{}> {}".format(admin_user, s))
    else:
        await lc.send(s)


# __          __        _                 
# \ \        / /       | |                
#  \ \  /\  / /__  _ __| | _____ _ __ ___ 
#   \ \/  \/ / _ \| '__| |/ / _ \ '__/ __|
#    \  /\  / (_) | |  |   <  __/ |  \__ \
#     \/  \/ \___/|_|  |_|\_\___|_|  |___/
                                         
                                         
async def post_checker():
    #start_time = time.time()
    post_count = 0
    check_subreddits = subreddits
    for sub_to_check in check_subreddits:
        print("Checking sub {}".format(sub_to_check.display_name))
        config_good = await validateconfig(sub_to_check.display_name)
        if config_good:
            cfg = getconfig(sub_to_check.display_name)
            time_to_reply = float(cfg["time_to_reply"])
            ignore_after = float(cfg["ignore_after"])
            new_posts = sub_to_check.new(limit=10)
            for submission in new_posts:
                try:
                        post_count += 1
                        await asyncio.sleep(1) # prevents blocking
                        op_provided_source = False # if this gets set to true, the comment will be edited thanking the user
                        already_modded = False # if this gets set to true, the bot will not leave a comment
                        is_repost = False # based on flair
                        is_oc = False # based on flair
                        is_crosspost = False # based on... well if it is a crosspost
                        to_remove = False # depends on whether the OP has replied to the comment properly. 
                        # to_remove gets set, then later the age of the bot comment is checked and if both are satisfied the post is removed.
                        bot_comment = None
                        
                        if submission.link_flair_text: # flair text should be required but just in case
                            flair_text = submission.link_flair_text
                            if flair_text in cfg["repost_flairs"]:
                                is_repost = True
                            elif flair_text in cfg["oc_flairs"]:
                                is_oc = True
                            else: # presumably, the only other flair options are the ones mods can use. Otherwise, this is not configured correctly.
                                already_modded = True
                            
                        else:
                            already_modded = True # they didn't flair it. Shouldn't be possible so ignore the post.
                            #await log("I found a post without a flair! {}".format(submission.url))
                    
                        if hasattr(submission, "crosspost_parent"):
                            is_crosspost = True
                        else:
                            is_crosspost = False
                        
                        if submission.approved_by: #approved (by a human, this bot will never approve posts only remove them)
                            already_modded = True
                        for comment in submission.comments:
                            if comment.stickied and not comment.author.name == username:
                                already_modded = True # modded by someone else, let the humans handle it
                                
                        if not already_modded:
                            for comment in submission.comments:
                                if comment.stickied: # mod commment by the bot
                                    already_modded = True # modded by the bot, no need for another comment
                                    bot_comment = comment
                                    await asyncio.sleep(1) # prevents blocking
                                    c_replies = comment.replies
                                    c_replies.replace_more()
                                    for c_reply in c_replies: # look for a comment reply by OP
                                        if c_reply.author.name == submission.author.name: 
                                            # Here, we found a comment by OP. 
                                            # Now we will check if the OP has provided a source (if it is a repost and not a crosspost).
                                            # If it is OC or a crosspost, we will just check for a reply by OP.
                                            if "http" in c_reply.body:
                                                op_provided_source = True
                                                # do NOT break the loop, in case OP posted multiple comments and only one is the one with the link
                                            elif is_oc or is_crosspost:
                                                op_provided_source = True
                                                break 
                                                # break because no need to keep searching for a comment from OP.
                                                # If it is OC or a crosspost, only requirement is that OP replied to the bot.
                                                
                            
                                                            
                            # Now, we decide what to do with the comment
                            if bot_comment:
                                time_delta = datetime.datetime.now(datetime.timezone.utc).timestamp() - bot_comment.created_utc
                                too_late = (time_delta > time_to_reply)
                                if is_oc and is_crosspost: # crosspost flaired as OC
                                    if op_provided_source: # This just means OP replied
                                        desired_text = cfg["crosspost_oc_thanks"]
                                        to_remove = False
                                    elif too_late: # Mod comment is too old; OP took too long
                                        desired_text = cfg["crosspost_oc_shame"]
                                        to_remove = True
                                    else: # OP hasn't replied yet, but it hasn't been long enough to remove the post
                                        desired_text = cfg["crosspost_oc_text"]
                                        to_remove = False
                                elif is_repost and is_crosspost: # crosspost flaired as a repost
                                    if op_provided_source: # This just means OP replied
                                        desired_text = cfg["crosspost_repost_thanks"]
                                        to_remove = False
                                    elif too_late: # Mod comment is too old; OP took too long
                                        desired_text = cfg["crosspost_repost_shame"]
                                        to_remove = True
                                    else: # OP hasn't replied yet, but it hasn't been long enough to remove the post
                                        desired_text = cfg["crosspost_repost_text"]
                                        to_remove = False
                                elif is_oc: # Flaired as OC, is not a crosspost
                                    if op_provided_source: # This just means OP replied
                                        desired_text = cfg["oc_thanks"]
                                        to_remove = False
                                    elif too_late: # Mod comment is too old; OP took too long
                                        desired_text = cfg["oc_shame"]
                                        to_remove = True
                                    else: # OP hasn't replied yet, but it hasn't been long enough to remove the post
                                        desired_text = cfg["oc_text"]
                                        to_remove = False
                                elif is_repost:
                                    if op_provided_source: # This just means OP replied
                                        desired_text = cfg["repost_thanks"]
                                        to_remove = False
                                    elif too_late: # Mod comment is too old; OP took too long (or replied, but didn't provide a link)
                                        desired_text = cfg["repost_shame"]
                                        to_remove = True
                                    else: # OP hasn't replied with a link yet, but it hasn't been long enough to remove the post
                                        desired_text = cfg["repost_text"]
                                        to_remove = False
                                    
                                                    
                                    
                                            
                                # Now, time to take action.
                                if bot_comment.body != desired_text:
                                    bot_comment.edit(body=desired_text)
                                if to_remove:
                                    submission.mod.remove(spam=False)
                                already_modded = True                
                            
                            else: # No human mod has approved and this bot has not already made a comment
                                time_delta = datetime.datetime.now(datetime.timezone.utc).timestamp() - submission.created_utc
                                if time_delta > ignore_after: # the post is too old and it would be unfair to require them to respond
                                    pass
                                else:
                                    # Get default text for the flair/crosspost condition
                                    if is_oc and is_crosspost:
                                        desired_text = cfg["crosspost_oc_text"]
                                    elif is_repost and is_crosspost:
                                        desired_text = cfg["crosspost_repost_text"]
                                    elif is_oc:
                                        desired_text = cfg["oc_text"]
                                    elif is_repost:
                                        desired_text = cfg["repost_text"]
                                
                                    # Post the comment
                                    bot_comment = submission.reply(body=desired_text)
                                    bot_comment.mod.distinguish(sticky=True)
                        
                except:
                    await log("Something went wrong processing this post: https://www.reddit.com{}".format(submission.permalink), emergent=False)
                    
        else: #config isn't good
            await log("Something is wrong with the config wiki page for the following subreddit: {}".format(sub_to_check.display_name), emergent=True)
    
    


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
sheevcloud.download_all()
dataWarehouse = sqlite3.connect("savedata/datawarehouse.db")
cursor = dataWarehouse.cursor()
bot.run(sheevsecrets.DISCORD_TOKEN)