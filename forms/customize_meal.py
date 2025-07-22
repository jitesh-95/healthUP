import streamlit as st

def render_customize_form():
    with st.sidebar:
      st.subheader('🥗 Customize Your Healthy Meal')

      with st.form("meal_form", border=False):
          ingredients = st.text_area("Ingredients you have", placeholder="e.g. rice, lentils, tomato")
          fitness_goal = st.selectbox("Goal", ["Weight Loss","Fat Loss", "Muscle Gain", "Maintenance"])
          specific_target = st.text_input("Specific target", placeholder="e.g. Gain 2kg in 2 weeks")

          medical_conditions = st.multiselect(
              "Medical conditions (if any)",
              ["No Medical Condition", "Diabetes", "Cholesterol", "Thyroid", "BP"]
          )
          if "No Medical Condition" in medical_conditions and len(medical_conditions) > 1:
              st.warning("Please select either 'No Medical Condition' or specific conditions, not both.")
              return None

          diet_type = st.selectbox("Diet type", ["Vegetarian", "Non-Vegetarian", "Vegan"])
          age_group = st.selectbox("Age Group", ["Child (0–12)", "Teenager (13–19)", "Adult (20–60)", "Senior (60+)"])
          cuisine = st.selectbox(
              "Preferred Cuisine",
              ["Any", "Indian", "South Indian", "North Indian", "Gujarati", "Punjabi", "Mughlai", "Rajasthani", "Bengali", "Continental", "Chinese", "Mexican"]
          )

          meal_type = st.radio("Meal type", ["Breakfast", "Lunch", "Dinner"],horizontal=True)
          portion_size = st.radio("Portion size", ["1 person", "2 people", "Family"],horizontal=True)
          additional_details = st.text_area("Additional details (if any)", placeholder="e.g. Use less oil, Any special condition, etc.")

          submitted = st.form_submit_button("Generate Plan", use_container_width=True)

          if submitted:
              required_fields = {
                  "Ingredients": ingredients,
                  "Fitness Goal": fitness_goal
              }
              missing = [k for k, v in required_fields.items() if not v.strip()]
              if missing:
                  st.error(f"Please fill in all required fields: {', '.join(missing)}.")
                  return None

              return {
                  "ingredients": ingredients.strip(),
                  "fitness_goal": fitness_goal.strip(),
                  "specific_target": specific_target.strip(),
                  "medical_conditions": medical_conditions,
                  "portion_size": portion_size,
                  "diet_type": diet_type,
                  "age_group": age_group,
                  "meal_type": meal_type,
                  "cuisine": cuisine,
                  "additional_details": additional_details
              }
    return None