import ollama
import re

def summary_cv_and_write_files(cv_text):
    model = 'deepseek-r1:8b_vram'
    prompt = """
You are a CV-to-JSON converter. Transform input CVs into JSON format following these rules:

1. PRESERVE THESE KEYS WITH EXACT TEXT:
   - "Name" (string)
   - "Technical Skills" (array)
   - "Education" (array)
   - "Foreign Languages" (array)
   - "Certifications" (array)
   - "Work Experience" (array, if exists)

2. PROCESS PROJECTS:
   "Project Experience" (object) containing:
   - "Hidden Skills" (array of 3-5 inferred skills)
   - "Technologies Used" (array of explicit tech items)

3. OUTPUT EXAMPLE:
{
  "Name": "Joh Doe",
  "Technical Skills": ["JavaScript", "React", "TypeScript", "Java", "Spring Boot", "AWS", "Docker", "SQL", "PostgreSQL"],
  "Foreign Languages": ["English", "Romanian"],
  "Education": [
    {
      "University Name": "MIT",
      "Program Duration": "2020-2024",
      "Degree Name": "BSc Computer Science"
    }
  ],
  "Certifications": [
    {
      "Title": "AWS Certified Machine Learning – Specialty",
      "Issuing Authority": "Amazon Web Services"
    },
    {
      "Title": "Data Science Professional",
      "Issuing Authority": "Data Science Council"
    }
  ],
  "Project Experience": [
    {
      "Title": "Machine Learning Model Deployment on AWS SageMaker",
      "Hidden Skills": ["Cloud Platforms Expertise", "Containerization Techniques", "CI/CD Pipeline Automation"],
      "Technologies Used": ["Python", "TensorFlow", "AWS SageMaker", "Docker", "Jenkins"]
    },
    {
      "Title": "Interactive Web Application Development",
      "Hidden Skills": ["Responsive Web Development", "UI/UX Design and Prototyping", "Database Integration"],
      "Technologies Used": ["JavaScript", "React.js", "Figma", "PostgreSQL"]
    }
  ]
}

4. SPECIAL RULES:
   - Omit "Project Experience" key entirely if no projects
   - Keep original dates/company names in "Work Experience"
   - Maintain exact certification/language wording
   - Only use double quotes, no trailing commas
   - No additional fields/comments

DO NOT ADD ANYTHING ELSE, STRICTLY FOLLOW THE OUTPUT EXAMPLE.
The text:
"""

    response = ollama.chat(
        model=model,
        # options={'keep_alive': '-1'},
        messages=[
            {'role': 'user', 'content': f"{prompt} {cv_text}"},
        ])
    # remove the entire <think>...<./think> section
    summary = (re.sub(r'<think\s*>.*?</think\s*>', '', response['message']['content'], flags=re.DOTALL)
               .replace('*', '')
               .replace('```json', '')
               .replace('```', '')
               .strip())
    return summary

if __name__ == '__main__':
    # Example CV text
    cv_text = """
Andrei Mihailescu
Technical Skills
- JavaScript, ReactJS, Node.js, SQL
- HTML, CSS, Bootstrap, AngularJS
- Python, Django, PostgreSQL, REST APIs
- TypeScript, VueJS, AWS, Docker
- Java, Spring Boot, OracleSQL, Kubernetes
Foreign Languages
- English: C1
- Spanish: B1
- French: A2
Education
- University Name: Politehnica University of Bucharest
- Program Duration: 4 years
- Master Degree Name: Politehnica University of Bucharest
- Program Duration: 2 years
Certifications
- AWS Certified Solutions Architect – Associate
- Certified Kubernetes Administrator (CKA)
- Oracle Certified Professional, Java SE 11 Developer
Project Experience
1. **Inventory Management System**
   Developed a robust inventory management system using Java and Spring Boot for the backend, with an OracleSQL database to handle complex queries and data storage. Implemented REST APIs to facilitate seamless communication between the backend and a responsive frontend built with AngularJS and Bootstrap. Deployed the application on a Kubernetes cluster, ensuring scalability and high availability. Technologies and tools used: Java, Spring Boot, OracleSQL, AngularJS, Bootstrap, Kubernetes.

2. **Real-time Data Analytics Platform**
   Created a real-time data analytics platform leveraging Python and Django for the backend, with PostgreSQL as the database to manage large datasets efficiently. Utilized ReactJS and TypeScript to build a dynamic and interactive user interface. Integrated AWS services for cloud storage and Docker for containerization, enabling smooth deployment and scalability. Technologies and tools used: Python, Django, PostgreSQL, ReactJS, TypeScript, AWS, Docker.
    """
    print(summary_cv_and_write_files(cv_text))