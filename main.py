from telethon import TelegramClient, events
from audiobook import search_book, fetch_book , download_book , download_image, login
import os 

api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
bot_token = os.environ.get('TOKEN_BOOK')

client = TelegramClient('book_bot', api_id, api_hash)
# Dictionary to keep track of user states
user_states = {}
download_books = {}
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('Hello! Welcome to the Audio Book Downloader Bot. Use /search to find an audio book.')
    raise events.StopPropagation

@client.on(events.NewMessage(pattern='/help'))
async def help(event):
    help_text = 'Download any audio book by sending the title of the book. Start with /search command.'
    await event.respond(help_text)
    raise events.StopPropagation

@client.on(events.NewMessage(pattern='/search'))
async def search(event):
    user_states[event.sender_id] = 'searching'
    await event.respond('Please send me the title of the book you want to download.')
    raise events.StopPropagation

@client.on(events.NewMessage)
async def handle_message(event):
    user_id = event.sender_id
    if user_id in user_states and user_states[user_id] == 'searching':
        # User is expected to send a book title
        download_books[user_id] = []
        title = event.message.message.strip()
        books = search_book(title)  # Assuming this function returns a list of books or a response
        if books:
            response = '\n\n'.join([
                f"{index + 1}. **{book['title'].split(' - ')[0]}** - _Author {book['title'].split(' - ')[1]}_" 
                for index, book in enumerate(books)
            ])
            # Note: MarkdownV2 requires escaping some characters like _, *, [, ], etc.
            response = response.replace('-', '\\-').replace('.', '\\.').replace('!', '\\!')
            user_states[user_id] = 'downloading'
            download_books[user_id] = books
            await event.respond(f"Found books:\n{response}", parse_mode='markdown')
            await event.respond('Please select a book by typing its number.')
        else:
            await event.respond("Sorry, no books found with that title.")
            user_states[user_id] = None  # Reset the state
    else:
        if user_id in user_states and user_states[user_id] == 'downloading' and event.message.message.isdigit():
            number = int(event.message.message)
            if number <= len(download_books[user_id]):
                await event.respond(" Fetching the Book...")
                link = download_books[user_id][number - 1]['link']
                book = fetch_book(link)
                if book:
                    await event.respond(f"\n ** {book['title']} ** by {book['author']}... \n Read by {book['read_by']} \n [Link to the book]({book['url']})")
                    image_path = download_image(book['image'])
                    if image_path:
                        await client.send_file(event.sender_id, image_path)
                        os.remove(image_path)

                    else:
                        await event.respond("Sorry, the image could not be downloaded.")
                    
                    #await event.send_file(download_book(link))
                else:
                    await event.respond("Sorry, the book could not be downloaded.")
        if not event.message.message.startswith('/'):
            await event.respond("Type /search to find a book or /help for assistance.")
    raise events.StopPropagation


async def main():
    await client.start(bot_token=bot_token)
    await client.run_until_disconnected()

if __name__ == '__main__':
    print('logging in audio book bay...')
    login()
    print('Starting the bot...')
    client.loop.run_until_complete(main())
