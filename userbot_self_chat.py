import asyncio
import random
import json
import os
from datetime import datetime, timedelta
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.messages import CreateChatRequest

# Session & API credentials from environment
API_ID = int(os.getenv('TELEGRAM_API_ID', '0'))
API_HASH = os.getenv('TELEGRAM_API_HASH', '')
SESSION_STRING = os.getenv('TELEGRAM_SESSION', '')

# Message pool — variety keeps it organic
MESSAGE_POOL = [
    "still here",
    "nothing new",
    "same as yesterday",
    "checking in",
    "quiet day",
    "running smooth",
    "no issues",
    "all clear",
    "holding steady",
    "status: normal",
    "nothing to report",
    "business as usual",
    "routine check",
    "monitoring",
    "systems nominal",
    "no alerts",
    "baseline stable",
    "traffic normal",
    "activity: low",
    "quiet shift",
    "watchdog active",
    "perimeter clear",
    "sensors green",
    "pattern: nominal",
    "telemetry clean",
    "no anomalies",
    "threshold: normal",
    "drift: none",
    "signal: clean",
    "noise floor: low",
]

CONFIG_FILE = "group_config.json"


def load_config():
    """Load saved group configuration."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def save_config(chat_id, group_name):
    """Save group configuration to disk."""
    config = {
        "chat_id": chat_id,
        "group_name": group_name,
        "created_at": datetime.now().isoformat()
    }
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)


class ActivitySimulator:
    """Simulates realistic chat activity patterns."""

    def __init__(self, client, chat_entity):
        self.client = client
        self.chat_entity = chat_entity
        self.running = False
        self.current_pattern = None

    def choose_pattern(self):
        """Randomly select activity pattern."""
        patterns = ['rapid_burst', 'question_answer', 'burst_silence_burst']
        self.current_pattern = random.choice(patterns)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Pattern selected: {self.current_pattern}")
        return self.current_pattern

    def get_message_count(self):
        """Weighted message count — 1 message most common, 3 rare."""
        roll = random.random()
        if roll < 0.70:  # 70% chance
            return 1
        elif roll < 0.92:  # 22% chance
            return 2
        else:  # 8% chance
            return 3

    def get_burst_delay(self):
        """Delay between messages in a multi-message burst."""
        return random.uniform(7, 14)

    def get_next_session_delay(self):
        """Time until next activity session — 50-130 second spread."""
        return random.uniform(50, 130)

    async def send_single_message(self):
        """Send one message from the pool."""
        msg = random.choice(MESSAGE_POOL)
        try:
            await self.client.send_message(self.chat_entity, msg)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Sent: {msg}")
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Failed to send: {e}")
            raise

    async def pattern_rapid_burst(self):
        """Pattern 1: Rapid Burst - 5-8 messages in 20-40 seconds."""
        count = random.randint(5, 8)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Rapid burst: {count} messages")

        for i in range(count):
            await self.send_single_message()
            if i < count - 1:
                delay = random.uniform(3, 7)
                await asyncio.sleep(delay)

    async def pattern_question_answer(self):
        """Pattern 5: Question-Answer simulation."""
        cycles = random.randint(3, 5)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Question-Answer: {cycles} cycles")

        for cycle in range(cycles):
            # "Question"
            await self.send_single_message()

            # Wait (simulating thinking/typing)
            wait = random.uniform(40, 90)
            mins, secs = divmod(int(wait), 60)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Waiting for 'answer': {mins:02d}:{secs:02d}")

            remaining = int(wait)
            while remaining > 0 and self.running:
                mins, secs = divmod(remaining, 60)
                print(f"\r⏳ Next message in: {mins:02d}:{secs:02d}", end='', flush=True)
                await asyncio.sleep(1)
                remaining -= 1
            print()

            # "Answer" - 2-3 messages quickly
            answer_count = random.randint(2, 3)
            for i in range(answer_count):
                await self.send_single_message()
                if i < answer_count - 1:
                    await asyncio.sleep(random.uniform(5, 10))

    async def pattern_burst_silence_burst(self):
        """Pattern 8: Burst-Silence-Burst (shortened silence)."""
        cycles = random.randint(2, 3)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Burst-Silence-Burst: {cycles} cycles")

        for cycle in range(cycles):
            # Burst
            burst_count = random.randint(3, 5)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Burst {cycle+1}: {burst_count} messages")

            for i in range(burst_count):
                await self.send_single_message()
                if i < burst_count - 1:
                    await asyncio.sleep(random.uniform(5, 10))

            # Silence (max 2 minutes)
            if cycle < cycles - 1:  # No silence after last burst
                silence = random.uniform(30, 120)  # 30 seconds to 2 minutes
                mins, secs = divmod(int(silence), 60)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Silence period: {mins:02d}:{secs:02d}")

                remaining = int(silence)
                while remaining > 0 and self.running:
                    mins, secs = divmod(remaining, 60)
                    print(f"\r⏳ Silence: {mins:02d}:{secs:02d}", end='', flush=True)
                    await asyncio.sleep(1)
                    remaining -= 1
                print()

    async def send_burst(self):
        """Send a single activity burst."""
        count = self.get_message_count()
        messages = random.sample(MESSAGE_POOL, min(count, len(MESSAGE_POOL)))

        for i, msg in enumerate(messages):
            try:
                await self.client.send_message(self.chat_entity, msg)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Sent: {msg}")
            except Exception as e:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Failed to send: {e}")
                raise

            if i < count - 1:  # Delay between messages in burst
                delay = self.get_burst_delay()
                await asyncio.sleep(delay)

    async def run(self):
        """Main activity loop with pattern rotation."""
        self.running = True
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Activity simulator started")

        while self.running:
            # Choose random pattern
            pattern = self.choose_pattern()

            # Execute pattern
            if pattern == 'rapid_burst':
                await self.pattern_rapid_burst()
            elif pattern == 'question_answer':
                await self.pattern_question_answer()
            elif pattern == 'burst_silence_burst':
                await self.pattern_burst_silence_burst()

            # Random delay before next pattern (30-120 seconds)
            delay = random.uniform(30, 120)
            next_time = datetime.now() + timedelta(seconds=delay)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Next pattern at {next_time.strftime('%H:%M:%S')} ({int(delay)}s)")

            # Countdown display with live updates
            remaining = int(delay)
            while remaining > 0 and self.running:
                mins, secs = divmod(remaining, 60)
                print(f"\r⏳ Next pattern in: {mins:02d}:{secs:02d}", end='', flush=True)
                await asyncio.sleep(1)
                remaining -= 1

            print()  # Newline after countdown completes

    def stop(self):
        self.running = False


async def get_or_create_group(client):
    """Returns existing group entity or creates a new one."""
    # Check if we already have a saved group
    config = load_config()

    if config:
        chat_id = config["chat_id"]
        group_name = config["group_name"]

        # Verify the group still exists and return entity
        try:
            entity = await client.get_entity(chat_id)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Using existing group: {group_name} (ID: {chat_id})")
            return entity
        except Exception:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Saved group no longer exists, creating new one")

    # Create new group
    adjectives = ["quiet", "silent", "shadow", "ghost", "phantom", "void", "null", "empty", "blank", "dark"]
    nouns = ["channel", "room", "space", "zone", "feed", "line", "wire", "net", "grid", "hub"]

    name = f"{random.choice(adjectives)}-{random.choice(nouns)}-{random.randint(1000, 9999)}"

    await client(CreateChatRequest(
        users=[],
        title=name
    ))

    # Query all dialogs to find the newly created group
    await asyncio.sleep(1)  # Brief delay for creation to propagate
    async for dialog in client.iter_dialogs(limit=10):
        if dialog.name == name:
            chat_id = dialog.id
            save_config(chat_id, name)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Created private group: {name} (ID: {chat_id})")
            return dialog.entity

    raise RuntimeError(f"Created group '{name}' but could not find it in dialogs")


async def main():
    if not SESSION_STRING:
        print("ERROR: TELEGRAM_SESSION not found in environment")
        print("Run generate_session.py locally to create one")
        return

    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

    await client.start()
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Client connected")

    # Get existing or create new private group
    chat_entity = await get_or_create_group(client)

    # Start activity simulator
    simulator = ActivitySimulator(client, chat_entity)
    try:
        await simulator.run()
    except KeyboardInterrupt:
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Shutting down...")
        simulator.stop()
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
