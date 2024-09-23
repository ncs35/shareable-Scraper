import praw
import json

# Subreddit to scrape name 
subreddit_name = "RealEstateAdvice"
# File to save to
output_file = "subreddit_data_RealEstateAdvice.json"


# Reddit API credentials - input your own api keys here after creating a developer account with Reddit
client_id = '#client ID here'
client_secret = '#client secret here'
user_agent = '#user agent here'

# Initialize PRAW
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

# Subreddit to scrape
subreddit = reddit.subreddit(subreddit_name)

# List to hold all post data
all_posts = []

# Define different sort types and the target time filter for the current year
sort_methods = ['top', 'hot', 'new', 'controversial']
time_filters = ['year', 'month', 'week', 'day']  # Focus on the current year's data

# Function to fetch posts based on sort and time filter
def fetch_posts(sort, time_filter, max_posts=1000):
    after = None
    posts_collected = 0

    while posts_collected < max_posts:
        try:
            # Fetch posts based on the sort method and time filter
            if sort in ['top', 'controversial']:
                posts = subreddit.top(limit=100, params={'after': after, 't': time_filter}) if sort == 'top' else subreddit.controversial(limit=100, params={'after': after, 't': time_filter})
            elif sort == 'hot':
                posts = subreddit.hot(limit=100, params={'after': after})
            elif sort == 'new':
                posts = subreddit.new(limit=100, params={'after': after})

            # Convert posts to a list and break if empty
            batch = list(posts)
            if not batch:
                break

            # Add fetched posts to the global list
            all_posts.extend(batch)
            after = batch[-1].name  # Update the 'after' parameter for pagination
            posts_collected += len(batch)
            print(f"Collected {posts_collected} posts for {sort} {time_filter}")

        except Exception as e:
            print(f"Error while fetching posts: {e}")
            break

# Loop through each sort method and time filter combination to collect posts
for sort in sort_methods:
    for time_filter in time_filters:
        print(f'Fetching {sort} posts from the {time_filter}...')
        fetch_posts(sort, time_filter)

# Remove duplicate posts by their unique Reddit ID
unique_posts = {post.id: post for post in all_posts}.values()

# Extract data from each unique post and save to JSON
output_data = [{
    'title': post.title,
    'score': post.score,
    'id': post.id,
    'url': post.url,
    'num_comments': post.num_comments,
    'created': post.created_utc,
    'body': post.selftext
} for post in unique_posts]

# Save the data to a JSON file
with open(output_file, 'w') as file:
    json.dump(output_data, file, indent=4)

print(f'Total number of unique posts saved: {len(output_data)}')
