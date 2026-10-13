import json
import re
from pathlib import Path


# contacts.json will be created next to this Python file
CONTACTS_FILE = Path(__file__).with_name("contacts.json")


def load_contacts():
    """Load contacts from JSON file."""
    if not CONTACTS_FILE.exists():
        return []

    try:
        with open(CONTACTS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list):
                return data

            return []

    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read contacts file.")
        return []


def save_contacts(contacts):
    """Save contacts to JSON file."""
    try:
        with open(CONTACTS_FILE, "w", encoding="utf-8") as file:
            json.dump(
                contacts,
                file,
                indent=4,
                ensure_ascii=False
            )

    except OSError:
        print("Error: Could not save contacts.")


def show_menu():
    print("\n" + "=" * 35)
    print("        CONTACT BOOK")
    print("=" * 35)

    print("1. Add Contact")
    print("2. Show Contacts")
    print("3. Search Contact")
    print("4. Edit Contact")
    print("5. Delete Contact")
    print("6. Exit")


def get_valid_name():
    while True:
        name = input("Enter contact name: ").strip()

        if name:
            return name

        print("Name cannot be empty.")


def is_valid_phone(number):
    """
    Accept numbers such as:
    09123456789
    +989123456789
    +1 555 123 4567
    """
    pattern = r"^\+?[0-9\s\-()]{7,20}$"

    return bool(re.match(pattern, number))


def get_valid_phone():
    while True:
        number = input("Enter phone number: ").strip()

        if is_valid_phone(number):
            return number

        print("Please enter a valid phone number.")


def add_contact(contacts):
    print("\n--- Add Contact ---")

    name = get_valid_name()
    number = get_valid_phone()

    # Prevent duplicate phone numbers
    for contact in contacts:
        if contact["number"] == number:
            print("A contact with this phone number already exists.")
            return

    contact = {
        "name": name,
        "number": number
    }

    contacts.append(contact)
    save_contacts(contacts)

    print(f"{name} added successfully.")


def show_contacts(contacts):
    print("\n--- Contact List ---")

    if not contacts:
        print("No contacts found.")
        return

    sorted_contacts = sorted(
        contacts,
        key=lambda contact: contact["name"].lower()
    )

    print("-" * 45)
    print(f"{'#':<5}{'Name':<20}{'Phone Number'}")
    print("-" * 45)

    for index, contact in enumerate(sorted_contacts, start=1):
        print(
            f"{index:<5}"
            f"{contact['name']:<20}"
            f"{contact['number']}"
        )

    print("-" * 45)


def search_contacts(contacts):
    if not contacts:
        print("No contacts found.")
        return []

    search_term = input(
        "Enter a name or phone number to search: "
    ).strip().lower()

    results = []

    for contact in contacts:
        if (
            search_term in contact["name"].lower()
            or search_term in contact["number"].lower()
        ):
            results.append(contact)

    if not results:
        print("No matching contacts found.")
        return []

    print("\nSearch Results:")

    for index, contact in enumerate(results, start=1):
        print(
            f"{index}. "
            f"{contact['name']} - "
            f"{contact['number']}"
        )

    return results


def select_contact(contacts):
    results = search_contacts(contacts)

    if not results:
        return None

    if len(results) == 1:
        return results[0]

    while True:
        try:
            choice = int(
                input("Select contact number: ")
            )

            if 1 <= choice <= len(results):
                return results[choice - 1]

            print("Invalid selection.")

        except ValueError:
            print("Please enter a number.")


def edit_contact(contacts):
    print("\n--- Edit Contact ---")

    contact = select_contact(contacts)

    if contact is None:
        return

    print("\nPress Enter to keep current value.")

    new_name = input(
        f"Name [{contact['name']}]: "
    ).strip()

    new_number = input(
        f"Phone [{contact['number']}]: "
    ).strip()

    if new_name:
        contact["name"] = new_name

    if new_number:

        if not is_valid_phone(new_number):
            print("Invalid phone number.")
            return

        # Check duplicate phone number
        for existing_contact in contacts:
            if (
                existing_contact is not contact
                and existing_contact["number"] == new_number
            ):
                print(
                    "Another contact already uses "
                    "this phone number."
                )
                return

        contact["number"] = new_number

    save_contacts(contacts)

    print("Contact updated successfully.")


def delete_contact(contacts):
    print("\n--- Delete Contact ---")

    contact = select_contact(contacts)

    if contact is None:
        return

    print(
        f"\nSelected: "
        f"{contact['name']} - "
        f"{contact['number']}"
    )

    confirm = input(
        "Are you sure you want to delete this contact? (y/n): "
    ).strip().lower()

    if confirm == "y":
        contacts.remove(contact)
        save_contacts(contacts)

        print("Contact deleted successfully.")

    else:
        print("Deletion cancelled.")


def main():
    contacts = load_contacts()

    while True:
        show_menu()

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            add_contact(contacts)

        elif choice == "2":
            show_contacts(contacts)

        elif choice == "3":
            search_contacts(contacts)

        elif choice == "4":
            edit_contact(contacts)

        elif choice == "5":
            delete_contact(contacts)

        elif choice == "6":
            print("\nGoodbye!")
            break

        else:
            print("Invalid choice. Please select 1-6.")


if __name__ == "__main__":
    main()
