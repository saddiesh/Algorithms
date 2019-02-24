#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 22:26:19 2019

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

def greedy_maze(ini_maze,steps,start,end,stepdict,savepath):
    label=1
    labeldict={888:(4,5)}
    costdict={888:14}
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
                    costdict[label]=compute_h_cost(new,end)
                    #print(costdict)
                    fatherdict[label]=maze[ex]
                    savepng=os.path.join(savepath,'{}'.format(label))
                    if new!=end:
                        vis.draw_maze(ini_maze,savepng,end,new[1],new[0],str(label))
                    label+=1
                    #print(ucs_maze)
                    if new==end:
                        break
        else:
            continue
        break
    return ini_maze,fatherdict


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
dirpath="/Users/stephaniexia/Documents/UM/S2/CIS 579/Project1/Greedy_image"
vis.draw_maze(maze,os.path.join(dirpath,"0.png"),end)

greedy_result,fatherdict=greedy_maze(maze,steps,start,end,stepdict,dirpath)

path=utils.listpath(fatherdict,start,end,greedy_result)

utils.show_result(greedy_result)
utils.show_path(greedy_result,path)

vis.draw_path(greedy_result,dirpath,end,path) 
vis.generate_gif(dirpath)
