import praw

reddit = praw.Reddit(
    client_id="your client id",
    client_secret="your client secret",
    password="your reddit account password",
    user_agent="the name of the script by /u/YourUsernameGoesHere",
    username="YourUsername",
)

subreddits = ['subreddit1', 'subreddit2']

#title of your post
title = "Your title goes here"
link = "https://www.yourlinkgoeshere.com"

for subreddit in subreddits:
    reddit.subreddit(subreddit).submit(title, url=link, send_replies=False)
