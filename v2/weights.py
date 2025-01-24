import csv
from enum import Enum

def load_weights_from_csv(csv_file_path, enum_name):
    """
    Loads weight matrix and creates an enum for labels.
    :param csv_file_path: (str) path to csv file
    :param enum_name: (str) name for enum
    :returns: (Enum, list of lists) label enum, weight matrix
    """
    enum_members = {}
    weight_matrix = []

    with open(csv_file_path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        header = next(csv_reader)  # Skip header row
        enum_counter = 0

        for row in csv_reader:
            label = row[0]
            enum_members[label] = enum_counter
            enum_counter += 1

            weights = []
            for i in range(1, len(row)):
                value = row[i]
                weights.append(float(value))
            weight_matrix.append(weights)

    ActionEnum = Enum(enum_name, enum_members)
    return ActionEnum, weight_matrix

# Reward weights for each action by motivation
Action, action_weights = load_weights_from_csv("action_weights.csv", "Action")

# Reward weights for each gamer type by motivation
GamerType, gamer_type_weights = load_weights_from_csv("gamer_type_weights.csv", "GamerType")

# Reward weights for each action by gamer type
weights = [[0] * len(GamerType) for _ in range(len(Action))]

# Calculate weights using weighted average
for i in range(len(weights)):
    for j in range(len(weights[i])):
        total = 0
        count = 0
        for k in range(12):
            if (action_weights[i][k] != 0):
                total += action_weights[i][k] * gamer_type_weights[j][k]
                count += 1  
        weights[i][j] = round(total / count, 2) if count > 0 else 0

# Test code
if __name__ == '__main__':
    # print("Action weights:")
    # for action_name in Action.__members__:
    #     action_enum_member = Action[action_name]
    #     print(f"{action_name}: {action_weights[action_enum_member.value]}")

    # print(f"\nAction weights for leveling: {action_weights[Action.LEVEL.value]}")

    # print("Gamer type weights:")
    # for gamer_type_name in GamerType.__members__:
    #     gamer_type_enum_member = GamerType[gamer_type_name]
    #     print(f"{gamer_type_name}: {gamer_type_weights[gamer_type_enum_member.value]}")

    # print(f"\nGamer type weights for Acrobat: {gamer_type_weights[GamerType.Acrobat.value]}")

    # Print reward weight matrix for actions by gamer type
    max_action_name_length = max(len(action_name) for action_name in Action.__members__)
    for i in range(len(Action)):
        padded_action_name = Action(i).name.ljust(max_action_name_length)
        formatted_weights = [f"{weight:5.2f}" for weight in weights[i]]
        weights_str = " ".join(formatted_weights)
        print(f"{padded_action_name} {weights_str}")