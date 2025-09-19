import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Provide Info – Internship Hub",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Minimal card button CSS
st.markdown("""
<style>
header, #MainMenu, footer { visibility: hidden; }
.input-container { max-width: 900px; margin: 0 auto; padding: 2.5rem 0; }
.input-title {
    text-align: center;
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 1rem;
}
.input-subtitle {
    text-align: center;
    color: #b1b3c6;
    font-size: 1.15rem;
    margin-bottom: 3rem;
}
.card-btn {
    background: white !important;
    border: 2.5px solid #eee !important;
    border-radius: 15px !important;
    box-shadow: 0 4px 28px rgba(102,126,234,0.08);
    padding: 2.35rem 0 2rem 0 !important;
    min-height: 180px !important;
    width: 100% !important;
    margin-bottom: 0;
    margin-top: 0;
    font-size: 1.26rem;
    font-weight: 750;
    color: #0e1333;
    text-align: center !important;
    transition: all .18s;
}
.card-btn:hover {
    border:2.5px solid #667eea !important;
    box-shadow: 0 8px 38px -10px #667eea35;
    color:#5336f6 !important;
    background:#f8f9ff !important;
}
@media (max-width: 768px) {
    .input-title { font-size: 2rem; }
    .input-subtitle { font-size: 1rem; margin-bottom: 2rem; }
    .card-btn { 
        font-size: 1.1rem;
        padding: 1.5rem 0 !important;
        min-height: 150px !important;
    }
}
</style>
""", unsafe_allow_html=True)

if 'manual_mode' not in st.session_state:
    st.session_state.manual_mode = False
if 'cv_mode' not in st.session_state:
    st.session_state.cv_mode = False

st.markdown('<div class="input-container">', unsafe_allow_html=True)
st.markdown('<div class="input-title">📝 Provide Your Information</div>', unsafe_allow_html=True)
st.markdown('<div class="input-subtitle">How would you like to share your details?</div>', unsafe_allow_html=True)

if not st.session_state.manual_mode and not st.session_state.cv_mode:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄\nUpload CV\n\nUpload your resume in PDF or DOCX format", key="cv_card", use_container_width=True):
            st.session_state.cv_mode = True
            st.session_state.manual_mode = False
        st.markdown('<style>#cv_card {margin-top:24px;} #cv_card button{min-height:180px;}</style>', unsafe_allow_html=True)
    with col2:
        if st.button("✏️\nManual Input\n\nEnter your details manually", key="manual_card", use_container_width=True):
            st.session_state.manual_mode = True
            st.session_state.cv_mode = False
        st.markdown('<style>#manual_card {margin-top:24px;} #manual_card button{min-height:180px;}</style>', unsafe_allow_html=True)

# CV Upload Section
if st.session_state.cv_mode:
    st.markdown("---")
    st.markdown("### 📄 Upload Your CV")
    st.markdown("""
    <div style='border:2px dashed #ccc; border-radius: 8px; padding:2rem; text-align:center; background:#fafafa; margin-bottom:1rem;'>
        <h4>Drag and drop your CV here</h4>
        <p>Supports PDF and DOCX files up to 10MB</p>
    </div>
    """, unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Choose your CV file",
        type=['pdf', 'docx'],
        help="Upload your resume in PDF or DOCX format"
    )
    if uploaded_file is not None:
        st.success("✅ CV uploaded successfully!")
        col1, col2, col3 = st.columns(3)
        with col1: st.info(f"**File:** {uploaded_file.name}")
        with col2: st.info(f"**Size:** {uploaded_file.size / 1024:.1f} KB")
        with col3: st.info(f"**Type:** {uploaded_file.type.split('/')[-1].upper()}")
        st.info("🔍 CV processing feature will extract your information automatically.")
        st.session_state.user_info = {
            'source': 'cv',
            'file_name': uploaded_file.name,
            'file_type': uploaded_file.type,
            'upload_date': datetime.now().isoformat()
        }

# Manual Input Section (minimal fields)
if st.session_state.manual_mode:
    st.markdown("---")
    st.markdown("### ✏️ Enter Details Manually")
    with st.form("simple_form"):
        col1, col2 = st.columns(2)
        with col1:
            technical_skills = st.text_area(
                "Technical Skills *",
                placeholder="E.g. Python, JavaScript, React, SQL, Data Analysis",
                help="Separate skills with commas",
                height=80
            )
            education_level = st.selectbox(
                "Education Level *",
                ["Select...", "High School", "Pursuing Bachelor's", "Completed Bachelor's", 
                 "Pursuing Master's", "Completed Master's", "PhD", "Other"]
            )
            work_experience = st.selectbox(
                "Work Experience Level *",
                ["Select...", "No experience", "0-6 months", "6 months-1 year", "1-2 years", "2+ years"]
            )
        with col2:
            course_name = st.text_input("Course Name *", placeholder="E.g. B.Tech, B.Sc, M.Sc, etc.")
            year_of_study = st.selectbox(
                "Year of Study *",
                ["Select..."] + [str(i) for i in range(1,7)]
            )
            specialisation = st.text_input("Specialisation *", placeholder="E.g. Computer Science, Mechanical, etc.")

        submitted = st.form_submit_button("🚀 Save Information", use_container_width=True)
        errors = []
        if submitted:
            if not technical_skills.strip():
                errors.append("Technical skills are required")
            if education_level == "Select...":
                errors.append("Education level is required")
            if not course_name.strip():
                errors.append("Course name is required")
            if year_of_study == "Select...":
                errors.append("Year of study is required")
            if not specialisation.strip():
                errors.append("Specialisation is required")
            if work_experience == "Select...":
                errors.append("Work experience level is required")
            if errors:
                st.error("Please fix the following:\n" + "\n".join(f"- {error}" for error in errors))
            else:
                st.session_state.user_info = {
                    "source": "manual",
                    "technical_skills": [s.strip() for s in technical_skills.split(",") if s.strip()],
                    "education_level": education_level,
                    "course_name": course_name,
                    "year_of_study": year_of_study,
                    "specialisation": specialisation,
                    "work_experience_level": work_experience
                }
                st.success("✅ Info saved!")
                st.info("You can now continue to get internship recommendations.")

st.markdown("---")
if 'user_info' in st.session_state:
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("← Back to Home", use_container_width=True):
            st.session_state.manual_mode = False
            st.session_state.cv_mode = False
            st.switch_page("app.py")
    with c2:
        if st.button("🔄 Reset", use_container_width=True):
            for key in ['user_info', 'manual_mode', 'cv_mode']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    with c3:
        if st.button("🔍 Continue to Recommendations", use_container_width=True):
            st.switch_page("pages/Recommendations.py")
else:
    if st.button("← Back to Home", use_container_width=True):
        st.session_state.manual_mode = False
        st.session_state.cv_mode = False
        st.switch_page("app.py")
st.markdown('</div>', unsafe_allow_html=True)