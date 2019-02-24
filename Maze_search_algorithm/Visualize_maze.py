#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 20:18:19 2019

@author: Di Shen
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import imageio,os

def draw_maze(arr,savename,end,i=None,j=None,text=None):
    maze=arr.copy()
    maze[maze==888] = 0.99
    maze[maze==0] = 0.2
    maze[maze==999] = 0
    maze[maze>=1]=0.5
    plt.imshow(maze,cmap = 'magma')
    plt.text(end[1], end[0], "Exit", horizontalalignment='center',verticalalignment='center', color='r')
    if text!=None:   
        plt.text(i, j, text, horizontalalignment='center',verticalalignment='center', color='w')
    plt.axis('off')
    plt.savefig(savename)

def draw_path(arr,savedir,end,path):
    maze=arr.copy()
    maze[maze==888] = 0.99
    maze[maze==0] = 0.2
    maze[maze==999] = 0
    textx=np.where(maze>=1)[0].astype(int)
    texty=np.where(maze>=1)[1].astype(int)
    maze[maze>=1]=0.5
    plt.imshow(maze,cmap = 'magma')
    plt.text(end[1], end[0], "Exit", horizontalalignment='center',verticalalignment='center', color='r')
    for i in range(len(textx)):   
        plt.text(texty[i], textx[i], str(int(arr[textx[i]][texty[i]])), horizontalalignment='center',verticalalignment='center', color='w')
    plt.axis('off')
    num=1
    for j in path:
        maze[arr==j]=0.7
        plt.imshow(maze,cmap = 'magma')
        savename=os.path.join(savedir,'{}.png'.format(900+num))
        plt.savefig(savename)
        num+=1

def generate_gif(dirpath):
    images = []
    filenames=[fn for fn in os.listdir(dirpath) if fn.endswith('.png')]
    filenames.sort(key= lambda x:float(x.split('.')[0]))
    print(filenames)
    for filename in filenames:
        images.append(imageio.imread(os.path.join(dirpath,filename)))
    imageio.mimsave(os.path.join(dirpath,'gif.gif'), images,duration=0.1)