import os

import google.generativeai as genai
import pdfplumber
from dotenv import find_dotenv, load_dotenv

from logger_module import configure_logger


_ = load_dotenv(find_dotenv())


# Macros and constants
GEMINI_MODEL = 'gemini-pro'

# Set up the Google AI API
API_KEY = os.getenv("GOOGLE_API_KEY")

# PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
# LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")
# os.makedirs(LOGS_DIR, exist_ok=True)
# LOGS_FILE = os.path.join(LOGS_DIR, "app.log")
# with open(LOGS_FILE, "w") as f:
#     pass


def initialize_logger():
    logger = configure_logger(log_level="INFO")

    return logger


logger = initialize_logger()


class ResumeReviewer:
    def __init__(self) -> None:
        genai.configure(api_key=API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)

        self.system_prompt = """\
You are a professional hiring manager tasked with reviewing a resume. \
Your goal is to provide comprehensive feedback on the content of the resume \
to help the candidate improve their chances of securing a job interview. \
Your review should analyze various aspects of the resume, including its \
structure, clarity, relevance, and completeness. Additionally, provide \
constructive criticism and suggestions for areas of improvement, such as \
formatting, language, skills presentation, and overall presentation. Your \
feedback should be detailed and tailored to help the candidate showcase \
their qualifications and experiences effectively. Please ensure your \
feedback is professional, respectful, and aimed at assisting the candidate \
in presenting their best self to potential employers.

Here's the resume content extracted from the PDF, delimited by \
square brackets below:
"""

    def _extract_text(self, pdffile) -> str | None:
        """Extract text from the pdf using pdfplumber."""

        text = ""

        try:
            with pdfplumber.open(pdffile) as pdf:
                for page in pdf.pages:
                    logger.info(f"""\
Extracting text from page {page.page_number}...\
""")
                    try:
                        text += page.extract_text()
                    except Exception as e:
                        logger.error(f"""\
Error extracting text from page: {e}
Continuing with the next page...\
""")
                        continue
            
            logger.info("Text extracted successfully!")
            return text
        except Exception as e:
            logger.error(f"Error extracting text from resume: {e}")
            return None


    def _build_prompt(self, resumefile: str) -> str | None:
        """
        Build the full prompt from the system prompt and the 
        extracted resume text.
        """

        resume_text = self._extract_text(resumefile)

        if not resume_text:
            return None
        
        logger.info("Building the prompt...")
        full_prompt = f"""{self.system_prompt}\n[\n{resume_text}\n]"""

        return full_prompt
    

    def generate_feedback(self, resumepdffile: str) -> str:
        """
        Generate feedback using the Google AI API.
        """

        prompt = self._build_prompt(resumepdffile)

        if not prompt:
            response = """\
I apologize for the inconvenience. It appears there was an error on our \
end while processing the PDF file. You can try uploading the file again, \
and if the issue persists after a few attempts, you may want to try \
again later. 😓

Rest assured, we'll investigate the problem on our backend to ensure it \
doesn't happen again. Thank you for your patience, and please don't hesitate \
to reach out if you encounter any further issues. 😊\
"""
            return response
        else:
            try:
                logger.info("Generating response from the model...")
                response = self.model.generate_content(prompt)

                logger.info(f"""\
Response generated successfully! Below is the response from the model:
{response}

Sending only the text of the response to the user...\
""")

                return response.text
            except Exception as e:
                logger.error(f"Error generating response: {e}")

                response = """\
We apologize for the inconvenience. It seems there was an error while \
fetching the response from our model. 😓 Please try again now.

If the issue persists, please try again later, as it might be traffic-related. \
Rest assured, our team is actively working to resolve this \
issue on our end. Thank you for your patience and understanding. If you \
have any further questions or concerns, feel free to reach out to us. 😊\
"""

                return response
