#### 2048 GAME LOGIC FUNCS ####
# https://www.geeksforgeeks.org/2048-game-in-python/
def compress(mat):
	changed = False
	new_mat = []
	for i in range(4):
		new_mat.append([0] * 4)
	for i in range(4):
		pos = 0

		for j in range(4):
			if(mat[i][j] != 0):

				new_mat[i][pos] = mat[i][j]

				if(j != pos):
					changed = True
				pos += 1
	return new_mat, changed

def merge(mat):
    changed = False
    for i in range(4):
        for j in range(3):
            if(mat[i][j] == mat[i][j + 1] and mat[i][j] != 0):
                mat[i][j] = mat[i][j] * 2
                mat[i][j + 1] = 0
                changed = True
    return mat, changed

def reverse(mat):
    new_mat =[]
    for i in range(4):
        new_mat.append([])
        for j in range(4):
            new_mat[i].append(mat[i][3 - j])
    return new_mat

def transpose(mat):
    new_mat = []
    for i in range(4):
        new_mat.append([])
        for j in range(4):
            new_mat[i].append(mat[j][i])
    return new_mat

def move_up(grid):
        new_grid, changed1 = compress(grid)
        new_grid, changed2 = merge(new_grid)
        changed = changed1 or changed2
        new_grid, temp = compress(new_grid)
        return new_grid, changed

def move_down(grid):
    new_grid = reverse(grid)
    new_grid, changed = move_up(new_grid)
    new_grid = reverse(new_grid)
    return new_grid, changed

def move_left(grid):
    new_grid = transpose(grid)
    new_grid, changed = move_up(new_grid)
    new_grid = transpose(new_grid)
    return new_grid, changed

def move_right(grid):
    new_grid = transpose(grid)
    new_grid, changed = move_down(new_grid)
    new_grid = transpose(new_grid)
    return new_grid, changed