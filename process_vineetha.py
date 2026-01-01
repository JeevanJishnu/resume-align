
import os
import json
import logging
from docx import Document
from main import (
    extract_summary, extract_skills, extract_work_experience, 
    extract_projects, extract_education, extract_certifications,
    preprocess_image, get_cv_segments, extract_name_and_contact
)
from template_engine.template_manager import get_template_schema
from template_engine.template_mapper import fill_template

# Setup logging
logging.basicConfig(level=logging.INFO)

CV_TEXT = """VINEETHA T

PROFESSIONAL SUMMARY
Vineetha T 8+ years of experience in Software Development in the IT industry. Experienced in Core PHP and frameworks such as Laravel and Yii. Skilled in front-end technologies including HTML, CSS, and JavaScript (AJAX). Demonstrated experience in leading and guiding small development teams — overseeing task allocation, code reviews, and ensuring timely project delivery. Strong knowledge of programming logic, debugging techniques, and software development best practices. Possesses hands-on experience across the full Software Development Life Cycle (SDLC) including design, development, review, and integration testing. A proactive team player with excellent interpersonal, communication, and leadership.
TECHNICAL SKILLS
diverse work environments, Laravel 11, JavaScript, HTML5, Core PHP, CSS, jQuery, JSON, AJAX, Elasticsearch, MySQL, Yii1, Tailwind CSS, PostgreSQL, Other Skills, Node.js, Angular.js, React, AWS, Lit, Web, component, Express, Python, Flask, Microsoft, Visual, Studio, Code, Kibana, Postman, Git, Asana, Create and maintain software documentation, Application, Developer, enhancements, required by the client organizations
PROFESSIONAL EXPERIENCE
Software Engineer
AlignMinds Technologies, Kochi, India	Feb 2021
N/A
•	Developed reusable web components using LitElement including email/SMS notification systems, message modals, quiz management interfaces, and document storage (DocuStore) that can be reused across applications.
•	Integrated web components into Angular/React applications and built supporting Node.js APIs for seamless functionality.
•	Optimized existing products through performance tuning and code refactoring, improving system efficiency.
•	Created automation test scripts using Node.js with Mocha and Jest frameworks.
•	Maintained IBM product schema and attribute mappings, ensuring data integrity.
•	Provided technical support for debugging and unit testing across development teams.
•	Developed comprehensive user documentation and technical guides.

PROJECT PORTFOLIO
WebComponent | VS Code, Git
Role: Front Development
•	Overview: Experienced in developing reusable and modular web components using LitElement and JavaScript.
•	Built UI elements such as modals, editors, and notification components with cross-framework compatibility, focusing on performance, maintainability, and consistent design across applications.
•	Responsibilities Developed modular, reusable web components for enterprise applications including email/SMS notification systems, message modals, quiz management interfaces, and DocuStore (document management system).
•	Integrated components into Angular/React based applications with Node.js backend APIs.
•	LMS Overview: A Learning Management System (LMS) platform that generates detailed reports on user activity, including course completion status (Completed, In Progress, Not Started, Archived) and usage statistics.

LMS Application | VS Code, Git
Role: Full stack Developer
•	Integrated email web component into the Angular-Node based Learning Management System, handling both front-end integration and backend connectivity.
•	Developed Node.js APIs and implemented AWS SQS queue with Lambda functions for reliable email notification processing.

LMS Reports | VS Code, Git, Postman
Role: Backend Developer
•	Resolved bugs within reporting modules to ensure accurate display of course statuses and user statistics.
•	Improved stability and data consistency across report views used by administrators and instructors.

ETC | VS Code, Git, Postman
Role: Frontend Developer
•	ETC is a global leader in the design and manufacturing of lighting, rigging, and control systems for entertainment and architectural applications.
•	Built features for project data extraction and enabled export/download of project configurations in XML and JSON formats, streamlining project documentation workflow.
•	Integrated REST APIs to fetch, display, and manage real-time project data, ensuring accuracy and seamless interactivity.

Thoroughbred | VS Code, Git, cPanel, Docker
Role: Backend Developer
•	Overview: Thoroughbred Analytics specializes in providing advanced data analytics for the thoroughbred horse racing industry.
•	The project focused on integrating new responsive pages into an existing PHP project, leveraging the latest JavaScript technologies.
•	Integrated responsive pages with legacy PHP and modern JavaScript.
•	Refactored core functions to support responsive design and improve UX.
•	Collaborated with frontend team for data consistency and performance.
•	Crunchet Overview: Crunchet is a platform that allows users to create and share meaningful stories by combining personal, web, and social media content.
•	The app allows users to sign up and manage their profiles, and can now support both personal and organizational accounts.

Crunchet Mobile App | VS Code, Git, Postman
Role: Backend Developer
•	Ensured smooth integration of the new feature with the app’s backend, enabling users to select from multiple categories during the signup process.
•	Added a new API to the existing app to support the signup process or organizational accounts, in addition to the pre-existing personal category.
•	Improved user experience by streamlining the registration process for both personal and organizational accounts.

Crunchet Web Application | VS Code, Git, Postman
Role: Full stack Developer
•	Collaborated on responsive UI design and component-based architecture.
•	Developed and integrated frontend components with dynamic API endpoints.
•	Managed environment configuration, CORS policies, and frontend-backend communication.

Tournament | VS Code, Git, Postman.
Role: Full stack Developer
•	Overview: The Tournament System is an admin portal for managing multiple tournaments, including team registration via a payment gateway, bracketing, scheduling, scoring, and standings.
•	Developed a new application from scratch using Laravel 8, incorporating features such as team registration, scoring, and scheduling to streamline tournament management.

Coast Soccer League | VS Code, Git, Postman
Role: Backend Developer
•	Overview: Coast Soccer League is the largest youth soccer gaming circuit in the United States.
•	The web application serves as the admin portal for the league, managing team registrations, scheduling, standings, and reporting, while supporting both the CSL and referee apps.
•	Users can utilize the CSL App to manage team details, report game results, and rate referees and other teams.
•	Similarly, the Referee App helps referees manage schedules, keep score, and submit match reports.
•	Added new features to existing web pages as per client requirements, enhancing the platform’s functionality.
•	Developed and maintained the backend logic to support team registration, match reporting, and user management.
•	Prepared detailed documentation at both the program and user levels, ensuring smooth communication and ease of access for future updates.
•	Provided timely bug fixes during critical situations, ensuring minimal downtime for users.

Xcruit | VS Code, Kibana, GIT, etc.
Role: Web Application Developer
•	Xcruit is an online job portal, which can connect recruiters and job seekers, providing better opportunities, that include both candidate and recruiter management.
•	Enhanced existing dynamic web pages by adding new features and optimizing performance to meet project deadlines.
•	Integrated open-source and third-party applications, maintaining quality assurance and system integrity.
•	Collaborated with the development team to create and debug small coding modules, ensuring proper execution.
•	Troubleshot, tested, and optimized web applications and databases for better performance and reliability.
•	Developed and deployed new features to streamline web application tools and procedures.
•	Utilized GitHub for version control and worked with various data types for backend management.

Dreamplore | Sublime, cPanel.
Role: Web Application Developer
•	Dreamplore is a dynamic website for tours and travels, managed by the admin, offering a range of features to enhance user and admin interaction.
•	Assisted in all phases of the development lifecycle, including requirement gathering, report preparation, and database maintenance.
•	Designed and developed dynamic websites based on client requirements, ensuring accurate data retrieval through PHP scripting.
•	Collaborated with clients to understand feature requests, implementing additional functionality on existing web pages to meet deadlines.
•	Developed and deployed new features to streamline web application processes and improve user experience.

Web your Campus | Sublime.
Role: Web Application Developer
•	Web Your Campus is a data-driven online platform that engages students, parents, and teachers in managing academic activities and performance.
•	Contributed to the analysis, design, and development of new features for the platform.
•	Designed, developed, and tested software enhancements for various application sizes (small, medium, large).
•	Conducted UI, functionality, and database access testing to meet client requirements.
•	Collaborated with developers to ensure accurate implementation of program and system specifications.
•	Worked with functional users to design alternative system solutions based on feedback.
•	Prepared documentation for both program and user levels, maintaining version control for updates.
•	Assisted in reviewing and analyzing program specifications to ensure alignment with work process changes.

EDUCATION
Masters of Computer Applications - N/A (2014)
Bachelors of Computer Applications - N/A (2010)
"""

def process_vineetha():
    # 1. Segmented Extraction
    segs = get_cv_segments(CV_TEXT)
    
    # 2. Extract Data using main.py logic
    fullname = "Vineetha T"
    work_exp = extract_work_experience(segs.get("experience", ""))
    companies = [job.get("company", "") for job in work_exp if job.get("company")]
    
    skills_obj = extract_skills(segs.get("skills", ""), fullname)
    
    extracted = {
        "full_name": fullname,
        "email": "N/A",
        "phone": "N/A",
        "linkedin": "N/A",
        "summary": extract_summary(segs.get("summary", "")),
        "skills": skills_obj["skills"],
        "tools": skills_obj["tools"],
        "work_experience": work_exp,
        "projects": extract_projects(segs.get("projects", ""), companies),
        "education": extract_education(segs.get("education", "")),
        "certifications": extract_certifications(segs.get("certifications", ""))
    }
    
    # 3. Load Template (Using AM0275 as default "premium" template)
    template_name = "AM0275"
    schema = get_template_schema(template_name)
    if not schema:
        print("Template not found!")
        return

    # 4. Fill Template
    output_path = "output/Vineetha_T_Reformatted_v6.docx"
    os.makedirs("output", exist_ok=True)
    
    fill_template(schema, extracted, output_path)
    print(f"Successfully generated reformatted CV at: {output_path}")
    print("\n--- Extracted Data Preview ---")
    print(json.dumps(extracted, indent=2))

if __name__ == "__main__":
    process_vineetha()

