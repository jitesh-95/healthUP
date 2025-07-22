import streamlit as st
import agent
from utils.helpers import parse_suggestions
from forms.customize_meal import render_customize_form
from forms.weekly_plan import render_weekly_plan_form

st.set_page_config(page_title="HealthUP – Diet Planner", layout="wide")
st.html("""
<div style="
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 10px;
    gap: 5px;
">
  <span style="font-size: 40px; font-weight: 600;">🥗 HealthUP</span>
  <span style="font-size: 25px; color: gray;">&ndash;</span>
  <span style="font-size: 25px; color: gray; text-decoration: underline; text-underline-offset: 5px; font-style: italic;">Your Smart Diet Planner Friend</span>
</div>
""")

NO_SUGGESTIONS_TEXT = "_No suggestions available._"
ERROR_MESSAGE = "⚠️ GPT did not return a valid meal plan. Please try again later."
SUCCESS_MESSAGE = "✅ Plan generated successfully!"

if "history" not in st.session_state:
    st.session_state.history = []
if "latest_inputs" not in st.session_state:
    st.session_state.latest_inputs = None
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "custom"

with st.sidebar:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🥗 Customize Meal", use_container_width=True):
            st.session_state.active_tab = "custom"
    with col2:
        if st.button("🗓️ Weekly Planning", use_container_width=True):
            st.session_state.active_tab = "week"

# ---------- Weekly Results Renderer ----------
def show_weekly_plan(plan):
    st.subheader("🗓️ Weekly Meal Plan")
    print(plan)
    # for day in plan["week_plan"]:
    #     st.markdown(f"### 📅 {day['day']}")
    #     for meal_type, meal in day["meals"].items():
    #         st.markdown(f"**🍽️ {meal_type.capitalize()}**")
    #         st.markdown(f"- **Name:** {meal.get('name', 'N/A')}")
    #         st.markdown(f"- **Description:** {meal.get('description', '')}")
    #         st.markdown(f"- **Prep Time:** {meal.get('prep_time', '')}")
    #         st.markdown(f"- **Cook Time:** {meal.get('cook_time', '')}")
    #         st.markdown(f"- **Nutrition Info:** {meal.get('nutrition_info', '')}")
    #         st.markdown("**Ingredients:**")
    #         st.markdown("\n".join(f"- {i}" for i in meal.get("ingredients", [])))
    #         st.markdown("**Instructions:**")
    #         st.markdown("\n".join(f"{i+1}. {step}" for i, step in enumerate(meal.get("instructions", []))))
    #         st.markdown("---")

    # if "grocery_list" in plan:
    #     st.subheader("🛒 Grocery List")
    #     grocery_text = "\n".join(plan["grocery_list"])
    #     st.text_area("Grocery Items", grocery_text, height=200)
    #     st.download_button("📥 Download Grocery List", grocery_text, file_name="grocery_list.txt")

    # if "suggestions" in plan:
    #     st.subheader("💡 Suggestions")
    #     for s in plan["suggestions"]:
    #         st.markdown(f"- {s}")

# ---------- Custom Meal Result Renderer ----------
def show_result(result: dict):
    if "description" in result:
        st.subheader("🍽️ Meal Description")
        st.markdown(result["description"])

    st.subheader("🍼 Meal Plan")
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

# ---------- Generation Handler ----------
def handle_generation(inputs: dict):
    with st.spinner("Generating your plan..."):
        if st.session_state.active_tab == "custom":
            result = agent.get_customize_meal_plan(**inputs)
            st.success(SUCCESS_MESSAGE)
            st.session_state.latest_inputs = inputs
            st.session_state.history.append(result)
            show_result(result)
        else:
            agent.generate_weekly_meal_plan(inputs)
            # for chunk in weekly_plan:
            #   if chunk.choices[0].delta:
            #     # full_response += chunk.choices[0].delta.content
            #     st.markdown(chunk.choices[0].delta.content + '\n')

            # if isinstance(weekly_plan, dict) and "week_plan" in weekly_plan:
            #     # grocery = agent.generate_weekly_grocery_list(weekly_plan["week_plan"])
            #     result = {
            #         "week_plan": weekly_plan["week_plan"],
            #         # "grocery_list": grocery.get("grocery_list", []),
            #     }
            # else:
            #     result = {"error": "Unable to generate weekly meal plan"}

    # if isinstance(result, dict):
    #     if "week_plan" in result:
    #         st.success(SUCCESS_MESSAGE)
    #         show_weekly_plan(result)
    #         return
    #     elif "meal_plan" in result:
    #         st.success(SUCCESS_MESSAGE)
    #         st.session_state.latest_inputs = inputs
    #         st.session_state.history.append(result)
    #         show_result(result)
    #         return

    # st.error(ERROR_MESSAGE)

# ---------- UI Buttons ----------
def show_more_button():
    if st.session_state.latest_inputs and st.session_state.active_tab == "custom":
        if st.button("🔁 Generate Another Recipe (Same Inputs)"):
            handle_generation(st.session_state.latest_inputs)

# ---------- History ----------
def render_history():
    if st.session_state.active_tab != "custom":
        return

    if len(st.session_state.history) > 1:
        with st.expander("📜 View Previously Generated Meals"):
            for idx, plan in enumerate(st.session_state.history[-2::-1], start=1):
                st.markdown(f"**Previous Meal #{idx}**")

                if "description" in plan:
                    st.markdown(f"**🍽️ Description:** {plan['description']}")

                st.markdown("**🍼 Meal Plan**")
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

# ---------- Main Execution ----------
if st.session_state.active_tab == 'custom':
  inputs = render_customize_form()
  if inputs:
      handle_generation(inputs)

if st.session_state.active_tab == 'week':
  inputs = render_weekly_plan_form()
  if inputs:
      handle_generation(inputs)

if st.session_state.active_tab == 'custom':
  show_more_button()
  render_history()

if not st.session_state.history and st.session_state.active_tab == 'custom':
  st.info("Please fill the details to generate a meal plan. 👈")
