# Telegram LeetCode Daily Task Bot

This is a Telegram bot that sends daily LeetCode tasks to a specified chat group and provides motivational quotes when users reply to the task message.

## Features

- Sends daily LeetCode task links at a specified time.
- Responds with a motivational quote when users reply to the daily task message.
- Uses GitHub Actions for scheduling and running the bot.

## Setup

### Prerequisites

- Python 3.x
- Git
- A Telegram bot token (You can get one by creating a bot on Telegram using BotFather)
- A GitHub account

### Files

- `bot.py`: Main bot script.
- `requirements.txt`: Python dependencies.
- `.github/workflows/main.yml`: GitHub Actions workflow file.
- `.gitignore`: Git ignore file to exclude unnecessary files.

### Instructions

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2. **Create a virtual environment and install dependencies:**

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    pip install -r requirements.txt
    ```

3. **Set up your bot token:**

    Add your Telegram bot token as a secret in your GitHub repository:
    
    - Go to your GitHub repository.
    - Click on `Settings`.
    - Go to `Secrets and variables` > `Actions` > `New repository secret`.
    - Add a new secret with the name `TOKEN` and your bot token as the value.

4. **Configure GitHub Actions:**

    Ensure the `.github/workflows/main.yml` file exists with the following content:

    ```yaml
    name: Telegram Bot

    on:
      schedule:
        - cron: "0 7 * * *"  # Runs every day at 7 AM UTC
      workflow_dispatch:  # Allows manual trigger from GitHub UI

    jobs:
      run-bot:
        runs-on: ubuntu-latest

        steps:
        - name: Checkout code
          uses: actions/checkout@v2

        - name: Set up Python
          uses: actions/setup-python@v2
          with:
            python-version: 3.x

        - name: Install dependencies
          run: |
            python -m pip install --upgrade pip
            pip install -r requirements.txt

        - name: Run the bot
          env:
            TOKEN: ${{ secrets.TOKEN }}
          run: |
            python bot.py
    ```

5. **Push your code to GitHub:**

    ```bash
    git add .
    git commit -m "Set up Telegram bot with GitHub Actions"
    git push origin master
    ```

## Usage

### Starting the Bot

The bot will automatically run every day at 7 AM UTC as specified in the GitHub Actions workflow. You can also manually trigger the workflow from the GitHub Actions tab in your repository.

### Commands

- **/start**: Starts the bot and schedules the daily task.
- **/send_now**: Immediately sends the daily task for testing purposes.

## Contributing

If you would like to contribute to this project, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
