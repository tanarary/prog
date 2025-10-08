def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:
    return min(nums), max(nums)


def unique_sorted(ls: list[float | int]) -> list[float | int]:
    return sorted(set(ls))
    

def flatten(mat: list[list | tuple]) -> list:
    fl = []
    for i in mat:
        if type(i) == list or type(i) == tuple:
            fl.extend(i)
        else:
            raise TypeError
    return fl

print(flatten([[1, 2], [3, 4]]))
print(flatten([[1, 2], (3, 4, 5)]))
print(flatten([[1], [], [2, 3]]))
print(flatten([[1, 2], "ab"]))


