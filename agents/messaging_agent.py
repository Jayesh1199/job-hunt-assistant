from crewai import Agent, Task
from utils.config import GEMINI_API_KEY
import os
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY or ""

def get_messaging_agent():
    return Agent(
        role="Professional Outreach Specialist",
        goal="Write short, compelling, and personalized outreach messages for job seekers to send to hiring managers.",
        backstory=(
            "You are a networking expert and career coach who has helped thousands "
            "of candidates land interviews through personalized outreach. You know "
            "how to write messages that are professional, concise, and hard to ignore. "
            "You specialize in government and federal job applications."
        ),
        llm="gemini/gemini-2.0-flash-lite",
        verbose=True
    )

def create_messaging_task(agent, job_summary, agency, user_bio):
    return Task(
        description=(
            f"Write a short, professional outreach message for a job seeker applying "
            f"to a position at {agency}.\n\n"
            f"--- JOB SUMMARY ---\n{job_summary}\n\n"
            f"--- CANDIDATE BIO ---\n{user_bio}\n\n"
            f"The message should:\n"
            f"1. Be under 150 words\n"
            f"2. Express genuine interest in the role and agency\n"
            f"3. Highlight one or two relevant strengths from the bio\n"
            f"4. End with a clear call to action\n"
            f"5. Be suitable for LinkedIn or email outreach"
        ),
        expected_output=(
            "A professional outreach message under 150 words, "
            "personalized to the job and agency, suitable for "
            "LinkedIn or email, with a clear call to action."
        ),
        agent=agent
    )
