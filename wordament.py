import numpy as np
from bisect import bisect_right
from copy import deepcopy

GRIDSIZE = 4
DEPTHBOUND = 16

# read in standard dictionary shipped with linux
dictionary = [word.strip() for word in open('/usr/share/dict/words') if word[0].islower() and word.find("'") == -1]  
	
def check_word( dictionary, word ):
    i = bisect_right(dictionary, word)
    if i == len(dictionary):
        return (False, False)
    prefix = dictionary[i].startswith(word)
    found = dictionary[i-1] == word
    return (found, prefix)
    

game_grid = [['l','s','e','a'], 
             ['k','a','s','r'], 
             ['e','a','n','e'],
             ['s','r','i','l']]

    
def word_search( i,j, word, visited ):
    if i < 0 or j < 0 or i >= GRIDSIZE or j >= GRIDSIZE:
        return
    if visited[i][j]:
        return       
    visited_copy = deepcopy(visited)
    visited_copy[i][j] = True
    word_copy = deepcopy(word)
    word_copy = word_copy + game_grid[i][j]
    (found, prefix) = check_word(dictionary, word_copy)
    if found and len(word) >= 3:
	    print word_copy
    if prefix and len(word_copy) < DEPTHBOUND:
        word_search( i+1, j, word_copy, visited_copy )
        word_search( i+1, j+1, word_copy, visited_copy )
        word_search( i, j+1, word_copy, visited_copy )
        word_search( i-1, j+1, word_copy, visited_copy )
        word_search( i-1, j, word_copy, visited_copy )
        word_search( i-1, j-1, word_copy, visited_copy )
        word_search( i, j-1, word_copy, visited_copy )
        word_search( i+1, j-1, word_copy, visited_copy )
        		
def grid_search( game_grid ):
    for i in range(GRIDSIZE):
        for j in range(GRIDSIZE):
            visited = np.zeros((GRIDSIZE,GRIDSIZE),dtype=np.bool)
            word_search( i, j, '', visited )
            
grid_search(game_grid)		    
		
