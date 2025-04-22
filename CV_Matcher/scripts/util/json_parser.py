from google import genai
from google.genai import types

from docx import Document
import glob

from IPython.display import Markdown, display
import ollama
import time
import os
import re

def summary_cv_and_write_files(cvs, amount=500):
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
    if not os.path.exists('text_files'):
        os.makedirs('text_files', exist_ok=True)

    if not os.path.exists('text_files/candidates'):
        os.makedirs('text_files/candidates', exist_ok=True)

    for index, (key, value) in enumerate(cvs.items()):
        if index >= amount:
            break

        start_time = time.time()
        print(f'Generating summary for {key}')
        response = ollama.chat(
            model=model,
            # options={'keep_alive': '-1'},
            messages=[
                {'role': 'user', 'content': f"{prompt} {value}"},
            ]
        )

        # remove the entire <think>...<./think> section
        summary = (re.sub(r'<think\s*>.*?</think\s*>', '', response['message']['content'], flags=re.DOTALL)
                   .replace('*', '')
                   .replace('```json', '')
                   .replace('```', '')
                   .strip()
                   )
        file_name = key.replace('DataSet/cv\\', '').replace('.docx', '').strip()
        print(f'Writing summary to file: {file_name}')
        try:
            with open(f'text_files/candidates/{file_name}.json', 'w', encoding='utf-8') as f:
                f.write(summary)
        except Exception as e:
            print(f"Error writing file {file_name}: {e}")

        end_time = time.time()
        overall_time = end_time - start_time
        print(f"Overall time for {file_name}: {overall_time:.2f} seconds")
