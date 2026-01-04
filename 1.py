# -*- coding: utf-8 -*-


def bfs_shortest_path(start, goal, width, height, blocked):
    """
    4 向广度优先搜索，返回任意一条起点到终点的最短路径（包含起点和终点）。
    坐标使用 1-based（与纸上标记一致），blocked 为无法通过的坐标集合。
    """
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    queue = [start]
    parent = {start: None}

    while queue:
        x, y = queue.pop(0)  # 简单列表实现队列，避免依赖额外模块
        if (x, y) == goal:
            break

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if not (1 <= nx <= width and 1 <= ny <= height):
                continue
            if (nx, ny) in blocked or (nx, ny) in parent:
                continue
            parent[(nx, ny)] = (x, y)
            queue.append((nx, ny))

    if goal not in parent:
        return []

    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path


def bfs_all_shortest_paths(start, goal, width, height, blocked):
    """
    计算所有最短路径：BFS 层序保证第一次到达终点时就是最短距离，
    使用多父节点表 parents 来恢复所有最短路径。
    """
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    queue = [start]
    dist = {start: 0}
    parents = {start: []}

    found_dist = None
    while queue:
        x, y = queue.pop(0)
        if found_dist is not None and dist[(x, y)] >= found_dist:
            continue
        if (x, y) == goal:
            found_dist = dist[(x, y)]
            continue

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if not (1 <= nx <= width and 1 <= ny <= height):
                continue
            nxt = (nx, ny)
            if nxt in blocked:
                continue

            if nxt not in dist:
                dist[nxt] = dist[(x, y)] + 1
                parents[nxt] = [(x, y)]
                queue.append(nxt)
            elif dist[nxt] == dist[(x, y)] + 1:
                # 另一条同长度的最短前驱
                parents[nxt].append((x, y))

    if found_dist is None:
        return []

    # 递归恢复所有最短路径
    all_paths = []

    def backtrack(node, path_rev):
        if node == start:
            all_paths.append(list(reversed(path_rev + [node])))
            return
        for p in parents[node]:
            backtrack(p, path_rev + [node])

    backtrack(goal, [])
    return all_paths


def dfs_backtracking(start, goal, width, height, blocked):
    """
    带显式回溯的深度优先搜索示例：遇到死路时弹栈退回上一单元继续尝试。
    不保证最短路径，只演示“死路退回”的过程。
    """
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    visited = set([start])
    stack = [start]  # 当前走过的路径

    while stack:
        x, y = stack[-1]
        if (x, y) == goal:
            return list(stack)

        # 找到一个尚未访问且可走的邻居
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if not (1 <= nx <= width and 1 <= ny <= height):
                continue
            nxt = (nx, ny)
            if nxt in blocked or nxt in visited:
                continue
            visited.add(nxt)
            stack.append(nxt)
            break
        else:
            # 没有可走的邻居 -> 死路，回退一步
            stack.pop()
0
    return []  # 无解


def render_path(width, height, blocked, path):
    """将路径/障碍可视化，方便对照纸上网格。"""
    path_set = set(path)
    lines = []
    for y in range(1, height + 1):
        row = []
        for x in range(1, width + 1):
            coord = (x, y)
            if coord == path[0]:
                row.append("S")
            elif coord == path[-1]:
                row.append("G")
            elif coord in blocked:
                row.append("#")
            elif coord in path_set:
                row.append("*")
            else:
                row.append(".")
        lines.append("".join(row))
    return "\n".join(lines)


if __name__ == "__main__":
    # 纸上是 12 列 × 8 行的网格；起点 (2,2)，终点 (10,5)。
    # 障碍重新调整，尽量贴合照片（左侧 3x3 含中心空格；右侧单列高墙在 x=9；下方小块靠中右）。
    width, height = 12, 8
    start, goal = (2, 2), (10, 5)
    blocked = {
        # 左侧大阴影块（中间留一个空格）
        (3, 2), (4, 2), (5, 2),
        (3, 3), (5, 3),
        (3, 4), (4, 4), (5, 4),
        # 中下方小块，位置稍靠右
        (6, 6), (7, 6), (6, 7),
        # 右侧竖直阴影块（单列高墙）
        (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6),
    }

    # 所有最短路径
    all_paths = bfs_all_shortest_paths(start, goal, width, height, blocked)
    if not all_paths:
        print("未找到通路")
    else:
        print(f"最短路径条数: {len(all_paths)}，最短步数: {len(all_paths[0]) - 1}")
        print("示例路径（第 1 条）:", all_paths[0])
        print("\n网格示意（S 起点, G 终点, # 障碍, * 路径）:")
        print(render_path(width, height, blocked, all_paths[0]))

    # 如果想看“死路退回”效果，可启用下方示例（DFS，非最短，仅演示回溯）：
    # path_dfs = dfs_backtracking(start, goal, width, height, blocked)
    # print("\nDFS 回溯路径:", path_dfs)
