import json
import google.generativeai as genai
from typing import List, Dict, Any
import streamlit as st
import os
import re
import logging

# ----------------------- Configuration -----------------------
# NOTE: You've asked to keep the API key inside this file.
# For production / shared repositories, move this to environment variables or a secrets manager.
GEMINI_API_KEY = "AIzaSyA83lSdFOBprXCSb7XwzSQptnnkYZ-hRnk"
genai.configure(api_key=GEMINI_API_KEY)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InternshipMatcher:
    def __init__(self):
        # We store a list of preferred model names and attempt to use them at runtime.
        self.model_names = [
            'gemini-1.5-flash',
            'gemini-1.5-pro',
            'gemini-pro-latest'
        ]

        # Keep a model object if the library exposes one in your installed version
        self.model = None
        self.model_name = None

        # Try to initialize a model object if the client supports it. If it fails,
        # we'll fall back to calling the library generically at runtime.
        for mn in self.model_names:
            try:
                # Some library versions may provide a GenerativeModel class
                self.model = genai.GenerativeModel(mn)
                self.model_name = mn
                st.info(f"Using Gemini model object: {mn}")
                break
            except Exception:
                # Not available or failed — we'll try the next
                self.model = None
                self.model_name = mn  # still keep a candidate name

        if self.model is None:
            st.info("No model object available locally; will attempt API calls with candidate model names.")

    def load_internships(self) -> List[Dict[str, Any]]:
        """Load internships from JSON file or fallback to hardcoded data"""
        json_path = 'internships.json'
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except Exception as e:
                st.warning(f"Could not load internships.json: {str(e)}. Using fallback data.")

        # Fallback hardcoded data (cleaned and fixed syntax errors)
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

    def create_user_profile(self, user_info: Dict[str, Any]) -> str:
        """Create a formatted user profile string for AI analysis"""
        if user_info.get('source') == 'manual':
            profile = (
                "User Profile:\n"
                f"- Technical Skills: {', '.join(user_info.get('technical_skills', []))}\n"
                f"- Education Level: {user_info.get('education_level', 'Not specified')}\n"
                f"- Course: {user_info.get('course_name', 'Not specified')}\n"
                f"- Year of Study: {user_info.get('year_of_study', 'Not specified')}\n"
                f"- Specialization: {user_info.get('specialisation', 'Not specified')}\n"
                f"- Work Experience: {user_info.get('work_experience_level', 'Not specified')}\n"
            )
        else:
            # For CV mode, we'd extract info here in the future
            profile = (
                "User Profile from CV:\n"
                f"- File: {user_info.get('file_name', 'Unknown')}\n"
                f"- Upload Date: {user_info.get('upload_date', 'Unknown')}\n"
                f"- Note: CV processing not fully implemented yet\n"
            )

        return profile

    def _call_gemini_api(self, prompt: str) -> str:
        """Centralized method to call Gemini using best available approach.

        This tries (in order):
          1) model.generate_content if model object exists and provides it
          2) genai.generate_text / genai.generate if available
          3) fallback to raising an exception so caller can use local fallback logic
        """
        # 1) If we have a model object and it exposes a generate_content method
        if self.model is not None and hasattr(self.model, 'generate_content'):
            try:
                resp = self.model.generate_content(prompt)
                # Many wrappers return an object with .text — try to extract
                text = getattr(resp, 'text', None)
                if text is None:
                    text = str(resp)
                return text.strip()
            except Exception as e:
                logger.warning(f"Model object generate_content failed: {e}")

        # 2) Try calling top-level genai APIs using candidate model names
        for mn in self.model_names:
            try:
                # try a few method names depending on the library version
                if hasattr(genai, 'generate_text'):
                    resp = genai.generate_text(model=mn, prompt=prompt)
                    text = getattr(resp, 'text', None) or str(resp)
                    return text.strip()
                elif hasattr(genai, 'generate'):
                    resp = genai.generate(model=mn, prompt=prompt)
                    text = getattr(resp, 'text', None) or str(resp)
                    return text.strip()
                else:
                    # Last resort: try calling genai directly and hope for a meaningful __str__
                    resp = genai.__dict__.get('generate')(model=mn, prompt=prompt) if 'generate' in genai.__dict__ else None
                    if resp is not None:
                        text = getattr(resp, 'text', None) or str(resp)
                        return text.strip()
            except Exception as e:
                logger.info(f"Attempt with model {mn} failed: {e}")
                continue

        raise RuntimeError("No working Gemini API method found in installed google.generativeai package")

    def analyze_match(self, user_profile: str, internship: Dict[str, Any]) -> Dict[str, Any]:
        """Use Gemini AI to analyze match between user and internship"""
        # If no model available, use fallback immediately
        if self.model is None and not hasattr(genai, 'generate_text') and not hasattr(genai, 'generate'):
            return self._create_fallback_analysis(user_profile, internship)

        prompt = f"""
You are an expert career counselor. Analyze how well this user matches with the given internship opportunity.

{user_profile}

Internship Details:
- Title: {internship['title']}
- Company: {internship['company']}
- Location: {internship['location']}
- Skills Required: {', '.join(internship['skills'])}
- Responsibilities: {'; '.join(internship['roles_responsibilities'][:3])}

Please provide a concise analysis in JSON format:
{{
    "match_score": <number 0-100>,
    "skill_alignment": "<brief 1-2 sentence description>",
    "key_strengths": "<brief 1-2 sentence description>",
    "areas_for_improvement": "<brief 1-2 sentence description>",
    "recommendation_reason": "<brief 1-2 sentence explanation>"
}}

Be specific and helpful. Focus on practical advice.
"""

        try:
            response_text = self._call_gemini_api(prompt)

            # Clean the response to extract JSON
            if response_text.startswith('```json'):
                response_text = response_text[len('```json'):]
                if response_text.endswith('```'):
                    response_text = response_text[:-3]
                response_text = response_text.strip()
            elif response_text.startswith('```'):
                response_text = response_text[3:]
                if response_text.endswith('```'):
                    response_text = response_text[:-3]
                response_text = response_text.strip()

            analysis = json.loads(response_text)

            # Validate the response structure
            required_keys = ['match_score', 'skill_alignment', 'key_strengths', 'areas_for_improvement', 'recommendation_reason']
            for key in required_keys:
                if key not in analysis:
                    analysis[key] = f"Analysis for {key} not available"

            # Ensure match_score is within valid range
            if not isinstance(analysis['match_score'], (int, float)) or analysis['match_score'] < 0 or analysis['match_score'] > 100:
                analysis['match_score'] = 50

            return analysis

        except json.JSONDecodeError as e:
            logger.warning(f"JSON parsing error for {internship['title']}: {str(e)}")
            return self._create_fallback_analysis(user_profile, internship)
        except Exception as e:
            logger.warning(f"AI Analysis Error for {internship['title']}: {str(e)}")
            return self._create_fallback_analysis(user_profile, internship)

    def _create_fallback_analysis(self, user_profile: str, internship: Dict[str, Any]) -> Dict[str, Any]:
        """Create a fallback analysis when AI fails"""
        # Robustly extract user skills from profile text
        user_skills: List[str] = []
        m = re.search(r"Technical Skills:\s*(.*)", user_profile)
        if m:
            user_skills = [s.strip() for s in m.group(1).split(',') if s.strip()]

        match_score = self.simple_skill_match(user_skills, internship['skills'])

        # Specific matching skills for description
        matching_skills = []
        for user_skill in user_skills:
            for req_skill in internship['skills']:
                if user_skill.lower() in req_skill.lower() or req_skill.lower() in user_skill.lower():
                    matching_skills.append(req_skill)
                    break

        skill_alignment = f"You have experience in {len(matching_skills)} out of {len(internship['skills'])} required skills"
        if matching_skills:
            skill_alignment += f": {', '.join(matching_skills[:2])}"
            if len(matching_skills) > 2:
                skill_alignment += f" and {len(matching_skills)-2} more"
        skill_alignment += "."

        missing_skills = [skill for skill in internship['skills'] if not any(user_skill.lower() in skill.lower() or skill.lower() in user_skill.lower() for user_skill in user_skills)]

        areas_improvement = "Focus on developing skills in "
        if missing_skills:
            areas_improvement += f"{', '.join(missing_skills[:2])}"
            if len(missing_skills) > 2:
                areas_improvement += f" and {len(missing_skills)-2} other areas"
        else:
            areas_improvement += "advanced concepts in your existing skill areas"
        areas_improvement += " to strengthen your candidacy."

        key_strengths = "Your technical foundation"
        if matching_skills:
            key_strengths += f" in {matching_skills[0]}" if len(matching_skills) == 1 else f" in areas like {matching_skills[0]}"
        key_strengths += f" aligns well with {internship['company']}'s technology stack."

        recommendation_reason = f"This {internship['title']} position at {internship['company']} offers "
        if match_score >= 60:
            recommendation_reason += "excellent growth opportunities building on your existing skills."
        elif match_score >= 30:
            recommendation_reason += "a good learning opportunity to expand your technical expertise."
        else:
            recommendation_reason += "a chance to explore new technologies and broaden your skill set."

        return {
            "match_score": int(match_score),
            "skill_alignment": skill_alignment,
            "key_strengths": key_strengths,
            "areas_for_improvement": areas_improvement,
            "recommendation_reason": recommendation_reason
        }

    def simple_skill_match(self, user_skills: List[str], required_skills: List[str]) -> float:
        """Enhanced skill matching algorithm"""
        if not user_skills or not required_skills:
            return 30.0  # Default score when no skills to compare

        user_skills_lower = [skill.lower().strip() for skill in user_skills]
        required_skills_lower = [skill.lower().strip() for skill in required_skills]

        matches = 0.0
        for req_skill in required_skills_lower:
            best_match = 0.0
            for user_skill in user_skills_lower:
                # Exact match
                if req_skill == user_skill:
                    best_match = 1.0
                    break
                # Partial match
                elif req_skill in user_skill or user_skill in req_skill:
                    best_match = max(best_match, 0.8)
                # Technology family matches
                elif any(tech in req_skill and tech in user_skill for tech in 
                        ['python', 'java', 'react', 'node', 'sql', 'css', 'html', 'js', 'api', 'data']):
                    best_match = max(best_match, 0.6)
                # Programming language generalization
                elif any(lang in req_skill for lang in ['python', 'java', 'javascript', 'c++', 'c#']) and \
                     any(lang in user_skill for lang in ['python', 'java', 'javascript', 'c++', 'c#']):
                    best_match = max(best_match, 0.4)

            matches += best_match

        score = (matches / len(required_skills)) * 100
        return min(100, max(0, score))  # Ensure score is between 0-100

    def get_recommendations(self, user_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get AI-ranked internship recommendations"""
        if not user_info:
            st.error("No user information provided")
            return []

        try:
            internships = self.load_internships()
            if not internships:
                st.error("No internships data available")
                return []

            user_profile = self.create_user_profile(user_info)
            recommendations: List[Dict[str, Any]] = []

            # Show progress bar
            progress_bar = st.progress(0.0)
            status_text = st.empty()

            total_internships = len(internships)

            for i, internship in enumerate(internships):
                try:
                    status_text.text(f'Analyzing {internship["title"]} at {internship["company"]}... ({i+1}/{total_internships})')

                    # Get AI analysis
                    analysis = self.analyze_match(user_profile, internship)

                    # Combine internship data with analysis
                    recommendation = {
                        **internship,
                        'ai_analysis': analysis,
                        'match_score': analysis.get('match_score', 50)
                    }

                    recommendations.append(recommendation)

                except Exception as e:
                    logger.exception(f"Error analyzing {internship.get('title', 'Unknown')}: {str(e)}")
                    # Add with default analysis
                    recommendation = {
                        **internship,
                        'ai_analysis': self._create_fallback_analysis(user_profile, internship),
                        'match_score': 40
                    }
                    recommendations.append(recommendation)

                progress_bar.progress((i + 1) / total_internships)

            # Sort by match score (highest first)
            recommendations.sort(key=lambda x: x.get('match_score', 0), reverse=True)

            status_text.text('Analysis complete!')
            progress_bar.empty()
            status_text.empty()

            return recommendations

        except Exception as e:
            logger.exception(f"Critical error in get_recommendations: {str(e)}")
            st.error(f"Critical error in get_recommendations: {str(e)}")
            return []


# Global instance
matcher = InternshipMatcher()


def get_internship_recommendations(user_info: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Main function to get recommendations"""
    try:
        return matcher.get_recommendations(user_info)
    except Exception as e:
        st.error(f"Failed to get recommendations: {str(e)}")
        return []


# If this file executed directly, simple Streamlit UI to test
if __name__ == '__main__':
    st.title("Internship Matcher (Demo)")

    st.write("Enter some basic info (manual mode) and click Get Recommendations")

    technical_skills = st.text_input("Technical skills (comma separated)", value="Python, TensorFlow")
    education_level = st.selectbox("Education Level", ["Undergraduate", "Graduate", "PhD", "Other"])
    course_name = st.text_input("Course name", value="Computer Science")
    year_of_study = st.text_input("Year of Study", value="3")
    specialisation = st.text_input("Specialisation", value="Machine Learning")
    work_experience_level = st.selectbox("Work experience", ["None", "0-1 years", "1-3 years", "3+ years"]) 

    if st.button("Get Recommendations"):
        user_info = {
            'source': 'manual',
            'technical_skills': [s.strip() for s in technical_skills.split(',') if s.strip()],
            'education_level': education_level,
            'course_name': course_name,
            'year_of_study': year_of_study,
            'specialisation': specialisation,
            'work_experience_level': work_experience_level
        }

        recs = get_internship_recommendations(user_info)

        st.write(f"Top {min(10, len(recs))} recommendations")
        for r in recs[:10]:
            st.markdown(f"**{r['title']}** at *{r['company']}* — Match: {r.get('match_score')}")
            st.text(r['ai_analysis'].get('skill_alignment', ''))
            st.write('---')
