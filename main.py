import random
from pathlib import Path

import yaml


def load_questions():
    questions_path = Path(__file__).resolve().parent / "questions.yaml"
    if not questions_path.exists():
        print("Unable to find questions.yaml.")
        return []

    with questions_path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}

    questions = data.get("questions", [])
    return [
        question
        for question in questions
        if question.get("question") and question.get("answer")
    ]


def get_user_choice(option_count):
    while True:
        choice = input("Your answer (enter the option number): ").strip()
        if choice.isdigit():
            selected = int(choice)
            if 1 <= selected <= option_count:
                return selected
        print("Please enter a valid option number.")


def ask_question(question, number):
    print(f"Question {number}: {question['question']}")
    options = list(question.get("wrong_answers", [])) + [question["answer"]]
    random.shuffle(options)

    for idx, option in enumerate(options, start=1):
        print(f"  {idx}. {option}")

    user_choice = get_user_choice(len(options))
    correct_choice = options.index(question["answer"]) + 1

    if user_choice == correct_choice:
        print("\033[92mCorrect!\033[0m")
        is_correct = True
    else:
        print(f"\033[91mIncorrect. The correct answer is {question['answer']}.\033[0m")
        is_correct = False

    explanation = question.get("explanation")
    if explanation:
        print(f"Explanation: {explanation}")

    print()
    return is_correct


def ask_question_count(max_questions):
    while True:
        raw = input(f"How many questions would you like? (1-{max_questions}): ").strip()
        if raw.isdigit():
            requested = int(raw)
            if 1 <= requested <= max_questions:
                return requested
        print("Please enter a valid number within range.")


def run_quiz():
    questions = load_questions()
    if not questions:
        print("No questions available to run the quiz.")
        return

    random.shuffle(questions)

    total_available = len(questions)
    total_questions = ask_question_count(total_available)
    selected_questions = questions[:total_questions]

    score = 0

    for idx, question in enumerate(selected_questions, start=1):
        if ask_question(question, idx):
            score += 1

    print(f"Quiz complete! Your final score: {score}/{total_questions}")


if __name__ == "__main__":
    run_quiz()
