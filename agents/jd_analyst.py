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
        llm="gemini/gemini-2.0-flash",
        verbose=True
    )


def create_jd_analysis_task(agent, job_description):
    return Task(
        description=(
            f"Analyze the following job description and extract the key details:\n\n"
            f"{job_description}\n\n"
            "Please identify and summarize:\n"
            "1. Job responsibilities\n"
            "2. Required skills and qualifications\n"
            "3. Preferred qualifications\n"
            "4. Key keywords a resume should include"
        ),
        expected_output=(
            "A structured markdown report with sections for:\n"
            "- Job Responsibilities\n"
            "- Required Skills & Qualifications\n"
            "- Preferred Qualifications\n"
            "- Resume Keywords"
        ),
        agent=agent,
        output_file="data/report.md"
    )
