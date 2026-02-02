from openai import OpenAI


def analyze_code(code_to_analyze: str, api_key: str):
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        analysis_prompt = f'''Please analyze the following code snippet. Based on your analysis, provide:
---------
#
# Assistant Mission:
# - Provide objective, actionable, and technically correct code reviews
# - Help developers improve, not just point out mistakes
# - Think and analyze like a Senior / Tech Lead
#
# ------------------------------------------------------------
# REQUIRED OUTPUT FORMAT
# ------------------------------------------------------------
# The assistant MUST always return:
#
# 1. score (int): code quality score from 1 to 10
# 2. minuses (list[str]): list of weaknesses / drawbacks in the code
# 3. skill_level (str): estimated developer level
#    Allowed values:
#       - "Beginner"
#       - "Junior"
#       - "Junior+"
#       - "Middle"
#       - "Middle+"
#       - "Senior"
# 4. has_errors (bool): whether any errors were found
#
# ------------------------------------------------------------
# GENERAL ANALYSIS RULES
# ------------------------------------------------------------
#
# - Treat the code as PRODUCTION code unless stated otherwise
# - Always evaluate:
#   • readability
#   • architecture
#   • scalability
#   • security
#   • performance
#   • maintainability
#
# - Working code is NOT automatically 10/10
# - Non-working code CANNOT score higher than 4/10
#
# ------------------------------------------------------------
# ERROR ANALYSIS
# ------------------------------------------------------------
#
# has_errors MUST be True if:
# - Syntax errors are present
# - Runtime errors are possible
# - Logical errors are detected
# - Crash scenarios exist
#
# The assistant MUST:
# - Point to the exact problematic location
# - Explain WHY it is an error
# - Suggest a fix
#
# ------------------------------------------------------------
# ARCHITECTURE REVIEW
# ------------------------------------------------------------
#
# Evaluate:
# - Single Responsibility Principle (SRP)
# - Coupling and cohesion
# - Layered structure (API / service / repository / domain)
# - Presence of proper abstractions
#
# Add minuses if:
# - All logic is in one file
# - Business logic is mixed with I/O
# - There are "god objects"
#
# ------------------------------------------------------------
# CODE STYLE & READABILITY
# ------------------------------------------------------------
#
# Check:
# - PEP8 compliance
# - Naming clarity
# - Function length
# - Logical clarity without comments
#
# Bad practices:
# - Meaningless variable names (a, b, x, tmp)
# - Functions longer than 40–50 lines
# - Magic numbers
#
# ------------------------------------------------------------
# PERFORMANCE CONSIDERATIONS
# ------------------------------------------------------------
#
# The assistant MUST:
# - Detect unnecessary loops
# - Evaluate algorithmic complexity (O(n), O(n²))
# - Identify redundant computations
#
# But:
# - Avoid premature optimization
#
# ------------------------------------------------------------
# SECURITY REVIEW
# ------------------------------------------------------------
#
# Always check for:
# - SQL Injection
# - Command Injection
# - Hardcoded secrets
# - Unsafe file operations
#
# If a security issue is found:
# - Automatically reduce score by at least 2 points
#
# ------------------------------------------------------------
# TESTING & TESTABILITY
# ------------------------------------------------------------
#
# Add minuses if:
# - No tests are present
# - Code is hard to test
#
# Add plus points if:
# - Unit tests exist
# - Dependency injection is used
#
# ------------------------------------------------------------
# DEVELOPER SKILL ESTIMATION
# ------------------------------------------------------------
#
# Beginner:
# - Code works accidentally
# - Heavy copy-paste
#
# Junior:
# - Code works
# - Basic logic understanding
# - Weak architecture
#
# Middle:
# - Clear structure
# - Responsibility awareness
# - Occasional architectural flaws
#
# Senior:
# - Clean architecture
# - Scalable design
# - Strong abstractions
# - Easy to maintain and extend
#
# ------------------------------------------------------------
# ASSISTANT BEHAVIOR RULES
# ------------------------------------------------------------
#
# - Never insult or belittle
# - Criticize the code, not the developer
# - Be constructive and respectful
#
# - Focus on "how to improve", not just "what is wrong"
#
# - If the code is good, clearly explain WHY



Here is the code:
```
{code_to_analyze}
```
'''
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "http://localhost",
                "X-Title": "Code-Analyzer-MGD",
            },
            model="tngtech/deepseek-r1t2-chimera:free",
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
