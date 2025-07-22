import streamlit as st

def render_weekly_plan_form():
    with st.sidebar:
      st.subheader('🗓️ Plan Your Week')
      with st.form("weekly_plan_form", border=False):
          country = st.text_input("Country", placeholder="e.g. India")
          city = st.selectbox("Living In",["Metro City", "Sub-Urban City", "Town"])
          climate = st.selectbox("Current Climate", ["Hot", "Cold", "Humid", "Dry", "Moderate"])
          goal = st.selectbox("Goal", ["Weight Loss","Fat Loss", "Muscle Gain", "Maintenance"])
          diet_type = st.selectbox("Diet type", ["Vegetarian", "Non-Vegetarian", "Vegan"])
          portion_size = st.radio("Portion size", ["1 person", "2 people", "Family"],horizontal=True)
          cuisine = st.selectbox(
              "Preferred Cuisine",
              ["Any", "Indian", "South Indian", "North Indian", "Gujarati", "Punjabi", "Mughlai", "Rajasthani", "Bengali", "Continental", "Chinese", "Mexican"],
          index=1)
          additional_details = st.text_area("Additional details (if any)", placeholder="e.g. Use less oil, Any special condition, etc.")
          include_snacks = st.toggle("Include Snacks")
          rotate_meals = st.toggle("Rotate Meals")

          submit = st.form_submit_button("Generate Weekly Plan", use_container_width=True)

          if submit:
              required_fields = {
                  "country": country,
              }
              missing = [k for k, v in required_fields.items() if not v.strip()]
              if missing:
                  st.error(f"Please fill in all required fields: {', '.join(missing)}.")
                  return None

              return {
                  "country": country.strip(),
                  "city": city,
                  "climate": climate,
                  "goal": goal,
                  "diet_type":diet_type,
                  "portion_size": portion_size,
                  "cuisine":cuisine,
                  "include_snacks": include_snacks,
                  "rotate_meals": rotate_meals,
                  "additional_details": additional_details,
              }
    return None
