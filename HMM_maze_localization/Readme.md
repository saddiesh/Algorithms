# Localization algorithm using HMM in maze problem

## Problem description

We consider a maze under a **windy condition** as shown in the following figure. 
We assume that a robot aims to locate itself in the windy maze. The robot will perform two kinds of actions: **sensing** and **moving**.

><div align=center><img width="550" height="400" src="https://github.com/saddiesh/Algorithms/blob/master/HMM_maze_localization/initial_maze.png"/>


### **Sensing:**
  
  In a square, the robot will sense the four directions to see if there is an obstacle in this direction. We assume that the whole maze is surrounded by obstacles and the black squares are also obstacle. However, the sensing is not perfect. We assume that the robot can detect the obstacle with 90% if there is and might mistake an open square as a obstacle with 5%. The detections in all directions are done independently.
  
### **Moving:**
  
  In the windy situation, the robot can drift to the left or the right with probability 0.1. If the drifting direction is an obstacle, it will be bounced back to the original position. For example, in the square of left bottom, if the robot moves northward, it will reach the square to the north with 80% and reach the square to the east with 10% and be bounced back to the original position with 10%.


We assume that the robot initially stays in one open square, but it doesn’t know its exact location except that it knows that it can’t be in any obstacle square. Then the robot performs the following sequence of actions:
1. Sensing: (-,-,-,-)
2. Moving northward 
3. Sensing: (-,-,-,-)
4. Moving northward 
5. Sensing: (-,-,o,-) 
6. Moving northward 
7. Sensing: (-,-,-,-)
8. Moving eastward 
9. Sensing: (-,-,o,o)
10. Moving northward
11. Sensing: (-,-,o,-)
where (W,N,E,S) indicates the observation at Directions (Westward, Northward, Eastward, Southward), respectively. ”-” indicates no obstacle is observed and ”o” indicates an obstacle is observed.
You are expected to report the posterior probability of the current robot location at each square after each action. The prior probability at each square is shown as follows (1.30 means 1.30%)


### **Smoothing(Forward-Backward HMM):**

In the above, we focus on filtering and prediction in HMM. In the following, we aim to address smoothing in HMM. After all the 11 actions including 5 moves, the robot wants to perform smoothing to improve the estimation of all previous 5 locations.
We use Information Entropy 1 to measure the uncertainty of the location. For n possible locations, we have n probabilities pi, i = 1, 2, . . . , n. Then the location entropy is − 􏰀ni=1 pi log2 pi. The smaller the entropy is, the lower uncertainty the location is.

## Results:

A probability array is printed to show the result for each step. The spuare with the highest value is where the robot most probably stays.
Example results are shown as followed. 

><div align=center><img width="550" height="700" src="https://github.com/saddiesh/Algorithms/blob/master/HMM_maze_localization/Results.png"/>
  
A gif is generated to show the process:
Deeper blue the square is, the higher probability it has.
><div align=center><img width="550" height="400" src="https://github.com/saddiesh/Algorithms/blob/master/HMM_maze_localization/HMM_localiztion.gif"/>


