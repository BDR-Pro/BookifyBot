# Audio Book Downloader Bot

This Telegram bot leverages the Telethon library to provide a simple interface for searching and downloading audio books. Users can interact with the bot to find books by title and download them directly through Telegram.

## Features

- **Search for Books**: Users can search for audio books by title.
- **Book Selection**: After searching, users can select from a list of available books.
- **Download Books**: Allows users to download the selected audio book and its cover image (if available).

## Commands

- `/start` - Start the conversation with the bot.
- `/help` - Get help about how to use the bot.
- `/search` - Initiate a search by entering a book title.

## Setup

1. **Clone the Repository**: Ensure you have a copy of the bot code.
2. **Install Dependencies**:

   ```bash
   pip install telethon
   ```

3. **Environment Variables**:
   - `API_ID`: Your Telegram API ID.
   - `API_HASH`: Your Telegram API Hash.
   - `TOKEN_BOOK`: The bot token from BotFather.

4. **Run the Bot**:

   ```bash
   python main.py
   ```

## Operational Flow

1. **Initialization**: Upon launching, the bot logs into the audio book service and starts listening for commands.
2. **User Interaction**:
   - Users can start the bot using the `/start` command, which will greet them and prompt to use the `/search` command.
   - The `/help` command provides a quick guide on how to use the bot.
   - The `/search` command prompts the user to send the title of the book they are looking for.
   - The bot then displays a list of books. The user can select a book by sending its corresponding number.
   - If the selected book is available, the bot fetches the book along with its cover image and provides a download link.

## Error Handling

- Users are informed if no books are found or if there is an error in downloading the book or its image.
- The bot resets the conversation state if needed to avoid issues from lingering state errors.

## Contribution

Contributions to the bot are welcome. Please ensure that you follow the existing coding style and add comments where necessary.
