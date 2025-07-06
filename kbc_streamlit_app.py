import streamlit as st
import random  # required for improved 50-50 logic

# Initialize session state
if "question_index" not in st.session_state:
    st.session_state.question_index = 0
    st.session_state.money = 0
    st.session_state.used_5050 = False
    st.session_state.used_5050_for = -1  # NEW: Track which question 50-50 was used on
    st.session_state.used_flip = False
    st.session_state.show_flip = False
    st.session_state.message = ""

questions = ["Capital of India", "Capital of MP", "Metro city of India", "PM of India", "President of India"]
options = [
    ["Delhi", "Mumbai", "Indore", "Noida"],
    ["Chandigarh", "Bhopal", "Indore", "Noida"],
    ["Chandigarh", "Mumbai", "Indore", "Noida"],
    ["Modi", "Rahul", "Yogi", "Amit Shah"],
    ["Droupadi Murmu", "Pratibha Patil", "Ramnath Kovind", "Pranab Mukherjee"]
]
correct_answers = [0, 1, 1, 0, 0]
prices = [1000, 2000, 3000, 4000, 5000]
flip_question = ["CEO of Google is?", "Satya Nadella", "Sundar Pichai", "Tim Cook", "Elon Musk"]
flip_answer_index = 1  # Sundar Pichai

# Title and rules
st.title("🧠 KBC Demo App")
st.markdown("""
**Rules:**
1. 5 questions with 4 options each  
2. You have 2 lifelines: 50-50 and Flip (one-time use).  
3. Get 2 answers right → ₹2000  
4. Get 4 answers right → ₹4000  
5. Get all answers right → ₹5000
""")

i = st.session_state.question_index

# --------------------- FLIP QUESTION ---------------------
if st.session_state.show_flip:
    st.subheader(f"Question for ₹{prices[i]}:")
    st.write(flip_question[0])
    flip_options = [flip_question[1], flip_question[2], flip_question[3], flip_question[4]]
    answer = st.radio("Choose your answer:", flip_options, key=f"flip_{i}")

    if st.button("Submit Flip Answer"):
        if flip_options.index(answer) == flip_answer_index:
            st.success("Correct answer!")
            st.session_state.money = prices[i]
            st.session_state.question_index += 1
            st.session_state.show_flip = False
            st.rerun()
        else:
            st.error("Wrong answer. Game over!")
            st.markdown(f"You walk away with ₹{st.session_state.money}")
            st.stop()
    st.stop()

# --------------------- REGULAR QUESTION ---------------------
st.subheader(f"Question for ₹{prices[i]}:")
st.write(questions[i])

# ✅ Apply corrected 50-50 logic
displayed_options = options[i].copy()
if st.session_state.used_5050 and st.session_state.used_5050_for == i:
    correct_idx = correct_answers[i]
    all_indices = [0, 1, 2, 3]
    incorrect_indices = [idx for idx in all_indices if idx != correct_idx]
    keep_incorrect = random.choice(incorrect_indices)
    displayed_options = [opt if idx in [correct_idx, keep_incorrect] else "" for idx, opt in enumerate(displayed_options)]

# Answer input
answer = st.radio("Choose your answer:", displayed_options, key=f"q_{i}")

# Lifeline buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Use 50-50 Lifeline"):
        if not st.session_state.used_5050:
            st.session_state.used_5050 = True
            st.session_state.used_5050_for = i
            st.rerun()
        else:
            st.warning("50-50 already used!")

with col2:
    if st.button("Flip the Question"):
        if not st.session_state.used_flip:
            st.session_state.used_flip = True
            st.session_state.show_flip = True
            st.rerun()
        else:
            st.warning("Flip already used!")

# Submit Answer
if st.button("Submit Answer"):
    if displayed_options.index(answer) == correct_answers[i]:
        st.success("Correct answer!")
        st.session_state.money = prices[i]
        st.session_state.question_index += 1

        if st.session_state.question_index == len(questions):
            st.balloons()
            st.success(f"🎉 Congratulations! You've won ₹{st.session_state.money}")
            st.stop()
        st.rerun()
    else:
        st.error(f"Wrong answer. Correct answer is **{options[i][correct_answers[i]]}**.")
        st.markdown(f"You walk away with ₹{st.session_state.money}")
        st.stop()

# Show current money
st.markdown(f"**Amount you have won so far: ₹{st.session_state.money}**")


