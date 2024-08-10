import requests
import logging
from pyrogram import Client, filters

# Enable logging
logging.basicConfig(level=logging.ERROR)

# Replace with your own API ID, API hash, and bot token
api_id = "15122558"
api_hash = "43042882a789e5c2e8526d2da740b9c1"
bot_token = "6401987505:AAHe1Tm28KiEa51lM-RBzVtpq4v7DeAe9yI"

app = Client("sesss", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.text)
async def echo(client, message):
    """Reply to text messages"""
    await message.reply_text(f"You said: {message.text}")

@app.on_message(filters.video)
async def video_size(client, message):
    """Reply with video size"""
    
    try:
        video = message.video
        file_id = video.file_id
        
        size_in_mb = video.file_size / (1024 * 1024)  # Convert size to MB
        await message.reply_text(f"The size of the video is {size_in_mb:.2f} MB")
        
        
        # Get the server URL from FileMoon API
        url = "https://filemoonapi.com/api/upload/server"
        params = {"key": "54845tb4kbkj7svvyig18"}
        response = requests.get(url, params=params)
        # Check if the response was successful
        if response:
            try:
                 server_url = response.json()
                 link = server_url['result']
                 await message.reply_text(f"processing")
            except ValueError:
                logging.error("Invalid JSON response from FileMoon API")
                await message.reply_text("Error: Invalid JSON response from FileMoon API")
                return
        else:
            logging.error(f"Error: {response.status} - {response}")
            await message.reply_text(f"Error: {response.status} - {response}")
            return
        # Download the video from Telegram
        video_file = await client.download_media(message)

        with open(video_file, 'rb') as f:
            # Upload the video to GoFile API
            files = {'file': f}
            data = {"key": "54845tb4kbkj7svvyig18"}
            response = requests.post(link, files=files, data=data)
            if response:
                resulst = response.json()
                if resulst['status'] == 200 and resulst['msg'] == 'OK':
                    filecode = resulst['files'][0]['filecode']
                    await message.reply_text(f"{filecode}")
                else:
                    logging.error(f"Error: {resulst['status']} - {resulst['msg']}")
                    await message.reply_text(f"Error: {resulst['status']} - {resulst['msg']}")

                
            else:
                logging.error(f"Error: {response.status} - {response}")
                await message.reply_text(f"Error: {response.status} - {response}")


        

    except Exception as e:
        logging.error(f"Error: {e}")


if __name__ == "__main__":
    print("Bot is starting...")
    app.run()
