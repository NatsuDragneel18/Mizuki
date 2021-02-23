from telethon import TelegramClient, events
from Mizuhararobot.modules.download_from_url import download_file
import os
import time
import datetime
import asyncio
import aiohttp
from Mizuhararobot.uputils import progress, humanbytes, time_formatter, convert_from_bytes
import traceback

@bot.on(events.NewMessage(pattern='/up'))
async def up(event):
    if event.reply_to_msg_id:
        start = time.time()
        url = await event.get_reply_message()
        ilk = await event.respond("Downloading...")
        
        try:
            filename = os.path.join(DOWNLOADPATH, os.path.basename(url.text))
            file_path = await download_file(url.text, filename, ilk, start, bot)
        except Exception as e:
            print(e)
            await event.respond(f"Downloading Failed\n\n**Error:** {e}")
        
        await ilk.delete()

        try:
            orta = await event.respond("Uploading to Telegram...")

            dosya = await bot.upload_file(filename, progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, orta, start, "Uploading to Telegram...")
                ))

            zaman = str(time.time() - start)
            await bot.send_file(event.chat.id, dosya, force_document=True, caption=f"Uploaded By @TheMizukiBot 👸")
        except Exception as e:
            traceback.print_exc()

            print(e)
            await event.respond(f"Uploading Failed\n\n**Error:** {e}")
        
        await orta.delete()

    raise events.StopPropagation

def main():
    if not os.path.isdir(DOWNLOADPATH):
        os.mkdir(DOWNLOADPATH)

if __name__ == '__main__':
    main()
