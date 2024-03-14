import os

from dotenv import find_dotenv, load_dotenv
from telegram import Bot, Update
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from logger_module import configure_logger
from resume_reviewer import ResumeReviewer


_ = load_dotenv(find_dotenv())


# Set up telegram's bot token
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Set up owner chat id
OWNER_CHAT_ID = os.getenv("OWNER_CHAT_ID")

# Setting up for Deployment
# BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
# OWNER_CHAT_ID = os.environ.get("OWNER_CHAT_ID")


def initialize_resume_reviewer() -> ResumeReviewer:
    """Initialize the ResumeReviewer class."""

    resume_reviewer = ResumeReviewer()

    return resume_reviewer


resume_reviewer_ai = initialize_resume_reviewer()


def initialize_logger():
    """Initialize the logger."""

    logger = configure_logger(log_level="INFO")

    return logger


logger = initialize_logger()


def start(update: Update, context: Bot) -> None:
    """Send a message when the command /start is issued."""

    # Greet the user and introduce the bot
    update.message.reply_text(
        """\
Hello! I am Resume Reviewer Bot. I am here to help you with your resume. \
Simply send me your resume in PDF format and I will review it for you. I shall \
provide you with feedback on how you can improve your resume. 😉\
"""
    )

    logger.info("User has started the bot...")


def forward_convo_to_owner(
    update: Update,
    resume_file_id: str,
    bot_response: str,
    context: Bot
) -> None:
    """
    Forward the conversations to the owner of the bot in real-time like logs
    """

    try:
        # Forward the conversation to the owner of the bot
        user_firstName = update.message.from_user.first_name
        conversation = f"""\
    ********************************
    {user_firstName}'s file id: {resume_file_id}

    ResumeReviewer_Bot: {bot_response}
    ********************************\
    """
        
        context.bot.send_message(chat_id=OWNER_CHAT_ID, text=conversation)

        logger.info("Convo forwarded to the owner of the bot...")
    except Exception as e:
        logger.error(f"Error while forwarding the convo to the owner: {e}")


def handle_message(update: Update, context: Bot):
    """
    Handle the message sent by the user and reply with the response from the
    bot. Furthermore, forward the conversation to the owner of the bot.
    """

    # Get the message sent by the user
    user_message = update.message.text

    # Get the response from the bot
    response = """\
Whoopsie-daisy! It looks like you've sent a text message instead of a \
file. While we love hearing from you and have a chat, our system is \
currently on a "PDFs only" diet. 📄✨

So, try sending your resume in PDF format, and we'll be more than happy \
to help you out! 😊\
"""

    # Reply with the response from the bot
    update.message.reply_text(response)

    # Forward the conversation to the owner of the bot
    forward_convo_to_owner(update, user_message, response, context)


def handle_pdf(update: Update, context: Bot) -> None:
    """
    Handle the PDF file sent by the user and reply with the response generated
    by the model on the backend.
    """

    wait_message = """\
Thanks for sending in your PDF! 📄✨

Please hold on just a moment while we work our magic...\
"""
    update.message.reply_text(wait_message)

    file_id = update.message.document.file_id
    
    file = context.bot.get_file(file_id)

    pdffile = 'input_resume.pdf'
    file.download(pdffile)
    
    response_text = resume_reviewer_ai.generate_feedback(pdffile)

    forward_convo_to_owner(update, file_id, response_text, context)
    
    update.message.reply_text(response_text)

    complementary_message = """\
We hope you find the feedback helpful and insightful. \
Keep up the great work, and best of luck with your endeavors! 🚀✨\
"""
    update.message.reply_text(complementary_message)


def main() -> None:
    """Start the bot."""

    updater = Updater(token=BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(
        Filters.document.mime_type("application/pdf"),
        handle_pdf
    ))
    dp.add_handler(MessageHandler(
        Filters.text & ~Filters.command,
        handle_message
    ))
    
    logger.info(
        "ResumeReviewer_Bot is now running and listening for updates..."
    )
    
    # Start the bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
