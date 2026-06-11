from crewai import Agent, Task
from utils.config import GEMINI_API_KEY
import os
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY or ""

def get_jd_analyst_agent():
    return Agent(
        role="Job Description Analyst",
        goal="Analyze job descriptions and extract key responsibilities, required skills, and qualifications.",
        backstory=(
            "You are an expert career coach and recruiter with years of experience "
            "reading and breaking down job postings. You help job seekers understand "
            "exactly what employers are looking for."
        ),
        llm="gemini/gemini-2.0-flash-lite",
        verbose=True
    )
