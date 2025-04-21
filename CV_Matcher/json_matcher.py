from google import genai
from google.genai import types
import glob

GOOGLE_API_KEY = ''

client = genai.Client(api_key=GOOGLE_API_KEY)

for model in client.models.list():
  if 'embedContent' in model.supported_actions:
    print(model.name)

def extract_text_from_docx(file_path):
    """Extract text from a .docx file, including paragraphs and tables."""
    doc = Document(file_path)
    text = []

    # Extract paragraphs
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)

    # Extract text from tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    text.append(paragraph.text)

    return '\n'.join(text)


def read_folder(folder_path):
    folder_path = f'{folder_path}/*.docx'

    # Extract text from all .docx files in the folder
    text_array = []
    ids_array = []
    cur_id = 1
    for file_path in glob.glob(folder_path):
        text = extract_text_from_docx(file_path)
        text_array.append(text)
        ids_array.append(cur_id)
        cur_id += 1

    return ids_array, text_array
