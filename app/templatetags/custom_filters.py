from django import template

register = template.Library()

@register.filter
def sum_prices(products):
    return sum(product['price'] * product['quantity'] for product in products)
from django import template

