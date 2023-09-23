import random

from packages.tools import strike_text


class Product:
    def __init__(self, name: str, stock: int, purchase_cost: int, price: int, uid: str = None, discounted_price: int = None):
        self.uid = random.randint(100000, 999999)
        if uid is not None:  # user can add custom UID if wanted
            self.uid = int(uid)
        self.name = name
        self.purchase_cost = purchase_cost
        self.price = price
        self.discounted_price = discounted_price
        self.stock = stock

    # convert object info to dict
    def to_dict(self):
        return {self.uid: {"name": self.name,
                           "stock": self.stock,
                           "purchase_cost": self.purchase_cost,
                           "price": self.price,
                           "discounted_price": self.discounted_price}}

    # add a discount to product
    def add_discount(self, percentage: int):
        self.discounted_price = self.price - self.price * (percentage / 100)

    # remove a previously added discount
    def remove_discount(self):
        self.discounted_price = None

    # get the correct price of a product
    def get_price(self):
        # if discount available, return discount. Else: return regular price
        if self.discounted_price is not None:
            return self.discounted_price
        else:
            return self.price

    # return price as text including currency.
    def get_price_text(self):
        if self.discounted_price is not None:  # a discount is present. Strike original price
            return strike_text(str(self.price) + " kr") + " " + str(self.discounted_price) + " kr"
        return str(self.price) + " kr"

    # sell an amount of this product
    def sell(self, num_to_sell: int):
        if self.stock >= num_to_sell:  # don't let the user sell more than in stock
            self.stock -= num_to_sell
            print("Sold product: " + self.name)
            return True

        # trying to sell more than in stock
        print("Product is out of stock. Cannot sell product")
        return False

    # restock product
    def restock(self, amount_to_add):
        self.stock += amount_to_add
