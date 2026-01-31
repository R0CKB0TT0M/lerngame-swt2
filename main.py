import random
from pathlib import Path

import yaml


def load_questions(questions_path):
    if not questions_path.exists():
        print(f"Unable to find {questions_path.name}.")
        return []

    with questions_path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}

    questions = data.get("questions", [])
    return [
        question
        for question in questions
        if question.get("question") and question.get("answer")
    ]


def discover_topics():
    base_path = Path(__file__).resolve().parent
    return {path.stem: path for path in base_path.glob("*.yaml") if path.is_file()}


def ask_topic_selection(topic_counts):
    topic_names = sorted(topic_counts.keys())
    if "All" in topic_names:
        topic_names.remove("All")
        topic_names.insert(0, "All")
    while True:
        print("Available topics:")
        for idx, name in enumerate(topic_names, start=1):
            count = topic_counts[name]
            label = "question" if count == 1 else "questions"
            print(f"  {idx}. {name} ({count} {label})")
        choice = input("Select a topic by number: ").strip()
        if choice.isdigit():
            selected = int(choice)
            if 1 <= selected <= len(topic_names):
                return topic_names[selected - 1]
        print("Please select a valid topic number.\n")


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
    topics = discover_topics()
    if not topics:
        print("No YAML topic files found in the current directory.")
        return

    topic_question_bank = {name: load_questions(path) for name, path in topics.items()}
    topic_counts = {
        name: len(questions) for name, questions in topic_question_bank.items()
    }
    total_questions_available = sum(topic_counts.values())
    if total_questions_available == 0:
        print("No questions available across the discovered topics.")
        return

    topic_counts_with_all = dict(topic_counts)
    topic_counts_with_all["All"] = total_questions_available

    topic_name = ask_topic_selection(topic_counts_with_all)
    if topic_name == "All":
        questions = [
            question
            for questions_list in topic_question_bank.values()
            for question in questions_list
        ]
    else:
        questions = topic_question_bank.get(topic_name, [])

    if not questions:
        if topic_name == "All":
            print("No questions available across the selected topics.")
        else:
            print(f"No questions available for the '{topic_name}' topic.")
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
