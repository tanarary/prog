def transpose(mat: list[list[float | int]]) -> list[list]:
    for i in range(len(mat)-1):
        if len(mat[i]) == len(mat[i+1]):
            continue
        else:
            raise ValueError
    new = []
    if mat == []:
        new = []
    else:
        for i in range(len(mat[0])):
            new_row = []
            for row in mat:
                new_row.append(row[i])
            new.append(new_row)
    return new



def row_sums(mat: list[list[float | int]]) -> list[float]:
    for i in range(len(mat)-1):
        if len(mat[i]) == len(mat[i+1]):
            continue
        else:
            raise ValueError
    new = [] 
    for row in mat:
        s = 0
        for i in row:
            if type(i) == float or type(i) == int:
                s += i
            else:
                raise TypeError
        new.append(s)
    return new 


def col_sums(mat: list[list[float | int]]) -> list[float]:
    for i in range(len(mat)-1):
        if len(mat[i]) == len(mat[i+1]):
            continue
        else:
            raise ValueError
    new = [] 
    for i in range(len(mat[0])):
        s = 0
        for row in mat:
            s += row[i]
        new.append(s)
    return new 



        