from google import genai
from google.genai import types
import glob

def extract_text_from_docx(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read().replace('\n', '')

    return text


def read_folder(folder_path):
    folder_path = f'{folder_path}/*.json'

    # Extract text from all .docx files in the folder
    text_array = []
    ids_array = []
    titles_array = []

    cur_id = 1
    for file_path in glob.glob(folder_path):
        text = extract_text_from_docx(file_path)
        text_array.append(text)
        ids_array.append(cur_id)
        titles_array.append(file_path)
        cur_id += 1

    return ids_array, text_array, titles_array
