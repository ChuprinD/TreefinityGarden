

from objects.achievement import Achievement


class Player:
    def __init__(self, name, garden):
        self.name = name
        self.garden = garden

        self.skins = {'1': [True, lambda: True], '2': [True, lambda: True], '3': [True, lambda: True],
                      '4': [False, lambda: self.unlock_tree4()], '5': [False, lambda: self.unlock_tree5()], '6': [False, lambda: self.unlock_tree6()],
                      '7': [False, lambda: self.unlock_tree7()], '8': [False, lambda: self.unlock_tree8()], '9': [False, lambda: self.unlock_tree9()]}

        self.all_achievements = []
        self.number_achievements = 9
        for i in range(self.number_achievements):
            achievement = Achievement(is_it_unlock=self.skins[str(i + 1)][0], condition=self.skins[str(i + 1)][1])
            self.all_achievements.append(achievement)

    def check_all_achievements(self, root, call_ids):
        for i, achievement in enumerate(self.all_achievements):
            self.skins[str(i + 1)][0] = achievement.check_condition()

        call_id = root.after(500, self.check_all_achievements, root, call_ids)
        call_ids.append(call_id)

    def unlock_tree4(self):
        if self.garden.day_counter == 5:
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
        if self.garden.number_felled_trees == 5:
            return True
        return False

    def unlock_tree8(self):
        if self.garden.number_planted_trees == 10:
            return True
        return False

    def unlock_tree9(self):
        if self.garden.day_counter == 50:
            return True
        return False

