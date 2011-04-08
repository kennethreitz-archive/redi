from models import *
from .config import redis, init

def value(key, r=redis):
    return Rvalue(key, r=r)
