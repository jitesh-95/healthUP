import streamlit as st
from agent import get_meal_plan
from utils.helpers import parse_suggestions

st.set_page_config(page_title="HealthUP – Diet Planner", layout="centered")
st.html("""
<div style="
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 10px;
    gap: 5px;
">
  <span style="font-size: 40px; font-weight: 600;">🥗 HealthUP</span>
  <span style="font-size: 25px; color: gray;">–</span>
  <span style="font-size: 25px; color: gray; text-decoration: underline; text-underline-offset: 5px; font-style: italic;">Your Smart Diet Planner Friend</span>
</div>
""")
# st.title("🥗 HealthUP – Your Smart Diet Planner Friend")

# Constants
NO_SUGGESTIONS_TEXT = "_No suggestions available._"
ERROR_MESSAGE = "⚠️ GPT did not return a valid meal plan. Please try again later."
SUCCESS_MESSAGE = "✅ Plan generated successfully!"

# Session init
if "history" not in st.session_state:
    st.session_state.history = []

if "latest_inputs" not in st.session_state:
    st.session_state.latest_inputs = None


def show_result(result: dict):
    if "description" in result:
        st.subheader("🍽️ Meal Description")
        st.markdown(result["description"])

    st.subheader("🥘 Meal Plan")
    st.markdown(result["meal_plan"])

    st.subheader("📊 Nutritional Information")
    st.markdown(result["nutrition_info"])

    st.subheader("💡 Suggestions to Improve")
    suggestions_list = parse_suggestions(result.get("suggestions", ""))
    if suggestions_list:
        for suggestion in suggestions_list:
            st.markdown(f"- {suggestion}")
    else:
        st.info(NO_SUGGESTIONS_TEXT)

    st.subheader("💬 Final Tip")
    st.markdown(result["tip"])


def handle_generation(inputs: dict):
    with st.spinner("Generating your plan..."):
        result = get_meal_plan(**inputs)

    if isinstance(result, dict) and result.get("meal_plan"):
        st.success(SUCCESS_MESSAGE)
        st.session_state.latest_inputs = inputs

        st.session_state.history.append(result)
        show_result(result)
    else:
        st.error(ERROR_MESSAGE)


def render_input_form():
    with st.sidebar:
      st.subheader("🧾 Customize Your Healthy Meal")

      with st.form("meal_form", border=False):
          ingredients = st.text_area("Ingredients you have", placeholder="e.g. rice, lentils, tomato")
          fitness_goal = st.text_input("Your fitness goal", placeholder="e.g. gain weight, fat loss")
          specific_target = st.text_input("Specific target", placeholder="e.g. Gain 2kg in 2 weeks")

          medical_conditions = st.multiselect(
              "Medical conditions (if any)",
              ["No Medical Condition", "Diabetes", "Cholesterol", "Thyroid", "BP"]
          )
          if "No Medical Condition" in medical_conditions and len(medical_conditions) > 1:
              st.warning("Please select either 'No Medical Condition' or specific conditions, not both.")
              return None

          diet_type = st.selectbox("Diet type", ["Veg", "Non-Veg", "Vegan"])
          age_group = st.selectbox("Age Group", ["Child (0–12)", "Teenager (13–19)", "Adult (20–60)", "Senior (60+)"])
          cuisine = st.selectbox(
              "Preferred Cuisine",
              ["Any", "Indian", "South Indian", "North Indian", "Gujarati", "Punjabi", "Mughlai", "Rajasthani", "Bengali", "Continental", "Chinese", "Mexican"]
          )

          meal_type = st.radio("Meal type", ["Breakfast", "Lunch", "Dinner"],horizontal=True)
          portion_size = st.radio("Portion size", ["1 person", "2 people", "Family"],horizontal=True)
          additional_details = st.text_area("Additional details (if any)", placeholder="e.g. use less oil or any special condition")

          submitted = st.form_submit_button("Generate Plan", use_container_width=True)

          if submitted:
              required_fields = {
                  "Ingredients": ingredients,
                  "Fitness Goal": fitness_goal,
                  "Specific Target": specific_target
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


def show_more_button():
    if st.session_state.latest_inputs:
        if st.button("🔁 Generate Another Recipe (Same Inputs)"):
            handle_generation(st.session_state.latest_inputs)


def render_history():
    if len(st.session_state.history) > 1:
        with st.expander("📜 View Previously Generated Meals"):
            for idx, plan in enumerate(st.session_state.history[-2::-1], start=1):
                st.markdown(f"**Previous Meal #{idx}**")

                if "description" in plan:
                    st.markdown(f"**🍽️ Description:** {plan['description']}")

                st.markdown("**🥘 Meal Plan**")
                st.markdown(plan["meal_plan"])

                st.markdown("**📊 Nutritional Info**")
                st.markdown(plan["nutrition_info"])

                st.markdown("**💡 Suggestions**")
                suggestions_list = parse_suggestions(plan.get("suggestions", ""))
                if suggestions_list:
                    for s in suggestions_list:
                        st.markdown(f"- {s}")
                else:
                    st.markdown(NO_SUGGESTIONS_TEXT)

                st.markdown("**💬 Final Tip**")
                st.markdown(plan["tip"])
                st.markdown("---")


# Run App Logic
user_inputs = render_input_form()
if user_inputs:
    handle_generation(user_inputs)

# Show this info message if no plan generated yet
if not st.session_state.history:
    st.info("Please fill the details to generate a meal plan. 👈")

show_more_button()
render_history()
