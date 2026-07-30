import asyncio
from telethon import TelegramClient, events
from config import API_ID, API_HASH, BOT_TOKEN
from facebook_creator import FacebookCreator

async def main():
    bot = TelegramClient('fb_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

    @bot.on(events.NewMessage(pattern='/start'))
    async def start(event):
        await event.reply("Welcome!\nUse /create to make a Facebook account.")

    @bot.on(events.NewMessage(pattern='/create'))
    async def create(event):
        await event.reply("Starting account creation... Please wait.")
        creator = FacebookCreator()
        try:
            data = creator.create_account()
            msg = (
                f"Account Created (Pending Verification)\n"
                f"Login: {data['login']}\n"
                f"Password: {data['password']}\n"
                f"DOB: {data['dob']}\n"
                f"Type: {data['type']}\n\n"
                f"Check your {data['type']} for the code."
            )
            await event.reply(msg)
        except Exception as e:
            await event.reply(f"Error: {str(e)}")
        finally:
            creator.close()

    print("Bot is running...")
    await bot.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
