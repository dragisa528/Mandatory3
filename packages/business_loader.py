from packages import storage_manager
from packages.business import Business
from packages.storage_manager import load_business_from_storage, business_exists
from packages.tools import clear_console, press_enter_to_continue, maybe_exit, get_version_number


# menu where user can create a new business, or load existing business.
# the menu have to return a business to proceed to next step
def get_business_from_menu():
    # print welcome message
    clear_console()
    print("WELCOME TO BWMS (Business Warehouse Management System)")
    print("Version: " + get_version_number())
    print()
    print("Menu options:")
    print("1) Create a new business")

    # menu options shown if any businesses exists
    business_list = list_businesses()
    if business_list is not None and business_list != "":
        print("2) Open existing business")
        print("3) Delete business")
    print("x) Exit")
    chosen_option = input("Please choose an option: ").lower()  # let user choose

    # process chosen option
    if chosen_option == "x":  # user wants to exit
        maybe_exit()
        return get_business_from_menu()
    if chosen_option == "1":  # create a new business
        create_a_business()
        return get_business_from_menu()
    elif chosen_option == "2":  # open existing business
        # welcome message
        clear_console()
        print("Please type the name of the business you would like to open")
        print()

        # print name of businesses available
        print("Available businesses:")
        print(list_businesses())
        print()
        print("Type 'x' to cancel")

        # let user type name of business
        name_of_business = input("Name of business: ")

        # check if user wants to exit
        if name_of_business.lower() == "x":
            return get_business_from_menu()

        # load business by name
        loaded_business = load_business_from_storage(name_of_business)

        # did a business get loaded?
        if loaded_business is False:  # business was not loaded, and we should show the menu again
            press_enter_to_continue()
            return get_business_from_menu()
        return loaded_business  # business was loaded. Success. Return true
    elif chosen_option == "3":
        # show delete business menu
        clear_console()
        print("------------------- DELETE BUSINESS -------------------")

        # list all businesses
        print(list_businesses())
        print("Type 'x' to cancel")

        # let user type the name of the business to delete
        delete_business = input("Name of business you would like to delete: ")
        clear_console()

        # check if user wants to exit
        if delete_business.lower() == "x":
            return get_business_from_menu()

        # warn user about data being deleted, and get confirmation
        print("WARNING! THIS WILL DELETE ALL INFORMATION ABOUT THIS BUSINESS, AND ALL PRODUCTS LINKED TO THIS BUSINESS!")
        print("Business to delete: " + delete_business)
        sure = input("Are you sure? Deleting a business cannot be undone! (y/n): ").lower()

        # does the user want to delete the business?
        if sure == "y":  # delete business
            storage_manager.delete_business(delete_business)
            press_enter_to_continue()
    else:  # unknown option from user
        print("'" + chosen_option + "' is not an option")
        press_enter_to_continue()

    # back to main menu
    return get_business_from_menu()


# create a new business
def create_a_business():
    # show create business menu
    clear_console()
    print("------------------- CREATE BUSINESS -------------------")
    print("Type 'x' to cancel")

    # collect business name
    business_name = input("Name of business: ")

    # let the user exit
    if business_name == "x":
        return

    # don't let the user use ',' in business name. This will break CSV file
    if "," in business_name:
        print("',' is not allowed in business name")
        press_enter_to_continue()
        create_a_business()
        return

    # make sure business name is not empty
    if business_name == "":
        print("The business must have a name!")
        press_enter_to_continue()
        create_a_business()
        return

    # make sure business not already exists
    if business_exists(business_name):
        print("Business already exists!")
        press_enter_to_continue()
        create_a_business()
        return

    # collect initial balance, and make sure it's numeric
    initial_balance = input("Initial balance: ")
    if initial_balance.isnumeric() is False:
        print("Initial balance must be a number")
        press_enter_to_continue()
        create_a_business()
        return

    # make sure initial balance more than 0
    if int(initial_balance) < 0:
        print("Initial balance cannot be a negative number")
        press_enter_to_continue()
        create_a_business()
        return

    # create business
    business = Business(business_name, int(initial_balance))
    storage_manager.create_business(business_name)

    # add business name
    storage_manager.business_name = business_name

    # save business
    business.save()
    print("Business created!")
    press_enter_to_continue()


# list all businesses
def list_businesses():
    try:
        # load businesses file
        with open("businesses.csv") as f:
            businesses = f.read()
            businesses.replace(", ", "\n")
            return businesses
    except FileNotFoundError:  # false if no file is found
        return None
    finally:  # try to close file
        try:
            f.close()
        except UnboundLocalError:
            return None
