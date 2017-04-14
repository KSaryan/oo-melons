"""Classes for melon orders."""

import random
from datetime import datetime


class TooManyMelonsError(ValueError):
    """ Raises error if melon order > 100. """

    def __init__(self):
        super(TooManyMelonsError, self).__init__("Too many melons ordered!")


class AbstractMelonOrder(object):
    """ All Melon orders """

    def __init__(self, species, qty, tax=0, order_type="government"):
        """ Initialize melon order attributes. """
        self.species = species
        self.qty = qty

        if self.qty > 100:
            raise TooManyMelonsError()

        self.shipped = False
        self.tax = tax
        self.order_type = order_type
        self.time = datetime.now()

    def get_base_price(self):
        """ Calculates base price. """

        base_price = random.randint(5, 9)

        if self.time.hour in range(8, 12) and self.time.weekday() in range(0, 5):
            base_price += 4

        return base_price

    def get_total(self):
        """Calculate price, including tax."""

        base_price = self.get_base_price()

        if self.species == "christmas":
            base_price *= 1.5

        total = (1 + self.tax) * self.qty * base_price

        if self.order_type == "international" and self.qty < 10:
            return total + 3
        else:
            return total

    def mark_shipped(self):
        """Record the fact than an order has been shipped."""

        self.shipped = True


class DomesticMelonOrder(AbstractMelonOrder):
    """A melon order within the USA."""

    def __init__(self, species, qty):
        """Initialize melon order attributes."""
        super(DomesticMelonOrder, self).__init__(species, qty, 0.08, "domestic")


class InternationalMelonOrder(AbstractMelonOrder):
    """An international (non-US) melon order."""

    def __init__(self, species, qty, country_code):
        """Initialize melon order attributes."""
        super(InternationalMelonOrder, self).__init__(species, qty, 0.17, "international")
        self.country_code = country_code

    def get_country_code(self):
        """Return the country code."""

        return self.country_code


class GovernmentMelonOrder(AbstractMelonOrder):
    """ A government melon order. """

    def __init__(self, species, qty):
        """Initialize melon order attributes."""
        super(GovernmentMelonOrder, self).__init__(species, qty)
        self.order_type = "government"
        self.passed_inspection = False

    def mark_inspection(self, passed):
        self.passed_inspection = passed

