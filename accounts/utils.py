import os
import random
import string
import time
from django.utils.text import slugify


def random_string_generator(size=4, chars=string.ascii_lowercase + string.digits):
    '''
    DOCSTRING for random_string_generator():
    This method generates random string. Takes parameters(size=default:4)
    Code: @Numan Ibn Mazid.
    '''
    return ''.join(random.choice(chars) for _ in range(size))


def random_number_generator(size=4, chars='0123456789'):
    '''
    DOCSTRING for random_number_generator():
    This method generates random number. Takes parameters(size=default:4)
    Code: @Numan Ibn Mazid.
    '''
    return ''.join(random.choice(chars) for _ in range(size))


def generate_time_str_num():
    '''
    DOCSTRING for generate_time_str_num():
    This method generates random characters by synchronizing timestamp, random string and number
    Code: @Numan Ibn Mazid.
    '''
    timestamp_d = time.strftime('%d')
    timestamp_m = time.strftime('%m')
    timestamp_y = time.strftime('%Y')
    timestamp_time = time.strftime('%H%M%S')
    random_str = random_string_generator()
    random_num = random_number_generator()
    char_sync = (
        random_str + timestamp_d + random_num + timestamp_time +
        timestamp_y + random_num + timestamp_m
    )
    return char_sync


def unique_slug_generator(instance, instance_field, new_slug=None):
    '''
    DOCSTRING for unique_slug_generator():
    Unique Slug Generator: requires 2 parameters(instance, instance.slug_field_name)
    Instance stands for model instance.
    instance.slug_field_name stands for the desired field from which the slug will be generated like instance.title, instance.name etc.
    Code: @Numan Ibn Mazid.
    '''
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance_field[:50])

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = f"{slug}-{random_string_generator(size=4)}"
        return unique_slug_generator(instance, instance_field, new_slug=new_slug)
    return slug
