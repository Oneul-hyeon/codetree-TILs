import sys
from collections import deque
input = sys.stdin.readline

# 1. 그룹 생성 함수 정의
def create_group() :
    # 1-1. BFS 함수 정의
    def bfs(x, y, num) :
        # 1-1-1. 해당 그룹에 속하는 인덱스 리스트, 인접한 다른 그룹의 인덱스 리스트 생성
        now, adjacent = [(x, y)], []
        # 1-1-2. 큐에 현재 위치 삽입 후 방문 처리
        queue = deque()
        queue.append((x, y))
        visited[x][y] = True
        # 1-1-3.
        while queue :
            # 위치 인덱스 반환
            x, y = queue.popleft()
            for dir_x, dir_y in [(-1, 0), (1, 0), (0, -1), (0, 1)] :
                # 다음 위치 정의
                nx, ny = x + dir_x, y + dir_y
                # 예외 처리 1 : 맵을 벗어나는 경우
                if nx < 0 or nx >= n or ny < 0 or ny >= n : continue
                # 예외 처리 2 : 현재 그룹이 아닌 경우
                if graph[nx][ny] != num :
                    # 인접한 다른 그룹의 인덱스 리스트 업데이트
                    adjacent.append((nx, ny))
                    continue
                # 방문한 적이 없는 경우
                if not visited[nx][ny] :
                    # 방문 처리
                    visited[nx][ny] = True
                    # 해당 그룹에 속하는 인덱스 리스트 업데이트
                    now.append((nx, ny))
                    # 큐에 다음 위치 삽입
                    queue.append((nx, ny))
        # 1-1-4. 현재 그룹에 속한 칸의 수, 해당 그룹에 속하는 인덱스 리스트, 인접한 다른 그룹의 인덱스 리스트 반환
        return len(now), now, adjacent
    # 1-2. 그룹 딕셔너리 생성
    group = dict()
    # 1-3. 방문 여부 리스트, 그룹 넘버 변수 생성
    visited = [[False for _ in range(n)] for _ in range(n)]
    group_number = 0
    # 1-4.
    for i in range(n) :
        for j in range(n) :
            # 1-4-1. 현재 위치에 방문한 적이 없을 경우
            if not visited[i][j] :
                # BFS 실행
                cnt, now_group, adjacent_group = bfs(i, j, graph[i][j])
                # 딕셔너리 정보 입력
                group[group_number] = [graph[i][j], cnt, now_group, adjacent_group]
                # 그룹 넘버 변수 업데이트
                group_number += 1
    # 1-5. 그룹 딕셔너리 반환
    return group
# 2. 조화로움 계산 함수
def calculate() :
    # 2-1. 조화로움 변수 생성
    value = 0
    # 2-2.
    for group1 in range(len(group.keys())) :
        for group2 in range(group1+1, len(group.keys())) :
            # 2-2-1.인접한 변의 수 계산
            side = 0
            for idx in group[group2][3] :
                # 1번째 그룹의 인덱스에 속할 경우 카운팅
                if idx in group[group1][2] : side += 1
            # 2-2-2. 조화로움 업데이트
            value += (group[group1][1] + group[group2][1]) * group[group1][0] * group[group2][0] * side
    # 2-3. 조화로움 반환
    return value
# 3. 회전 함수 정의
def rotate() :
    sub_graph = [line[:] for line in graph]
    # 3-1. 십자 모양 회전
    # 3-1-1. 사이즈 생성
    size = n
    # 3-1-2. 가운데 위치 생성
    mid = size // 2
    # 3-1-3. 삽자 모양의 가로 업데이트
    col = []
    for i in range(n) : col.append(sub_graph[i][mid])
    graph[mid] = col
    # 3-1-4. 십자 모양의 세로 업데이트
    row = sub_graph[mid].copy()[::-1]
    for i in range(n) :
        graph[i][mid] = row[i]

    # 3-2. 그 외 부분 회전
    # 3-2-1. 사이즈 생성
    size = n // 2
    # 3-2-2.
    for r, c in [(0, 0), (0, size+1), (size+1, 0), (size+1, size+1)] :
        for x in range(r, r+size) :
            for y in range(c, c+size) :
                # 회전
                ox, oy = x - r, y - c
                mx, my = oy, size - ox - 1
                ex, ey = mx + r, my + c
                graph[ex][ey] = sub_graph[x][y]


if __name__ == "__main__" :
    n = int(input())
    # 4. 그래프 생성
    graph = [list(map(int, input().split())) for _ in range(n)]
    # 5.
    ans = 0
    for i in range(4) :
        # 5-1. 그룹 생성
        group = create_group()
        # 5-2. 조화로움 계산
        value = calculate()
        # 5-3. 출력 변수 업데이트
        ans += value
        # 5-4. 회전
        if i < 3 : rotate()
    # 6. 결과 출력
    print(ans)