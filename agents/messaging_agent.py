from crewai import Agent, Task
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.config import GEMINI_API_KEY

# Using gemini-3.1-flash-lite (same as other agents for quota consistency)
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    google_api_key=GEMINI_API_KEY,
    temperature=0.8
)


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
        llm=llm,
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