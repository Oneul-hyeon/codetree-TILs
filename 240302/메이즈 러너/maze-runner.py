import sys
input = sys.stdin.readline

# 1. 방향 설정 함수 정의
def target_direction(x, y) :
    # 1-1. 최소 방향, 최소 거리 변수 생성
    dir, updated_dist = 0, abs(x - exit[0]) + abs(y - exit[1])
    # 1-2.
    for d in range(1, 5):
        dir_x, dir_y = dirs[d][0], dirs[d][1]
        # 1-2-1. 다음 위치 설정
        nx, ny = x + dir_x, y + dir_y
        # 1-2-2. 예외 처리
        if nx < 0 or nx >= n or ny < 0 or ny >= n : continue
        if graph[nx][ny] != 0 : continue
        # 1-2-3. 거리 계산
        dist = abs(nx - exit[0]) + abs(ny - exit[1])
        # 1-2-4. 정보 업데이트
        if updated_dist > dist : dir, updated_dist = d, dist
    # 1-3. 방향 반환
    return dir
# 2. 이동 함수 정의
def move() :
    global cnt, information
    updated_information = []
    # 2-1.
    for info in information :
        # 2-1-1. 최단 방향 탐색
        dir = target_direction(info[0], info[1])
        nx, ny = info[0] + dirs[dir][0], info[1] + dirs[dir][1]
        # 2-1-2. 이동
        # 2-1-3. 출구에 도달한 경우
        if [nx, ny] != exit :
            updated_information.append([nx, ny])
        # 2-1-4. 이동 거리 카운팅
        if dir : cnt += 1
    information = updated_information[:]
# 3. 미로 선정 함수 정의
def find_maze() :
    # 3-1.
    for l in range(1, n+1) :
        for r in range(n-l+1) :
            for c in range(n-l+1) :
                # 3-1-1. 정사각형의 우측 하단 위치 구하기
                er, ec = r + l, c + l
                # 3-1-2. 출구가 포함되지 않았다면 continue
                if r <= exit[0] <= er and c <= exit[1] <= ec :
                    # 3-1-3.
                    for x, y in information :
                        if r <= x <= er and c <= y <= ec :
                            # 참가자가 1명이라도 포함된 경우 l, r, c 반환
                            return l, r, c
# 4. 회전 함수 정의
def rotate() :
    global exit
    state = False
    # 4-1. 회전시킬 미로 구하기
    l, r, c = find_maze()
    # 4-2. 회전
    sub_graph = [line[:] for line in graph]
    sub_information = information[:]
    for x in range(r, r+l+1) :
        for y in range(c, c+l+1) :
            ox, oy = x - r, y - c
            nx, ny = oy, l - ox
            ex, ey = nx + r, ny + c
            # 내구도 감소
            graph[ex][ey] = sub_graph[x][y] - 1 if sub_graph[x][y] else sub_graph[x][y]
            # 출구 변수 업데이트
            if [x, y] == exit and not state:
                exit = [ex, ey]
                state = True
            # 참가자 정보 업데이트
            for i, info in enumerate(sub_information) :
                if info == [x, y] :
                    information[i] = [ex, ey]

if __name__ == "__main__" :
    n, m, k = map(int, input().split())
    dirs = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]
    cnt = 0
    # 5. 그래프 생성
    graph = [list(map(int, input().split())) for _ in range(n)]
    # 6. 참가자 정보 딕셔너리 생성
    information = []
    for _ in range(m) :
        x, y = map(int, input().split())
        information.append([x-1, y-1])
    exit = list(map(int, input().split()))
    exit[0] -= 1
    exit[1] -= 1
    # 7.
    for _ in range(k) :
        # 7-1. 참가자 이동
        move()
        # 7-2. 모든 참가자가 미로 탈출 시 결과 출력
        if not information : break
        # 7-3. 미로 회전
        rotate()
    # 8. 결과 출력
    print(f'{cnt}\n{exit[0] + 1} {exit[1] + 1}')