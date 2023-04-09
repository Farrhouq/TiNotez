import math


def farsan_encrypt(strin: str):
    '''Encrypts a given string'''
    string = strin[::-1]
    row = math.floor(len(string)**0.5)
    column = math.ceil(len(string)**0.5)

    rows = []
    i = 0
    reved = True
    while i < len(string):
        cut = string[i:i+column]
        if reved:
            reved = False
        else:
            reved = True
            cut = cut[::-1]
        rows.append(cut)
        i += column

    coded = []
    for i in range(len(rows[0])):
        line = []
        for j in rows:
            if len(j) > (i):
                coded.append(j[i])
                line.append(j[i])

    return ''.join(coded)


def farsan_decrypt(strin: str):
    '''Decrypts a string based on the `Farsan` encryption method.'''
    string = strin
    decoded = []
    row = math.ceil(len(string)**0.5)
    hanging = len(string) % row
    intend = len(string)//row
    i = 0

    hang = 0
    rows = []
    while i < len(string):
        cut = string[i:i+intend]
        if hang < hanging:
            cut = string[i:i+intend+1]
            i += intend+1
        else:
            i += intend
        rows.append(cut)
        hang += 1

    i = 0
    reved = True
    hang = 0

    reved = True
    for i in range(len(rows[0])):
        reved = not reved
        c = rows
        if reved:
            c = rows[::-1]

        for j in c:
            if len(j) > i:
                decoded.append(j[i])

    return ''.join(decoded)[::-1]


n = 0
e = "abcde"
ee = farsan_encrypt(e)

def determine(string, original, i):
    if farsan_encrypt(string) == original:
        return i
    return determine(farsan_encrypt(string), original, i+1)

print(determine(e, e, 1))


# while ee != e:
#     ee = farsan_encrypt(ee)
#     n += 1
#     print(ee)
# print(n)


# string = input("Enter a string for testing: ")
# print(f'The string is "{string}"')
# print(f"The encrypted string is {(farsan_encrypt(string))}")
# print(f"The decrypted string is {farsan_decrypt(farsan_encrypt(string))}")
