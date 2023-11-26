import math


class Tree:
    def __init__(self, canvas, pos, trunk_length, trunk_angle, branch_angle, branch_length_coefficient,
                 max_recursion_depth, min_branch_thickness, max_branch_thickness):
        self.canvas = canvas
        self.pos = pos
        self.trunk_length = trunk_length
        self.trunk_angle = trunk_angle
        self.branch_angle = branch_angle
        self.branch_length_coefficient = branch_length_coefficient
        self.max_recursion_depth = max_recursion_depth
        self.min_branch_thickness = min_branch_thickness
        self.max_branch_thickness = max_branch_thickness

    def draw_tree(self, pos, angle, length, depth):
        if depth:
            new_pos = [pos[0] + int(math.cos(math.radians(angle)) * length),
                       pos[1] - int(math.sin(math.radians(angle)) * length)]

            self.canvas.create_line(pos[0], pos[1], new_pos[0], new_pos[1],
                                    # here I use linear interpolation so that the thickness of the branches depends
                                    # on the depth of the recursion. [min_recursion_depth, min_branch_thickness] and
                                    # [min_recursion_depth, max_branch_thickness], min_recursion_depth = 1
                                    width=((depth - 1) * (self.max_branch_thickness - self.min_branch_thickness)) / (
                                                self.max_recursion_depth - 1) + 1)

            length *= self.branch_length_coefficient

            self.draw_tree(new_pos, angle - self.branch_angle[0], length, depth - 1)
            self.draw_tree(new_pos, angle + self.branch_angle[1], length, depth - 1)

    def draw(self):
        self.draw_tree(self.pos, self.trunk_angle, self.trunk_length, self.max_recursion_depth)

    def increase_trunk_length(self):
        self.trunk_length += 10
        self.draw()

    def increase_max_recursion_depth(self):
        self.max_recursion_depth += 1
        self.draw()

    def change_branch_angle(self):
        self.branch_angle = (self.branch_angle[0] + 10, self.branch_angle[1] - 5)
        self.draw()
