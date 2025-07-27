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

# ---------- Generation Handler ----------
def handle_generation(inputs: dict):
        if st.session_state.active_tab == "custom":
            with st.spinner("Generating your customize plan..."):
                st.session_state.latest_inputs = inputs
                response_placeholder = st.empty()
                full_response = ""

                # Render as it streams
                for chunk in agent.get_customize_meal_plan(**inputs):
                    full_response += chunk
                    response_placeholder.markdown(full_response)

                st.session_state.history.append(full_response)
        else:
            with st.spinner('Generating your weekly plan & then grocery list...'):
                response_placeholder = st.empty()
                full_response = ""

                for chunk in agent.generate_weekly_meal_plan(inputs):
                    full_response += chunk
                    response_placeholder.markdown(full_response)

                # Save it for reuse
                st.session_state["meal_plan"] = full_response
            
            st.divider()

            with st.spinner('Generating your grocery list...'):
                response_placeholder = st.empty()
                grocery_response = ""

                for chunk in agent.generate_weekly_grocery_list(full_response):
                    grocery_response += chunk
                    response_placeholder.markdown(grocery_response)

                # Save it for later
                st.session_state["grocery_text"] = grocery_response

            if "grocery_text" in st.session_state:
                st.download_button(
                    label="📥 Download Grocery List",
                    data=st.session_state["grocery_text"],
                    file_name="grocery_list.txt",
                    mime="text/plain",
                    on_click="ignore"
                )


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

                st.markdown(plan)
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
