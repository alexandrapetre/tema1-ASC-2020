"""
Petre Alexandra 335CB
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2020
"""
import time
import threading

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor
        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.id_producer = -1
        self.id_cart = -1
        self.list_of_carts = []
        self.list_of_producers = []

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        mutex = threading.Lock()

        self.id_producer += 1
        producers = []
        mutex.acquire()
        self.list_of_producers.append(producers)
        mutex.release()
        return str(self.id_producer)

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        mutex = threading.Lock()
        quantity = product[1]
        sleep_time = product[2]
        id_p = int(producer_id)

        if len(self.list_of_producers[id_p]) == self.queue_size_per_producer:
            return False

        if len(self.list_of_producers[id_p]) + quantity < self.queue_size_per_producer:
            mutex.acquire()
            while quantity > 0:
                time.sleep(sleep_time)
                self.list_of_producers[id_p].append(product[0])
                quantity -= 1
            mutex.release()
        else:
            return False

        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        mutex = threading.Lock()
        cart = []

        mutex.acquire()
        self.list_of_carts.append(cart)
        self.id_cart += 1
        mutex.release()
        return self.id_cart

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        mutex = threading.Lock()
        verify = 0
        list_p = []

        for list_p in self.list_of_producers:
            if product in list_p:
                verify = 1
                break

        if verify == 1:
            mutex.acquire()
            self.list_of_carts[cart_id].append(product)
            list_p.remove(product)
            mutex.release()

        if verify == 0:
            return False
        return True

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart"""

        mutex = threading.Lock()
        if product in self.list_of_carts[cart_id]:
            mutex.acquire()
            self.list_of_carts[cart_id].remove(product)
            self.list_of_producers[0].append(product)
            mutex.release()

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        return_list = self.list_of_carts[cart_id]
        return return_list
