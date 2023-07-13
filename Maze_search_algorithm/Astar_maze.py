#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 22:36:45 2019

@author: Di Shen
"""

import MazeSearch_Utils as utils
import Visualize_maze as vis
import os

def compute_h_cost(loc1,endloc):
    ycos=2*abs(loc1[1]-endloc[1])
    if loc1[0]>=endloc[0]:
        xcos=loc1[0]-endloc[0]
    else:
        xcos=3*(endloc[0]-loc1[0])
    cost=ycos+xcos
    return cost

def Astar_maze(ini_maze,steps,start,end,stepdict,stepcost,savepath):
    label=1
    labeldict={888:(4,5)}
    costdict={888:0}
    gcostdict={888:0}
    cost_all = {}
    fatherdict={}
    while costdict!={}:
        costsort=sorted(costdict.items(),key=lambda d:d[1])
        expand=costsort[0]
        ex=labeldict[expand[0]]
        costdict.pop(expand[0])
        #print(maze[ex])
        for step in range(4):
            new=(ex[0]+stepdict[step][0],ex[1]+stepdict[step][1])
            #print(new)
            if 0<=new[0]<=7 and 0<=new[1]<=10:
                if ini_maze[new[0]][new[1]]==0:
                    utils.rep_val(ini_maze,new,label)
                    labeldict[label]=new
                    gcostdict[label]=gcostdict[expand[0]]+stepcost[step]
                    costdict[label]=gcostdict[expand[0]]+stepcost[step]+compute_h_cost(new,end)
                    #print(costdict)
                    cost_all[new] = gcostdict[expand[0]]+stepcost[step]+compute_h_cost(new,end)
                    fatherdict[label]=maze[ex]
                    savepng=os.path.join(savepath,'{}'.format(label))
                    # if new!=end:
                        # vis.draw_maze(ini_maze,savepng,end,new[1],new[0],str(label))
                    label+=1
                    #print(ucs_maze)
                    if new==end:
                        break
        else:
            continue
        break
    # print(cost_all)
    # print(labeldict)
    path = utils.listpath(fatherdict, start, end, ini_maze, labeldict)
    print(path)
    return path


mazeshape=(8,11)
start=(4,5)
end=(0,10)
walls=[(4,3),(4,4),(3,4),(2,4),(2,5),(2,6),(2,7),(3,7),(4,7),(5,7),(5,6)]

#windy condition steps:
steps=[(0,-1),(-1,0),(0,1),(1,0)]
stepdict={0:(0,-1),1:(-1,0),2:(0,1),3:(1,0)}
stepcost={0:2,1:1,2:2,3:3}

#initial maze
maze=utils.init_maze(mazeshape, start, walls)

#save images and gif under:
dirpath="./"
vis.draw_maze(maze,os.path.join(dirpath,"0.png"),end)

path=Astar_maze(maze,steps,start,end,stepdict,stepcost,dirpath)

# utils.show_result(Astar_result)
# utils.show_path(Astar_result,path)
#
# vis.draw_path(Astar_result,dirpath,end,path)
# vis.generate_gif(dirpath)