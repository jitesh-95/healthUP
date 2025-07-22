# agent.py
import os
import json
import logging
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
client = OpenAI(api_key=os.getenv("API_KEY"))

# Logging config
logging.basicConfig(level=logging.INFO)

# Safe prompt path resolution
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEAL_PROMPT_PATH = os.path.join(BASE_DIR, "prompts", "meal_prompt.txt")
WEEKLY_PROMPT_PATH = os.path.join(BASE_DIR, "prompts", "weekly_meal_prompt.txt")
GROCERY_PROMPT_PATH = os.path.join(BASE_DIR, "prompts", "weekly_grocery_prompt.txt")  # <-- Add this file

def load_prompt_template(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        logging.error("Prompt template file not found.")
        return None

def sanitize_input(text):
    return text.replace("{", "").replace("}", "").replace('"', "'").strip()

def safe_parse_json(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        logging.error("Failed to parse JSON from GPT response: %s", text)
        return None

# ------------------- asking GPT--------------------------
def askGPT(prompt):
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    content = response.choices[0].message.content.strip()
    data = safe_parse_json(content)
    return data if data else {"error": "Invalid GPT response format."}

#------------------- Custom Meal --------------------------
def get_customize_meal_plan(ingredients, fitness_goal, specific_target, medical_conditions, portion_size, diet_type, age_group, meal_type, cuisine, additional_details=''):
    medical = ", ".join([c for c in medical_conditions if c != "No Medical Condition"]) or "No Medical Condition"

    prompt_template = load_prompt_template(MEAL_PROMPT_PATH)
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
        return askGPT(prompt=prompt)
    except Exception:
        logging.exception("GPT call failed.")
        return {"error": "Internal error. Please try again later."}

#------------------- Weekly Plan --------------------------
def generate_weekly_meal_plan(inputs: dict):
    prompt_template = load_prompt_template(WEEKLY_PROMPT_PATH)
    if not prompt_template:
        return {"error": "Prompt not available"}

    prompt = prompt_template.format(
        country=inputs.get("country", ""),
        city=inputs.get("city", ""),
        climate=inputs.get("climate", ""),
        goal=inputs.get("goal", ""),
        diet_type=inputs.get("diet_type", ""),
        portion_size=inputs.get("portion_size", ""),
        cuisine=inputs.get("cuisine", ""),
        include_snacks="Yes" if inputs.get("include_snacks") else "No",
        rotate_meals="Yes" if inputs.get("rotate_meals") else "No",
        additional_details=inputs.get("additional_details", "")
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            stream=True
        )
        placeholder = st.empty()
        full_response = ''
        for chunk in response:
            if chunk.choices[0].delta:
                full_response += chunk.choices[0].delta.content
                placeholder.markdown(full_response)
        
        # return full_response
    except Exception:
        logging.exception("GPT weekly plan generation failed.")
        return {"error": "Internal error during weekly meal plan generation"}

#------------------- Grocery List --------------------------
def generate_weekly_grocery_list(inputs: dict):
    prompt_template = load_prompt_template(GROCERY_PROMPT_PATH)
    if not prompt_template:
        return {"error": "Grocery prompt not available"}

    prompt = prompt_template.format(
        country=inputs.get("country", ""),
        goal=inputs.get("goal", ""),
        diet_type=inputs.get("diet_type", ""),
        portion_size=inputs.get("portion_size", ""),
        cuisine=inputs.get("cuisine", ""),
        include_snacks="Yes" if inputs.get("include_snacks") else "No"
    )

    try:
        return askGPT(prompt=prompt)
    except Exception:
        logging.exception("GPT grocery list generation failed.")
        return {"error": "Internal error during grocery list generation"}
