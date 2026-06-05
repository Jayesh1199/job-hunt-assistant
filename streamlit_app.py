import streamlit as st
from usajobs_api import fetch_usajobs
from orchestrator import run_pipeline

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="AI Job Hunt Assistant",
    page_icon="💼",
    layout="centered"
)

# ── Title & Intro ─────────────────────────────────────────────
st.title("💼 AI Job Hunt Assistant")
st.markdown("""
Welcome! This tool uses **AI agents** powered by CrewAI and Google Gemini to:
- 🔍 Fetch real government job listings from USAJobs
- 📊 Analyze the job description
- 📝 Tailor your resume summary and cover letter
- 📨 Draft a personalized LinkedIn outreach message
""")

st.divider()

# ── Input Form ────────────────────────────────────────────────
st.subheader("🔎 Job Search Settings")

keyword = st.text_input("Job Keyword", value="business analyst")
location = st.text_input("Location", value="remote")

st.subheader("👤 Your Information")

resume_text = st.text_area(
    "Paste Your Resume",
    height=250,
    placeholder="Paste your full resume text here..."
)

user_bio = st.text_area(
    "Short Bio",
    height=100,
    placeholder="e.g. I'm a data professional with 3 years of experience..."
)

st.divider()

# ── Step 1: Fetch Jobs Button ─────────────────────────────────
if st.button("🔍 Search Jobs", type="primary"):
    if not resume_text or not user_bio:
        st.warning("⚠️ Please fill in both your resume and bio first.")
    else:
        with st.spinner("Fetching jobs from USAJobs..."):
            jobs = fetch_usajobs(keyword, location, results_per_page=5)
            if not jobs:
                st.error("❌ No jobs found. Try a different keyword or location.")
            else:
                st.session_state["jobs"] = jobs
                st.session_state["resume_text"] = resume_text
                st.session_state["user_bio"] = user_bio
                st.success(f"✅ Found {len(jobs)} jobs! Select the ones you want to apply to.")

# ── Step 2: Show Job Checkboxes ───────────────────────────────
if "jobs" in st.session_state:
    st.subheader("📋 Select Jobs to Apply To")

    selected_jobs = []

    for i, job in enumerate(st.session_state["jobs"]):
        title = job["MatchedObjectDescriptor"]["PositionTitle"]
        agency = job["MatchedObjectDescriptor"]["OrganizationName"]
        location_display = job["MatchedObjectDescriptor"]["PositionLocationDisplay"]

        checked = st.checkbox(
            f"**{title}** — {agency} ({location_display})",
            key=f"job_{i}"
        )
        if checked:
            selected_jobs.append(job)

    st.divider()

    # ── Step 3: Apply Button ──────────────────────────────────
    if st.button("🚀 Apply to Selected Jobs", type="primary"):
        if not selected_jobs:
            st.warning("⚠️ Please select at least one job.")
        else:
            for job in selected_jobs:
                title = job["MatchedObjectDescriptor"]["PositionTitle"]
                agency = job["MatchedObjectDescriptor"]["OrganizationName"]

                st.subheader(f"📝 {title} at {agency}")

                with st.spinner(f"Running AI agents for {title}..."):
                    result = run_pipeline(
                        job_data=job,
                        resume_text=st.session_state["resume_text"],
                        user_bio=st.session_state["user_bio"]
                    )

                st.markdown(result)
                st.divider()