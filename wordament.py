"""
Solver for wordament game.
Four rows of the game are entered as follows:
enter row1: ab[cd]e
enter row2: [fg-]hij
enter row3: klm[n|o]
enter row4: [-p]qrs
It finds all the words using the standard unix dictionary and prints them out from largest to 
smallest.
"""
import numpy as np
from bisect import bisect_right
import re

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

# results from the word search are stored here    
results = set()

# depth first search for words starting from (i,j)
def word_search( game_grid, i,j, word = '', visited = np.zeros((GRIDSIZE,GRIDSIZE),dtype=np.bool)):
    # return if out of bounds or already visited
    if i < 0 or j < 0 or i >= GRIDSIZE or j >= GRIDSIZE or visited[i][j]:
        return
    # return if required to be starting letters and are not
    if len(game_grid[i][j]) == 3 and game_grid[i][j][2] == '-' and len(word) > 0:
        return    
    # mark as visited
    visited[i][j] = True
    # extract 1 or 2 suffixes from current square
    suffixes = []
    if game_grid[i][j][0] == '-':
        suffixes.append(game_grid[i][j][1:])
    elif game_grid[i][j][-1] == '-':
        suffixes.append(game_grid[i][j][:-1])
    elif len(game_grid[i][j]) == 3 and game_grid[i][j][1] == '|': 
        suffixes.append(game_grid[i][j][0])
        suffixes.append(game_grid[i][j][-1])
    else:
        suffixes.append(game_grid[i][j])
    for s in suffixes:
        word = word + s
        # search for word in dictionary and record it if found
        (found, prefix) = check_word(dictionary, word)
        if found and len(word) >= 3:
            results.add(word)
        # continue on if word is prefix of another word 
        if game_grid[i][j][0] != '-' and prefix and len(word) < DEPTHBOUND:
            word_search( game_grid, i+1, j, word, visited )
            word_search( game_grid, i+1, j+1, word, visited )
            word_search( game_grid, i, j+1, word, visited )
            word_search( game_grid, i-1, j+1, word, visited )
            word_search( game_grid, i-1, j, word, visited )
            word_search( game_grid, i-1, j-1, word, visited )
            word_search( game_grid, i, j-1, word, visited )
            word_search( game_grid, i+1, j-1, word, visited )
        word = word[:-len(s)]
    # mark as unvisited 
    visited[i][j] = False

# search for words starting at every possible location
def grid_search( game_grid ):
    for i in range(GRIDSIZE):
        for j in range(GRIDSIZE):
            word_search( game_grid, i, j )
            
def parse_row( row ):
    pat = '[a-z]|\[-?[a-z]{1,2}\]|\[[a-z]{1,2}-\]|\[[a-z]\|[a-z]\]'
    strict_pat = re.compile('^(?:' + pat + '){4}$')
    if re.match(strict_pat, row) is None:
        return None
    extract_pat = re.compile('(' + pat + ')')
    parsed_row = [entry[1:-1] if len(entry) > 1 else entry for entry in re.findall(extract_pat,row)]
    return parsed_row
    
if __name__ == "__main__":
    game_grid = []
    for r in range(1,GRIDSIZE+1):
        repeat = True
        while repeat:
            row = raw_input('enter row'+str(r)+':')
            parsed_row = parse_row(row)
            repeat = parsed_row is None
            if repeat:
                print 'ERROR try again.'
        game_grid.append(parsed_row)
    grid_search(game_grid)
    for word in sorted(results,key=len,reverse=True):
        print word
    
    
