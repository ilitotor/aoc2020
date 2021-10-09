from typing import List, Tuple, Set

Coordinate = Tuple[int, int, int, int]
Dimension = List[List[List[List[bool]]]]

def createDimension(
  lines: List[str], size: Coordinate
) -> Dimension:
  output = [[[[False for _ in range(size[0])] for _ in range(size[1])] for _ in range(size[2])] for _ in range(size[3])]
  x_start = (size[0] - len(lines[0])) // 2
  y_start = (size[1] - len(lines)) // 2
  z_start = (size[2] - 1) // 2
  w_start = (size[3] - 1) // 2
  for y in range(len(lines)):
    for x in range(len(lines[y])):
      output[w_start][z_start][y + y_start][x + x_start] = lines[y][x] == '#'
  return output

def countActiveNeighbors(matrix: Dimension, coordinate: Coordinate) -> int:
  c = 0
  x, y, z, w = coordinate[0], coordinate[1], coordinate[2], coordinate[3]
  for wi in range(max([0, w-1]), min(len(matrix), w+2)):
    for zi in range(max([0, z-1]), min(len(matrix[w]), z+2)):
      for yi in range(max([0, y-1]), min(len(matrix[w][z]), y+2)):
        for xi in range(max([0, x-1]), min(len(matrix[w][z][y]), x+2)):
          if matrix[wi][zi][yi][xi]:
            c += 1
  if matrix[w][z][y][x]:
    c -= 1
  return c

def updateStatus(matrix: Dimension, coordinate: Coordinate) -> bool:
  x, y, z, w = coordinate[0], coordinate[1], coordinate[2], coordinate[3]
  active_neighbors = countActiveNeighbors(matrix, coordinate)
  if matrix[w][z][y][x]:
    return 2 <= active_neighbors <= 3
  else:
    return active_neighbors == 3

def updateCycle(matrix: Dimension, w_z_range: Tuple[int, int]):
  updateList: Set[Coordinate] = set()
  for w in range(w_z_range[0], w_z_range[1] + 1):
    for z in range(w_z_range[0], w_z_range[1] + 1):
      for y in range(len(matrix[w][z])):
        for x in range(len(matrix[w][z][y])):
          if matrix[w][z][y][x] != updateStatus(matrix, (x, y, z, w)):
            updateList.add((x, y, z, w))
  for x, y, z, w in updateList:
    matrix[w][z][y][x] = not matrix[w][z][y][x]

def printMatrix(matrix: Dimension):
  for w_slice in matrix:
    for z_slice in w_slice:
      for y_slice in z_slice:
        out = ''.join(map(lambda b: '#' if b else '.', y_slice))
        print(out)
      print()

def countActive(matrix: Dimension) -> int:
  c = 0
  for w_slice in matrix:
    for z_slice in w_slice:
      c += sum([y_slice.count(True) for y_slice in z_slice])
  return c

f = open('input.txt', 'r')
lines = f.read().splitlines()
matrix = createDimension(lines, (20, 20, 13, 13))
middle_point = len(matrix)// 2
for cycle in range(1, 7):
  updateCycle(matrix, (middle_point - cycle, middle_point + cycle))
print(f'Active cubes: {countActive(matrix)}')