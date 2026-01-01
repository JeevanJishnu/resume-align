
import os
import sys
import json
import re

# Add the project root to sys.path to import from main.py and template_engine
sys.path.append(os.getcwd())

from main import (
    get_cv_segments, 
    extract_summary, 
    extract_work_experience, 
    extract_projects, 
    extract_education, 
    extract_skills_it,
    extract_certifications
)

cv_text = """
Profile Summary

•	8+ years of experience in Software Development in the IT industry. Experienced in Core PHP and frameworks such as Laravel and Yii. Skilled in front-end technologies including HTML, CSS, and JavaScript (AJAX). Demonstrated experience in leading and guiding small development teams — overseeing task allocation, code reviews, and ensuring timely project delivery. Strong knowledge of programming logic, debugging techniques, and software development best practices. Possesses hands-on experience across the full Software Development Life Cycle (SDLC) including design, development, review, and integration testing. A proactive team player with excellent interpersonal, communication, and leadership

Work Experience

•  at Tecnonauts Technology Services Pvt Ltd, Kochi, India (Feb 2018 - Oct 2018| Web Developer)
Participated in analysis, design, and new development of applications. Designed, developed, and tested small, medium, and large-scale software Create website layout/user interface by using standard HTML/CSS practices.

•  at Aventus Informatics, Koratty, India (Nov 2018 - Feb 2021 |Jr. Software Engineer)
Worked on Laravel to build the Web Application. Worked on both the Frontend and Backend sides of various applications. Built various features for the client's products. Supported the team with technical debugging and unit testing. Worked on user guides.

• Software Engineer at AlignMinds Technologies, Kochi, India (Feb 2021)
Developed reusable web components using LitElement including email/SMS notification systems, message modals, quiz management interfaces, and document storage (DocuStore) that can be reused across applications. Integrated web components into Angular/React applications and built supporting Node.js APIs for seamless functionality. Optimized existing products through performance tuning and code refactoring, improving system efficiency. Created automation test scripts using Node.js with Mocha and Jest frameworks. Maintained IBM product schema and attribute mappings, ensuring data integrity. Provided technical support for debugging and unit testing across development teams. Developed comprehensive user documentation and technical guides.


Education

• Bachelors of Computer Applications from N/A (2010)
• Masters of Computer Applications from N/A (2014)

Project Details

• Web your Campus (N/A)
Role: Role: Web Application Developer. Web Your Campus is a data-driven online platform that engages students, parents, and teachers in managing academic activities and performance. Contributed to the analysis, design, and development of new features for the platform. Designed, developed, and tested software enhancements for various application sizes (small, medium, large). Conducted UI, functionality, and database access testing to meet client requirements. Collaborated with developers to ensure accurate implementation of program and system specifications. Worked with functional users to design alternative system solutions based on feedback. Prepared documentation for both program and user levels, maintaining version control for updates. Assisted in reviewing and analyzing program specifications to ensure alignment with work process changes.
Tech Stack: Laravel, AJAX, JS, MySQL, etc.

• Dreamplore (N/A)
Role: Role: Web Application Developer. Dreamplore is a dynamic website for tours and travels, managed by the admin, offering a range of features to enhance user and admin interaction. Assisted in all phases of the development lifecycle, including requirement gathering, report preparation, and database maintenance. Designed and developed dynamic websites based on client requirements, ensuring accurate data retrieval through PHP scripting. Collaborated with clients to understand feature requests, implementing additional functionality on existing web pages to meet deadlines. Developed and deployed new features to streamline web application processes and improve user experience.
Tech Stack: Core PHP, MySQL, etc., Sublime, cPanel.

• Xcruit (N/A)
Role: Role: Web Application Developer. Xcruit is an online job portal, which can connect recruiters and job seekers, providing better opportunities, that include both candidate and recruiter management. Enhanced existing dynamic web pages by adding new features and optimizing performance to meet project deadlines. Integrated open-source and third-party applications, maintaining quality assurance and system integrity. Collaborated with the development team to create and debug small coding modules, ensuring proper execution. Troubleshot, tested, and optimized web applications and databases for better performance and reliability. Developed and deployed new features to streamline web application tools and procedures. Utilized GitHub for version control and worked with various data types for backend management.
Tech Stack: Laravel, JS, AJAX, Elasticsearch, MySQL, etc., VS Code, Kibana, GIT, etc.

• Coast Soccer League (N/A)
Role: Role: Backend Developer. Overview: Coast Soccer League is the largest youth soccer gaming circuit in the United States. The web application serves as the admin portal for the league, managing team registrations, scheduling, standings, and reporting, while supporting both the CSL and referee apps. Users can utilize the CSL App to manage team details, report game results, and rate referees and other teams. Similarly, the Referee App helps referees manage schedules, keep score, and submit match reports. Added new features to existing web pages as per client requirements, enhancing the platform’s functionality. Developed and maintained the backend logic to support team registration, match reporting, and user management. Prepared detailed documentation at both the program and user levels, ensuring smooth communication and ease of access for future updates. Provided timely bug fixes during critical situations, ensuring minimal downtime for users.
Tech Stack: Yii1, AJAX, JS, XML, CSS, MySQL, VS Code, Git, Postman

• Tournament (N/A)
Role: Role: Full stack Developer. Overview: The Tournament System is an admin portal for managing multiple tournaments, including team registration via a payment gateway, bracketing, scheduling, scoring, and standings. Developed a new application from scratch using Laravel 8, incorporating features such as team registration, scoring, and scheduling to streamline tournament management.
Tech Stack: Laravel 8, MySQL., VS Code, Git, Postman.

• Crunchet Web Application (N/A)
Role: Role: Full stack Developer. Collaborated on responsive UI design and component-based architecture. Developed and integrated frontend components with dynamic API endpoints. Managed environment configuration, CORS policies, and frontend-backend communication.
Tech Stack: React, Node.js, Express, VS Code, Git, Postman

• Crunchet Mobile App (N/A)
Role: Role: Backend Developer. Ensured smooth integration of the new feature with the app’s backend, enabling users to select from multiple categories during the signup process. Added a new API to the existing app to support the signup process or organizational accounts, in addition to the pre-existing personal category. Improved user experience by streamlining the registration process for both personal and organizational accounts.
Tech Stack: Laravel 5.3, MySQL, VS Code, Git, Postman

• Thoroughbred (N/A)
Role: Role: Backend Developer. Overview: Thoroughbred Analytics specializes in providing advanced data analytics for the thoroughbred horse racing industry. The project focused on integrating new responsive pages into an existing PHP project, leveraging the latest JavaScript technologies. Integrated responsive pages with legacy PHP and modern JavaScript. Refactored core functions to support responsive design and improve UX. Collaborated with frontend team for data consistency and performance. Crunchet Overview: Crunchet is a platform that allows users to create and share meaningful stories by combining personal, web, and social media content. The app allows users to sign up and manage their profiles, and can now support both personal and organizational accounts.
Tech Stack: Core PHP 5.4, MySQL, JavaScript, VS Code, Git, cPanel, Docker

• ETC (N/A)
Role: Role: Frontend Developer. ETC is a global leader in the design and manufacturing of lighting, rigging, and control systems for entertainment and architectural applications. Built features for project data extraction and enabled export/download of project configurations in XML and JSON formats, streamlining project documentation workflow. Integrated REST APIs to fetch, display, and manage real-time project data, ensuring accuracy and seamless interactivity.
Tech Stack: React 18, VS Code, Git, Postman

• LMS Reports (N/A)
Role: Role: Backend Developer. Resolved bugs within reporting modules to ensure accurate display of course statuses and user statistics. Improved stability and data consistency across report views used by administrators and instructors.
Tech Stack: Laravel 5.3, MySQL, VS Code, Git, Postman

• LMS Application (N/A)
Role: Role: Full stack Developer. Integrated email web component into the Angular-Node based Learning Management System, handling both front-end integration and backend connectivity. Developed Node.js APIs and implemented AWS SQS queue with Lambda functions for reliable email notification processing.
Tech Stack: Angular 19, NodeJS, LitElement, VS Code, Git

• WebComponent (N/A)
Role: Role: Front Development. Overview: Experienced in developing reusable and modular web components using LitElement and JavaScript. Built UI elements such as modals, editors, and notification components with cross-framework compatibility, focusing on performance, maintainability, and consistent design across applications. Responsibilities Developed modular, reusable web components for enterprise applications including email/SMS notification systems, message modals, quiz management interfaces, and DocuStore (document management system). Integrated components into Angular/React based applications with Node.js backend APIs. LMS Overview: A Learning Management System (LMS) platform that generates detailed reports on user activity, including course completion status (Completed, In Progress, Not Started, Archived) and usage statistics.
Tech Stack: Lit, VS Code, Git


Key Skills and Knowledge
Laravel 11, 8.0, 5.2, 4.2, JavaScript, HTML5, Core PHP, CSS, jQuery, JSON, AJAX, Elasticsearch, MySQL, Yii1, Tailwind CSS, PostgreSQL, Other Skills, Node.js, Angular.js, React, AWS, Lit (Web component), Express, Python, Flask, Microsoft Visual Studio, Code, Kibana Postman Git Asana, Kochi, India, design, and tested small, medium, and large-scale software, enhancements., application functionality, and database access as

Other Skills
Laravel 11, 8.0, 5.2, 4.2, JavaScript, HTML5, Core PHP, CSS, jQuery, JSON, AJAX, Elasticsearch, MySQL, Yii1, Tailwind CSS, PostgreSQL, Other Skills, Node.js, Angular.js, React, AWS, Lit (Web component), Express, Python, Flask, Microsoft Visual Studio, Code, Kibana Postman Git Asana, Kochi, India, design, and tested small, medium, and large-scale software, enhancements., application functionality, and database access as

Tools
Laravel 11, 8.0, 5.2, 4.2, JavaScript, HTML5, Core PHP, CSS, jQuery, JSON, AJAX, Elasticsearch, MySQL, Yii1, Tailwind CSS, PostgreSQL, Other Skills, Node.js, Angular.js, React, AWS, Lit (Web component), Express, Python, Flask, Microsoft Visual Studio, Code, Kibana Postman Git Asana, Kochi, India, design, and tested small, medium, and large-scale software, enhancements., application functionality, and database access as
"""

def main():
    # 1. Segment the CV
    segments = get_cv_segments(cv_text)
    
    # 2. Extract specific data
    extracted_data = {
        "summary": extract_summary(segments.get("summary", "")),
        "work_experience": extract_work_experience(segments.get("experience", "")),
        "projects": extract_projects(segments.get("projects", "")),
        "education": extract_education(segments.get("education", "")),
        "skills": extract_skills_it(segments.get("skills", ""))["skills"],
        "tools": extract_skills_it(segments.get("skills", ""))["tools"],
        "certifications": extract_certifications(segments.get("certifications", ""))
    }
    
    # Print segments found
    print("--- SEGMENTS DETECTED ---")
    for k, v in segments.items():
        if v:
            print(f"{k.upper()}: {len(v)} chars")
            
    print("\n--- EXTRACTED DATA ---")
    print(json.dumps(extracted_data, indent=2))

if __name__ == "__main__":
    main()
