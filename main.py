import praw, datetime, os, random

reddit = praw.Reddit(
    client_id=os.environ["REDDIT_CLIENT_ID"],
    client_secret=os.environ["REDDIT_CLIENT_SECRET"],
    username=os.environ["REDDIT_USERNAME"],
    password=os.environ["REDDIT_PASSWORD"],
    user_agent="DailyPosterBot/1.0 by u/YourUsername"
)

# rotate through subreddits
subreddits = ["test", "sub2", "sub3", "sub4"]
index = datetime.datetime.utcnow().day % len(subreddits)
target = subreddits[index]

title = f"Daily test post {datetime.datetime.utcnow().strftime('%b %d, %Y')}"
body = "## Hello Reddit!\n\nThis is a **Markdown** test post."

print(f"Posting to {target}...")
reddit.subreddit(target).submit(title=title, selftext=body)
print("Done!")
