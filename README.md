# Science News

A Dockerized Telegram bot that fetches science news articles, summarizes and translates them using AI, and publishes them to a Telegram channel with a link to the full article.

## Features

- Fetches science news from RSS feeds
- Uses OpenAI to summarize and translate news
- Posts automated hourly news updates to a Telegram channel
- Uses an SQLite database to store processed news and avoid duplicates


## Installation

### Configuration
Required environment variables (set in `.env`):
* `TELEGRAM_TOKEN`: Your Telegram bot token from @BotFather
* `OPENAI_KEY`: API key for OpenAI services
* `TELEGRAM_CHANNEL_ID`: Target channel username (e.g., @sc1ence_news)

### Setup
1. Clone the repository:
   ```bash
   git clone git@github.com:pravdanet/ScienceNews.git
   ```
2. Copy `.env.example` to `.env` file:
    ```bash
    cp .env.example .env
    ```
3. Edit the `.env` file with your credentials:
    * TELEGRAM_TOKEN - your_tg_bot_token
    * OPENAI_KEY - your_openai_api_key
    * CHANNEL_ID - @your_tg_channel
4. Build and run with Docker:
    ```bash
    docker-compose up -d --build
    ```

### Prerequisites
- Docker 20.10+
- Python 3.9+

## Usage
Once deployed, the bot will automatically:
1. Fetch new articles from the configured source
2. Process them through AI summarization/translation
3. Post to the Telegram channel
4. Store processed articles in the database to prevent reposts

### Manual Control
To manually trigger an update:
    ```bash
    docker-compose exec science-news-bot python main.py --update
    ```
To view logs:
    ```bash
    docker-compose logs -f
    ```

## File Structure
- `main.py` - Main application logic
- `news.db` - SQLite database for processed articles
- `Dockerfile` - Container configuration
- `docker-compose.yml` - Service definition
- `requirements.txt` - Python dependencies

## License
This project is licensed under the terms of the MIT License.