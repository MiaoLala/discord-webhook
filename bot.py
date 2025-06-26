import os
import discord
from meeting_notify import get_meeting_notification_by_dc_id

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = discord.Client(intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Discord Bot 上線：{bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_message = message.content.strip()

    if user_message == "會議通知":
        await message.channel.send("📢 這是會議通知訊息（可整合 Notion 資料）")
    elif user_message == "我要綁定":
        await message.channel.send("請輸入格式：員編：XXXX，進行綁定")
    elif user_message.startswith("員編："):
        await message.channel.send(f"✅ 綁定成功：{user_message}")
    else:
        await message.channel.send("❓ 指令錯誤，請重試")

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
