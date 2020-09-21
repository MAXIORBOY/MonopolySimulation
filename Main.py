import random as rnd
import matplotlib.pyplot as plt
import numpy as np
import math as mth


def generate_cards():
    cards = []
    for i in range(16):
        cards.append(i+1)

    rnd.shuffle(cards)

    return cards


def cc_card_definition(actual_position, cc_card_value):
    ap = actual_position
    if cc_card_value == 1:
        ap = 0

    elif cc_card_value == 2:
        ap = 10

    return ap


def ch_card_definition(actual_position, ch_card_value):
    ap = actual_position

    def one():
        return 0

    def two():
        return 10

    def three():
        return 11

    def four():
        return 24

    def five():
        return 39

    def six():
        return 5

    def seven_eight():
        if 5 < actual_position < 15:
            return 15
        elif 15 < actual_position < 25:
            return 25
        elif 25 < actual_position < 35:
            return 35
        else:
            return 5

    def nine():
        if 12 < actual_position < 28:
            return 28
        else:
            return 12

    def ten(pos):
        return pos - 3

    switcher = {1: one(), 2: two(), 3: three(), 4: four(), 5: five(), 6: six(), 7: seven_eight(), 8: seven_eight(), 9: nine(), 10: ten(ap)}

    if ch_card_value < 11:
        ap = switcher.get(ch_card_value)

    return ap


def throw_dice(sides=6):
    dice1 = rnd.randint(1, sides)
    dice2 = rnd.randint(1, sides)

    double = dice1 == dice2

    return dice1 + dice2, double


def simulation(turns=100, games=100000):  # simulation options
    cc_locations = [2, 17, 33]
    ch_locations = [7, 22, 36]
    squares_all_games = [0] * 40

    for g in range(games):
        squares_one_game = [0] * 40
        actual_position = 0
        double_this_turn = False
        doubles = 0
        cc_cards = generate_cards()
        ch_cards = generate_cards()
        cc_cards_counter = 0
        ch_cards_counter = 0

        for t in range(turns):
            if not double_this_turn:
                doubles = 0
            position_advance, double_this_turn = throw_dice()
            if double_this_turn:
                doubles += 1
            if doubles == 3:
                actual_position = 10
            else:
                actual_position += position_advance
                if actual_position > 39:
                    actual_position -= 40

            if actual_position == 30:
                actual_position = 10

            elif actual_position in ch_locations:
                actual_position = ch_card_definition(actual_position, ch_cards[ch_cards_counter])
                ch_cards_counter += 1
                if ch_cards_counter > 15:
                    ch_cards_counter = 0

            elif actual_position in cc_locations:
                actual_position = cc_card_definition(actual_position, cc_cards[cc_cards_counter])
                cc_cards_counter += 1
                if cc_cards_counter > 15:
                    cc_cards_counter = 0

            squares_one_game[actual_position] += 1

        for i in range(len(squares_all_games)):
            squares_all_games[i] += squares_one_game[i]

    sum_of_all = sum(squares_all_games)
    for i in range(len(squares_all_games)):
        squares_all_games[i] = round(100 * squares_all_games[i] / sum_of_all, 2)

    return squares_all_games


def convert_list_to_matrix(square_list):
    rows = []
    for i in range(11):
        if i == 0:
            rows.append(square_list[0:11])
        elif i < 10:
            row = [square_list[-i]]
            row.extend([0.00] * 9)
            row.extend([square_list[10 + i]])
            rows.append(row)
        else:
            rows.append(square_list[30:19:-1])

    return np.array(rows)


def visualization(matrix):
    norm_matrix = []

    for i in range(len(matrix)):
        row = []
        for j in range(len(matrix[0])):
            row.append(mth.log(matrix[i][j] + 1, 10))

        norm_matrix.append(row)

    norm_matrix = np.array(norm_matrix)

    fig, ax = plt.subplots()

    ax.imshow(norm_matrix, cmap='jet')

    for i in range(len(norm_matrix)):
        for j in range(len(norm_matrix)):
            if i == 0 or i == len(norm_matrix) - 1 or j == 0 or j == len(norm_matrix) - 1:
                ax.text(j, i, matrix[i, j], ha="center", va="center", color="k")

    ax.set_title("A percentage chance for ending a turn at the particular square in the Monopoly game \n")
    fig.tight_layout()
    plt.axis('off')
    plt.show()


visualization(convert_list_to_matrix(simulation()))
