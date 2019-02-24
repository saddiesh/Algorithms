#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 20:02:57 2019

@author: Di Shen
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import imageio,os

def rep_val(maze,loc,value):
    '''replace value in maze:
    loc = (x,y) in indices
    value: traget value
    '''
    maze[loc[0]][loc[1]]=value
    
def init_maze(shape, start, walls):
    '''
        shape: tuple, shape of maze
        start: tuple
        walls: list of tuples
        walls are labeled as 999 in matrix
        start is labeled as 888
        end is not labeled
    '''
    maze=np.zeros(shape)
    for wall in walls:
        rep_val(maze, wall,999)
    rep_val(maze,start,888)

    return maze

def listpath(fatherdict,start,end,res_maze):
    '''if want to show solution path, 
    list the labels of the path'''
    
    endlabel=res_maze[end[0]][end[1]]
    pathlist=[endlabel]
    label=endlabel
    while label!= 888:
        fatherlabel=fatherdict[label]
        pathlist.append(fatherlabel)
        label=fatherlabel
        
    return pathlist


def show_result(maze):
    '''Just show the expanding order'''
    mazeframe=pd.DataFrame(maze).astype(int)
    mazeframe=mazeframe.replace(999,'##')
    mazeframe=mazeframe.replace(0,'[]')
    mazeframe=mazeframe.replace(888,'00')
    mazeframe=mazeframe.astype(str)
    print(mazeframe.to_string(index=False,header=False))


def show_path(maze,pathlist):
    '''Show the expanding order labels and path as well'''
    mazeframe=pd.DataFrame(maze).astype(int)
    mazeframe=mazeframe.replace(999,'###')
    mazeframe=mazeframe.replace(0,'[]')
    mazeframe=mazeframe.replace(888,'Start')
    mazeframe=mazeframe.replace(pathlist[0],'End')
    for l in pathlist[1:]:
        mazeframe=mazeframe.replace(l,'*^*')
    mazeframe=mazeframe.astype(str)
    print(mazeframe.to_string(index=False,header=False))