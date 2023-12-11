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

@bot.slash_command(name="ping",description="Check if the bot is working", guild_ids=[mod_server])
async def ping(ctx):
    await ctx.send("Pong!")
    
@bot.slash_command(name="set_config",description="Set a config parameter", guild_ids=[mod_server])
async def set_config(ctx,parameter,value):
    await ctx.send("Please wait...")
    cfg_params_str = reddit.subreddit("PrequelMemes").wiki["sheevbotparams"].content_md
    cfg_params = json.loads(cfg_params_str)
    cfg = getconfig()
    
    success = False
    error_msg = "Something unexpected went wrong."
    cont = True # continue
    try:
        if parameter in cfg_params:
            if cfg_params[parameter] == "int":
                try:
                    val = int(value)
                except:
                    cont = False
                    success = False
                    error_msg = "That isn't an integer."
            elif cfg_params[parameter] == "str":
                val = str(value)
            else:
                cont = False
                success = False
                error_msg = "The data type in the sheevbotparams page is invalid, please fix this before proceeding."
                
            if cont:   
                if not parameter in cfg:
                    success = False
                    error_msg = "That parameter is not in the sheevbot page."
                else:
                    try:
                        setconfig(parameter, val, who="{} (id:{})".format(ctx.user.display_name, ctx.user.id)) # record their id in case they set their username to another user's username
                        success = True
                    except:
                        success = False
                        error_msg = "I couldn't update the sheevbot page."
        else:
            success = False
            error_msg = "That parameter is not in the sheevbotparams page."
        
        
        
    except:
        success = False
        error_msg = "Something unexpected went wrong."
        
    if success:
        await ctx.send("Success!")
    else:
        await ctx.send(error_msg)
    

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
    
    
def getconfig(sub="PrequelMemes"):
    cfg_str = reddit.subreddit(sub).wiki["sheevbot"].content_md
    cfg = json.loads(cfg_str)
    return cfg
        
    
def setconfig(param,value,who="Unknown",sub="PrequelMemes"):
    cfg_str = reddit.subreddit(sub).wiki["sheevbot"].content_md
    cfg = json.loads(cfg_str)
    cfg[param] = value
    cfg_str = json.dumps(cfg, sort_keys=True, indent=4)
    reddit.subreddit(sub).wiki["sheevbot"].edit(content=cfg_str,reason="Config updated by {0} by command.".format(who))
    
    
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
            await asyncio.sleep(1) # prevents blocking
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
                                   
async def log(s, emergent=False):
    lc = bot.get_channel(channels["log"])
    print(s)
    if emergent:    
        await lc.send("<@145372956304867328> {}".format(s))
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
    config_good = await validateconfig()
    if not config_good:
        return
    cfg = getconfig()
    time_to_reply = float(cfg["time_to_reply"])
    ignore_after = float(cfg["ignore_after"])
    #repost_cooldown = float(cfg["repost_cooldown"])
    post_count = 0
    check_subreddits = subreddits
    #check_subreddits = [test_subreddit]
    for sub_to_check in check_subreddits:
        new_posts = sub_to_check.new(limit=100)
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
                        if "REPOST" in submission.link_flair_text.upper():
                            is_repost = True
                        elif "OC" in submission.link_flair_text.upper():
                            is_oc = True
                        else:
                            already_modded = True # only other flair is the mod flair
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
                        if comment.stickied and not comment.author.name == "SheevBot":
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
                await log("Something went wrong processing this post: {}".format(submission.url), emergent=True)
    
    


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