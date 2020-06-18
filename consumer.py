"""
Petre Alexandra 335CB
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2020
"""
import time
from threading import Thread


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.carts = carts
        self.id_cart = 0
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time

    def wait(self):
        """
        wait time
        """
        time.sleep(self.retry_wait_time)

    def print_output(self):
        """
        print result
        """
        cart = self.marketplace.place_order(self.id_cart)
        for element in cart:
            print(self.name + ' bought ' + str(element))

    def run(self):
        for cart in self.carts:
            self.id_cart = self.marketplace.new_cart()
            for operation in cart:
                if operation['type'] == "add":
                    quantity = operation['quantity']
                    product = operation['product']
                    while quantity > 0:
                        if self.marketplace.add_to_cart(self.id_cart, product) is False:
                            self.wait()
                        else:
                            quantity -= 1
                if operation['type'] == "remove":
                    quantity = operation['quantity']
                    product = operation['product']
                    while quantity > 0:
                        self.marketplace.remove_from_cart(
                            self.id_cart, product)
                        quantity -= 1
            self.print_output()
