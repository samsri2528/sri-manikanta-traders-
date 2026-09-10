import time


def run_quiz():
  # Questions database stored in a dictionary format
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
              "Ee kinda ichina vatillo konchem 'immutable' (marppuleni)"
              " data type edi?"
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

  score = 0
  print("=" * 45)
  print("   WELCOME TO PYTHON MINI QUIZ GAME!   ")
  print("=" * 45)
  time.sleep(1)

  for index, q in enumerate(quiz_data, start=1):
    print(f"\nQuestion {index}: {q['question']}")
    for option in q["options"]:
      print(option)

    user_ans = input(
        "\nNeeku nachina option enter chey (A/B/C/D): "
    ).strip().upper()

    if user_ans == q["answer"]:
      print("Correct! Super answer.")
      score += 1
    else:
      print(f"Wrong! Correct option {q['answer']}.")
    print("-" * 45)
    time.sleep(0.5)

  # Final Score Board
  print("\n" + "=" * 20 + " RESULT " + "=" * 20)
  print(f"Total Questions: {len(quiz_data)}")
  print(f"Neeku vachina Score: {score}")

  percentage = (score / len(quiz_data)) * 100
  print(f"Percentage: {percentage}%")

  if percentage == 100:
    print("Grade: Outstanding! Ekkaastham brilliant.")
  elif percentage >= 50:
    print("Grade: Good job! Inkonchem practice chey.")
  else:
    print("Grade: Need improvement. Malli try chey.")
  print("=" * 48)


if __name__ == "__main__":
  run_quiz()
