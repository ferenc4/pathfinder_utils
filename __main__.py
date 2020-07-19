from time import time
from typing import Dict, Any

from directions import Direction
from position import Position
from steps import DistancedStep


def find_shortest(from_pos: Position, to_pos: Position, step_map_for_target: dict):
    try:
        start_time = time()
        step_map: dict = step_map_for_target.get(to_pos)
        path = []
        while from_pos != to_pos:
            path.append(from_pos)
            next_step: DistancedStep = step_map.get(from_pos)
            from_pos = next_step.position
        path.append(to_pos)
        print("Search finished in", time() - start_time, "seconds")
        return path
    except:
        return None


def is_blocker(grid: [[]], pos: Position):
    return grid[pos.y][pos.x] == 1


def is_within_bounds(grid: [[]], pos: Position):
    return 0 <= pos.y < len(grid) and 0 <= pos.x < len(grid[0])


def precompute(grid: [[]]):
    start_time = time()
    step_map_for_target: Dict[Position, Dict[Position, DistancedStep]] = dict()
    for row_i, row in enumerate(grid):
        for col_i, col in enumerate(row):
            start = Position(x=col_i, y=row_i)
            if is_within_bounds(grid=grid, pos=start) and not is_blocker(grid=grid, pos=start):
                move_stack = [[start]]
                while move_stack.__len__() > 0:
                    moves = move_stack.pop(0)
                    # print("Moves", moves)
                    for direction in [Direction.LEFT, Direction.RIGHT, Direction.DOWN, Direction.UP]:
                        target = moves[-1].moved(direction=direction)
                        if is_within_bounds(grid=grid, pos=target):
                            if grid[target.y][target.x] == 0:
                                step_map = step_map_for_target.get(target, dict())
                                for move_i, move in enumerate(moves):
                                    if move == target:
                                        step_map[move] = DistancedStep(distance=0, position=move)
                                    else:
                                        old_next_step: DistancedStep = step_map.get(move, None)
                                        new_distance = moves.__len__() - move_i
                                        if old_next_step is None or old_next_step.distance > new_distance:
                                            if move_i + 1 < moves.__len__():
                                                new_next_position = moves[move_i + 1]
                                            else:
                                                new_next_position = target
                                            step_map[move] = DistancedStep(distance=new_distance,
                                                                           position=new_next_position)

                                            move_stack.append(moves + [target])
                                step_map_for_target[target] = step_map

    for target, step_map in step_map_for_target.items():
        for from_pos, next_step in step_map.items():
            next_step: DistancedStep = next_step
            print("target:", target,
                  "from_pos:", from_pos,
                  "next step:", next_step.position,
                  "distance:", next_step.distance)
        print()
    print("Time:", time() - start_time)
    return step_map_for_target


def print_path(path):
    if path is None:
        print("No solution")
    else:
        print(" > ".join(str(elem) for elem in path))


def test():
    for row_i, row1 in enumerate(grid):
        for col_i, col1 in enumerate(row1):
            pos1 = Position(x=col_i, y=row_i)
            for row_j, row2 in enumerate(grid):
                for col_j, col2 in enumerate(row2):
                    pos2 = Position(x=col_j, y=row_j)
                    if pos1 != pos2 and not is_blocker(grid=grid, pos=pos1) and not is_blocker(grid=grid, pos=pos2):
                        shortest = find_shortest(pos1, pos2, step_map_for_target)
                        assert shortest is not None, f"Precomputed was None for start_pos={pos1}, to_pos={pos2}"


if __name__ == "__main__":
    grid = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0],
        [1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0],
        [1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    step_map_for_target = precompute(grid=grid)
    print_path(find_shortest(Position(18, 16), Position(8, 9), step_map_for_target))
    print_path(find_shortest(Position(0, 0), Position(20, 20), step_map_for_target))
    print_path(find_shortest(Position(0, 0), Position(20, 20), step_map_for_target))
    test()
