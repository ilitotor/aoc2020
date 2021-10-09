from typing import List

def getNthTerm(seed: List[int], n: int) -> int:
  index_map = {}
  for i in range(len(seed) - 1):
    index_map[seed[i]] = i + 1
  last_number = seed[-1]
  for i in range(len(seed), n):
    if last_number in index_map:
      previous_position = index_map[last_number]
      index_map[last_number] = i
      last_number = i - previous_position
    else:
      index_map[last_number] = i
      last_number = 0
  return last_number

print(getNthTerm([9,3,1,0,8,4], 30000000))