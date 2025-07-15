# Importing Libraries
import sys
import os
import time
import random
import requests
import praw

from dotenv import load_dotenv


# Load variables from .env into the environment
load_dotenv()


# Configuring the API'S

# Access the variables using os.getenv
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USER_AGENT = os.getenv("USER_AGENT")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")
OPENROUTER_ENDPOINT = os.getenv("OPENROUTER_ENDPOINT")


# Scraping & Sampling Limits

REDDIT_FETCH_LIMIT = 50       # Max posts/comments per type
SLEEP_BETWEEN_CALLS = 2         # Seconds between Reddit API calls


# Fetching the data from Reddit

def get_reddit_instance():
    return praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=USER_AGENT
    )


def fetch_user_content(username):
    reddit = get_reddit_instance()
    user = reddit.redditor(username)
    posts = []
    comments = []

    try:
        print(" Fetching posts...")
        for i, post in enumerate(user.submissions.new(limit=REDDIT_FETCH_LIMIT), start=1):
            print(f"  ➤ Post #{i}: {post.title}")
            posts.append({
                'type': 'post',
                'title': post.title,
                'body': post.selftext,
                'url': post.url,
                'permalink': f"https://reddit.com{post.permalink}"
            })
            time.sleep(SLEEP_BETWEEN_CALLS)

        print(" Fetching comments...")
        for i, comment in enumerate(user.comments.new(limit=REDDIT_FETCH_LIMIT), start=1):
            print(f"  ➤ Comment #{i}")
            comments.append({
                'type': 'comment',
                'body': comment.body,
                'permalink': f"https://reddit.com{comment.permalink}"
            })
            time.sleep(SLEEP_BETWEEN_CALLS)

    except Exception as e:
        print(f" Error fetching content: {e}")

    return posts + comments


# Building User Persona using OpenRouter

def generate_persona(posts_and_comments, username, reddit_temperature=0.5, openai_temperature=0.7):
    import json

    sample_count = min(20, len(posts_and_comments))
    sampled_items = (
        random.choices(posts_and_comments, k=sample_count)
        if reddit_temperature > 0 else posts_and_comments[:sample_count]
    )

    text_snippets = []
    for item in sampled_items:
        snippet = (
            f"Post: {item['title']}\n{item['body']}"
            if item['type'] == 'post'
            else f"Comment: {item['body']}"
        )
        text_snippets.append(snippet)

    input_text = "\n\n---\n\n".join(text_snippets)

    prompt = f"""
You are an expert persona profiler. Based on Reddit content, generate a user persona that resembles the following layout:

#  Reddit User Persona: {username}

##  Basic Info
- **Age**: [Inferred or 'Not mentioned']
- **Occupation**: [Inferred or 'Not mentioned']
- **Status**: [e.g., Single, Married, Unknown]
- **Location**: [Inferred from content or Unknown]
- **Tier**: [Beginner / Early Adopter / Influencer]
- **Archetype**: [The Creator / Explorer / etc.]

---

##  Motivations
- Convenience: ▰▰▰▱▱
- Wellness: ▰▰▱▱▱
- Speed: ▰▰▰▰▱
- Preferences: ▰▰▰▰▰
- Comfort: ▰▰▰▱▱
- Dietary Needs: ▰▱▱▱▱

---

##  Personality Traits
- **Introvert ↔ Extrovert**: ____
- **Sensing ↔ Intuition**: ____
- **Thinking ↔ Feeling**: ____
- **Judging ↔ Perceiving**: ____

---

##  Behaviour & Habits
- [List behavioral trends, subreddit usage, activity style]

---

##  Frustrations
- [List top user complaints or expressed pain points]

---

##  Goals & Needs
- [What the user hopes to accomplish based on content]

---

##  Citations
Provide at least 5 Reddit post or comment links used to infer the persona.

Now here is the user's Reddit content:

{input_text}
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "temperature": openai_temperature,
        "messages": [{"role": "user", "content": prompt}]
    }

    print(" Sending request to OpenRouter...")

    try:
        response = requests.post(OPENROUTER_ENDPOINT, json=payload, headers=headers)
        print(" Status:", response.status_code)

        # Print raw response text for debugging
        print(" Raw response text (first 500 chars):")
        print(response.text[:500])

        data = response.json()
        return data['choices'][0]['message']['content']

    except requests.exceptions.RequestException as req_err:
        print(" Request failed:", req_err)
        return ""

    except json.JSONDecodeError as json_err:
        print(" JSON decode error:", json_err)
        print(" Raw response (truncated):", response.text[:500])
        return ""

    except Exception as e:
        print(" Unexpected error:", e)
        return ""   


# Save User Persona as Text File

def save_persona_to_file(username, persona_text):
    """Saves the generated persona to a text file."""
    filename = f"{username}_persona.txt"
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(persona_text)
        print(f" User persona saved to: {filename}")
    except Exception as e:
        print(f" Failed to save file: {e}")


# Entry Point

def main():
    """Main entry point of the script."""
    if len(sys.argv) != 2:
        print("Usage: python reddit_persona_generator.py <RedditUsername>")
        sys.exit(1)

    username = sys.argv[1].strip().lstrip('u/').lstrip('/u/')

    print(f"\n Fetching content for: u/{username}...\n")
    content = fetch_user_content(username)

    if not content:
        print("No content found for this user.")
        sys.exit(1)

    print(" Generating persona using OpenRouter...\n")
    persona = generate_persona(
        posts_and_comments=content,
        username=username,
        reddit_temperature=0.5,
        openai_temperature=0.7
    )

    if persona:
        save_persona_to_file(username, persona)
    else:
        print("Failed to generate persona.")


if __name__ == "__main__":
    main()