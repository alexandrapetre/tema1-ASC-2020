"""
Petre Alexandra 335CB
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2020
"""
import time
from threading import Thread


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.products = products
        self.marketplace = marketplace
        self.id_producer = self.marketplace.register_producer()
        self.republish_wait_time = republish_wait_time

    def wait(self):
        """
        wait time
        """
        time.sleep(self.republish_wait_time)

    def run(self):
        while True:
            for product in self.products:
                while self.marketplace.publish(self.id_producer, product) is False:
                    self.wait()
