from crewai import Agent, Task
from utils.config import GEMINI_API_KEY
import os
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY or ""

def get_resume_cl_agent():
    return Agent(
        role="Resume and Cover Letter Writer",
        goal="Tailor resumes and write personalized cover letters that match job descriptions perfectly.",
        backstory=(
            "You are an expert career consultant and professional writer with 15 years "
            "of experience helping candidates land government jobs. You know exactly how "
            "to highlight relevant skills and craft compelling cover letters that get "
            "candidates noticed by federal hiring managers."
        ),
        llm="gemini/gemini-2.0-flash-lite",
        verbose=True
    )

def create_resume_cl_task(agent, job_summary, resume_text):
    return Task(
        description=(
            f"Using the job description and the candidate's resume below, do two things:\n\n"
            f"1. Tailor the candidate's resume summary to match the job requirements.\n"
            f"2. Write a personalized cover letter suitable for a government job application.\n\n"
            f"--- JOB DESCRIPTION ---\n{job_summary}\n\n"
            f"--- CANDIDATE RESUME ---\n{resume_text}\n\n"
            f"Format your response EXACTLY like this:\n"
            f"<<RESUME_SUMMARY>>\n"
            f"(write the tailored resume summary here)\n\n"
            f"<<COVER_LETTER>>\n"
            f"(write the full cover letter here)"
        ),
        expected_output=(
            "A tailored resume summary marked with <<RESUME_SUMMARY>> "
            "and a full cover letter marked with <<COVER_LETTER>>."
        ),
        agent=agent,
        output_file="data/resume_agent_output.txt"
    )
