import random as rnd
import matplotlib.pyplot as plt
import numpy as np
import math as mth


class Cards:
    def __init__(self, number_of_cards):
        self.number_of_cards = number_of_cards
        self.deck_order = self.generate_cards()
        self.shuffle_deck()
        self.card_index = 0

    def generate_cards(self):
        return [i + 1 for i in range(self.number_of_cards)]

    def shuffle_deck(self):
        rnd.shuffle(self.deck_order)

    def increment_card_index(self):
        self.card_index += 1
        if self.card_index > self.number_of_cards - 1:
            self.card_index = 0

    def reset_card_index(self):
        self.card_index = 0


class CommunityChestCards(Cards):
    def __init__(self):
        super().__init__(number_of_cards=17)
        self.cards_pick_up_locations = [3, 18, 34]
        self.card_definitions = self.define_cards()

    @staticmethod
    def define_cards():
        return {1: {'set': 1},
                6: {'set': 11}}


class ChanceCards(Cards):
    def __init__(self):
        super().__init__(number_of_cards=16)
        self.cards_pick_up_locations = [8, 23, 37]
        self.card_definitions = self.define_cards()

    @staticmethod
    def define_cards():
        return {1: {'set': 1},
                2: {'set': 25},
                3: {'set': 12},
                4: {'nearest': [13, 29]},
                5: {'nearest': [6, 16, 26, 36]},
                8: {'move': -3},
                9: {'set': 11},
                12: {'set': 6},
                13: {'set': 40}}


class MonopolySimulation:
    def __init__(self, turns=100, games=1000000):
        self.turns = turns
        self.games = games

        self.community_chest_cards = CommunityChestCards()
        self.chance_cards = ChanceCards()

        self.end_turn_fields_occurrences_array = [0] * 40
        self.percentage_matrix = np.zeros((11, 11))
        self.run_simulation()
        self.end_turn_fields_percentages_array = self.convert_occurrences_into_percentages()
        self.build_matrix_from_array()

    @staticmethod
    def throw_dice(sides=6):
        dice1 = rnd.randint(1, sides)
        dice2 = rnd.randint(1, sides)

        double = dice1 == dice2

        return dice1 + dice2, double

    def register_end_turn_field(self, field):
        self.end_turn_fields_occurrences_array[field - 1] += 1

    @staticmethod
    def bring_position_value_back_to_range(position):
        if position < 1:
            position += 40

        elif position > 40:
            position -= 40

        return position

    def change_current_position_based_on_card(self, movement_instruction, current_position):
        movement_type, movement_value = list(movement_instruction.items())[0]
        if movement_type == 'set':
            return movement_value

        elif movement_type == 'nearest':
            distance_array = [self.bring_position_value_back_to_range(value - current_position) for value in movement_value]
            return movement_value[distance_array.index(min(distance_array))]

        elif movement_type == 'move':
            return self.bring_position_value_back_to_range(current_position + movement_value)

    def run_simulation(self):
        for game in range(self.games):
            current_position = 1
            doubles = 0
            for turn in range(self.turns):
                going_to_jail = False
                dice_value, is_double = self.throw_dice()
                doubles += int(is_double)

                if is_double:
                    doubles += 1
                    if doubles == 3:
                        doubles = 0
                        current_position = 11
                        going_to_jail = True
                else:
                    doubles = 0

                if not going_to_jail:
                    current_position += dice_value
                    current_position = self.bring_position_value_back_to_range(current_position)
                    if current_position == 31:
                        current_position = 11
                    else:
                        if current_position in self.chance_cards.cards_pick_up_locations:
                            movement_instruction = self.chance_cards.card_definitions.get(self.chance_cards.deck_order[self.chance_cards.card_index], None)
                            self.chance_cards.increment_card_index()
                            if movement_instruction is not None:
                                current_position = self.change_current_position_based_on_card(movement_instruction, current_position)

                        if current_position in self.community_chest_cards.cards_pick_up_locations:
                            movement_instruction = self.community_chest_cards.card_definitions.get(self.community_chest_cards.deck_order[self.community_chest_cards.card_index], None)
                            self.community_chest_cards.increment_card_index()
                            if movement_instruction is not None:
                                current_position = self.change_current_position_based_on_card(movement_instruction, current_position)

                self.register_end_turn_field(current_position)

            self.community_chest_cards.shuffle_deck()
            self.community_chest_cards.reset_card_index()
            self.chance_cards.shuffle_deck()
            self.chance_cards.reset_card_index()

    def convert_occurrences_into_percentages(self):
        sum_of_all_end_turn_fields = sum(self.end_turn_fields_occurrences_array)
        return [100 * self.end_turn_fields_occurrences_array[i] / sum_of_all_end_turn_fields for i in range(len(self.end_turn_fields_occurrences_array))]

    def build_matrix_from_array(self):
        self.percentage_matrix[0, 0:-1] = self.end_turn_fields_percentages_array[0: 10]
        self.percentage_matrix[0:-1, -1] = self.end_turn_fields_percentages_array[10: 20]
        self.percentage_matrix[-1, 1:] = list(reversed(self.end_turn_fields_percentages_array[20: 30]))
        self.percentage_matrix[1:, 0] = list(reversed(self.end_turn_fields_percentages_array[30: 40]))

    def transform_percentage_matrix(self):
        return np.array([[mth.log(self.percentage_matrix[i, j] + 1, 10) for j in range(len(self.percentage_matrix[i]))] for i in range(len(self.percentage_matrix))])

    def view_results(self):
        fig, ax = plt.subplots()
        ax.imshow(self.transform_percentage_matrix(), cmap='jet')

        for i in range(len(self.percentage_matrix)):
            for j in range(len(self.percentage_matrix)):
                if i == 0 or i == len(self.percentage_matrix) - 1 or j == 0 or j == len(self.percentage_matrix) - 1:
                    if i != 0 or j != 0:
                        ax.text(j, i, f'{round(self.percentage_matrix[i, j], 2)}%', ha="center", va="center", color="k")
                    else:
                        ax.text(j, i, f'START -> \n{round(self.percentage_matrix[i, j], 2)}%', ha="center", va="center", color="k")

        ax.set_title("A percentage chance for ending a turn at the particular square in the Monopoly game \n")
        fig.tight_layout()
        plt.axis('off')
        plt.show()
