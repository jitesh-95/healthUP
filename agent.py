# agent.py
import os
import json
import logging
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("API_KEY"))

# Logging config
logging.basicConfig(level=logging.INFO)

# Safe prompt path resolution
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPT_TEMPLATE_PATH = os.path.join(BASE_DIR, "prompts", "meal_prompt.txt")

def load_prompt_template():
    try:
        with open(PROMPT_TEMPLATE_PATH, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        logging.error("Prompt template file not found.")
        return (
            "You are a health-focused AI assistant. Return a healthy meal plan in JSON format. "
            "Include: description, meal_plan, nutrition_info, suggestions, and tip."
        )

def sanitize_input(text):
    return text.replace("{", "").replace("}", "").replace('"', "'").strip()

def safe_parse_json(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        logging.error("Failed to parse JSON from GPT response: %s", text)
        return None

def get_meal_plan(ingredients, fitness_goal, specific_target, medical_conditions, portion_size, diet_type, age_group, meal_type, cuisine, additional_details=''):
    medical = ", ".join([c for c in medical_conditions if c != "No Medical Condition"]) or "No Medical Condition"

    prompt_template = load_prompt_template()
    prompt = prompt_template.format(
        ingredients=sanitize_input(ingredients),
        fitness_goal=sanitize_input(fitness_goal),
        specific_target=sanitize_input(specific_target),
        medical_conditions=medical,
        portion_size=portion_size,
        diet_type=diet_type,
        age_group=age_group,
        meal_type=meal_type,
        cuisine=cuisine,
        additional_details=additional_details
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        content = response.choices[0].message.content.strip()
        data = safe_parse_json(content)
        return data if data else {"error": "Invalid GPT response format."}
    except Exception:
        logging.exception("GPT call failed.")
        return {"error": "Internal error. Please try again later."}
