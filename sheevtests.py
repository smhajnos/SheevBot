# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 17:26:17 2023

@author: sam
"""

import praw
import sheevsecrets

def login():
    username = "SheevBot"

    reddit = praw.Reddit(client_id=sheevsecrets.REDDIT_CLIENT_ID,
                         client_secret=sheevsecrets.REDDIT_SECRET,
                         password=sheevsecrets.REDDIT_PASSWORD,
                         user_agent='SheevBot, the /r/PrequelMemes mod bot',
                         username=username) 
    return reddit


def test1():
    repost_text = "REPOST DETECTED. Source?"
    oc_text = "OC DETECTED. Confirm you made it?"
    repost_thanks = "OP provided a source"
    oc_thanks = "OP Confirmed they made this!"
    repost_shame = "Fuck you OP you didn't supply a source"
    oc_shame = "Fuck you OP you didn't make this"
    reddit = login()
    test_subreddit = reddit.subreddit("PrequelMemesTest")
    new_posts = test_subreddit.new()
    op_provided_source = False # if this gets set to true, the comment will be edited thanking the user
    already_modded = False # if this gets set to true, the bot will not leave a comment
    is_repost = False
    is_oc = False
    for submission in new_posts:
        if submission.link_flair_text:
            if "REPOST" in submission.link_flair_text.upper():
                is_repost = True
            elif "OC" in submission.link_flair_text.upper():
                is_oc = True
            for comment in submission.comments.list():
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
                            # TODO: check age
                            comment.edit(body=repost_shame)
                            # TODO: remove post
                        elif op_provided_source and is_oc:
                            comment.edit(body=oc_thanks)
                        elif is_oc:
                            # TODO: check age
                            comment.edit(body=oc_shame)
                            # TODO: remove psot
                    break # no need to keep looking for stickied comments
                            
        if submission.approved_by:
            already_modded = True              
        if not already_modded and is_repost:
            comment = submission.reply(body=repost_text)
            comment.mod.distinguish(sticky=True)
        if not already_modded and is_oc:
            comment = submission.reply(body=oc_text)
            comment.mod.distinguish(sticky=True)