# Reddit User Persona Generator

This script generates a user persona based on a Reddit user's recent posts and comments. It fetches content from Reddit, uses the OpenRouter API to analyze the text and generate a detailed persona, and then saves the persona to a text file.

## Features

  - Fetches a user's latest posts and comments from Reddit.
  - Utilizes OpenRouter with a specified model to generate a structured user persona.
  - Samples a random subset of the user's content for analysis.
  - Saves the generated persona to a local text file named `{username}_persona.txt`.

## Prerequisites

Before you begin, ensure you have the following installed:

  - [Python 3.6 or higher](https://www.python.org/downloads/)
  - [pip](https://pip.pypa.io/en/stable/installation/) (Python's package installer)

You will also need API credentials for:

  - **Reddit API**: To fetch user data.
  - **OpenRouter API**: To generate the persona.

## ⚙️ Setup Instructions

Follow these steps to set up your environment and run the application.

### 1\. Clone the Repository

First, clone this repository to your local machine or download and unzip the source code.

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2\. Create a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

**On macOS and Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3\. Install Dependencies

Install the necessary Python libraries using the `requirements.txt` file. If a `requirements.txt` file is not available, you can install the packages directly.

Create a `requirements.txt` file with the following content:

```
requests
praw
python-dotenv
```

Then run the following command:

```bash
pip install -r requirements.txt
```

### 4\. Configure Environment Variables

This script uses a `.env` file to manage API keys and other configuration variables.

1.  Create a new file named `.env` in the root of your project directory.
2.  Add the following lines to the `.env` file and replace the placeholder values with your actual API credentials.

<!-- end list -->

```env
# Reddit API Credentials
REDDIT_CLIENT_ID="YOUR_REDDIT_CLIENT_ID"
REDDIT_CLIENT_SECRET="YOUR_REDDIT_CLIENT_SECRET"
USER_AGENT="YOUR_APP_NAME_BY_YOUR_REDDIT_USERNAME"

# OpenRouter API Credentials
OPENROUTER_API_KEY="YOUR_OPENROUTER_API_KEY"
OPENROUTER_MODEL="anthropic/claude-3-haiku" # Or any other model you prefer
OPENROUTER_ENDPOINT="https://openrouter.ai/api/v1/chat/completions"
```

#### How to get your credentials:

  * **Reddit API**:

    1.  Go to the [Reddit App Preferences](https://www.reddit.com/prefs/apps).
    2.  Click "are you a developer? create an app...".
    3.  Fill out the form:
          * **name**: A unique name for your application.
          * **type**: Select "script".
          * **redirect uri**: You can use `http://localhost:8080`.
    4.  Click "create app". Your `client_id` (under your app name) and `client_secret` will be displayed.
    5.  For the `USER_AGENT`, a good practice is a descriptive string, like `MyAppName v1.0 by /u/YourUsername`.

  * **OpenRouter API**:

    1.  Sign in to your [OpenRouter.ai account](https://openrouter.ai/).
    2.  Navigate to your account settings or keys page.
    3.  Generate a new API key.

## 🚀 How to Execute the Script

Once you have completed the setup, you can run the script from your terminal.

1.  Make sure your virtual environment is activated.
2.  Run the `app.py` script using the following command, replacing `<RedditUsername>` with the Reddit username you want to analyze:

<!-- end list -->

```bash
python app.py <RedditUsername>
```

### Example:

To generate a persona for the user `u/spez`, you would run:

```bash
python app.py spez
```

The script will then:

1.  Fetch the latest posts and comments for the specified user.
2.  Send the content to the OpenRouter API for analysis.
3.  Generate the persona.
4.  Save the output to a file named `spez_persona.txt` in the same directory.

The terminal will display the progress, including fetching status and API responses. If successful, you will see a confirmation message indicating that the user persona has been saved.