#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 15:39:16 2019

@author: Di Shen / Linyan Wang
"""
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import imageio,os
####### Utils : #############
def rep_val(maze,loc,value):
    #replace value in maze:
    #loc = (x,y) in indices
    #value: traget value
    maze[loc[0]][loc[1]]=value
    
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

def init_maze():
    maze=np.zeros((8,11))
    walls=[(4,3),(4,4),(3,4),(2,4),(2,5),(2,6),(2,7),(3,7),(4,7),(5,7),(5,6)]
    for wall in walls:
        rep_val(maze, wall,999)
    start=(4,5)
    rep_val(maze,start,888)
    #maze=maze.astype(int)
    #print('\n','initialize maze:','\n',maze)
    return maze

def listpath(fatherdict,start,end,res_maze):
    endlabel=res_maze[end[0]][end[1]]
    pathlist=[endlabel]
    label=endlabel
    while label!= 888:
        fatherlabel=fatherdict[label]
        pathlist.append(fatherlabel)
        label=fatherlabel
    return pathlist

def show_result(maze):
    print('Author: Di Shen / Linyan Wang')
    print (time.strftime("%Y-%m-%d %H:%M:%S\n", time.localtime()))
    mazeframe=pd.DataFrame(maze).astype(int)
    mazeframe=mazeframe.replace(999,'##')
    mazeframe=mazeframe.replace(0,'[]')
    mazeframe=mazeframe.replace(888,'00')
    mazeframe=mazeframe.astype(str).applymap(lambda x: x.zfill(2))
    print(mazeframe.to_string(index=False,header=False))

def show_path(maze,pathlist):
    print('Author: Di Shen / Linyan Wang')
    print (time.strftime("%Y-%m-%d %H:%M:%S\n", time.localtime()))
    mazeframe=pd.DataFrame(maze).astype(int)
    mazeframe=mazeframe.replace(999,'###')
    mazeframe=mazeframe.replace(0,'[]')
    mazeframe=mazeframe.replace(888,'Start')
    mazeframe=mazeframe.replace(pathlist[0],'End')
    for l in pathlist[1:]:
        mazeframe=mazeframe.replace(l,'*^*')
    mazeframe=mazeframe.astype(str).applymap(lambda x: x.zfill(2))
    print(mazeframe.to_string(index=False,header=False))
    

############ BFS algorithm :   #######################

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
                    rep_val(ini_maze,new,label)
                    expanding.append(new)
                    fatherdict[label]=ini_maze[ex]
                    #print(fatherdict)
#                    savepng=os.path.join(savepath,'{}'.format(label))
#                    if new!=end:
#                        draw_maze(ini_maze,savepng,end,new[1],new[0],str(label))
                    label+=1
                    #print(bfs_maze)
                    if new==end:
                        break
        else:
            continue
        break
    return ini_maze,fatherdict


##############  UCS algorithm : ###################

def ucs_maze(ini_maze,steps,start,end,stepdict,stepcost,savepath):
    label=1
    labeldict={888:(4,5)}
    costdict={888:0}
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
                    rep_val(ini_maze,new,label)
                    labeldict[label]=new
                    costdict[label]=expand[1]+stepcost[step]
                    fatherdict[label]=maze[ex]
                    savepng=os.path.join(savepath,'{}'.format(label))
                    if new!=end:
                        draw_maze(ini_maze,savepng,end,new[1],new[0],str(label))
                    label+=1
                    #print(ucs_maze)
                    if new==end:
                        break
        else:
            continue
        break
    return ini_maze,fatherdict

##############  DFS algorithm : ###################
    
def dfs_maze(ini_maze,steps,start,end,savepath):
    expanding=[start]#list waiting for expanding
    label=1
    fatherdict={}
    while expanding!=[]:
        ex=expanding.pop(-1)
        #print(maze[ex])
        for step in steps:
            new=(ex[0]+step[0],ex[1]+step[1])
            #print(new)
            if 0<=new[0]<=7 and 0<=new[1]<=10:
                if ini_maze[new[0]][new[1]]==0:
                    rep_val(ini_maze,new,label)
                    expanding.append(new)
                    fatherdict[label]=maze[ex]
                    savepng=os.path.join(savepath,'{}'.format(label))
                    if new!=end:
                        draw_maze(ini_maze,savepng,end,new[1],new[0],str(label))
                    label+=1
                    #print(dfs_maze)
                    if new==end:
                        break
        else:
            continue
        break
    return ini_maze,fatherdict

##############  Greedy algorithm : ###################
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
                    rep_val(ini_maze,new,label)
                    labeldict[label]=new
                    costdict[label]=compute_h_cost(new,end)
                    #print(costdict)
                    fatherdict[label]=maze[ex]
#                    savepng=os.path.join(savepath,'{}'.format(label))
#                    if new!=end:
#                        draw_maze(ini_maze,savepng,end,new[1],new[0],str(label))
                    label+=1
                    #print(ucs_maze)
                    if new==end:
                        break
        else:
            continue
        break
    return ini_maze,fatherdict

##############  A* (A star) algorithm : ###################
def Astar_maze(ini_maze,steps,start,end,stepdict,stepcost,savepath):
    label=1
    labeldict={888:(4,5)}
    costdict={888:14}
    gcostdict={888:0}
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
                    rep_val(ini_maze,new,label)
                    labeldict[label]=new
                    gcostdict[label]=gcostdict[expand[0]]+stepcost[step]
                    costdict[label]=gcostdict[expand[0]]+stepcost[step]+compute_h_cost(new,end)
                    #print(costdict)
                    fatherdict[label]=maze[ex]
                    savepng=os.path.join(savepath,'{}'.format(label))
                    if new!=end:
                        draw_maze(ini_maze,savepng,end,new[1],new[0],str(label))
                    label+=1
                    #print(ucs_maze)
                    if new==end:
                        break
        else:
            continue
        break
    return ini_maze,fatherdict

############ initialize parameters: ##################
    
start=(4,5)
end=(0,10)
steps=[(0,-1),(-1,0),(0,1),(1,0)]
stepdict={0:(0,-1),1:(-1,0),2:(0,1),3:(1,0)}
stepcost={0:2,1:1,2:2,3:3}
maze=init_maze()
print('~~~~~~~~~~~~~~~~initialize maze:~~~~~~~~~~~~~~~~','\n',maze)
########### BFS algorithm implemented: #################
#maze=init_maze()
#dirpath="/Users/stephaniexia/Documents/UM/S2/CIS 579/Project1/BFS_image"
##draw_maze(maze,os.path.join(dirpath,"0.png"),end)
#bfs_result,fatherdict=bfs_maze(maze,steps,start,end,dirpath)
#
#path=listpath(fatherdict,start,end,bfs_result)
#print('\n','~~~~~~~~~~~~~~~~bfs_result:~~~~~~~~~~~~~~~~:')
#show_result(bfs_result)
#print('\n','bfs_path::')
#show_path(bfs_result,path)
#draw_path(bfs_result,dirpath,end,path) 
#generate_gif(dirpath)
############## UCS algorithm implemented: #################
#maze=init_maze()
#dirpath="/Users/stephaniexia/Documents/UM/S2/CIS 579/Project1/UCS_image"
#draw_maze(maze,os.path.join(dirpath,"0.png"),end)
#ucs_result,fatherdict=ucs_maze(maze,steps,start,end,stepdict,stepcost,dirpath)
#path=listpath(fatherdict,start,end,ucs_result)
#print('\n','~~~~~~~~~~~~~~~~ucs_result:~~~~~~~~~~~~~~~~:')
#show_result(ucs_result)
#print('\n','ucs_path:')
#show_path(ucs_result,path)
#draw_path(ucs_result,dirpath,end,path) 
#generate_gif(dirpath)
############## DFS algorithm implemented: #################
#maze=init_maze()
#dirpath="/Users/stephaniexia/Documents/UM/S2/CIS 579/Project1/DFS_image"
#draw_maze(maze,os.path.join(dirpath,"0.png"),end)
#dfs_result,fatherdict=dfs_maze(maze,steps,start,end,dirpath)
#path=listpath(fatherdict,start,end,dfs_result)
#print('\n','~~~~~~~~~~~~~~~~dfs_result:~~~~~~~~~~~~~~~~')
#show_result(dfs_result)
#print('\n','dfs_path:')
#show_path(dfs_result,path)
#draw_path(dfs_result,dirpath,end,path) 
#generate_gif(dirpath)
#############  Greedy algorithm implemented: ###################
#maze=init_maze()
#dirpath="/Users/stephaniexia/Documents/UM/S2/CIS 579/Project1/Greedy_image"
##draw_maze(maze,os.path.join(dirpath,"0.png"),end)
#greedy_result,fatherdict=greedy_maze(maze,steps,start,end,stepdict,dirpath)
#path=listpath(fatherdict,start,end,greedy_result)
##print(path)
#print('\n','~~~~~~~~~~~~~~~~greedy_result:~~~~~~~~~~~~~~~~')
#show_result(greedy_result)
#print('\n','greedy_path:')
#show_path(greedy_result,path)
#draw_path(greedy_result,dirpath,end,path)   
#generate_gif(dirpath)     
##############  A* algorithm implemented: ###################
maze=init_maze()
dirpath="/Users/stephaniexia/Documents/UM/S2/CIS 579/Project1/Astar_image"
draw_maze(maze,os.path.join(dirpath,"0.png"),end)
Astar_result,fatherdict=Astar_maze(maze,steps,start,end,stepdict,stepcost,dirpath)
path=listpath(fatherdict,start,end,Astar_result)
print('\n','~~~~~~~~~~~~~~~~Astar_result:~~~~~~~~~~~~~~~~')
show_result(Astar_result)
print('\n','Astar_path:')
show_path(Astar_result,path)
draw_path(Astar_result,dirpath,end,path)   
generate_gif(dirpath) 

########## Iterative deepening search algorithm : ################

class iter_DFS:
    def __init__(self,start,end,steps):
        self.start=start
        self.end=end
        self.steps=steps
    def init_maze(self):
        maze=np.zeros((8,11))
        walls=[(4,3),(4,4),(3,4),(2,4),(2,5),(2,6),(2,7),(3,7),(4,7),(5,7),(5,6)]
        for wall in walls:
            rep_val(maze, wall,999)
        start=(4,5)
        rep_val(maze,start,888)
        maze=maze.astype(int)
        #print('initialize maze:','\n',maze)
        return maze
    def dfs_maze(self,ini_maze,steps,start,end,lim):
        expanding=[888]#list waiting for expanding
        label=1
        labeldict={888:start}
        fatherdict={}
        stepdepth={888:0}
        while expanding!=[]:
            ex=expanding.pop(-1)
            if stepdepth[ex]>=lim:
                continue
            else:
                #print(maze[ex])
                for step in steps:
                    new=(labeldict[ex][0]+step[0],labeldict[ex][1]+step[1])
                    #print(new)
                    if 0<=new[0]<=7 and 0<=new[1]<=10:
                        if ini_maze[new[0]][new[1]]==0:
                            rep_val(ini_maze,new,label)
                            expanding.append(label)
                            labeldict[label]=new
                            stepdepth[label]=stepdepth[ex]+1
                            fatherdict[label]=ex
                            label+=1
                            #print(dfs_maze)
                            if new==end:
                                return ini_maze,fatherdict
        return None
    
    def iter_dfs(self):
        lim=1
        result=self.dfs_maze(self.init_maze(),self.steps,self.start,self.end,0)
        while result==None:
            lim+=1
            #maze=init_maze()
            result=self.dfs_maze(self.init_maze(),self.steps,self.start,self.end,lim)
        return result,lim
    
########## Iterative deepening search algorithm implemented: ################
#
#iterdfs=iter_DFS(start,end,steps)
#iterdfs_results,lim=iterdfs.iter_dfs()
#iterdfs_result_maze,fatherdict=iterdfs_results
#path=listpath(fatherdict,start,end,iterdfs_result_maze)
#print('\n','~~~~~~~~~~~~~~~~iter_dfs_result:~~~~~~~~~~~~~~~~')
#print('\n','The least limit to get out is : {}'.format(lim))
#show_result(iterdfs_result_maze)
#print('\n','iter_dfs_path:')
#show_path(iterdfs_result_maze,path)