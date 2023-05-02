import random
from .shuffle import shuffle


def gen_pass(no):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    numbers = '1234567890'
    special = '!@#$%^&*{}|\/<>~?;=()[+_-]'
    lu = [upper for upper in letters.upper()]
    ll = [g for g in letters.lower()]
    nn = [t for t in numbers]
    ss = [s for s in special]
    password = 'm' * no
    no -= 1
    p_list = [char for char in password]
    while no > 0:
        p_list[no] = random.choices(lu)
        p_list[no - 1] = random.choices(ll)
        p_list[no - 2] = random.choices(ss)
        p_list[no - 3] = random.choices(nn)
        no -= 4
    p_list2 = []
    for item in p_list:
        p_list2.append(item[0])

    your_password = shuffle((''.join(p_list2)))
    return your_password