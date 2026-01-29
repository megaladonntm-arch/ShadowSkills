import os
from openai import OpenAI
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

class CodeRequest(BaseModel):
    prompt: str

api_key = ""

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=api_key,
)

def analyze_code(request: CodeRequest):
    try:
        code_to_analyze = request.prompt
        analysis_prompt = f'''Please analyze the following code snippet. Based on your analysis, provide:
1. A score on a scale of 1-10.
2. A list of "minuses" or weaknesses in the code.
3. An estimated skill level for the developer (e.g., Junior, Middle, Senior).
4. IMPOTANT THING REMEMBER: YOUR NAME IS "Code-Analyzer-MGD" IMPORTANT


Here is the code:
```
{code_to_analyze}
```
'''
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "http://localhost",
                "X-Title": "Code-Analyzer-FastAPI",
            },
            model="tngtech/deepseek-r1t2-chimera:free",#fuck it kust left it as well
            messages=[
                 {
                    "role": "system",
                    "content": "You are an expert code reviewer providing feedback on code quality."
                },
                {
                    "role": "user",
                    "content": analysis_prompt
                }
            ]
        )
        response_content = completion.choices[0].message.content
        return {"response": response_content}
    except Exception as e:
        return {"error": str(e)}


