import random


class RandomData:

    @staticmethod
    def random_deposit_amount():
        return random.randint(1000, 9000)

    @staticmethod
    def credit_request_amount():
        return random.randint(5000, 15000)



