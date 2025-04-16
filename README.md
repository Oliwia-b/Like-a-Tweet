# Python Script: Like a Tweet by ID

Project uses the Twitter API and authenticates with OAuth 1.0a

## How to run the project
1. Clone the repository.
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Replace the example API credentials with you own in .env file.

   *Note: In case of problems when running a program, make sure some other system variable is not used instead of the ones from .env*
5. Set TWEET_ID as an ID of the tweet you want to like. It should be a number, not a string.
6. Run the program.
   - If authentication is successful, your browser will open a Twitter authorization page.
   - Approve the app and copy the 7-digit PIN code.
   - Enter the PIN in the terminal.
