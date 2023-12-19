def set_tree_to_file(data, file_name):
    with open(file_name, 'w') as file:
        file.write('tree\n')
        for key, value in data.items():
            file.write(f'{key}: {value}\n')


def get_tree_from_file(file):
    result_dict = {}
    for line in file:
        key, value = line.strip().split(': ')
        if key == 'branch_angle':
            value = value[1:-1]
            value = [int(num) for num in value.split(",")]
        elif key == 'branch_length_coefficient':
            value = float(value)
        elif key == 'max_branch_thickness':
            value = int(value)
        elif key == 'color_function_name':
            value = str(value)

        result_dict[key] = value

    return result_dict


def set_player_to_file(player_data, garden_data, trees_data, file_name):
    with open(file_name, 'w') as file:
        file.write('player\n')
        for key, value in player_data.items():
            file.write(f'{key}: {value}\n')

        file.write('garden\n')
        for key, value in garden_data.items():
            file.write(f'{key}: {value}\n')

        for i in range(len(trees_data)):
            file.write('tree' + str(trees_data[i]['pos']) + '\n')
            for key, value in trees_data[i].items():
                file.write(f'{key}: {value}\n')


def set_player_default_file(file_name):
    with open(file_name, 'w') as file:
        file.write('player\n')
        file.write('name: Bob\n')
        file.write('skins: [4, 5, 6, 7, 8, 9]\n')

        file.write('garden\n')
        file.write('day_counter: 0\n')
        file.write('cur_season: 0\n')
        file.write('number_planted_trees: 0\n')
        file.write('number_felled_trees: 0\n')


def get_player_from_file(file):
    result_dict = {}
    cur_player = {}
    while True:
        line = file.readline().strip()
        if line == 'garden' or not line:
            break

        key, value = line.split(': ')
        if key == 'skins':
            value = value[1:-1]
            if len(value) != 0:
                value = [int(skin) for skin in value.split(',')]
            else:
                value = []

        cur_player[key] = value

    result_dict['player'] = cur_player


    cur_garden = {}
    while True:
        line = file.readline().strip()
        if line[:-1] == 'tree' or not line:
            break

        key, value = line.split(': ')
        if key == 'day_counter' or key == 'cur_season' or key == 'number_planted_trees' or key == 'number_felled_trees':
            value = int(value)

        cur_garden[key] = value

    result_dict['garden'] = cur_garden


    trees = []
    while True:
        if not line:
            break

        if line[:-1] == 'tree':
            cur_tree = {}
            while True:
                current_position = file.tell()
                line = file.readline().strip()
                if line[:-1] == 'tree' or not line:
                    file.seek(current_position)
                    break

                key, value = line.split(': ')
                if key == 'pos' or key == 'trunk_length' or key == 'max_recursion_depth' or key == 'max_branch_thickness':
                    value = int(value)
                elif key == 'branch_length_coefficient':
                    value = float(value)
                elif key == 'branch_angle':
                    value = value[1:-1]
                    value = [int(num) for num in value.split(',')]

                cur_tree[key] = value

            trees.append(cur_tree)

        line = file.readline().strip()

    result_dict['trees'] = trees
    return result_dict


def get_data_from_file(file_name) -> dict:
    with open(file_name, 'r') as file:
        object_type = file.readline().strip()
        if object_type == 'tree':
            result_dict = get_tree_from_file(file).copy()
        elif object_type == 'player':
            result_dict = get_player_from_file(file).copy()

    return result_dict
