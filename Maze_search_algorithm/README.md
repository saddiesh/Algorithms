# Search algorithm in maze problem

## Problem description

  We consider a maze under a **windy condition** as shown in the following figure. 

><div align=center><img width="550" height="400" src="https://github.com/saddiesh/Algorithms/blob/master/Maze_search_algorithm/displayed_results/Initial_Maze.png"/>  
  
  We assume that the wind comes from the south and **the cost of one step** for the agent is defined as follows: 

         **1**  for moving northward; 
         **2**  for moving eastward or westward; 
         **3**  for moving southward.      
         
  We assume that the square labeled with **0** is the **starting square**, 
  and the **top right** is the **goal square** and all **dark-shaded** squares are **obstacles**.

  For the best-first search algorithms (Greedy or A∗), we use a modified **Manhattan distance** as the heuristic function h(n)by considering the windy situation.   
  For example, for the start node, the agent has to move at least 3 steps eastward and 3 steps northward in order to reach the goal. 
  Therefore, we have h(n) = 3 ∗ 2 + 3 ∗ 1 = 9 at the start node.
  
  ## Result Formats
  Two kinds of results can be shown:  
  The first one is showing the expanding results in order:
><div align=center><img width="350" height="200" src="https://github.com/saddiesh/Algorithms/blob/master/Maze_search_algorithm/displayed_results/Expanding.png"/>  
  The second one is showing the expanding order as well as the solution path:  
><div align=center><img width="350" height="200" src="https://github.com/saddiesh/Algorithms/blob/master/Maze_search_algorithm/displayed_results/Path_solution.png"/>  
  
  ## Results of BFS, DFS, UCS, Greedy, A* algorithms
  In the visualize module, the results of every step will be saved as images and a gif can be generated showing the whole process.
 >A* algorithm result:
 >><div align=center><img width="550" height="400" src="https://github.com/saddiesh/Algorithms/blob/master/Maze_search_algorithm/displayed_results/Astar_result.gif"/>  
 >Greedy algorithm result:
 >><div align=center><img width="550" height="400" src="https://github.com/saddiesh/Algorithms/blob/master/Maze_search_algorithm/displayed_results/Greedy_result.gif"/>  
 >UCS algorithm result:
 >><div align=center><img width="550" height="400" src="https://github.com/saddiesh/Algorithms/blob/master/Maze_search_algorithm/displayed_results/UCS_result.gif"/>  
 >BFS algorithm result:
 >><div align=center><img width="550" height="400" src="https://github.com/saddiesh/Algorithms/blob/master/Maze_search_algorithm/displayed_results/BFS_result.gif"/>  
 >DFS algorithm result:
 >><div align=center><img width="550" height="400" src="https://github.com/saddiesh/Algorithms/blob/master/Maze_search_algorithm/displayed_results/DFS_result.gif"/>  
