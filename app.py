import streamlit as st

st.set_page_config(
    page_title="Python Quiz Game", page_icon="🎯", layout="centered"
)

st.title("🎯 Python Mini Quiz Game")
st.write("Ee quiz lo questions ki answers select chesi mee score chuskondi!")

quiz_data = [
    {
        "question": "Python lo 'print' function deniki upayogistaru?",
        "options": [
            "A) Output screen meeda chupinchadaniki",
            "B) Input tesukovadaniki",
            "C) File create cheyyadaniki",
            "D) Loop run cheyyadaniki",
        ],
        "answer": "A",
    },
    {
        "question": (
            "Ee kinda ichina vatillo konchem 'immutable' (marppuleni) data type"
            " edi?"
        ),
        "options": ["A) List", "B) Dictionary", "C) Tuple", "D) Set"],
        "answer": "C",
    },
    {
        "question": "Python lo comments rayadaniki em use chestham?",
        "options": [
            "A) // comment",
            "B) # comment",
            "C) /* comment */",
            "D) <!-- comment -->",
        ],
        "answer": "B",
    },
]

with st.form("quiz_form"):
  user_answers = []
  for i, q in enumerate(quiz_data):
    st.subheader(f"Question {i+1}: {q['question']}")
    ans = st.radio("Options:", q["options"], key=f"q_{i}", index=None)
    user_answers.append(ans)

  submitted = st.form_submit_button("Submit Quiz")

if submitted:
  score = 0
  all_answered = True
  for ans in user_answers:
    if ans is None:
      all_answered = False
      break

  if not all_answered:
    st.warning("Dayachesi anni questions ki answer select cheyandi!")
  else:
    for i, q in enumerate(quiz_data):
      selected_option = user_answers[i][0]
      if selected_option == q["answer"]:
        score += 1

    st.success(f"Quiz Complete! Mee Score: {score} / {len(quiz_data)}")
    percentage = (score / len(quiz_data)) * 100
    st.info(f"Percentage: {percentage}%")

    if percentage == 100:
      st.balloons()
      st.write("Grade: Outstanding! Ekkaastham brilliant.")
    elif percentage >= 50:
      st.write("Grade: Good job! Inkonchem practice chey.")
    else:
      st.write("Grade: Need improvement. Malli try chey.")
