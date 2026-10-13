import json
import random
from pathlib import Path


FILE_NAME = "words.json"


def load_words():
    """Load saved words from JSON file."""

    if not Path(FILE_NAME).exists():
        return []

    with open(FILE_NAME, "r", encoding="utf-8") as file:
        return json.load(file)



def save_words(words):
    """Save words into JSON file."""

    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(
            words,
            file,
            indent=4,
            ensure_ascii=False
        )



def menu():

    print("\n" + "=" * 35)
    print("     VOCABULARY TRAINER")
    print("=" * 35)

    print("1. Add Word")
    print("2. Show Words")
    print("3. Search Word")
    print("4. Delete Word")
    print("5. Start Quiz")
    print("6. Exit")



def add_word(words):

    print("\n--- Add New Word ---")

    word = input("Enter word: ").strip()
    meaning = input("Enter meaning: ").strip()
    example = input("Enter example: ").strip()


    for item in words:

        if item["word"].lower() == word.lower():

            print("This word already exists.")
            return


    new_word = {

        "word": word,
        "meaning": meaning,
        "example": example
    }


    words.append(new_word)

    save_words(words)

    print("Word added successfully.")



def show_words(words):

    print("\n--- Word List ---")


    if not words:

        print("No words found.")
        return


    for index, item in enumerate(words, start=1):

        print(f"\n{index}. {item['word']}")
        print("Meaning:", item["meaning"])
        print("Example:", item["example"])

        print("-" * 25)



def search_word(words):

    search = input(
        "Enter word to search: "
    ).lower()


    for item in words:

        if item["word"].lower() == search:

            print("\nFound:")
            print("Word:", item["word"])
            print("Meaning:", item["meaning"])
            print("Example:", item["example"])

            return


    print("Word not found.")



def delete_word(words):

    word = input(
        "Enter word to delete: "
    ).lower()


    for item in words:

        if item["word"].lower() == word:

            words.remove(item)

            save_words(words)

            print("Word deleted.")

            return


    print("Word not found.")



def quiz(words):

    if len(words) == 0:

        print("No words available.")
        return


    amount = min(5, len(words))


    questions = random.sample(
        words,
        amount
    )


    score = 0


    print("\n--- Quiz Started ---")


    for number, item in enumerate(questions, start=1):

        print(
            f"\nQuestion {number}"
        )


        print(
            "Meaning:",
            item["meaning"]
        )


        answer = input(
            "Your answer: "
        )


        if answer.lower() == item["word"].lower():

            print("Correct!")

            score += 1

        else:

            print(
                "Wrong!",
                "Answer:",
                item["word"]
            )


    print("\nQuiz Finished")
    print(
        f"Score: {score}/{amount}"
    )



def main():

    words = load_words()


    while True:

        menu()


        choice = input(
            "\nChoose option: "
        )


        if choice == "1":

            add_word(words)


        elif choice == "2":

            show_words(words)


        elif choice == "3":

            search_word(words)


        elif choice == "4":

            delete_word(words)


        elif choice == "5":

            quiz(words)


        elif choice == "6":

            print("Goodbye!")

            break


        else:

            print("Invalid choice.")



if __name__ == "__main__":

    main()
