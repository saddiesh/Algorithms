from Maze import Maze
from robot import Robot
from Search import Search


if __name__ == "__main__":
    mazeshape=(8,11)
    start=(4,5)
    end=(0,10)
    walls=[(4,3),(4,4),(3,4),(2,4),(2,5),(2,6),(2,7),(3,7),(4,7),(5,7),(5,6)]

    maze = Maze(walls,mazeshape,end)
    robot = Robot()
    search = Search(maze, robot, start)
    search.a_star()
    print(search.backtrack_path())
    # print(search.cost_all)