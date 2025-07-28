# 🥗 HealthUP – Your Smart Diet Planner Friend [Visit Here](https://healthup.streamlit.app/)

**HealthUP** is an AI-powered assistant that helps users build personalized, healthy, and goal-driven diet plans — whether for a single meal or an entire week — using OpenAI's GPT-4-turbo.

---

## 🚀 Features at a Glance

### ✅ Meal Customizer (MVP)

Create a personalized meal plan using:

* Available **Ingredients**
* Your **Fitness Goals** and **Targets**
* Any **Medical Conditions**
* Preferences like **Diet Type**, **Cuisine**, **Meal Type**, **Age Group**, and **Portion Size**

💡 AI-generated output with typing like animation:

* 📝 Meal description
* 🥘 Meal plan
* 📊 Nutritional breakdown
* ➕ Suggestions for improvement
* 💬 Personalized health tip

### 📅 Weekly Planner & Grocery Assistant

Generate a **7-Day Meal Plan** along with a **Smart Grocery List** using:

* Your **Location**,**Fitness Goal**, **Protion Size** **Cusine** and **Diet Type (Veg/Non-veg/Vegan)**
* Option to include **Snacks**
* Climate-aware meal suggestions and tips

💡 AI-generated tabular output with typing like animation:

* Daily meals **(breakfast, lunch, snacks, dinner)**
* Deduplicated grocery list by category
* Downloadable `.txt` grocery list
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

## ⚙️ Agent Based Response

* Customize Meal Generator
* Weekly Meal Plan Generator
* Grocery List Generator

---

## ⚙️ Tech Stack

| Layer      | Tool/Library       |
| ---------- | ------------------ |
| Frontend   | Streamlit          |
| Backend    | OpenAI GPT-4.1     |
| State Mgmt | `st.session_state` |
| Nutrition  | GPT-estimated      |

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

## 🧠 Future Plans

* 📈 Weekly goal tracking (calorie alignment)
* 📊 Integration with nutrition APIs
* 🧠 Smarter prompts and dietary suggestions
* 💪 Exercise recommendations for better results

---

## 📦 Prerequisites

- Python 3.8 or higher
- A valid [OpenAI API key](https://platform.openai.com/account/api-keys)

---

## 🛠️ Installation

Follow these steps to clone and run the app locally:

### 1. Clone the Repository

```bash
git clone https://github.com/jitesh-95/healthUP.git
cd healthUP
```

### 2. Create a Virtual Environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Setup `.env` File

Create a `.env` file in the root directory of the project and add your OpenAI API key like this:

```
API_KEY=your_openai_api_key_here
```

> 🔒 Make sure `.env` is listed in `.gitignore` to keep your key secure.

---

## ▶️ Running the App

After setting up everything, start the Streamlit app using:

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
├── app.py
├── requirements.txt
├── .env
├── README.md
└── ...
```

---

## 🧠 Powered by

- [Streamlit](https://streamlit.io/)  
- [OpenAI](https://platform.openai.com/)  
- [Python](https://www.python.org/)  

---

<h3 style="text-align: center;">Made with ❤️ using OpenAI + Streamlit</h3>
<h3 style="text-align: center; font-style: italic;">“Your health, one smart meal at a time.”</h3>

