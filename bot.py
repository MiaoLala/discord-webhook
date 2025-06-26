import os
import discord
import logging

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = discord.Client(intents=intents)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@bot.event
async def on_ready():
    logger.info(f"✅ Discord Bot 上線：{bot.user}")

@bot.event
async def on_message(message):
    try:
        if message.author == bot.user:
            return

        channel_id = message.channel.id
        user_message = message.content.strip()

        if channel_id == 1387409881237028974:
            if user_message == "會議通知":
                await message.channel.send("查詢中請稍後...")  # 先回覆提示訊息
                dc_id = message.author.id
                reply_text = get_meeting_notification_by_dc_id(dc_id)
                await message.channel.send(reply_text)
            elif user_message == "我要綁定":
                await message.channel.send("請輸入格式：員編：XXXX，進行綁定")
            elif user_message.startswith("員編："):
                await message.channel.send(f"✅ 綁定成功：{user_message}")
            else:
                await message.channel.send("❓ 指令錯誤，請重試")
        else:
            # 其他頻道不回應或給通用訊息
            pass
    except Exception as e:
        logger.error(f"on_message 發生錯誤: {e}", exc_info=True)

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
