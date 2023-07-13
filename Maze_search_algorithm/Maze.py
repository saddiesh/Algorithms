class Maze(object):
    def __init__(self, walls, shape, end):
        self.shape = shape
        self.walls = walls
        self.end = end

    def Manhattan_dist_to_end(self, cur_loc):
        ycos = 2 * abs(cur_loc[1] - self.end[1])
        if cur_loc[0] >= self.end[0]:
            xcos = cur_loc[0] - self.end[0]
        else:
            xcos = 3 * (self.end[0] - cur_loc[0])
        cost = ycos + xcos
        return cost

    def pos_is_valid(self, loc):
        x,y = loc
        r, c = self.shape
        if  0<=x<r and 0<=y<c:
            return True
        return False
