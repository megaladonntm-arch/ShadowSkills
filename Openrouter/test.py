import os
from openai import OpenAI
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn

api_key = ""

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=api_key,
)

app = FastAPI()

class CodeRequest(BaseModel):
    prompt: str


#FRONT MADE BY AI NOT BY MGD LOL
html_content = """
<!DOCTYPE html>
<html>
    <head>
        <title>AI Code Analyzer</title>
        <style>
            body { font-family: sans-serif; margin: 2em; background-color: #f4f4f9; color: #333; }
            h1 { text-align: center; color: #4a4a4a; }
            #container { max-width: 900px; margin: auto; background: white; padding: 2em; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            textarea { width: 100%; padding: 0.5em; margin-bottom: 1em; border-radius: 4px; border: 1px solid #ccc; font-size: 1em; min-height: 200px; font-family: monospace; }
            button { width: 100%; padding: 0.7em; border: none; background-color: #5c67f2; color: white; font-size: 1em; border-radius: 4px; cursor: pointer; }
            button:hover { background-color: #4a54e1; }
            #response { margin-top: 1em; padding: 1em; background: #eee; border-radius: 4px; white-space: pre-wrap; font-family: monospace; }
        </style>
    </head>
    <body>
        <div id="container">
            <h1>AI Code Analyzer</h1>
            <textarea id="prompt" rows="15" placeholder="Paste your code here to get it rated..."></textarea>
            <button onclick="sendCode()">Analyze Code</button>
            <h2>Analysis:</h2>
            <div id="response">(AI analysis will appear here)</div>
        </div>
        <script>
            async function sendCode() {
                const codeText = document.getElementById('prompt').value;
                const responseDiv = document.getElementById('response');
                responseDiv.innerText = "Analyzing...";

                try {
                    const response = await fetch('/analyze', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ prompt: codeText })
                    });
                    const data = await response.json();
                    if (data.response) {
                        responseDiv.innerText = data.response;
                    } else {
                        responseDiv.innerText = 'Error: ' + (data.detail || 'Unknown error');
                    }
                } catch (error) {
                    responseDiv.innerText = 'Error: ' + error.toString();
                }
            }
        </script>
    </body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def get_home():
    return HTMLResponse(content=html_content)

@app.post("/analyze")
async def analyze(request: CodeRequest):
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

if __name__ == "__main__":
    print("Starting FastAPI server for Code Analyzer...")
    print("Go to http://127.0.0.1:8000 in your browser.")

    uvicorn.run(app, host="127.0.0.1", port=8000)
