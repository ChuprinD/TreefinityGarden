from src.objects.achievement import Achievement
from src.objects.tree import Tree
from src.utilities.json import get_data_from_file, set_player_to_file


class Player:
    def __init__(self, name, garden):
        self.name = name
        self.garden = garden

        self.skins = {'4': [False, lambda: self.unlock_tree4()], '5': [False, lambda: self.unlock_tree5()], '6': [False, lambda: self.unlock_tree6()],
                      '7': [False, lambda: self.unlock_tree7()], '8': [False, lambda: self.unlock_tree8()], '9': [False, lambda: self.unlock_tree9()]}

        self.all_achievements = []
        self.number_achievements = len(self.skins)
        for key, value in self.skins.items():
            achievement = Achievement(is_it_unlock=value[0], condition=value[1], unlocked_tree=key)
            self.all_achievements.append(achievement)

    def save_player(self):
        cur_skins = []
        for key in self.skins.keys():
            if not self.skins[key][0]:
                cur_skins.append(int(key))

        player_data = {'name': self.name, 'skins': cur_skins}

        garden_data = {'day_counter': self.garden.day_counter, 'cur_season': self.garden.cur_season,
                       'number_planted_trees': self.garden.number_planted_trees, 'number_felled_trees': self.garden.number_felled_trees}

        trees_data = []
        for i, tree in enumerate(self.garden.trees):
            if tree is not None:
                cur_tree = {'pos': i + 1, 'trunk_length': tree.trunk_length, 'max_recursion_depth': tree.max_recursion_depth, 'branch_length_coefficient': tree.branch_length_coefficient,
                            'branch_angle': tree.branch_angle, 'max_branch_thickness': tree.max_branch_thickness, 'color_function_name': tree.color_function_name}
                trees_data.append(cur_tree)

        set_player_to_file(player_data, garden_data, trees_data, 'resources/players/player.txt')

    def load_player(self):
        data = get_data_from_file('resources/players/player.txt')
        player_data = data['player']
        self.name = player_data['name']
        for achievement in self.all_achievements:
            is_it_locked = int(achievement.unlocked_tree) in player_data['skins']
            achievement.is_it_unlock = not is_it_locked
            self.skins[achievement.unlocked_tree][0] = not is_it_locked



        garden_data = data['garden'].copy()
        self.garden.day_counter = garden_data['day_counter']
        self.garden.cur_season = garden_data['cur_season']
        self.garden.number_planted_trees = garden_data['number_planted_trees']
        self.garden.number_felled_trees = garden_data['number_felled_trees']

        self.garden.trees = [None] * self.garden.max_number_trees
        trees_data = data['trees'].copy()
        if len(trees_data) != 0:
            for tree in trees_data:
                cur_tree = Tree(self.garden.canvas, pos=self.garden.trees_pos[tree['pos'] - 1], trunk_length=tree['trunk_length'], max_recursion_depth=tree['max_recursion_depth'],
                                branch_length_coefficient=tree['branch_length_coefficient'], branch_angle=tree['branch_angle'], max_branch_thickness=tree['max_branch_thickness'],
                                color_function_name=tree['color_function_name'])
                self.garden.trees[tree['pos'] - 1] = cur_tree

    def check_all_achievements(self, root, call_ids):
        for achievement in self.all_achievements:
            self.skins[achievement.unlocked_tree][0] = achievement.check_condition()

        call_id = root.after(500, self.check_all_achievements, root, call_ids)
        call_ids.append(call_id)

    def unlock_tree4(self):
        if self.garden.day_counter >= 5:
            return True
        return False

    def unlock_tree5(self):
        if self.garden.seasons[self.garden.cur_season] == 'Winter':
            return True
        return False

    def unlock_tree6(self):
        if self.garden.get_first_free_position() == -1:
            return True
        return False

    def unlock_tree7(self):
        if self.garden.number_felled_trees >= 5:
            return True
        return False

    def unlock_tree8(self):
        if self.garden.number_planted_trees >= 10:
            return True
        return False

    def unlock_tree9(self):
        if self.garden.day_counter >= 50:
            return True
        return False
