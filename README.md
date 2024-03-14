# Resume-Reviewer.ai

The `resume-reviewer.ai` is a Telegram bot ([find it here](https://t.me/ResumeReviewer_bot)) designed to help users analyze and receive feedback on their resumes using the **Google Gemini LLM** (Large Language Model) API. This bot allows users to upload their resume **in PDF format**, after which the bot extracts the text, generates a comprehensive prompt for analysis, and sends it to the Google Gemini API to get a response back. The model reviews the resume content and provides feedback, which is sent back to the user via the same Telegram Bot.

## Features

- **PDF Processing**: Users can upload their resume in PDF format to the bot for analysis.
- **Resume Analysis**: The bot extracts text from the uploaded PDF, constructs a prompt for analysis, and sends it to the Google Gemini model for review.
- **Feedback Generation**: The Google Gemini model generates feedback on the resume content, which is then sent back to the user.
- **Logging**: The project includes a logger module for logging events and errors throughout the application.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Zad-100/Resume-Reviewer.ai.git
   ```

2. Install dependencies:

   ```bash
   cd Resume-Reviewer.ai
   pip install -r requirements.txt
   ```

3. Set up environment variables:

   Create a `.env` file in the project directory and add the following variables:

   ```
   GOOGLE_API_KEY=your_google_api_key
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   ```

4. Run the Telegram bot:

   ```bash
   python telegram_bot.py
   ```

## Usage

1. Start a conversation with the Telegram bot by searching for `@ResumeReviewer_bot` ([the t.me/ link](https://t.me/ResumeReviewer_bot)) in the Telegram app.
2. Upload your resume in PDF format when prompted.
3. Wait for the bot to process the resume and provide feedback.

## Dependencies

- `google.generativeai`: Python library for interacting with the Google Gemini LLM API.
- `pdfplumber`: Python library for extracting text from PDF files.
- `python-telegram-bot`: Python wrapper for the Telegram Bot API.
- `dotenv`: Python library for loading environment variables from a `.env` file.

## APIs

The `@ResumeReviewer_bot` utilizes two primary APIs to provide its functionality:

### Google Gemini API

- **Description**: Gemini is a series of multimodal generative AI models developed by Google. Gemini models can accept text and image in prompts, depending on what model variation you choose, and output text responses. The Gemini API gives you access to the latest generative models from Google.
  
- **Integration**: The `@ResumeReviewer_bot` interacts with the Google Gemini API by sending the extracted resume content along with a prompt. The model then generates response based on pre-defined prompts and returns the analysis to the bot.

- **Usage**: The bot utilizes the API to offer users valuable insights and recommendations for improving their resumes, thereby increasing their chances of securing job interviews.

For more information on the Google Gemini API, visit the [official documentation by Google AI for Developers](https://ai.google.dev/docs/gemini_api_overview).  
For the Python Quickstart guide, visit the [official documentation here](https://ai.google.dev/tutorials/python_quickstart).

### Telegram Bot API

- **Description**: The Telegram Bot API is a feature-rich platform that enables developers to create interactive bots (special accounts that do not require an additional phone number to set up; that serve as an interface for code running somewhere on your server) for the Telegram messaging platform. It provides various methods for sending and receiving messages, managing conversations, and handling user interactions.

- **Integration**: The `@ResumeReviewer_bot` utilizes the Telegram Bot API to handle communication between users and the bot. It allows users to interact with the bot by sending messages and uploading PDF files containing their resumes. The bot processes these files, sends them to the Google Gemini API for analysis, and responds with the generated response/feedback.

- **Functionality**: Through the Telegram Bot API, the bot can receive resumes from users, provide real-time feedback, and facilitate seamless communication between users and the bot owner.

For detailed information on the Telegram Bot API, visit the [official API Reference by Telegram](https://core.telegram.org/bots/api#authorizing-your-bot).  
For an example Python-based implementation, check out the [GitLab Tutorial here](https://gitlab.com/Athamaxy/telegram-bot-tutorial/-/blob/main/TutorialBot.py).

## Contributing

Contributions to the project are welcome! If you have any ideas for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
