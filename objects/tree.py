import math
from tkinter import messagebox

from utilities.color import get_coloring_by_name
from utilities.math import linear_interpolation
from utilities.json import get_data_from_file


class Tree:
    def __init__(self, canvas, pos=(0, 0), trunk_length=150, trunk_angle=90, branch_angle=(30, 30),
                 branch_length_coefficient=0.7,
                 max_recursion_depth=7, min_branch_thickness=1, max_branch_thickness=4,
                 color_function_name='default_coloring'):
        self.canvas = canvas
        self.pos = pos
        self.trunk_length = trunk_length
        self.trunk_angle = trunk_angle
        self.branch_angle = branch_angle
        self.branch_length_coefficient = branch_length_coefficient
        self.max_recursion_depth = max_recursion_depth
        self.min_branch_thickness = min_branch_thickness
        self.max_branch_thickness = max_branch_thickness
        self.absolut_max_branch_thickness = 20
        self.color_function_name = color_function_name
        self.gap_between_tree_hit_box = 4
        self.trunk_hit_box = []
        self.hit_box = [[self.canvas.winfo_reqwidth(), self.canvas.winfo_reqheight()], [0, 0]]

    def generate_tree(self, pos, angle, length, depth, to_draw):
        if depth:
            new_pos = [pos[0] + int(math.cos(math.radians(angle)) * length),
                       pos[1] - int(math.sin(math.radians(angle)) * length)]

            if to_draw:
                self.canvas.create_line(pos[0], pos[1], new_pos[0], new_pos[1],
                                        # here I use linear interpolation so that the thickness of the branches depends
                                        # on the depth of the recursion. [min_recursion_depth, min_branch_thickness] and
                                        # [min_recursion_depth, max_branch_thickness], min_recursion_depth = 1
                                        width=linear_interpolation(depth, 1, max(self.min_branch_thickness, self.max_branch_thickness - self.max_recursion_depth),
                                                                   self.max_recursion_depth, self.max_branch_thickness),
                                        fill=get_coloring_by_name(self.color_function_name)(depth,
                                                                                            self.max_recursion_depth))

            length *= self.branch_length_coefficient

            if not to_draw:
                self.hit_box = [
                    [min(self.hit_box[0][0], pos[0], new_pos[0]), min(self.hit_box[0][1], pos[1], new_pos[1])],
                    [max(self.hit_box[1][0], pos[0], new_pos[0]), max(self.hit_box[1][1], pos[1], new_pos[1])]]

            self.generate_tree(new_pos, angle - self.branch_angle[0], length, depth - 1, to_draw)
            self.generate_tree(new_pos, angle + self.branch_angle[1], length, depth - 1, to_draw)

    def draw(self):
        self.update_trunk_hit_box()
        self.hit_box = [[self.canvas.winfo_reqwidth(), self.canvas.winfo_reqheight()], [0, 0]]
        if self.check_tree_visibility():
            self.generate_tree(pos=self.get_tree_coordinates(), angle=self.trunk_angle, length=self.trunk_length,
                               depth=self.max_recursion_depth, to_draw=True)

    def increase_trunk_length(self) -> bool:
        self.trunk_length += 10
        if not self.check_tree_visibility():
            self.trunk_length -= 10
            return False

        return True

    def increase_max_recursion_depth(self) -> bool:
        self.max_recursion_depth += 1
        if not self.check_tree_visibility():
            self.max_recursion_depth -= 1
            return False

        return True

    def change_branch_angle(self) -> bool:
        self.branch_angle = (self.branch_angle[0] + 10, self.branch_angle[1] - 5)
        if not self.check_tree_visibility():
            self.branch_angle = (self.branch_angle[0] - 10, self.branch_angle[1] + 5)
            return False

        return True

    def load_tree_from_json(self, file_name):
        loaded_data = get_data_from_file('./trees/' + file_name + '.txt')

        self.trunk_length = loaded_data['trunk_length']
        self.branch_length_coefficient = loaded_data['branch_length_coefficient']
        self.max_branch_thickness = loaded_data['max_branch_thickness']
        self.max_recursion_depth = loaded_data['max_recursion_depth']
        self.branch_angle = loaded_data['branch_angle']
        self.max_branch_thickness = loaded_data['max_branch_thickness']
        self.color_function_name = loaded_data['color_function_name']

    def check_overlapping_hix_box(self, x, y) -> bool:
        if (self.trunk_hit_box[0][0] <= x <= self.trunk_hit_box[1][0] and
                self.trunk_hit_box[0][1] <= y <= self.trunk_hit_box[1][1]):
            return True
        return False

    def update_trunk_hit_box(self):
        coords_tree = self.get_tree_coordinates()

        if self.max_branch_thickness < self.absolut_max_branch_thickness:
            self.trunk_hit_box = [
                [coords_tree[0] - self.absolut_max_branch_thickness / 2 - self.gap_between_tree_hit_box,
                 coords_tree[1] - self.trunk_length - self.gap_between_tree_hit_box],
                [coords_tree[0] + self.absolut_max_branch_thickness / 2 + self.gap_between_tree_hit_box,
                 coords_tree[1] + self.gap_between_tree_hit_box]]
        else:
            self.trunk_hit_box = [[coords_tree[0] - self.max_branch_thickness / 2 - self.gap_between_tree_hit_box,
                                   coords_tree[1] - self.trunk_length - self.gap_between_tree_hit_box],
                                  [coords_tree[0] + self.max_branch_thickness / 2 + self.gap_between_tree_hit_box,
                                   coords_tree[1] + self.gap_between_tree_hit_box]]

    def get_tree_coordinates(self):
        return self.pos[0] * self.canvas.winfo_reqwidth(), self.pos[1] * self.canvas.winfo_reqheight()

    def check_tree_visibility(self):
        self.generate_tree(pos=self.get_tree_coordinates(), angle=self.trunk_angle, length=self.trunk_length,
                           depth=self.max_recursion_depth, to_draw=False)

        if (0 <= self.hit_box[0][0] and self.hit_box[1][0] <= self.canvas.winfo_reqwidth() and
            self.canvas.winfo_reqheight() // 6 <= self.hit_box[0][1] and self.hit_box[1][1] <= self.canvas.winfo_reqheight()):
            return True

        messagebox.showinfo("Warning", "Tree is bigger than screen")
        return False