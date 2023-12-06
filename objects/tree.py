import math
from utilities.color import get_coloring_by_name
from utilities.math import linear_interpolation
from utilities.json import get_data_from_file


class Tree:
    def __init__(self, canvas, pos, trunk_length=150, trunk_angle=90, branch_angle=(30, 30), branch_length_coefficient=0.7,
                 max_recursion_depth=7, min_branch_thickness=1, max_branch_thickness=4, color_function_name='default_coloring'):
        self.canvas = canvas
        self.pos = pos
        self.trunk_length = trunk_length
        self.trunk_angle = trunk_angle
        self.branch_angle = branch_angle
        self.branch_length_coefficient = branch_length_coefficient
        self.max_recursion_depth = max_recursion_depth
        self.min_branch_thickness = min_branch_thickness
        self.max_branch_thickness = max_branch_thickness
        self.color_function_name = color_function_name
        self.hit_box = ()
        self.update_hit_box()

    def draw_tree(self, pos, angle, length, depth):
        if depth:
            new_pos = [pos[0] + int(math.cos(math.radians(angle)) * length),
                       pos[1] - int(math.sin(math.radians(angle)) * length)]

            self.canvas.create_line(pos[0], pos[1], new_pos[0], new_pos[1],
                                    # here I use linear interpolation so that the thickness of the branches depends
                                    # on the depth of the recursion. [min_recursion_depth, min_branch_thickness] and
                                    # [min_recursion_depth, max_branch_thickness], min_recursion_depth = 1
                                    width=linear_interpolation(depth, 1, self.min_branch_thickness, self.max_recursion_depth, self.max_branch_thickness),
                                    fill=get_coloring_by_name(self.color_function_name)(depth, self.max_recursion_depth))

            length *= self.branch_length_coefficient

            self.draw_tree(new_pos, angle - self.branch_angle[0], length, depth - 1)
            self.draw_tree(new_pos, angle + self.branch_angle[1], length, depth - 1)

    def draw(self):
        self.draw_tree(self.pos, self.trunk_angle, self.trunk_length, self.max_recursion_depth)

    def increase_trunk_length(self):
        self.trunk_length += 10
        self.update_hit_box()

    def increase_max_recursion_depth(self):
        self.max_recursion_depth += 1

    def change_branch_angle(self):
        self.branch_angle = (self.branch_angle[0] + 10, self.branch_angle[1] - 5)

    def load_tree_from_json(self, file_name):
        loaded_data = get_data_from_file('../trees/' + file_name + '.txt')

        self.trunk_length = loaded_data['trunk_length']
        self.branch_length_coefficient = loaded_data['branch_length_coefficient']
        self.max_branch_thickness = loaded_data['max_branch_thickness']
        self.max_recursion_depth = loaded_data['max_recursion_depth']
        self.branch_angle = loaded_data['branch_angle']
        self.max_branch_thickness = loaded_data['max_branch_thickness']
        self.color_function_name = loaded_data['color_function_name']

        self.update_hit_box()

    def check_overlapping_hix_box(self, x, y) -> bool:
        if (self.hit_box[0] <= x <= self.hit_box[2] and
                self.hit_box[1] <= y <= self.hit_box[3]):
            return True
        return False

    def update_hit_box(self):
        self.hit_box = (self.pos[0] - self.max_branch_thickness / 2 - 4,
                        self.pos[1] - self.trunk_length - 4,
                        self.pos[0] + self.max_branch_thickness / 2 + 4,
                        self.pos[1] + 4)