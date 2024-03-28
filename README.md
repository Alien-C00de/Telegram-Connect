# Telegram-Connect - Python Code

This repository contains Python code to connect to multiple Telegram channels using a Python script. The program supports both single channels and lists of channels from a text file.

## Features

- Automatically join a single Telegram channel.
- Join multiple channels from a list specified in a text file.


## Installation

### Prerequisites

You must have a Telegram API ID and API HASH to run this program. Create your own using the following link and insert them into the `config.ini` file:
- Telegram API ID and HASH

### Required Libraries

Install the following libraries to ensure the scraper runs smoothly:
```bash
pip install Telethon
pip install configparser
pip install colorama
```
## Usage

Execute the tool with the following commands based on your data retrieval needs:

- To scrape data from groups you are associated with:
   ```bash
   python Telegram_Connect.py -s https://t.me/alientest001
   ```
- To display basic details of a group on the screen:
   ```bash
   python Telegram_Connect.py -m channel_list.txt
   ```

📨 Happy Telegram Connect! 🚀
