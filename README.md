# Science News

A Dockerized Telegram bot that fetches science news articles, summarizes and translates them using AI, and publishes them to a Telegram channel with a link to the full article.

## Features

- Fetches science news from RSS feeds
- Uses OpenAI to summarize and translate news
- Posts automated hourly news updates to a Telegram channel
- Uses an SQLite database to store processed news and avoid duplicates

## Requirements
- Python 3.9+
- Docker
- Telegram Bot API token
- OpenAI API key

## Installation
1. Clone the repository:
   ```bash
   git clone git@github.com:pravdanet/ScienceNews.git
   ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
or 
    ```bash
    pip3 install -r requirements.txt
    ```

## Configuration
1. Copy or rename `.env.example` to `.env`:
    ```bash
    cp .env.example .env
    ```
2. Edit the `.env` file with your credentials:
    ```TELEGRAM_TOKEN=your_tg_bot_token
    OPENAI_KEY=your_openai_api_key
    CHANNEL_ID=@your_tg_channel
    ```
Required environment variables (set in `.env`):
* `TELEGRAM_TOKEN`: Your Telegram bot token from @BotFather
* `OPENAI_KEY`: API key for OpenAI services
* `TELEGRAM_CHANNEL_ID`: Target channel username (e.g., @sc1ence_news)

## Running with Docker
1. Build the image:
    ```bash
    docker-compose build
    ```
2. Start the container:
    ```bash
    docker-compose up -d
    ```
3. To stop:
    ```bash
    docker-compose down
    ```
4. To manually trigger an update:
    ```bash
    docker-compose exec science-news-bot python main.py --update
    ```
5. To view logs:
    ```bash
    docker-compose logs -f
    ```

## Manual Execution
    ```bash
    python main.py
    ```
or
    ```bash
    python3 main.py
    ```

## Usage
Once deployed, the bot will automatically:
1. Fetch new articles from the configured source
2. Process them through AI summarization/translation
3. Post to the Telegram channel
4. Store processed articles in the database to prevent reposts

## File Structure
- `main.py` - Main application logic
- `news.db` - SQLite database for processed articles
- `Dockerfile` - Container configuration
- `docker-compose.yml` - Service definition
- `requirements.txt` - Python dependencies

## Author
Aleksandra Ivanova  - aleksndraivanoffa@gmail.com

## License
This project is licensed under the terms of the MIT License.