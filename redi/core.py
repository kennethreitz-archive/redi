from models import *


def value(key, r=redis):
    return Rvalue(key, r=r)
