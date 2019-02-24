#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 20:06:02 2019

@author: Di Shen
"""
import MazeSearch_Utils as utils
import Visualize_maze as vis
import os

def bfs_maze(ini_maze,steps,start,end,savepath):
    expanding=[start]#list waiting for expanding
    label=1
    fatherdict={}
    while expanding!=[]:
        ex=expanding.pop(0)
        #print(maze[ex])
        for step in steps:
            new=(ex[0]+step[0],ex[1]+step[1])
            #print(new)
            if 0<=new[0]<=7 and 0<=new[1]<=10:
                if ini_maze[new[0]][new[1]]==0:
                    utils.rep_val(ini_maze,new,label)
                    expanding.append(new)
                    fatherdict[label]=ini_maze[ex]
                    #print(fatherdict)
                    savepng=os.path.join(savepath,'{}'.format(label))
                    if new!=end:
                        vis.draw_maze(ini_maze,savepng,end,new[1],new[0],str(label))
                    label+=1
                    #print(bfs_maze)
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
dirpath="/Users/stephaniexia/Documents/UM/S2/CIS 579/Project1/BFS_image"
vis.draw_maze(maze,os.path.join(dirpath,"0.png"),end)

bfs_result,fatherdict=bfs_maze(maze,steps,start,end,dirpath)

path=utils.listpath(fatherdict,start,end,bfs_result)

utils.show_result(bfs_result)
utils.show_path(bfs_result,path)

vis.draw_path(bfs_result,dirpath,end,path) 
vis.generate_gif(dirpath)