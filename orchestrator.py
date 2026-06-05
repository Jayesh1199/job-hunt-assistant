from crewai import Crew, Process
from agents.jd_analyst import get_jd_analyst_agent, create_jd_analysis_task
from agents.resume_cl_agent import get_resume_cl_agent, create_resume_cl_task
from agents.messaging_agent import get_messaging_agent, create_messaging_task
from usajobs_api import fetch_usajobs
from utils.tracking import log_application, save_cover_letter_file


def load_resume():
    with open("data/sample_resume.txt", "r") as f:
        return f.read()


def extract_between_markers(text, start_marker, end_marker=None):
    """Extract text between two markers. If no end_marker, extract till end."""
    if start_marker not in text:
        return ""
    start = text.index(start_marker) + len(start_marker)
    if end_marker and end_marker in text[start:]:
        end = text.index(end_marker, start)
        return text[start:end].strip()
    return text[start:].strip()


def run_pipeline(job_data, resume_text, user_bio):
    # Extract job details from the job_data dictionary
    job_summary = job_data["MatchedObjectDescriptor"]["UserArea"]["Details"]["JobSummary"]
    job_title = job_data["MatchedObjectDescriptor"]["PositionTitle"]
    agency_name = job_data["MatchedObjectDescriptor"]["OrganizationName"]

    print(f"\nAnalyzing job: {job_title} at {agency_name}\n")

    # Create all three agents
    jd_agent = get_jd_analyst_agent()
    resume_agent = get_resume_cl_agent()
    messaging_agent = get_messaging_agent()

    # Create all three tasks
    jd_task = create_jd_analysis_task(jd_agent, job_summary)
    resume_task = create_resume_cl_task(resume_agent, job_summary, resume_text)
    messaging_task = create_messaging_task(messaging_agent, job_summary, agency_name, user_bio)

    # Build and run the Crew
    crew = Crew(
        agents=[jd_agent, resume_agent, messaging_agent],
        tasks=[jd_task, resume_task, messaging_task],
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()

    # ── Extract resume summary and cover letter ───────────────
    resume_output = str(resume_task.output)

    resume_summary = extract_between_markers(
        resume_output,
        "<<RESUME_SUMMARY>>",
        "<<COVER_LETTER>>"
    )

    cover_letter = extract_between_markers(
        resume_output,
        "<<COVER_LETTER>>"
    )

    # ── Log the application ───────────────────────────────────
    log_application(job_title, agency_name, resume_summary)
    print(f"✅ Application logged for: {job_title}")

    # ── Save the cover letter ─────────────────────────────────
    cover_letter_path = save_cover_letter_file(job_title, cover_letter)
    print(f"✅ Cover letter saved to: {cover_letter_path}")

    return str(result)


if __name__ == "__main__":
    jobs = fetch_usajobs("business analyst")
    if jobs:
        result = run_pipeline(
            job_data=jobs[0],
            resume_text=load_resume(),
            user_bio="I'm a data professional passionate about public service."
        )
        print("\n===== FINAL RESULT =====")
        print(result)