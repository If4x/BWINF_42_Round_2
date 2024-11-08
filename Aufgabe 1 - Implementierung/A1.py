# 42. Bundeswettbewerb Informatik Runde 2

# Aufgabe 1
# Bearbeiter dieser Aufgabe: Imanuel Fehse

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import seaborn as sns
from datetime import datetime
import os as os

# create colormap that is being used
custom_cmap = ListedColormap(['blue', 'white'])


# get current time
def get_time():
    return datetime.now().strftime("%d_%B_time_%H_%M_%S")


class Schoolyard:
    def __init__(self, filename):
        # setup
        self.filename = filename
        self.dimensions = []
        self.schoolyard = []
        self.total_leafs = 0
        self.create_schoolyard(filename)
        self.final_field = []
        self.final_area = []
        self.final_arrangement = None
        self.target_field_blow = []
        self.movements = []

        self.number_of_walls = []
        self.get_walls()

    def create_schoolyard(self, file):
        f = open(file, "r")
        raw_data = f.read().splitlines()
        f.close()
        self.dimensions.append(int(raw_data[0].split(" ")[0]))
        self.dimensions.append(int(raw_data[0].split(" ")[1]))
        for y in range(self.dimensions[0]):
            c_y = []
            for x in range(self.dimensions[1]):
                if raw_data[y + 1][x] == "1":
                    c_y.append([1, 100])
                    self.total_leafs += 100
                else:
                    c_y.append([0, 0, [4, [1, 1, 1, 1]]])
            self.schoolyard.append(c_y)

    def plot_schoolyard(self, folder):
        schoolyard_plot = []
        for y in range(self.dimensions[0]):
            c_y = []
            for x in range(self.dimensions[1]):
                c_y.append(self.schoolyard[y][x][0])
            schoolyard_plot.append(c_y)
        leaf_plot = []
        for y in range(self.dimensions[0]):
            c_y = []
            for x in range(self.dimensions[1]):
                c_y.append(float(self.schoolyard[y][x][1]))
            leaf_plot.append(c_y)
        # create map from schoolyard layout
        sns.heatmap(schoolyard_plot, cbar=False, linewidths=0.5, linecolor="black", cmap=custom_cmap)
        plt.axis("off")
        plt.title(self.filename + " - Schoolyard" + " - " + get_time())
        # save graph in folder with 300 dpi
        plt.savefig(folder + "/schoolyard.png", dpi=300)
        # show graph
        plt.show()

        # create heatmap from leaf count
        sns.heatmap(leaf_plot, annot=True, fmt=".1f", cbar=True, linewidths=0.5, linecolor="white")
        plt.axis("off")
        plt.title(self.filename + " - heatmap" + " - " + get_time())
        # save graph in folder with 300 dpi
        plt.savefig(folder + "/heatmap.png", dpi=300)
        # show graph
        plt.show()

    def get_walls(self):
        def above(c_x, c_y):
            if self.schoolyard[c_y - 1][c_x][0] == 0:
                return True
            else:
                return False

        def below(c_x, c_y):
            if self.schoolyard[c_y + 1][c_x][0] == 0:
                return True
            else:
                return False

        def left(c_x, c_y):
            if self.schoolyard[c_y][c_x - 1][0] == 0:
                return True
            else:
                return False

        def right(c_x, c_y):
            if self.schoolyard[c_y][c_x + 1][0] == 0:
                return True
            else:
                return False

        for y in range(len(self.schoolyard)):
            for x in range(len(self.schoolyard[y])):
                wall_positions = [0, 0, 0, 0]
                # if field is part of schoolyard
                c_walls = 0
                if self.schoolyard[y][x][0] == 1:
                    # if in first line
                    if y == 0:
                        c_walls += 1
                        wall_positions[0] = 1
                        if below(x, y):
                            c_walls += 1
                            wall_positions[2] = 1

                    # if in last line
                    elif y == self.dimensions[1] - 1:
                        c_walls += 1
                        wall_positions[2] = 1
                        if above(x, y):
                            c_walls += 1
                            wall_positions[0] = 1

                    # all fields between
                    else:
                        if above(x, y):
                            c_walls += 1
                            wall_positions[0] = 1
                        if below(x, y):
                            c_walls += 1
                            wall_positions[2] = 1

                    # if in first column
                    if x == 0:
                        c_walls += 1
                        wall_positions[3] = 1
                        if right(x, y):
                            c_walls += 1
                            wall_positions[1] = 1
                    # if in last column
                    elif x == self.dimensions[0] - 1:
                        c_walls += 1
                        wall_positions[1] = 1
                        if left(x, y):
                            c_walls += 1
                            wall_positions[3] = 1
                    # all fields between
                    else:
                        if left(x, y):
                            c_walls += 1
                            wall_positions[3] = 1
                        if right(x, y):
                            c_walls += 1
                            wall_positions[1] = 1

                    self.schoolyard[y][x].append([c_walls, wall_positions])

    def strategy(self):
        # blow everything downwards
        y_skip = 0
        # check if a line (from downwards) is all walls
        for y in range(self.dimensions[1]-1):
            c_line = []
            for x in range(self.dimensions[0]):
                c_line.append(self.schoolyard[self.dimensions[1]-y-1][x][0])
            # count walls in line
            num_walls = c_line.count(0)
            if num_walls == self.dimensions[0]:
                y_skip += 1
            else:
                # check if two not walls are next to each other
                two_next_to_each_other = False
                for x in range(self.dimensions[0]-1):
                    if c_line[x] == 1 and c_line[x+1] == 1:
                        two_next_to_each_other = True
                        break
                    else:
                        pass
                if two_next_to_each_other:
                    break
                else:
                    y_skip += 1
                    # clear fields that are in the line
                    for x in range(self.dimensions[0]):
                        if c_line[x] == 1:
                            # blow upwards
                            self.blow(self.dimensions[1]-y-1, x, 0)

        for y in range(self.dimensions[1]-(1 + y_skip)):
            for x in range(self.dimensions[0]):
                # if field is part of the schoolyard
                if self.schoolyard[y][x][0] == 1:
                    # check if field has a wall downwards
                    if self.schoolyard[y][x][2][1][2] == 1:
                        # check if there is a way to the right
                        found_way_right = False
                        found_way_left = False
                        # while no way was found
                        move_right = 0
                        move_left = 0
                        move_up_right = 0
                        move_up_left = 0
                        move_list_right = []
                        move_list_left = []
                        fail_right = False
                        fail_left = False

                        # check for way to the right
                        while not found_way_right:
                            # check if there is no wall downwards and last movement wasn't upwards
                            if self.schoolyard[y+move_up_right][x+move_right][2][1][2] == 0 and move_list_right[-1] != "up":
                                # as long as you can move down
                                while self.schoolyard[y+move_up_right][x+move_right][2][1][2] == 0:
                                    move_up_right += 1
                                    move_list_right.append("down")
                                    # check if move ended up lower as starting field
                                    if move_up_right > 0:
                                        found_way_right = True
                                        break
                            # check if there is no wall to the right
                            elif self.schoolyard[y+move_up_right][x+move_right][2][1][1] == 0:
                                move_right += 1
                                move_list_right.append("right")
                            # if there is no wall upwards
                            elif self.schoolyard[y+move_up_right][x+move_right][2][1][0] == 0:
                                move_up_right -= 1
                                move_list_right.append("up")
                            else:
                                fail_right = True
                                break
                            if fail_right:
                                break

                        # check for way to the left
                        while not found_way_left:
                            # check if there is no wall downwards and last movement wasn't upwards
                            if self.schoolyard[y+move_up_left][x+move_left][2][1][2] == 0 and move_list_left[-1] != "up":
                                # as long as you can move down
                                while self.schoolyard[y+move_up_left][x+move_left][2][1][2] == 0:
                                    move_up_left += 1
                                    move_list_left.append("down")
                                    # check if move ended up lower as starting field
                                    if move_up_left > 0:
                                        found_way_left = True
                                        break
                            # check if there is no wall to the left
                            elif self.schoolyard[y+move_up_left][x+move_left][2][1][3] == 0:
                                move_left -= 1
                                move_list_left.append("left")
                            # if there is no wall upwards
                            elif self.schoolyard[y+move_up_left][x+move_left][2][1][0] == 0:
                                move_up_left -= 1
                                move_list_left.append("up")
                            else:
                                failLleft = True
                                break
                            if fail_left:
                                break


                        """EXECUTION"""
                        def execute_right():
                            execute_x_addition = 0
                            execute_y_addition = 0
                            for move in move_list_right:
                                if move == "up":
                                    # blow upwards
                                    self.blow(x + execute_x_addition, y + execute_y_addition, 0)
                                    # move next execution up
                                    execute_y_addition -= 1
                                elif move == "right":
                                    # blow right
                                    self.blow(x + execute_x_addition, y + execute_y_addition, 1)
                                    # move next execution right
                                    execute_x_addition += 1
                                elif move == "down":
                                    # blow downwards
                                    self.blow(x + execute_x_addition, y + execute_y_addition, 2)
                                    # move next execution down
                                    execute_y_addition += 1

                        def execute_left():
                            execute_x_addition = 0
                            execute_y_addition = 0
                            for move in move_list_left:
                                if move == "up":
                                    # blow upwards
                                    self.blow(x + execute_x_addition, y + execute_y_addition, 0)
                                    # move next execution up
                                    execute_y_addition -= 1
                                elif move == "left":
                                    # blow left
                                    self.blow(x + execute_x_addition, y + execute_y_addition, 3)
                                    # move next execution left
                                    execute_x_addition -= 1
                                elif move == "down":
                                    # blow downwards
                                    self.blow(x + execute_x_addition, y + execute_y_addition, 2)
                                    # move next execution down
                                    execute_y_addition += 1

                        # if a way to the right was found and a way to the left was found
                        if found_way_right and found_way_left:
                            # check which one is shorter
                            if len(move_list_right) <= len(move_list_left):
                                execute_right()
                            else:
                                execute_left()
                        # if only a way to the right was found
                        elif found_way_right:
                            execute_right()
                        # if only a way to the left was found
                        elif found_way_left:
                            execute_left()
                        # if no way was found
                        else:
                            break

                    # if field has no wall downwards, blow leafs downwards
                    else:
                        self.blow(x, y, 2)
        # concentrate all leaves underneath the final field
        x_final_field = self.final_field[0]
        for x in range(x_final_field):
            # if there is no wall to the right side of the field
            if self.schoolyard[self.dimensions[1] - 1 - y_skip][x][2][1][1] == 0:
                self.blow(x, self.dimensions[1] - 1 - y_skip, 1)
        for x in range(self.dimensions[0] - 1, x_final_field, -1):
            # if there is no wall to the left side of the field
            if self.schoolyard[self.dimensions[1] - 1 - y_skip][x][2][1][3] == 0:
                self.blow(x, self.dimensions[1] - 1 - y_skip, 3)

        # final blow functions
        def final_blow_0():
            self.blow(self.final_field[0] - 1, self.final_field[1], 2)
            self.blow(self.final_field[0] - 1, self.final_field[1] + 1, 1)
            self.blow(self.final_field[0], self.final_field[1] + 1, 0)

        def final_blow_1():
            self.blow(self.final_field[0], self.final_field[1] + 1, 3)
            self.blow(self.final_field[0] - 1, self.final_field[1] + 1, 0)
            self.blow(self.final_field[0] - 1, self.final_field[1], 1)

        def final_blow_2():
            self.blow(self.final_field[0] + 1, self.final_field[1], 2)
            self.blow(self.final_field[0] + 1, self.final_field[1] + 1, 3)
            self.blow(self.final_field[0], self.final_field[1] + 1, 0)

        def final_blow_3():
            self.blow(self.final_field[0], self.final_field[1] + 1, 1)
            self.blow(self.final_field[0] + 1, self.final_field[1] + 1, 0)
            self.blow(self.final_field[0] + 1, self.final_field[1], 3)

        def final_blow_4():
            self.blow(self.final_field[0], self.final_field[1] - 1, 1)
            self.blow(self.final_field[0] + 1, self.final_field[1] - 1, 2)
            self.blow(self.final_field[0] + 1, self.final_field[1], 3)

        def final_blow_5():
            self.blow(self.final_field[0] + 1, self.final_field[1], 0)
            self.blow(self.final_field[0] + 1, self.final_field[1] - 1, 3)
            self.blow(self.final_field[0], self.final_field[1] - 1, 2)

        def final_blow_6():
            self.blow(self.final_field[0], self.final_field[1] - 1, 3)
            self.blow(self.final_field[0] - 1, self.final_field[1] - 1, 2)
            self.blow(self.final_field[0] - 1, self.final_field[1], 1)

        def final_blow_7():
            self.blow(self.final_field[0] - 1, self.final_field[1], 0)
            self.blow(self.final_field[0] - 1, self.final_field[1] - 1, 1)
            self.blow(self.final_field[0], self.final_field[1] - 1, 2)

        # final blow process dependent on final arrangement
        if self.final_arrangement == 0:
            final_blow_0()
        elif self.final_arrangement == 1:
            final_blow_1()
        elif self.final_arrangement == 2:
            final_blow_2()
        elif self.final_arrangement == 3:
            final_blow_3()
        elif self.final_arrangement == 4:
            final_blow_4()
        elif self.final_arrangement == 5:
            final_blow_5()
        elif self.final_arrangement == 6:
            final_blow_6()
        elif self.final_arrangement == 7:
            final_blow_7()

        # if percentage of leafs in final field is less than 0.85, start correction process
        if (self.schoolyard[self.final_field[1]][self.final_field[0]][1] / self.total_leafs) < 0.85:
            if self.final_arrangement == 0:
                self.blow(self.final_field[0]+1, self.final_field[1], 3)
                final_blow_0()
            elif self.final_arrangement == 1:
                self.blow(self.final_field[0], self.final_field[1]-1, 3)
                final_blow_1()
            elif self.final_arrangement == 2:
                self.blow(self.final_field[0]-1, self.final_field[1], 1)
                final_blow_2()
            elif self.final_arrangement == 3:
                self.blow(self.final_field[0]-1, self.final_field[1]-1, 1)
                final_blow_3()
            elif self.final_arrangement == 4:
                self.blow(self.final_field[0], self.final_field[1]+1, 0)
                final_blow_4()
            elif self.final_arrangement == 5:
                self.blow(self.final_field[0]-1, self.final_field[1], 1)
                final_blow_5()
            elif self.final_arrangement == 6:
                self.blow(self.final_field[0], self.final_field[1]+1, 0)
                final_blow_6()
            elif self.final_arrangement == 7:
                self.blow(self.final_field[0]+1, self.final_field[1], 3)
                final_blow_7()

    def find_final_field(self):
        def get_final_field(c_x, c_y, final_arrangement):
            if final_arrangement == 0 or final_arrangement == 1:
                return [c_x + 1, c_y]
            elif final_arrangement == 2 or final_arrangement == 3:
                return [c_x, c_y]
            elif final_arrangement == 4 or final_arrangement == 5:
                return [c_x, c_y + 1]
            elif final_arrangement == 6 or final_arrangement == 7:
                return [c_x + 1, c_y + 1]
            else:
                print("invalid input")
        # constellations of possible arrangements
        possible_arrangements = [
            # 0
            [
                [1, ["?", 0, 0, "?"]], [1, [0, 0, 0, 0]],
                [1, [0, 0, "?", 1]], [1, [0, "?", "?", 0]]
            ],
            # 1
            [
                [1, ["?", 0, 0, "?"]], [1, [0, 0, 0, 0]],
                [1, [0, 0, 1, "?"]], [1, [0, "?", "?", 0]]
            ],
            # 2
            [
                [1, [0, 0, 0, 0]], [1, ["?", "?", 0, 0]],
                [1, [0, 0, "?", "?"]], [1, [0, 1, "?", 0]]
            ],
            # 3
            [
                [1, [0, 0, 0, 0]], [1, ["?", "?", 0, 0]],
                [1, [0, 0, "?", "?"]], [1, [0, "?", 1, 0]]
            ],

        ]

        # get all 2x2 areas
        areas = []
        for y in range(self.dimensions[1]-1):
            for x in range(self.dimensions[0]-1):
                # select 2x2 area
                c_area = []
                for a_y in range(2):
                    for a_x in range(2):
                        c_area.append(self.schoolyard[y+a_y][x+a_x])
                areas.append([x, y, c_area])

        # check if area is a possible arrangement
        possible_areas = []
        for raw_area in areas:
            sublist = raw_area[2]
            area = []
            for field in sublist:
                area.append([field[0], field[2][1]])

            # check if area is a possible arrangement
            for arrangement in possible_arrangements:
                valid_arrangement = True
                for field in range(4):
                    # if type of field of area is equal to the type of field of arrangement
                    if arrangement[field][0] != area[field][0]:
                        valid_arrangement = False
                        break
                    # check if walls are at the same positions
                    for wall in range(4):
                        # if wall can be anything
                        if arrangement[field][1][wall] == "?":
                            pass
                        # if wall is not at the same position
                        elif arrangement[field][1][wall] != area[field][1][wall]:
                            valid_arrangement = False
                            break
                # if one arrangement was found
                if valid_arrangement:
                    c_arrangement = possible_arrangements.index(arrangement)
                    possible_areas.append([raw_area, c_arrangement, get_final_field(raw_area[0], raw_area[1],
                                                                                    c_arrangement)])
        # select area with final field in the lowest line and leftmost column
        self.final_area = possible_areas[0]
        for possible_area in possible_areas:
            # if current area with final field is in a lower line or more left, set new final values
            if self.final_area[2][0] > possible_area[2][0] or self.final_area[2][1] < possible_area[2][1]:
                self.final_area = possible_area

            self.final_field = possible_area[2]
            self.final_arrangement = possible_area[1]

        # get final target field
        if self.final_arrangement == 0 or self.final_arrangement == 1:
            self.target_field_blow = [self.final_field[0]-1, self.final_field[1]+1]
        elif self.final_arrangement == 2 or self.final_arrangement == 3:
            self.target_field_blow = [self.final_field[0]+1, self.final_field[1]+1]
        elif self.final_arrangement == 4 or self.final_arrangement == 5:
            self.target_field_blow = [self.final_field[0]+1, self.final_field[1]-1]
        elif self.final_arrangement == 6 or self.final_arrangement == 7:
            self.target_field_blow = [self.final_field[0]-1, self.final_field[1]-1]

    def blow(self, x, y, direction):
        # upwards
        if direction == 0:
            walls_around_target = self.schoolyard[y - 1][x][2][1]

            # BLOW STAGE ONE
            # if there is a wall above target
            if walls_around_target[0] == 1:
                pass
            # if there is no wall above target
            else:
                self.movements.append([x, y, "up"])
                leafs_target_field = self.schoolyard[y-1][x][1]
                percentage_above_target = 0.1
                percentage_target_field = 0.9

                # transfer leafs from blow stage 1
                self.schoolyard[y-1][x][1] = leafs_target_field * percentage_target_field
                self.schoolyard[y-2][x][1] += leafs_target_field * percentage_above_target

            # BLOW STAGE TWO
            percentage_target_field = 0.8
            percentage_right_field = 0.1
            percentage_left_field = 0.1
            leafs_c_field = self.schoolyard[y][x][1]
            # if target has a wall left
            if walls_around_target[3] == 1:
                percentage_left_field = 0
                percentage_target_field += 0.1
            # if target has a wall right
            if walls_around_target[1] == 1:
                percentage_right_field = 0
                percentage_target_field += 0.1

            # transfer leafs from blow stage 2
            self.schoolyard[y][x][1] = 0
            self.schoolyard[y - 1][x][1] += leafs_c_field * percentage_target_field
            if walls_around_target[3] == 0:
                self.schoolyard[y - 1][x - 1][1] += leafs_c_field * percentage_left_field
            if walls_around_target[1] == 0:
                self.schoolyard[y - 1][x + 1][1] += leafs_c_field * percentage_right_field

        # downwards
        elif direction == 2:
            walls_around_target = self.schoolyard[y + 1][x][2][1]

            # BLOW STAGE One
            # if there is a wall below target
            if walls_around_target[2] == 1:
                pass
            else:
                self.movements.append([x, y, "down"])
                leafs_target_field = self.schoolyard[y+1][x][1]
                percentage_below_target = 0.1
                percentage_target_field = 0.9

                # transfer leafs from blow stage 1
                self.schoolyard[y+1][x][1] = leafs_target_field * percentage_target_field
                self.schoolyard[y+2][x][1] += leafs_target_field * percentage_below_target

            # BLOW STAGE TWO
            percentage_target_field = 0.8
            percentage_right_field = 0.1
            percentage_left_field = 0.1
            leafs_c_field = self.schoolyard[y][x][1]
            # if target has a wall left
            if walls_around_target[3] == 1:
                percentage_left_field = 0
                percentage_target_field += 0.1
            # if target has a wall right
            if walls_around_target[1] == 1:
                percentage_right_field = 0
                percentage_target_field += 0.1

            # transfer leafs from blow stage 2
            self.schoolyard[y][x][1] = 0
            self.schoolyard[y + 1][x][1] += leafs_c_field * percentage_target_field
            if walls_around_target[3] == 0:
                self.schoolyard[y + 1][x - 1][1] += leafs_c_field * percentage_left_field
            if walls_around_target[1] == 0:
                self.schoolyard[y + 1][x + 1][1] += leafs_c_field * percentage_right_field

        # left
        elif direction == 3:
            walls_around_target = self.schoolyard[y][x - 1][2][1]

            # BLOW STAGE ONE
            # if there is a wall left of target
            if walls_around_target[3] == 1:
                pass
            else:
                self.movements.append([x, y, "left"])
                leafs_target_field = self.schoolyard[y][x-1][1]
                percentage_left_of_target = 0.1
                percentage_target_field = 0.9

                # transfer leafs from blow stage 1
                self.schoolyard[y][x-1][1] = leafs_target_field * percentage_target_field
                self.schoolyard[y][x-2][1] += leafs_target_field * percentage_left_of_target

            # BLOW STAGE TWO
            percentage_target_field = 0.8
            percentage_above_field = 0.1
            percentage_below_field = 0.1
            leafs_c_field = self.schoolyard[y][x][1]
            # if target has a wall above
            if walls_around_target[0] == 1:
                percentage_above_field = 0
                percentage_target_field += 0.1
            # if target has a wall below
            if walls_around_target[2] == 1:
                percentage_below_field = 0
                percentage_target_field += 0.1

            # transfer leafs from blow stage 2
            self.schoolyard[y][x][1] = 0
            self.schoolyard[y][x - 1][1] += leafs_c_field * percentage_target_field
            if walls_around_target[0] == 0:
                self.schoolyard[y - 1][x - 1][1] += leafs_c_field * percentage_above_field
            if walls_around_target[2] == 0:
                self.schoolyard[y + 1][x - 1][1] += leafs_c_field * percentage_below_field

        # right
        elif direction == 1:
            walls_around_target = self.schoolyard[y][x + 1][2][1]

            # BLOW STAGE One
            # if there is a wall right of target
            if walls_around_target[1] == 1:
                pass
            else:
                self.movements.append([x, y, "right"])
                leafs_target_field = self.schoolyard[y][x+1][1]
                percentage_right_of_target = 0.1
                percentage_target_field = 0.9

                # transfer leafs from blow stage 1
                self.schoolyard[y][x+1][1] = leafs_target_field * percentage_target_field
                self.schoolyard[y][x+2][1] += leafs_target_field * percentage_right_of_target

            # BLOW STAGE TWO
            percentage_target_field = 0.8
            percentage_above_field = 0.1
            percentage_below_field = 0.1
            leafs_c_field = self.schoolyard[y][x][1]
            # if target has a wall above
            if walls_around_target[0] == 1:
                percentage_above_field = 0
                percentage_target_field += 0.1
            # if target has a wall below
            if walls_around_target[2] == 1:
                percentage_below_field = 0
                percentage_target_field += 0.1

            # transfer leafs from blow stage 2
            self.schoolyard[y][x][1] = 0
            self.schoolyard[y][x + 1][1] += leafs_c_field * percentage_target_field
            if walls_around_target[0] == 0:
                self.schoolyard[y - 1][x + 1][1] += leafs_c_field * percentage_above_field
            if walls_around_target[2] == 0:
                self.schoolyard[y + 1][x + 1][1] += leafs_c_field * percentage_below_field

        # invalid direction
        else:
            print("ERROR: Invalid direction")

    def save(self):
        # create a folder for the results in the "res" folder
        if not os.path.exists("res"):
            os.mkdir("res")
        folder = "res/" + get_time()
        if not os.path.exists(folder):
            os.mkdir(folder)
        # save
        # plots
        self.plot_schoolyard(folder)
        # movements and data
        f = open(folder + "/movements.txt", "w")
        # write movements as list to file
        f.write("final field:" + str(self.final_field) + "\n" +
                "final percentage:" + str(self.schoolyard[self.final_field[1]][self.final_field[0]][1]/self.total_leafs) + "\n" +
                "movements:\n" + str(self.movements))
        f.close()


# RUN
Test = Schoolyard("filename") # change filename to the name of the file
Test.find_final_field()
Test.strategy()
Test.save()

print(Test.total_leafs)
print(Test.final_arrangement)
print(Test.final_field)
print("final on field percentage", Test.schoolyard[Test.final_field[1]][Test.final_field[0]][1]/Test.total_leafs)
print("movements:", Test.movements)


