import os
import threading
import asyncio
from flask import Flask, request, jsonify

import discord

# 環境變數設定
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(1387409881237028974)  # int(os.getenv("DISCORD_CHANNEL_ID"))

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

discord_bot = discord.Client(intents=intents)
app = Flask(__name__)

# 啟動 Discord Bot 的背景執行緒
def run_discord_bot():
    asyncio.set_event_loop(asyncio.new_event_loop())
    discord_bot.run(DISCORD_TOKEN)

@discord_bot.event
async def on_ready():
    print(f"✅ Discord Bot 上線：{discord_bot.user}")

@discord_bot.event
async def on_message(message):
    if message.author == discord_bot.user:
        return

    user_message = message.content.strip()

    # ✅ 處理指令
    if user_message == "會議通知":
        await message.channel.send("📢 這是會議通知訊息（可整合 Notion 資料）")
    else:
        await message.channel.send("❓ 指令錯誤，請重試")

@app.route("/", methods=["GET"])
def home():
    return "Discord Bot Webhook Running!"

if __name__ == "__main__":
    threading.Thread(target=run_discord_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
