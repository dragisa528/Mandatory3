import os

# used to get more debug information
debug_mode = False


# version number
def get_version_number():
    return "1.0.0"


# strike text
def strike_text(text):
    result = ''
    for c in text:  # add strike to every character
        result = result + c + '\u0336'
    return result


# convert money int to string, and add currency
def money_text(money: int):
    return str(money) + " kr"


# clear the console
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


# ask user to press enter to carry on
def press_enter_to_continue():
    print("[PRESS ENTER TO CONTINUE]", end="")
    input()


# exit if user confirms
def maybe_exit():
    sure = input("Sure? (y/n)").lower()
    if sure == "y":
        exit(0)


# tell the user that 'x' will take them back
def print_x_to_go_back():
    print("You can also type 'x' to go back")


# tell the user that 'x' will exit
def print_x_to_exit():
    print("You can also type 'x' to go exit")
