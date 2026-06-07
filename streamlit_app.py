st.markdown("#### 📄 Upload Your Resume")
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

resume_text = ""

if uploaded_file is not None:
    import pdfplumber
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            resume_text += page.extract_text() or ""
    st.success("✅ Resume uploaded and extracted successfully!")
else:
    resume_text = st.text_area(
        "Or paste your resume text here",
        height=200,
        placeholder="Paste your full resume text here..."
    )
