from django import template
from guitars.models import *
from cart.cart import Cart

register = template.Library()


@register.simple_tag()
def get_shapes():
    return Category.objects.filter(cat_type='shape').all()


@register.simple_tag()
def get_coils():
    return Category.objects.filter(cat_type='coil').all()


@register.simple_tag()
def get_description(post_name):
    return Guitars.objects.filter(name=post_name).first().description


@register.simple_tag()
def get_total(request):
    cart = Cart(request)
    return cart.total()
