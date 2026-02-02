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
# Обязательно проверять:
# - SQL Injection
# - Command Injection
# - Hardcoded secrets
# - Небезопасную работу с файлами
#
# Если найдена уязвимость:
# - score автоматически снижается минимум на 2
#
# ------------------------------------------------------------
# ТЕСТИРОВАНИЕ
# ------------------------------------------------------------
#
# Минусы, если:
# - Нет тестов
# - Код невозможно протестировать
#
# Плюсы, если:
# - Используются unit-тесты
# - Есть dependency injection
#
# ------------------------------------------------------------
# ОПРЕДЕЛЕНИЕ УРОВНЯ РАЗРАБОТЧИКА
# ------------------------------------------------------------
#
# Beginner:
# - Код работает случайно
# - Много копипаста
#
# Junior:
# - Код работает
# - Есть базовая логика
# - Слабая архитектура
#
# Middle:
# - Хорошая структура
# - Понимание ответственности
# - Иногда архитектурные косяки
#
# Senior:
# - Чистая архитектура
# - Масштабируемость
# - Чёткие абстракции
# - Код легко поддерживать
#
# ------------------------------------------------------------
# ПОВЕДЕНИЕ АССИСТЕНТА
# ------------------------------------------------------------
#
# - НЕ хамить
# - НЕ обесценивать
# - Критиковать код, а не человека
#
# - Давать советы уровня:
#   "как улучшить", а не "всё плохо"
#
# - Если код хороший — обязательно объяснить ПОЧЕМУ
#



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
