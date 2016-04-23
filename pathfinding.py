import math
import heapq
from collections import OrderedDict
import pygame

#This is a buggy A* implementation.
#Most of this module was done using this link from class and coding the
#written algorithim:
#http://www.policyalmanac.org/games/aStarTutorial.htm

#The heurstic was from here:
#http://theory.stanford.edu/~amitp/GameProgramming/

#Collision checks where done using pygame sprite collisions which is the
#the main contributer to the slow down, so there is definitally a better
#way to implement that.

#Additionally if the move speed of the sprite increases it messes up
#the algorithm, probably the move speed needs to be taken into account
#in the algorithm calculations but I just hard coded the speed.

#LastUpdatedOrderedDict is from python docs recipe
#It is a dictionary that is ordered
class LastUpdatedOrderedDict(OrderedDict):
    def __setitem__(self,key,value):
        if key in self:
            del self[key]
        OrderedDict.__setitem__(self,key,value)

#This class acts as the grid square for the A* algorithm
class a_star_square():
    def __init__(self,xy,g,h):
        self.h = h
        self.g = g
        self.f = h+g
        self.xy = xy
        
    #cmp method for heapq
    def __lt__(self,other):
        return self.f < other.f

    def __eq__(self,other):
        return self.xy == other.xy

    def __hash__(self):
        return hash(tuple(self.xy))

#Dummy sprite class to test for collisions    
class C_Test(pygame.sprite.Sprite):
    def __init__(self,pix_size):
        super().__init__()

        self.image = pygame.Surface([pix_size,pix_size])
        self.rect = self.image.get_rect()

#This is the actual implementation of the algorithm
class a_star():
    def __init__(self,collids,pixel_box_size):
        self.colid = collids
        self.mobs = []
        self.open_list = []
        self.closed_list = []
        self.pix_size = pixel_box_size
        self.around = [(-1,0),(-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1)]
        self.goal = 0
        self.colid_test = C_Test(pixel_box_size)

    def heuristic(self,pos):
        dx = math.fabs(pos[0] - self.goal.xy[0])
        dy = math.fabs(pos[1] - self.goal.xy[1])
        return max(int(dx), int(dy))

    def find_path(self,start):
        not_found = True
        h = self.heuristic(start)
        g = 0
        dist_start = 1
        current_square = a_star_square(start,g,h)
        last_square = current_square
        #Path is the tree structure
        path = LastUpdatedOrderedDict()
        path[current_square] = []
        self.closed_list.append(current_square.xy)
        while(not_found):
            self.get_adjecents(current_square,dist_start,path)
            try:
                current_square = heapq.heappop(self.open_list)
            except IndexError:
                no_path = []
                no_path.append(start)
                return no_path

            self.closed_list.append(current_square.xy)
            dist_start += 1
            #For all places where I use the zip method to add two lists elements
            #togheter I found it through this stack overflow question:
            #http://stackoverflow.com/questions/14050824/add-sum-of-values-of-two-lists-into-new-list
            goal_check = [x - y for x,y in zip(self.goal.xy,current_square.xy)]

            if goal_check[0] < 30 and goal_check[1] < 30:
                not_found = False
                last_square = current_square
        return self.parse_path(path,last_square)

    def parse_path(self,path,last_square):
        found_path = []
        rev = list(path.items())
        rev.reverse()
        path = LastUpdatedOrderedDict(rev)
        a_child = last_square
        found_path.append(self.goal.xy)
        for parent,child in path.items():
            if a_child in child:
                found_path.append(a_child.xy)
                a_child = parent
        return found_path
            
    def get_adjecents(self,current_square,dist_start,path):
        adjecents = []
        for x in range(8):
            about = [squar * self.pix_size for squar in self.around[x]]
            about = [z + y for z,y in zip(about,current_square.xy)]
            self.colid_test.rect.x = about[0]
            self.colid_test.rect.y = about[1]
            
            hit_list = pygame.sprite.spritecollide(self.colid_test,
                                                   self.colid,False)
            if about not in self.closed_list and not hit_list:
                if (x%2):
                    new_square = a_star_square(about,
                                                14*dist_start,
                                                self.heuristic(about))
                    if new_square not in self.open_list:
                        heapq.heappush(self.open_list,new_square)
                        self.add_item(current_square,
                                      new_square
                                      ,path)
                    else:
                        if (current_square.g + 14) < new_square.g:
                            for parent,children in path.items():
                                if new_square in children:
                                    children.remove(new_square)
                                    self.add_item(current_square,
                                                  new_square,
                                                  path)
                                    break
                else:
                    new_square = a_star_square(about,
                                                10*dist_start,
                                                self.heuristic(about))
                    if new_square not in self.open_list:
                        heapq.heappush(self.open_list,new_square)
                        self.add_item(current_square,
                                      new_square,
                                      path)
                    else:
                        if (current_square.g + 10) < new_square.g:
                            for parent,children in path.items():
                                if new_square in children:
                                    children.remove(new_square)
                                    self.add_item(current_square,
                                                  new_square,
                                                  path)
                                    break
                        
    def summation(self,to_sum,n):
        for i in range(n):
            to_sum += to_sum
        return to_sum

    def add_item(self,current_square,new_square,path):
        if current_square not in path:
            path[current_square] = []
            path[current_square].append(new_square)
        else:
            path[current_square].append(new_square)                                                
    def get_path(self,start,goal):
        self.open_list = []
        self.closed_list = []
        self.goal = a_star_square(goal,0,0)
        path = self.find_path(start)
        return path
