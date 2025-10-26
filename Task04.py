from typing import Callable, Dict, Tuple


Contacts = Dict[str, str]


def input_error(func: Callable) -> Callable:
    """
    Декоратор обробляє KeyError, ValueError, IndexError та повертає
    дружні повідомлення без завершення програми.
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError as e:
            # якщо в повідомленні вже є деталь — покажемо її
            return str(e) if str(e) else "Give me name and phone please."
        except IndexError:
            return "Enter the argument for the command"
    return inner


def parse_args(user_input: str) -> Tuple[str, Tuple[str, ...]]:
    """
    Розбиває рядок на команду та аргументи.
    """
    parts = user_input.strip().split()
    if not parts:
        return "", tuple()
    return parts[0].lower(), tuple(parts[1:])


@input_error
def add_contact(args: Tuple[str, ...], contacts: Contacts) -> str:
    if len(args) < 2:
        raise ValueError("Give me name and phone please.")
    name, phone = args[0], args[1]
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args: Tuple[str, ...], contacts: Contacts) -> str:
    if len(args) < 2:
        raise ValueError("Give me name and phone please.")
    name, phone = args[0], args[1]
    if name not in contacts:
        raise KeyError(name)
    contacts[name] = phone
    return "Phone changed."


@input_error
def get_phone(args: Tuple[str, ...], contacts: Contacts) -> str:
    if not args:
        raise IndexError
    name = args[0]
    return contacts[name]  # KeyError обробляється декоратором


@input_error
def show_all(_: Tuple[str, ...], contacts: Contacts) -> str:
    if not contacts:
        return "No contacts yet."
    lines = [f"{n}: {p}" for n, p in contacts.items()]
    return "\n".join(lines)


def main() -> None:
    contacts: Contacts = {}

    print("Welcome to CLI Assistant. Type 'help' for commands.")
    while True:
        user_input = input("Enter a command: ").strip()
        if not user_input:
            print("Enter the argument for the command")
            continue

        command, args = parse_args(user_input)

        if command in ("exit", "close"):
            print("Good bye!")
            break
        if command == "help":
            print("Commands: hello | add <name> <phone> | change <name> <phone> | "
                  "phone <name> | all | exit|close")
            continue
        if command == "hello":
            print("How can I help you?")
            continue
        if command == "add":
            print(add_contact(args, contacts))
            continue
        if command == "change":
            print(change_contact(args, contacts))
            continue
        if command == "phone":
            print(get_phone(args, contacts))
            continue
        if command == "all":
            print(show_all(args, contacts))
            continue

        print("Unknown command. Type 'help' for available commands.")


if __name__ == "__main__":
    main()
