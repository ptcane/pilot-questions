import streamlit as st
import random
import json
from pathlib import Path

# Load questions from JSON file
def load_questions():
    file_path = Path("questions.json")
    with open(file_path, "r") as file:
        return json.load(file)

questions_data = load_questions()

questions_per_quiz = 10

# Initialize session state
if "used_questions" not in st.session_state:
    st.session_state["used_questions"] = {}
if "current_questions" not in st.session_state:
    st.session_state["current_questions"] = []
if "score" not in st.session_state:
    st.session_state["score"] = 0
if "question_index" not in st.session_state:
    st.session_state["question_index"] = 0

# Reset session for a new quiz
def reset_quiz(topic):

    available_questions = [q for q in questions_data[topic] if q["question_number"] not in st.session_state["used_questions"].get(topic, [])]
    if len(available_questions) < questions_per_quiz:
        st.session_state["used_questions"][topic] = list()
        available_questions = [q for q in questions_data[topic]]

    st.session_state["current_questions"] = random.sample(available_questions,
        k=min(questions_per_quiz, len(questions_data[topic]))
    )
    st.session_state["score"] = 0
    st.session_state["question_index"] = 0
    if topic not in st.session_state["used_questions"]:
        st.session_state["used_questions"][topic] = []

def next_question():

    st.session_state["used_questions"][topic].append(question["question_number"])
    st.session_state["question_index"] += 1
    return

def clear_current_questions():
    st.session_state["current_questions"] = list()
    return

# Main app
st.logo("parachute.png")
st.title("Pilot Quiz")


# Step 1: Choose a topic
topic = st.selectbox("Choose a topic:", list(questions_data.keys()), on_change=clear_current_questions)

if st.session_state["current_questions"] == list():
    st.button("Start Quiz", on_click=reset_quiz, args=[topic])

else:

    # Step 2: Display questions
    current_index = st.session_state["question_index"]
    if current_index < len(st.session_state["current_questions"]):
        question = st.session_state["current_questions"][current_index]

        st.write(f"**Question {current_index + 1}:** {question['question']}")

        user_answer = st.radio(
            "Select an answer:",
            options=list(question["options"].keys()),
            format_func=lambda x: f"{x}: {question['options'][x]}"
        )

        if st.button("Submit Answer"):
            if user_answer == question["correct_answer"]:
                st.session_state["score"] += 1
                st.success("Correct!")
                st.info(f"{question['explanation']}")
            else:
                st.error(
                    f"Wrong. The correct answer is {question['correct_answer']}: "
                    f"{question['options'][question['correct_answer']]}."
                )
                st.info(f"{question['explanation']}")

            # Go to next question and mark question as used
            st.button("Next Question", on_click=next_question)
            

    else:
        # Step 3: Show results and allow retry
        st.write(f"### Quiz Complete! You scored {st.session_state['score']} out of {len(st.session_state['current_questions'])}.")

        st.button("Try Again", on_click=reset_quiz, args=[topic])
