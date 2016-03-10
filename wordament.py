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


# depth first search for words starting from (i,j)
def word_search( i,j, word = '', visited = np.zeros((GRIDSIZE,GRIDSIZE),dtype=np.bool)):
    # return if out of bounds or already visited
    if i < 0 or j < 0 or i >= GRIDSIZE or j >= GRIDSIZE or visited[i][j]:
        return
    # mark as visited and extend word
    visited[i][j] = True
    word = word + game_grid[i][j]
    # search for word in dictionary and record it if found
    (found, prefix) = check_word(dictionary, word)
    if found and len(word) >= 3:
	    print word
    # continue on if word is prefix of another word 
    if prefix and len(word) < DEPTHBOUND:
        word_search( i+1, j, word, visited )
        word_search( i+1, j+1, word, visited )
        word_search( i, j+1, word, visited )
        word_search( i-1, j+1, word, visited )
        word_search( i-1, j, word, visited )
        word_search( i-1, j-1, word, visited )
        word_search( i, j-1, word, visited )
        word_search( i+1, j-1, word, visited )
    # mark as unvisited and remove character from word just before return
    visited[i][j] = False
    word = word[:-1]


def grid_search( game_grid ):
    for i in range(GRIDSIZE):
        for j in range(GRIDSIZE):
            word_search( i, j )
            
grid_search(game_grid)		    
		
