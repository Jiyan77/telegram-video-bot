# Telegram Anonymous Video Sender Bot

A Telegram bot for anonymous video forwarding within group chats. The bot receives videos from users and forwards them to a specific Telegram group without revealing the sender's identity.

## Features

- **Anonymous Video Forwarding:** Videos uploaded to the bot are forwarded to the target group without revealing the sender's identity.
- **Filtering:** Only accepts video files. Rejects videos with captions or links with the error message "Please upload only desi video."
- **User Tracking:** Tracks user interactions in a JSON file.
- **Broadcast System:** Regular scheduled broadcasts to all users with backup channel information.

## Configuration for Bots.Business

1. Clone this repository to your GitHub account
2. In Bots.Business admin panel, go to "Git sync" section
3. Paste your GitHub repository URL
4. Click "Import from git"

## Bot Settings


- **Target Group ID:** Already configured with your group ID: `-1002300932976`
- **Backup Channel URL:** Already configured with your backup channel: `https://t.me/+exNiJX3B_1AzNjdh`

## Commands 

The bot has the following commands:

- `/start` - Sends welcome message with backup channel button
- `/help` - Sends help message with backup channel button

## Message Handling

- Only accepts videos without captions or links
- Rejects any other types of media with "Please upload only desi video" message
- Broadcasts backup channel link to all users every 24 hours
