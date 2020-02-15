#!/usr/bin/env python3
# coding=utf8

import random
import string


def errors_to_dict(errors):
    """
    form.errors can not be serialized, converted into dict, serialized into json to the front end
    """
    return {k: [str(t) for t in v] for (k, v) in errors.items()}


def get_sample_str(length=8):
    return ''.join(random.sample(string.ascii_lowercase, length))
