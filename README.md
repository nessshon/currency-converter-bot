<h1 align="center">🤖 Telegram Bot Currency Converter</h1>

#### Telegram Bot currency converter, based on Google Search.
Bot example: [@nCurrencyConverterBot](https://nCurrencyConverterBot.t.me)

## Requirements

* Python 3.10 and above.
* Systemd or Docker.

## Usage

Clone this repo via [link](https://github.com/nessshon/currency-converter-bot)

```bash
git clone https://github.com/nessshon/currency-converter-bot
```

Go to the project folder

```bash
cd currency-converter-bot
```

Create environment variables file

```bash
cp .env.example .env
```

Edit [environment variables](#environment-variables-reference) in `.env`

```bash
nano .env
```

### Launch using Docker

1. Install [docker](https://docs.docker.com/get-docker) and [docker compose](https://docs.docker.com/compose/install/)
   
2. Build and run your container
   ```bash
   docker-compose up -d
   ```

### Launch using systemd

1. Create a virtual environment
   ```bash
   python3.10 -m venv env
   ```

2. Activate virtual environment
   ```bash
   source env/bin/activate
   ```

3. Install required packages
   ```bash
   pip install -r requirements.txt
   ```

4. Check if the bot is running
   ```bash
   python -m app
   ```

5. Set **WorkingDirectory** to the path to the project folder.
   ```bash
   nano telegram-bot.service
   ```

6. Copy telegram-bot.service to /lib/systemd/system/currency-converter-bot
   ```bash
   sudo cp telegram-bot.service /lib/systemd/system/currency-converter-bot.service
   ```
7. Enable autostart on boot
   ```bash
   sudo systemctl enable currency-converter-bot.service
   ```
8. Launch Bot
   ```bash
   sudo systemctl start currency-converter-bot.service
   ```

### Environment variables reference

| Variable   | Type   | Description                                               |
|------------|--------|-----------------------------------------------------------|
| BOT_TOKEN  | str    | Token, get it from [@BotFather](https://t.me/BotFather)   |
| USE_REDIS  | bool   | Set to True if you are using Redis                        |
| REDIS_HOST | str	   | Set "redis" if you will be using docker                   |