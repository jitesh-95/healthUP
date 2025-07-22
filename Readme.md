# 🥗 HealthUP – Your Smart Diet Planner Friend

**HealthUP** is an AI-powered assistant that helps users build personalized, healthy, and goal-driven diet plans — whether for a single meal or an entire week — using OpenAI's GPT-4-turbo.

---

## 🚀 Features at a Glance

### ✅ Phase 1 – Meal Customizer (MVP)

Create a personalized meal plan using:

* Available **ingredients**
* Your **fitness goals** and **targets**
* Any **medical conditions**
* Preferences like **diet type**, **cuisine**, **meal type**, and **portion size**

💡 GPT-generated outputs:

* 📝 Meal description
* 🥘 Meal plan
* 📊 Nutritional breakdown
* ➕ Suggestions for improvement
* 💬 Personalized health tip

### 📅 Phase 2 – Weekly Planner & Grocery Assistant

Generate a **7-day meal plan** along with a **smart grocery list** using:

* Your past profile info + new inputs (location, climate, goals)
* Option to include **snacks**
* Climate-aware meal suggestions and tips

💡 Outputs:

* Daily meals (breakfast, lunch, snacks, dinner)
* Deduplicated grocery list by category
* Downloadable `.txt` or `.csv`
* Smart tips like bulk-buying and seasonal choices

---

## 🧠 User Inputs

| Field              | Description                         |
| ------------------ | ----------------------------------- |
| Ingredients        | Pantry items                        |
| Fitness Goal       | E.g. gain weight, lose fat          |
| Specific Target    | E.g. lose 2kg in 2 weeks            |
| Medical Conditions | Diabetes, cholesterol, etc.         |
| Portion Size       | Number of servings                  |
| Diet Type          | Veg / Non-Veg / Vegan               |
| Age Group          | Child / Teen / Adult / Senior       |
| Meal Type          | Breakfast / Lunch / Dinner          |
| Cuisine            | Indian, Mexican, etc.               |
| Climate / City     | (Phase 2) Used for contextual logic |

---

## ⚙️ Tech Stack

| Layer      | Tool/Library       |
| ---------- | ------------------ |
| Frontend   | Streamlit          |
| Backend    | OpenAI GPT-4-turbo |
| State Mgmt | `st.session_state` |
| Nutrition  | GPT-estimated      |

---

## 🗂️ Folder Structure

```bash
healthup/
├── app.py
├── agent.py
├── requirements.txt
├── .env
├── prompts/
│   ├── meal_prompt.txt
│   ├── weekly_meal_prompt.txt
│   └── weekly_grocery_prompt.txt
├── utils/
│   ├── helpers.py
│   └── grocery_generator.py
├── forms/
│   ├── customize_meal.py
│   └── weekly_plan.py
```

---

## 🧪 Testing Scenarios

| Persona                      | Target                    |
| ---------------------------- | ------------------------- |
| Diabetic adult               | Fat loss                  |
| Vegan teen                   | Muscle gain               |
| Senior with cholesterol      | Low-fat, digestible meals |
| Tier 2 teen (rainy climate)  | Protein-rich plan         |
| Working adult in hot climate | Low-prep meals            |

---

## 📦 Deployment Options

* ✅ [Streamlit Cloud](https://streamlit.io/cloud) (1-click deploy)
* Optional: Render or Vercel (with Python wrapper)

---

## 💸 Cost & Token Usage

| Interaction         | Estimate        |
| ------------------- | --------------- |
| GPT-4 (single meal) | \~\$0.01–\$0.03 |
| Weekly planning     | \~\$0.05–\$0.15 |
| Monthly usage       | \~\$5 or less   |

---

## 📌 Notes

* Nutrition values are GPT-estimated (no external API yet)
* Climate, city tier, and age improve contextual meal logic
* Phase 3 may integrate real nutrition APIs like Edamam or Calorieninjas

---

## 🧠 Future Plans

* 📈 Weekly goal tracking (calorie alignment)
* 📊 Integration with nutrition APIs
* 📆 Auto-rotation logic for repeated meals
* 🧠 Smarter prompts and dietary suggestions

---

### Made with ❤️ using OpenAI + Streamlit

*“Your health, one smart meal at a time.”*
