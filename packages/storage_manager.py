import json
import os
import shutil

from packages.tools import debug_mode

business_name = ""


# load the business from a json file
def load_business_from_storage(name_of_business):
    global business_name
    business_name = name_of_business
    from packages.business import Business

    if debug_mode:  # debug mode enabled, print some debug info
        print("Attempting to load business from: " + business_name + os.sep + "SaveFile.json")

    # load the file as a string
    saved_data = load_string_from_file("SaveFile.json")

    if saved_data is not None:  # data was successfully loaded
        json_converted = json.loads(saved_data)  # transfer string to json

        # create business object, and add all products to it
        business = Business(json_converted["name"], int(json_converted["balance"]))
        for element in json_converted["products"]:
            business.add_product_from_json(element, json_converted["products"][element])
        return business
    else:  # SaveFile.json returned empty string
        print("Failed to load business")
        return False


# create a business
def create_business(name_of_business):
    global business_name
    business_name = name_of_business

    # create business directory
    os.mkdir(name_of_business)

    # add business to businessList
    try:
        # make sure the businesses.csv file exists
        if os.path.exists("businesses.csv") is False:
            open("businesses.csv", "w+").close()

        # open businesses.csv file
        with open("businesses.csv", "r+") as f:
            # read businesses.csv
            file_content = f.read()

            # add ',' if file is not empty
            if file_content != "":
                file_content += ", "

            # add business name
            file_content += business_name

            # write to file and close it
            f.seek(0)
            f.write(file_content)
            f.truncate()
            f.close()
    except ValueError:  # failed to save business
        print("Error: Could not save business")
        return


# check if business exits
def business_exists(name_of_business):
    return os.path.exists(name_of_business + "/SaveFile.json")


# delete a business
def delete_business(business_to_delete):
    # remove directory
    shutil.rmtree(business_to_delete)

    # remove from businesses CSV
    try:
        # open businesses csv file
        with open("businesses.csv", "r+") as f:
            # read file
            file_content = f.read()

            # remove instances of business
            file_content = file_content.replace(", " + business_to_delete, "")
            file_content = file_content.replace(business_to_delete + ", ", "")
            file_content = file_content.replace(business_to_delete, "")

            # write to file
            f.seek(0)
            f.write(file_content)
            f.truncate()
    except FileNotFoundError:  # file was not found
        print("File not found")
    finally:  # attempt to close file
        try:
            f.close()
        except UnboundLocalError:
            return False

    print("Business was deleted!")
    return True


# load string from a file
def load_string_from_file(filepath):
    global business_name
    try:
        # open file from business directory
        with open(business_name + os.sep + filepath, "r") as f:
            return f.read()
    except:  # something went wrong
        return None
    finally:  # attempt to close file
        try:
            f.close()
        except UnboundLocalError:
            return


# write string to a file
def write_string_to_file(filepath, content):
    global business_name

    if debug_mode:  # debug mode enabled, provide some more information
        print("Attemting to write to file: " + business_name + os.sep + filepath + ". Content: " + content)

    # attempt to write to file
    try:
        with open(business_name + os.sep + filepath, "w") as f:
            f.write(content)
            return True
    except:  # something went wrong
        print("Could not save to file")
        return False
    finally:  # attempt to close file
        try:
            f.close()
        except UnboundLocalError:
            return False