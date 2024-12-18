import vertexai
from vertexai.generative_models import GenerativeModel
from text_extraction import detect_document
import json
import os 
from dotenv import load_dotenv

load_dotenv()
project_id = os.getenv("PROJECT_ID")

def give_json(text):
    vertexai.init(project=project_id)#, location="us-central1")

    prompt="Prompt start: Using the info in the medical text, give a json output with the following format:{\"patient\":{\"name\":\"John Doe\",\"age\":42,\"gender\":\"Male\",\"birthDate\":\"1982-01-15\"},\"observations\":[{\"type\":\"Blood Pressure\",\"value\":\"120/80 mmHg\",\"date\":\"2023-11-22\"}],\"conditions\":[{\"code\":\"ICD10-DM\",\"description\":\"Diabetes Mellitus\"}],\"medications\":[{\"name\":\"Metformin\",\"dosage\":\"500mg twice daily\",\"prescriptionDate\":\"2023-10-10\"}],\"allergies\":[{\"allergen\":\"Penicillin\",\"severity\":\"Severe\"}],\"procedures\":[{\"type\":\"Surgery\",\"date\":\"2023-09-05\"}],\"diagnosticReports\":[{\"type\":\"Lab Test\",\"results\":{\"WBC\":8000,\"RBC\":4.5},\"date\":\"2023-12-01\"}]} Medical text:"

    model = GenerativeModel("gemini-2.0-flash-exp")

    prompt+=text
    response = model.generate_content(prompt)

    print(response.text)
    json_str = response.text
    json_str = json_str.replace('```json', '')
    json_str = json_str.replace('```', '')
    data = json.loads(json_str)

    return data
   


