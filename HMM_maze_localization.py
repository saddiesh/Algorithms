#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 11:06:49 2019

@author: Di Shen
"""

import numpy as np
import math
import time
from matplotlib import pyplot as plt
import matplotlib.patches as patches
 


# Utilities:
def show_rights(author):
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),"  //  by: ", author)



def rep_val(array,loc,value,maze_size):
    #replace value in maze:
    #loc = (x,y) in indices
    #value: traget value
    x=loc[0]
    y=loc[1]
    if x >= 0 and x < maze_size[0] and y >= 0 and y < maze_size[1]:
        array[x][y]=value
    
    
def get_val(array,loc, maze_size):
    #replace value in maze:
    #loc = (x,y) in indices
    #value: traget value
    x = loc[0]
    y = loc[1]
    
    if x < 0 or x >= maze_size[0] or y < 0 or y >= maze_size[1]:
        return 0
    
    return array[x][y]
    
    
def move_coord(loc, step):
    '''
    loc=(x,y); step=(delta_x, delta_y)
    des=(x+delta_x, y+delta_y)
    '''
    des=(loc[0]+step[0], loc[1]+step[1])
    return des


def cal_entropy(array):
    arr = array.copy()
    height, width = arr.shape
    for i in range(height):
        for j in range(width):
            if arr[i][j] != 0:
                value = arr[i][j]*math.log(arr[i][j],2)
                arr[i][j] = value
    sum_entropy = -np.sum(arr)
    return sum_entropy



class Config_Maze():
    
    steps=[(0,-1),(-1,0),(0,1),(1,0)]
    origins=[(0,-1),(-1,0),(0,1),(1,0),(0,0)]
    maze_size = (8,11)    
    init_prob = 0.013
    obstacles = [(4,3),(4,4),(3,4),(2,4),(2,5),(2,6),(2,7),(3,7),(4,7),(5,7),(5,6)]
    decimal = 3
    sensing = [ (1,1,1,1), (1,1,1,1), (1,1,0,1), (1,1,1,1), (1,1,0,0), (1,1,0,1) ]
    moving = ["northward", "northward", "northward", "eastward", "northward"]
    author = "Saddie"


class HMM_in_maze():
    
    def __init__(self, config):
        self.config = config
        
        
    def env_St ( self, coord, steps, maze, maze_size):
        '''coord = St (x,y) index in the probability array'''
        
        St = []
        for step in steps:
            coor = move_coord(coord, step)
            St.append( get_val(maze,coor, maze_size) )
            
        return St
    
    
    def init_prob_arr(self, obstacles, maze_size, init_prob):
    
        s1_prob = np.full( maze_size, init_prob )
        for obs in obstacles:
            rep_val( s1_prob, obs, 0 ,maze_size)
    
        return s1_prob


    def init_maze(self,obstacles, maze_size):
        
        maze = np.full( maze_size, 1 )
        for obs in obstacles:
            rep_val( maze, obs, 0, maze_size )
        
        return maze
    
    
    def cal_P_Zt_St( self, Zt, coord, steps, init_maze, maze_size ):
        '''
        P( Zt|St )
        Zt = (w,n,e,s): value of w/n/e/s is 0 or 1 ; 0 means detecting obstacle; 1 means detecting space
        coord = St (x,y) index in the probability array
        '''
        St = np.array( self.env_St( coord, steps, init_maze, maze_size) )
        Zt = np.array( Zt )
        
        TF = (Zt==St).astype(int)
        pos_prob = np.where(St==1, 0.95, 0.9)
        neg_prob = 1-pos_prob
        
        P_Zt_St = TF*pos_prob + (1-TF)*neg_prob
        P_Zt_St = P_Zt_St.prod()
        
        return P_Zt_St
    
    
    def cal_P_Zt_St_arr( self, Zt, steps, init_maze, maze_size ):
        '''
        P(Zt_St) for every non-obstacle square:
        '''
        P_Zt_St_arr = np.zeros(maze_size)
        
        for x in range( maze_size[0] ):
            for y in range( maze_size[1] ):
                if get_val(init_maze, (x,y) , maze_size) == 0:
                    continue
                P_Zt_St = self.cal_P_Zt_St( Zt, (x,y), steps, init_maze, maze_size )
                rep_val(P_Zt_St_arr, (x,y), P_Zt_St, maze_size)
        
        return P_Zt_St_arr
    
    
    def cal_P_St_St_1( self, moving_direction, coord, init_maze, maze_size, origins, P_St_1_Zt_1_arr ):
        
        St_env = np.array( self.env_St(coord, origins, init_maze, maze_size) )
        #print("St_env:", St_env, "\n")
        P_St_1_Zt_1 = np.array( self.env_St(coord, origins, P_St_1_Zt_1_arr, maze_size) )
        #print("P_St_1_Zt_1:", P_St_1_Zt_1, "\n")
    
        P_stay = 0
        
        if moving_direction == "northward":
            
            dir_prob=np.array([0.1, 0, 0.1, 0.8, 0])
            if St_env[0] == 0:
                P_stay += 0.1
            if St_env[1] == 0:
                P_stay += 0.8
            if St_env[2] == 0:
                P_stay += 0.1
            dir_prob[4] = P_stay
            
            
        if moving_direction == "eastward":
            
            dir_prob=np.array([0.8, 0.1, 0, 0.1, 0])
            if St_env[1] == 0:
                P_stay += 0.1
            if St_env[2] == 0:
                P_stay += 0.8
            if St_env[3] == 0:
                P_stay += 0.1    
            dir_prob[4] = P_stay
        
        P_St_Zt_1 = np.sum( dir_prob * P_St_1_Zt_1 )
                        
        return P_St_Zt_1
    
    
    def cal_P_St_St_1_arr( self, moving_direction, coord, init_maze, maze_size, origins):
        
        res_arr = np.zeros(maze_size)
        St_env = np.array( self.env_St(coord, origins, init_maze, maze_size) )
        #print("St_env:", St_env, "\n")
    
        P_stay = 0
        
        if moving_direction == "northward":
            
            dir_prob=np.array([0.1, 0.8, 0.1, 0, 0])
            if St_env[0] == 0:
                P_stay += 0.1
            if St_env[1] == 0:
                P_stay += 0.8
            if St_env[2] == 0:
                P_stay += 0.1
            dir_prob[4] = P_stay
            
            
        if moving_direction == "eastward":
            
            dir_prob=np.array([0, 0.1, 0.8, 0.1, 0])
            if St_env[1] == 0:
                P_stay += 0.1
            if St_env[2] == 0:
                P_stay += 0.8
            if St_env[3] == 0:
                P_stay += 0.1  
            dir_prob[4] = P_stay
        
        P_St_Zt_1 = dir_prob
        for step in range(len(origins)):
            rep_val( res_arr, move_coord(coord, origins[step]), P_St_Zt_1[step] ,maze_size)
        #print("P_St_St_1_arr:\n", res_arr)
                        
        return res_arr
    
    
    def filtering( self, P_St_Zt_1, Zt, steps, init_maze, maze_size):
        '''
        P_St_Zt_1: P(St | Zt-1) for every square 
        Zt = (w,n,e,s): value of w/n/e/s is 0 or 1 ; 0 means detecting obstacle; 1 means detecting space  
        
        Target:
        P(St|Zt) = P(Zt,St) / sum_St'_( ( P(Zt,St') )
        P(Zt,St) = P(Zt|St) * P(St|Zt-1)
        
        '''
        P_Zt_St_arr = self.cal_P_Zt_St_arr( Zt, steps, init_maze, maze_size )
        #print("P(Zt|St)",P_Zt_St_arr,"\n")

        P_ZtSt_arr = P_Zt_St_arr * P_St_Zt_1
        #print("P(Zt,St)",P_ZtSt_arr,"\n")
        
        total = np.sum(P_ZtSt_arr)
        
        P_St_Zt_arr = np.divide( P_ZtSt_arr , total, where=total!=0 ) 
        
        return P_Zt_St_arr, P_St_Zt_arr.round(decimals=self.config.decimal)
    
    
    def predicting ( self, moving_direction, init_maze, maze_size, origins, P_St_1_Zt_1_arr):
        '''
        Calculate and return P(St|Zt-1) array 
        '''
        
        P_St_Zt_1_arr = np.zeros(maze_size)
        
        for x in range( maze_size[0] ):
            for y in range( maze_size[1] ):
                if get_val(init_maze, (x,y) , maze_size) == 0:
                    continue
                P_St_Zt_1 =self.cal_P_St_St_1(moving_direction, (x,y), init_maze, maze_size, origins, P_St_1_Zt_1_arr )
                rep_val(P_St_Zt_1_arr, (x,y), P_St_Zt_1, maze_size)
        
        return P_St_Zt_1_arr.round(decimals=self.config.decimal)
    
    
    def draw_heatmap( self, data_arr, walls, maze_size, title ):   
        
        figure=plt.figure(facecolor='w',figsize=(maze_size[1], maze_size[0]))
        data_display_arr = data_arr[::-1] 
        ax=figure.add_subplot(1,1,1)
        ax.axis([0, maze_size[1], 0, maze_size[0] ])
        ax.imshow(data_display_arr[::-1], cmap='plasma', extent=(0,11,0,8), aspect='auto',vmin=0,vmax=1)
        for wall in walls:
            coord = ( wall[1], maze_size[0] - 1 - wall[0])
            ax.add_patch( patches.Rectangle(coord, 1, 1, facecolor="black" ) )
        ax.set_title(title)
    
        plt.show()
        
        
    def HMM_process(self):
        P_S1 = self.init_prob_arr( self.config.obstacles, self.config.maze_size, self.config.init_prob )
        maze = self.init_maze( self.config.obstacles, self.config.maze_size ) 
   
        print(P_S1)
        print(maze)
        
        Z1 = self.config.sensing[0]
        print("Z1: ", Z1,"\n\n")
        
        P_Z1_S1_arr,P_S1_Z1 = self.filtering(P_S1, Z1, self.config.steps, maze, self.config.maze_size)
        ent = cal_entropy(P_S1_Z1)
        
        show_rights(self.config.author)
        print("P( S1|Z1 ) :   entropy:{} \n".format(ent), P_S1_Z1*100,"\n")
        #self.draw_heatmap(P_S1_Z1, self.config.obstacles, self.config.maze_size, "P( S1|Z1 )" )
        
        P_St_Zt_save = [P_S1_Z1]
        P_Zt_St_save = [P_Z1_S1_arr]
        
        P_St_1_Zt_1 = P_S1_Z1
        
        P_St_St_1_save = []
        
        for t in range(len(self.config.moving)):
            
            move = self.config.moving[t]
            print("t{}---move: {}\n".format(t+2,move))
            
            P_St_Zt_1 = self.predicting (move, maze, self.config.maze_size, self.config.origins, P_St_1_Zt_1)
            show_rights(self.config.author)
            print("P( S{}|Z{} ) :\n".format(t+2, t+1), P_St_Zt_1*100,"\n")
            #self.draw_heatmap(P_St_Zt_1, self.config.obstacles, self.config.maze_size, "P( S{}|Z{} ) :\n".format(t+2, t+1) )
            P_St_St_1_save.append(P_St_Zt_1)
            
            sense = self.config.sensing[t+1]
            print("t{}---Z{}: {}\n".format(t+2, t+2, sense))
            
            P_Zt_St_arr,P_St_Zt = self.filtering(P_St_Zt_1, sense, self.config.steps, maze, self.config.maze_size)
            ent = cal_entropy(P_St_Zt)
            show_rights(self.config.author)
            print("P( S{}|Z{} ):  entropy:{} \n".format(t+2, t+2, ent), P_St_Zt*100,"\n\n")
            #self.draw_heatmap(P_St_Zt, self.config.obstacles, self.config.maze_size, "P( S{}|Z{} ) :\n".format(t+2, t+2) )
            
            P_St_Zt_save.append(P_St_Zt)
            P_Zt_St_save.append(P_Zt_St_arr)
            
            P_St_1_Zt_1 = P_St_Zt
        
        self.smoothing(maze, self.config.maze_size, self.config.origins, P_Zt_St_save,P_St_Zt_save)
    
    def cal_backward(self, moving_direction, init_maze, maze_size, origins, P_Zkp1_Skp1, P_Zkp2_Skp1 ):
        '''
        P( Zk+1:t|Sk ) = sum_Sk+1_( P( Zk+1|Sk+1 ) * P( Zk+2:t|Sk+1 ) * P( Sk+1|Sk ) )
        k=5: P( Z6|S5 ) = sum_S6_( P( Z6|S6 ) * P( |S6 ) * P( S6|S5 ) )
        '''
        
        P_back = np.zeros(maze_size)
        for x in range( maze_size[0] ):
            for y in range( maze_size[1] ):
                if get_val(init_maze, (x,y) , maze_size) == 0:
                    continue
                P_Skp1_Sk = self.cal_P_St_St_1_arr( moving_direction, (x,y), init_maze, maze_size, origins)
                #print(P_Skp1_Sk)
                P_Zkp1_Sk = np.sum( P_Zkp1_Skp1* P_Zkp2_Skp1 * P_Skp1_Sk)
                #print(P_Zkp1_Sk.round(decimals = 3))
                rep_val(P_back, (x,y), P_Zkp1_Sk, maze_size)
        total = np.sum(P_back)
        P_back /= total
        return P_back
       
            
    def smoothing(self, init_maze, maze_size, origins, P_Zt_St_save,P_St_Zt_save ):
        '''
        P( Sk|Z1:t ) = alpha * P( Sk|Z1:k ) * P( Zk+1:t|Sk )
        P( Zk+1:t|Sk ) = sum_Sk+1_( P( Zk+1|Sk+1 ) * P( Zk+2:t|Sk+1 ) * P( Sk+1|Sk ) )
        
        k=5:
            P(S5|Z1:6) = alpha * P( S5|Z1:5 ) * P( Z6|S5 )
            P( Z6|S5 ) = sum_S6_( P( Z6|S6 ) * P( |S6 ) * P( S6|S5 ) )
            
        k=4:
            P( S4|Z1:6 ) = alpha * P( S4|Z1:4 ) * P( Z5|S4 )
            P( Z5|S4 ) = sum_S5_( P( Z5|S5 ) * P( Z6|S5 ) * P( S5|S4 ) )
        ''' 
        P_Zkp2_Skp1 = 1
        for k in range( len(self.config.moving), 0, -1 ):
        #for k in range(5,4,-1):
            #print("moving step: ", self.config.moving[k-1])
            P_Zkp1_Sk = self.cal_backward(self.config.moving[k-1], init_maze, maze_size, origins,
                                     P_Zt_St_save[k], P_Zkp2_Skp1 )
            
            #print(P_Zkp1_Sk.round(decimals=3))
            P_Sk_z = P_St_Zt_save[k-1] * P_Zkp1_Sk
            total = np.sum( P_Sk_z )
            P_Sk_z /= total
            P_Sk_z = P_Sk_z.round(decimals=self.config.decimal)
            ent = cal_entropy(P_Sk_z)
            
            P_Zkp2_Skp1 = P_Zkp1_Sk
            show_rights(self.config.author)
            print("time:{}---P( S{}|Z1:6 ):   entropy:{} \n{}\n\n".format(k,k,ent, P_Sk_z*100))
            
            
            

maze_config = Config_Maze()
hmm_maze = HMM_in_maze(maze_config)
hmm_maze.HMM_process()

