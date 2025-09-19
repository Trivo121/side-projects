import streamlit as st
import json

st.set_page_config(page_title="Internship Hub", page_icon="🎯", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    header { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .main-container{
        max-width:1300px;
        margin:0 auto;
        padding:2rem 1rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .page-title{
        text-align:center;
        font-size:3.5rem;
        font-weight:800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom:0.5rem;
        padding:0;
    }
    .page-subtitle{
        text-align:center;
        color:#999;
        font-size:1.15rem;
        margin-bottom:2.6rem;
        font-weight:300;
    }
    .get-started-btn-container{
        position:absolute;
        top:1.5rem;
        right:1.5rem;
        z-index:1000;
    }
    .get-started-btn{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color:white;
        padding:0.9rem 2.2rem;
        border:none;
        border-radius:32px;
        font-size:1.05rem;
        font-weight:600;
        cursor:pointer;
        transition:all 0.25s ease;
        box-shadow:0 5px 18px rgba(102,126,234,0.35);
        white-space:nowrap;
    }
    .get-started-btn:hover{ transform: translateY(-3px); }
    
    /* Flip Card Styles */
    .flip-card {
        background-color: transparent;
        width: 100%;
        max-width: 320px;
        height: 300px;
        perspective: 1000px;
        margin-bottom: 1.6rem;
    }
    .flip-card-inner {
        position: relative;
        width: 100%;
        height: 100%;
        text-align: left;
        transition: transform 0.6s;
        transform-style: preserve-3d;
    }
    .flip-card:hover .flip-card-inner {
        transform: rotateY(180deg);
    }
    .flip-card-front, .flip-card-back {
        position: absolute;
        width: 100%;
        height: 100%;
        -webkit-backface-visibility: hidden;
        backface-visibility: hidden;
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.06);
        border: 1px solid #f6f6f8;
        border-left: 4px solid #667eea20;
        padding: 1.4rem 1.2rem;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        overflow: hidden;
    }
    .flip-card-front {
        background: #ffffff;
    }
    .flip-card-back {
        background: #ffffff;
        transform: rotateY(180deg);
        justify-content: flex-start;
        overflow-y: auto;
    }
    
    /* Existing Card Styles - Adapted for HTML */
    .card-title{
        font-size:1.35rem !important;      
        font-weight:800 !important;          
        line-height:1.12 !important;
        margin:0 0 0.32rem 0 !important;
        letter-spacing:0.1px !important;
        color: #222 !important;
        -webkit-text-fill-color: #222 !important;
        opacity: 1 !important;
        filter: none !important;
        position: relative !important;
        z-index: 5 !important;
        display: -webkit-box !important;
        -webkit-box-orient: vertical !important;
        -webkit-line-clamp: 2 !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        word-break: break-word !important;
    }
    .card-company{
        font-size:0.95rem;
        color:#667EEA;
        font-weight:600;
        margin:0.13rem 0 0.55rem 0;
        letter-spacing:0.2px;
    }
    .card-skills{
        display:flex;
        flex-wrap:wrap;
        gap:0.32rem;
        margin:0.6rem 0 0.25rem 0;
    }
    .skill-tag{
        background: #f6f8fc;
        color:#5f6c7b;
        font-size:0.77rem;
        font-weight:500;
        padding:0.22rem 0.80rem;
        border-radius:8px;
        border:1px solid #e5e7eb;
        box-shadow:none;
        letter-spacing:0.1px;
        transition: background 0.2s;
    }
    .skill-tag:hover {
        background: #eaecff;
        color:#4338ca;
        border:1px solid #c7d2fe;
    }
    .card-details{
        display:flex;
        justify-content:space-between;
        align-items:center;
        margin-top:0.48rem;
    }
    .card-location{
        font-size:0.92rem;
        color:#717687;
        display:flex;
        align-items:center;
        gap:0.4rem;
        font-weight:400;
    }
    .card-stipend{
        font-size:1rem;
        font-weight:700;
        color:#21b573;
        letter-spacing:0.2px;
    }
    .back-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #52489C;
        margin-bottom: 1rem;
    }
    .back-list {
        list-style-type: disc;
        padding-left: 1.2rem;
        margin: 0;
        flex: 1;
        overflow-y: auto;
    }
    .back-list li {
        font-size: 0.9rem;
        color: #555;
        margin-bottom: 0.5rem;
        line-height: 1.3;
    }
    
    @media (max-width:768px){
        .page-title{ font-size:2.4rem; }
        .page-subtitle{ font-size:1.0rem; margin-bottom:1.6rem; }
        .card-title{ font-size:1.03rem !important; }
        .flip-card-front, .flip-card-back { padding:1.1rem; height: 260px; }
        .skill-tag{ font-size:0.72rem; padding:0.16rem 0.55rem; }
        .back-list li { font-size: 0.85rem; }
    }
</style>
""", unsafe_allow_html=True)

def get_internships():
    # Full data with roles_responsibilities as you provided:
    return [
        {
            "id": 1,
            "title": "Frontend Developer Intern",
            "company": "TechCorp",
            "location": "Bangalore",
            "stipend": "15K",
            "skills": ["HTML/CSS", "JavaScript", "React", "Bootstrap"],
            "roles_responsibilities": [
                "Assist in developing and implementing responsive web pages using HTML, CSS, JavaScript, and frameworks like React and Bootstrap.",
                "Collaborate with UX/UI designers and backend developers to translate wireframes and prototypes into functional products.",
                "Conduct cross-browser and cross-device testing, debug and resolve frontend issues to enhance user experience.",
                "Participate in code reviews and maintain code quality, adhering to modern development standards.",
                "Stay up-to-date with the latest frontend trends and suggest improvements to optimize website performance."
            ]
        },
        {
            "id": 2,
            "title": "ML Engineer Intern",
            "company": "DataTech",
            "location": "Hyderabad",
            "stipend": "20K",
            "skills": ["Python", "Machine Learning", "TensorFlow", "Data Analysis"],
            "roles_responsibilities": [
                "Support development and validation of machine learning models using Python, TensorFlow, and scikit-learn.",
                "Assist in cleaning, preprocessing, and exploration of large datasets for model training.",
                "Document experiment results, evaluate model performance, and tune parameters.",
                "Collaborate with engineering teams to integrate ML models into product pipelines.",
                "Research and report on state-of-the-art trends in data science and AI applications."
            ]
        },
        {
            "id": 3,
            "title": "Backend Developer Intern",
            "company": "ServerStack",
            "location": "Mumbai",
            "stipend": "18K",
            "skills": ["Node.js", "API Development", "Databases", "Server Management"],
            "roles_responsibilities": [
                "Help design, develop, and maintain RESTful APIs and server-side applications using Node.js or similar technologies.",
                "Work with relational and NoSQL databases: schema design, writing queries, and optimization.",
                "Troubleshoot backend issues, support server deployment, and perform debugging and performance tuning.",
                "Implement authentication, data validation, and security measures.",
                "Collaborate with cross-functional teams to integrate backend systems with frontend interfaces."
            ]
        },
        {
            "id": 4,
            "title": "Data Analyst Intern",
            "company": "AnalyticsPro",
            "location": "Delhi",
            "stipend": "16K",
            "skills": ["SQL", "Excel", "Python", "Data Visualization"],
            "roles_responsibilities": [
                "Gather, preprocess, and analyze data using Excel, SQL, and Python for business insights and reporting.",
                "Create dashboards and data visualizations using tools like Power BI/Tableau.",
                "Collaborate with different departments to understand data needs and deliver actionable insights.",
                "Document analysis workflows, data cleaning procedures, and ensure data quality.",
                "Support ad-hoc analysis and reports to assist ongoing business strategies."
            ]
        },
        {
            "id": 5,
            "title": "DevOps Engineer Intern",
            "company": "CloudSolutions",
            "location": "Remote",
            "stipend": "17K",
            "skills": ["Docker", "AWS", "CI/CD", "Kubernetes"],
            "roles_responsibilities": [
                "Assist in building and maintaining CI/CD pipelines using Jenkins/GitLab CI.",
                "Support Docker containerization and deployment of applications on Kubernetes clusters.",
                "Monitor infrastructure health and automate common processes in cloud deployments (AWS/GCP/Azure).",
                "Document scripts, workflows, and assist in writing operation runbooks.",
                "Help troubleshoot, diagnose, and resolve infrastructure-related issues."
            ]
        },
        {
            "id": 6,
            "title": "Mobile App Developer Intern",
            "company": "AppWorks",
            "location": "Chennai",
            "stipend": "16K",
            "skills": ["React Native", "Flutter", "Mobile UI", "API Integration"],
            "roles_responsibilities": [
                "Participate in building cross-platform mobile applications using React Native or Flutter.",
                "Design and implement user interfaces following platform-specific guidelines.",
                "Integrate mobile apps with backend services via APIs.",
                "Test and debug apps on real devices and simulators.",
                "Contribute ideas to improve functionality, performance, and reliability of mobile apps."
            ]
        },
        {
            "id": 7,
            "title": "UX/UI Designer Intern",
            "company": "DesignStudio",
            "location": "Bangalore",
            "stipend": "14K",
            "skills": ["Figma", "Adobe XD", "Prototyping", "User Research"],
            "roles_responsibilities": [
                "Create wireframes and prototypes using Figma, Adobe XD as per product requirements.",
                "Conduct user research, analyze user feedback, and contribute to user journey maps.",
                "Collaborate with developers to ensure the feasibility and fidelity of the final design.",
                "Maintain style guides and support design system development.",
                "Participate in design reviews and iterate on concepts based on feedback."
            ]
        },
        {
            "id": 8,
            "title": "Cloud Engineer Intern",
            "company": "CloudInfra",
            "location": "Pune",
            "stipend": "19K",
            "skills": ["AWS", "Azure", "Cloud Architecture", "Terraform"],
            "roles_responsibilities": [
                "Assist in designing and deploying cloud infrastructure using AWS/Azure.",
                "Support Infrastructure as Code (IaC) automation via Terraform, CloudFormation.",
                "Monitor system health and implement best practices for cloud security and governance.",
                "Help with cloud cost optimization and usage analysis.",
                "Troubleshoot cloud-related issues and create technical documentation."
            ]
        },
        {
            "id": 9,
            "title": "Python Developer Intern",
            "company": "CodeMasters",
            "location": "Remote",
            "stipend": "18K",
            "skills": ["Python", "Django", "Flask", "REST APIs"],
            "roles_responsibilities": [
                "Design, develop, and maintain backend components/applications using Python, Flask, or Django.",
                "Implement RESTful APIs and integrate with databases.",
                "Write clean, efficient, and testable code while following best practices.",
                "Participate in code reviews and collaborate with team members.",
                "Debug, test, and document modules for ongoing projects."
            ]
        },
        {
            "id": 10,
            "title": "React Developer Intern",
            "company": "WebCraft",
            "location": "Gurgaon",
            "stipend": "17K",
            "skills": ["React", "JavaScript", "Redux", "CSS"],
            "roles_responsibilities": [
                "Develop and maintain user-facing features with React.js and Redux.",
                "Build reusable components and front-end libraries for future use.",
                "Work closely with backend teams to integrate APIs.",
                "Optimize components for maximum performance and responsiveness.",
                "Participate in bug fixing, code reviews, and continuous improvement."
            ]
        },
        {
            "id": 11,
            "title": "AI Research Intern",
            "company": "NeuroLabs",
            "location": "Bangalore",
            "stipend": "22K",
            "skills": ["Python", "Deep Learning", "PyTorch", "Research Methodology"],
            "roles_responsibilities": [
                "Assist in the research and development of AI/ML models using PyTorch and TensorFlow.",
                "Perform literature reviews and implement state-of-the-art algorithms.",
                "Analyze research data/results and prepare technical documentation or research papers.",
                "Collaborate with researchers to design new experiments and prototypes.",
                "Present findings at internal meetings or conferences."
            ]
        },
        {
            "id": 12,
            "title": "Product Manager Intern",
            "company": "Productify",
            "location": "Mumbai",
            "stipend": "21K",
            "skills": ["Product Strategy", "Market Research", "Analytics", "Agile"],
            "roles_responsibilities": [
                "Assist in market research, competitor analysis, and user interviews.",
                "Help define product requirements, maintain product documentation, and update roadmaps.",
                "Work with engineering, design, and sales teams to support product lifecycle management.",
                "Analyze user feedback and product data to identify improvement opportunities.",
                "Participate in Agile ceremonies and support sprint planning and tracking."
            ]
        },
        {
            "id": 13,
            "title": "Data Scientist Intern",
            "company": "DataForge",
            "location": "Bangalore",
            "stipend": "23K",
            "skills": ["Python", "Machine Learning", "Statistics", "Data Mining"],
            "roles_responsibilities": [
                "Clean, preprocess, and analyze large datasets to extract insights.",
                "Implement supervised and unsupervised machine learning models in Python.",
                "Visualize data and results using Matplotlib, Seaborn, or Tableau.",
                "Assist in experimentation, reporting, and presentation of analytical findings.",
                "Collaborate on building data pipelines for scalable solutions."
            ]
        },
        {
            "id": 14,
            "title": "iOS Developer Intern",
            "company": "AppleTech",
            "location": "Hyderabad",
            "stipend": "19K",
            "skills": ["Swift", "Xcode", "iOS SDK", "Core Data"],
            "roles_responsibilities": [
                "Participate in designing and developing iOS applications using Swift and Xcode.",
                "Implement UI designs and integrate app features with Core Data and other iOS services.",
                "Conduct unit testing, resolve bugs, and update apps for App Store guidelines compliance.",
                "Work closely with designers and backend teams to deliver high-quality user experiences.",
                "Contribute to documentation and codebase improvement initiatives."
            ]
        },
        {
            "id": 15,
            "title": "Android Developer Intern",
            "company": "GoogleWorks",
            "location": "Mumbai",
            "stipend": "18K",
            "skills": ["Kotlin", "Android Studio", "Firebase", "Material Design"],
            "roles_responsibilities": [
                "Develop and maintain Android mobile apps using Kotlin and Android Studio.",
                "Follow Material Design guidelines to build beautiful, accessible UIs.",
                "Integrate Firebase for analytics, authentication, and notifications.",
                "Debug apps, write unit tests, and ensure device and version compatibility.",
                "Document development process and assist with release cycles."
            ]
        },
        {
            "id": 16,
            "title": "Full Stack Developer Intern",
            "company": "StackMasters",
            "location": "Delhi",
            "stipend": "20K",
            "skills": ["JavaScript", "Node.js", "React", "MongoDB"],
            "roles_responsibilities": [
                "Build complete web solutions using React for frontend and Node.js/MongoDB for backend.",
                "Create, document, and maintain RESTful APIs.",
                "Collaborate with designers to implement high-quality, responsive UIs.",
                "Debug and optimize application flow end-to-end.",
                "Participate in Agile development, reviews, and sprints."
            ]
        },
        {
            "id": 17,
            "title": "UI Designer Intern",
            "company": "DesignHub",
            "location": "Remote",
            "stipend": "15K",
            "skills": ["Figma", "Adobe Creative Suite", "Prototyping", "CSS"],
            "roles_responsibilities": [
                "Design interface mockups and high-fidelity prototypes using Figma or Adobe Suite.",
                "Develop and maintain a design system for consistent branding.",
                "Work with frontend developers to implement designs accurately.",
                "Incorporate feedback and iterate on visuals based on testing.",
                "Maintain clear documentation and style guidelines."
            ]
        },
        {
            "id": 18,
            "title": "QA Engineer Intern",
            "company": "QualityTech",
            "location": "Chennai",
            "stipend": "16K",
            "skills": ["Testing", "Automation", "Selenium", "Bug Tracking"],
            "roles_responsibilities": [
                "Design and execute manual and automated test cases for web/mobile apps.",
                "Maintain bug tracking records and communicate defects to development.",
                "Develop automation scripts using Selenium and related tools.",
                "Perform regression, functional, and performance testing.",
                "Document QA processes and participate in code reviews for testability."
            ]
        },
        {
            "id": 19,
            "title": "Game Developer Intern",
            "company": "GameStudio",
            "location": "Bangalore",
            "stipend": "17K",
            "skills": ["Unity", "C#", "Game Design", "3D Modeling"],
            "roles_responsibilities": [
                "Assist in developing core game features in Unity/C#.",
                "Integrate 3D models and design game mechanics.",
                "Participate in playtesting and iterative design for game balancing.",
                "Debug, profile, and optimize gameplay for various platforms.",
                "Collaborate creatively with art and sound teams."
            ]
        },
        {
            "id": 20,
            "title": "Network Engineer Intern",
            "company": "NetSolutions",
            "location": "Pune",
            "stipend": "18K",
            "skills": ["Networking", "Cisco", "Security", "Troubleshooting"],
            "roles_responsibilities": [
                "Assist in configuring and maintaining routing, switching, and firewall devices.",
                "Monitor network performance, troubleshoot issues, and escalate as needed.",
                "Support network documentation and inventory tracking.",
                "Participate in network security audits and configuration reviews.",
                "Work with IT teams to implement reliable and secure network solutions."
            ]
        },
        {
            "id": 21,
            "title": "Security Analyst Intern",
            "company": "SecureTech",
            "location": "Remote",
            "stipend": "19K",
            "skills": ["Cybersecurity", "Penetration Testing", "Risk Assessment", "SIEM"],
            "roles_responsibilities": [
                "Monitor security alerts and incidents via SIEM tools.",
                "Assist with vulnerability assessments, penetration testing, and reporting.",
                "Document and update security policies, incident responses, and risk assessments.",
                "Support internal security training/awareness programs.",
                "Research and implement industry best practices for cybersecurity."
            ]
        },
        {
            "id": 22,
            "title": "Database Admin Intern",
            "company": "DataBase Pro",
            "location": "Gurgaon",
            "stipend": "16K",
            "skills": ["SQL", "MySQL", "Database Design", "Performance Tuning"],
            "roles_responsibilities": [
                "Assist with daily DB maintenance, backup/restore, and data integrity checks.",
                "Optimize performance via query tuning and indexing.",
                "Support database migrations, configuration, user permissions, and troubleshooting.",
                "Document backup procedures, performance reports, and data policies.",
                "Collaborate with devs for schema design and data modeling."
            ]
        },
        {
            "id": 23,
            "title": "BI Analyst Intern",
            "company": "BusinessIntel",
            "location": "Bangalore",
            "stipend": "20K",
            "skills": ["SQL", "Tableau", "Power BI", "Data Warehousing"],
            "roles_responsibilities": [
                "Develop and maintain BI dashboards/reports in Tableau/Power BI.",
                "Extract, clean, and transform data for business intelligence needs.",
                "Work with stakeholders to gather report requirements and suggest KPIs.",
                "Participate in data warehousing efforts for scalable reporting.",
                "Document BI processes and provide training to business users."
            ]
        },
        {
            "id": 24,
            "title": "Tech Support Intern",
            "company": "SupportPlus",
            "location": "Mumbai",
            "stipend": "15K",
            "skills": ["Troubleshooting", "Customer Service", "Hardware", "Software"],
            "roles_responsibilities": [
                "Respond to user queries and technical support requests in person, by phone, or by email.",
                "Troubleshoot hardware/software problems and guide users through solutions.",
                "Log issues and escalate complex problems to higher-level support.",
                "Assist with installation, configuration, and ongoing maintenance of IT equipment.",
                "Maintain technical documentation and contribute to self-help resources."
            ]
        }
    ]

internships = get_internships()

st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Get Started Button (positioned via CSS)
col1, col2 = st.columns([1, 10])
with col1:
    st.markdown('<div class="get-started-btn-container">', unsafe_allow_html=True)
    if st.button("🚀 Get Started", key="get_started_top_right", help="Start your application"):
        st.switch_page("pages/2_Input.py")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="page-title">🍋 Internship Hub</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Discover your perfect internship from top companies</div>', unsafe_allow_html=True)

# Display internships in grid
cards_per_row = 4
for i in range(0, len(internships), cards_per_row):
    cols = st.columns(cards_per_row)
    for j in range(cards_per_row):
        idx = i + j
        if idx < len(internships):
            internship = internships[idx]
            with cols[j]:
                # Spacer for alignment
                st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
                
                # Flip Card HTML
                skills_html = ''.join([f'<span class="skill-tag">{skill}</span>' for skill in internship["skills"]])
                responsibilities_html = ''.join([f'<li>{rr}</li>' for rr in internship["roles_responsibilities"]])
                
                st.markdown(f"""
                <div class="flip-card">
                    <div class="flip-card-inner">
                        <div class="flip-card-front">
                            <div class="card-title">{internship['title']}</div>
                            <div class="card-company">{internship['company']}</div>
                            <div class="card-skills">
                                {skills_html}
                            </div>
                            <div class="card-details">
                                <div class="card-location">📍 {internship['location']}</div>
                                <div class="card-stipend">₹{internship['stipend']}</div>
                            </div>
                        </div>
                        <div class="flip-card-back">
                            <div class="back-title">Roles & Responsibilities</div>
                            <ul class="back-list">
                                {responsibilities_html}
                            </ul>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)