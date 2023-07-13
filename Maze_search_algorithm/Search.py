
class Search(object):

    def __init__(self, maze, robot, start):
        self.robot = robot
        self.maze = maze
        self.start = start
        self.visited = []
        self.options = [(start,0)]
        self.father_node = {}
        self.acts = [(-1, 0), (0, 1), (0, -1), (1, 0)]
        self.g_cost = {start:0}

    def a_star(self):
        #
        while len(self.options)>0:
            # choose a grid option with lowest cost
            self.options.sort(key = lambda x: x[1])
            cur_loc, _ = self.options.pop(0)
            cur_g_cost = self.g_cost[cur_loc]

            # loop action
            for act in self.acts:
                xy = self.robot.take_action(cur_loc, act) #(x,y)

                # if reach end, return
                if xy == self.maze.end:
                    self.father_node[xy] = cur_loc
                    return

                # else if position is a new valid grid
                if self.maze.pos_is_valid(xy) and (xy not in self.visited) \
                        and (xy not in self.maze.walls):
                    self.visited.append(xy)
                    # print(xy, ":  ", cur_cost, self.robot.act2cost[act], self.maze.Manhattan_dist_to_end(xy))
                    g_cost = cur_g_cost + self.robot.act2cost[act]
                    self.g_cost[xy] = g_cost
                    cost = g_cost + self.maze.Manhattan_dist_to_end(xy)
                    # self.cost_all[xy] = cost
                    self.options.append((xy,cost))
                    self.father_node[xy] = cur_loc

        return

    def backtrack_path(self):

        pos = self.maze.end
        shortest_path = [pos]
        while pos!=self.start:
            next_pos = self.father_node[pos]
            shortest_path.append(next_pos)
            pos = next_pos

        return shortest_path
