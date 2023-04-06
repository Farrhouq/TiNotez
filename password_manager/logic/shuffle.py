def shuffle(string):
    import random
    string_list_copy1, string_list_copy_2 = list(string), list(string)

    new = []
    i = 0
    length = len(string_list_copy1)
    while i < len(string_list_copy1):
        new.append(string_list_copy_2.pop(random.randint(0, length - 1)))
        length -= 1
        i += 1
    return ''.join(new)


# lisst = ['nerd', 'beans', 'arrange', ]
# shuffle('')
# chance = 3
# level = 1
# for word in lisst:
#     correct = word
#     run = True
#     while chance != 0 and run:
#         #print('\n')
#         shuffle(word)
#         ans = input('Arrange to form a word?: ')
#         if ans == correct:
#             print('You won!')
#             level += 1
#             if level < len(lisst):
#                 print(f'\nLevel {level}')
#             run = False
#         else:
#             print('Try Again!')
#             chance -= 1
