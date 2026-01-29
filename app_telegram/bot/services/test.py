from ai_service import get_code_analysis


def analyze_code(prompt):
    ai_resl = get_code_analysis(prompt)
    return ai_resl

print(analyze_code("print('Hello, World!')"))
