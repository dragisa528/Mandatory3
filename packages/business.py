import json
from datetime import datetime

from packages.product import Product
from packages.storage_manager import write_string_to_file, load_string_from_file
from packages.tools import money_text, strike_text


class Business:
    products = []

    def __init__(self, name, initial_balance: int):
        self.name = name
        self.balance = initial_balance

    # add a product to list of products list
    def add_product(self, product):
        self.products.append(product)

    # add a product from json object
    def add_product_from_json(self, uid, element):
        self.add_product(Product(element["name"], element["stock"], element["purchase_cost"],
                                 element["price"], uid=uid, discounted_price=element["discounted_price"]))

    # delete a product from products list
    def delete_product(self, product_id):
        product = self.get_product(product_id)

        # make sure product exists
        if product is None:
            print("Could not find product with productID: " + product_id)
            return False

        # remove the product
        self.products.remove(product)
        print(product.name + " was deleted!")

        # save and return true
        self.save()
        return True

    # checks if product exists
    def product_exists(self, product_id):
        try:
            # loop through all products and check if ID matches productID from parameter
            for product in self.products:
                if int(product.uid) == int(product_id):  # product matches
                    return True
            return False  # product not found
        except TypeError:  # product id was not a number
            print("Product ID should be a number")
            return False
        except ValueError:
            print("Could not find product")
            return False

    # get a product by productID
    def get_product(self, product_id) -> Product or None:
        try:
            for product in self.products:  # loop through all products and try to match
                if int(product.uid) == int(product_id):  # found product
                    return product
            return None  # product not found
        except TypeError:  # product id was not a number
            print("Product ID should be a number")
            return None

    # increase balance, decrease stock
    def sell_product(self, product_id, amount_to_sell: int):
        if self.product_exists(product_id):  # does the product exists?
            product = self.get_product(product_id)  # get the product

            # make sure we have enough in stock
            if amount_to_sell > product.stock:
                print(self.name + " does not have " + str(amount_to_sell) + " " + product.name +
                      " in stock. Current stock: " + str(product.stock))
                return False

            # get selling price, either discounted or normal if no discount
            sold_for = product.discounted_price
            if sold_for is None:
                sold_for = product.price

            # add money to balance
            self.balance += sold_for*amount_to_sell

            # add transaction to transaction history
            self.add_row_to_transactions("Sold " + str(amount_to_sell) + " " + product.name +
                                         " for " + money_text(sold_for) + " each")

            # return result of product.sell in product class
            return product.sell(amount_to_sell)

        # product did not exist
        print("Could not find product with productID: " + product_id)
        return False

    # restock product if business have enough money
    def restock_product(self, product_id, amount: int):
        # get product and calculate purchase cost
        product = self.get_product(product_id)
        total_purchase_cost = product.purchase_cost * amount

        # make sure business has enough money
        if total_purchase_cost > self.balance:
            print(self.name + " cannot afford to buy " + str(amount) + " " + product.name
                  + " for " + money_text(total_purchase_cost) + " as "
                  + self.name + " only has " + money_text(self.balance) + " in it's account")
            return False  # failed, return false

        # withdraw business balance
        self.balance -= total_purchase_cost

        # restock warehouse
        product.restock(amount)

        # add transaction to transaction history
        self.add_row_to_transactions("Bought " + str(amount) + " " + product.name +
                                     " for " + money_text(product.purchase_cost) + " each")

        print(self.name + " puchased " + str(amount) + " " + product.name + " for " + money_text(total_purchase_cost) +
              ". " + self.name + "'s new balance is: " + money_text(self.balance))

        # save and return True
        self.save()
        return True

    # add a discount to product
    def discount_product(self, product_id, discount_percentage: int):
        # make sure product exists
        if self.product_exists(product_id):
            # make sure discount percentage is reasonable
            if discount_percentage >= 100 or discount_percentage <= 0:
                print("Discount percentage must be a number greater than 0, and less than 100")
                return False  # failed as discount was too large or small, return false

            # get product and add discount
            product = self.get_product(product_id)
            product.add_discount(discount_percentage)
            print(product.name + " just got discounted! Old price: " + strike_text(money_text(product.price)) +
                  ". New price: " + money_text(product.discounted_price))

            # save and return True
            self.save()
            return True
        else:
            return False  # failed: product does not exist, return false

    # removes a discount from a product
    def remove_discount(self, product_id) -> bool:
        # remove business if product_id exists
        if self.product_exists(product_id):
            self.get_product(product_id).remove_discount()
            self.save()
            return True

        # product was not found, tell user and return false
        print("ProductID was not found: " + product_id)
        return False

    # print a list of all products with corresponding information
    def print_list_of_products(self):
        # loop through all products, and print info about product
        for product in self.products:
            print(str(product.uid) + ") " + product.name + " (Stock: " + str(
                product.stock) + ", Price: " + product.get_price_text() + ")")

        # if there are no products, tell the user
        if len(self.products) == 0:
            print("There are no products yet")

    # add row to transaction history for business
    def add_row_to_transactions(self, row:str):
        # get current date and time
        current_date = datetime.today().strftime('%d.%m.%Y %H:%M:%S')

        # load transactions file
        current_transaction_log = load_string_from_file("transactions.txt")

        # if there are transactions in the file: add new line
        if current_transaction_log is not None and current_transaction_log != "":
            current_transaction_log += "\n"
        elif current_transaction_log is None:  # this is the first transaction, don't add new line
            current_transaction_log = ""

        # add current transaction line, and save file
        current_transaction_log += current_date + ": " + row
        write_string_to_file("transactions.txt", current_transaction_log)

    # create dict of business object, including products
    def to_dict(self):
        # create a dict of all products
        products_dicts = {}
        for product in self.products:
            products_dicts.update(product.to_dict())

        # return business object dict including products dict
        return {"name": self.name, "balance": self.balance, "products": products_dicts}

    # save business to SaveFile.json in business folder
    def save(self):
        return write_string_to_file("SaveFile.json", json.dumps(self.to_dict()))
