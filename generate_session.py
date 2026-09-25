#!/usr/bin/env python3
"""
Generates Telegram StringSession for use in GitHub Actions.
Run this locally once, copy the output to GitHub Secrets.
"""
import asyncio
import os
from telethon import TelegramClient
from telethon.sessions import StringSession

# Load credentials from .env
API_ID = int(os.getenv('TELEGRAM_API_ID', '0'))
API_HASH = os.getenv('TELEGRAM_API_HASH', '')
PHONE = os.getenv('TELEGRAM_PHONE', '')

async def main():
    if not all([API_ID, API_HASH, PHONE]):
        print("ERROR: Missing credentials in .env file")
        print("Required: TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE")
        return

    print("Connecting to Telegram...")
    print(f"Phone: {PHONE}")

    client = TelegramClient(StringSession(), API_ID, API_HASH)

    await client.start(phone=PHONE)

    session_string = client.session.save()

    print("\n" + "="*60)
    print("SUCCESS! Copy this StringSession to GitHub Secrets:")
    print("="*60)
    print(session_string)
    print("="*60)
    print("\nAdd it as: TELEGRAM_SESSION")
    print("\nYou can now use this session in GitHub Actions without SMS codes.")

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
