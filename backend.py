import base64
import os
from google.generativeai import types
from google.generativeai import GenerativeModel
import google.generativeai as genai
from dotenv import load_dotenv
from pydantic import BaseModel
import json

load_dotenv()


class suggestion(BaseModel):
    codeExplanation: str
    codeError: str
    codeSolution: str

api_key= os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)


generation_config={
    'temperature':0.85,
    'response_mime_type': "text/plain",
    'response_mime_type': "application/json",
    'response_schema': suggestion,
}

model= genai.GenerativeModel(
    model_name="gemini-2.5-flash-preview-05-20",
    generation_config=generation_config
    )






def generate_prompt(language, code_snippet):

    prompt = f"""
You are CodeMentor, an AI coding tutor.  
Given a snippet of code and the programming language, your job is to:
1. Explain the code clearly.
2. Identify and explain any errors (if any).
3. Suggest an improved or corrected version of the code.

Return ONLY valid JSON in this exact format:

{{
  "codeExplanation": "Clear, beginner-friendly explanation of what the code does.",
  "codeError": "Description of the error",
  "codeSolution": "How to fix the error"
}}


Code Snippet:{code_snippet}
Programming Language: {language} 

Instructions:
- If there are no errors, return an empty array for errorsFound.
-If Programming Language is empty, still return a response
-Always return the answers, everytime!
- Output ONLY valid JSON with no extra formatting or explanations.
"""
    
    try:
        input= model.generate_content([

            f'example of prompt: {prompt}',
            'output: ',
        ]   
        )
        input= json.loads(input.text)
        Explanation= input['codeExplanation']
        Error= input['codeError']
        solution= input['codeSolution']

        return Explanation, Error, solution


    except Exception as e:
        print(f'error is : {e}')

    
    
 






if __name__ == "__main__":
    while True:
        prompt= input('YOU: ')
        if prompt.lower() in ['bye','exit', 'close', 'quit']:
            print('Goodbye')
            break
        Explanation, Error, solution= generate_prompt(prompt)

        print(f'BOT code explanation is: {Explanation}')
        print(f'BOT error found is: {Error}')
        print(f'BOT solution found is: {solution}')

