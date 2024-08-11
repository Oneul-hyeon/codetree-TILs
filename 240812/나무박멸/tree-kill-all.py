import sys

# 1. 전체 나무 성장 함수 정의
def grow() :
    # 1-1. 성장 그루 수 계산 함수 정의
    def add_tree(x, y) :
        # 1-1-1. 카운트 변수 생성
        cnt = 0
        # 1-1-2.
        for dir_x, dir_y in [(-1, 0), (0, 1), (1, 0), (0, -1)] :
            nx, ny = x + dir_x, y + dir_y
            # 범위를 벗어나는 경우 예외 처리
            if nx < 0 or nx >= n or ny < 0 or ny >= n : continue
            # 인접 위치에 나무가 있을 경우 카운팅
            if graph[nx][ny] > 0 : cnt += 1
        # 1-1-3. 카운트 변수 반환
        return cnt
    # 1-2.
    for x in range(n) :
        for y in range(n) :
            # 1-2-1. 나무 성장
            if graph[x][y] > 0 :
                graph[x][y] += add_tree(x, y)

# 2. 나무 번식 함수 정의
def breeding() :
    # 2-1.칸 별 번식 함수 정의
    def breeding_(x, y) :
        # 2-1-1. 번식 칸 리스트 생성
        index = []
        # 2-1-2.
        for dir_x, dir_y in [(-1, 0), (0, 1), (1, 0), (0, -1)] :
            nx, ny = x + dir_x, y + dir_y
            # 범위를 벗어나는 경우 예외 처리
            if nx < 0 or nx >= n or ny < 0 or ny >= n : continue
            # 서브 그래프에 벽이나 다른 나무가 위치해 있지 않으면서 제초제가 뿌려지지 않은 경우
            if sub_graph[nx][ny] == 0 and herbicide[nx][ny] == 0 :
                # 번식 칸 리스트에 해당 인덱스 삽입
                index.append((nx, ny))
        # 2-1-3. 번식 나무 수 정의
        if index :
            cnt = sub_graph[x][y] // len(index)
            # 2-1-4.
            for nx, ny in index :
                # 번식
                graph[nx][ny] += cnt
    # 2-2. 서브 그래프 생성
    sub_graph = [line[:] for line in graph]
    # 2-3.
    for x in range(n) :
        for y in range(n) :
            # 2-3-1. 서브 그래프의 해당 위치에 나무가 있는 경우
            if sub_graph[x][y] > 0 :
                # 칸 별 번식 함수 실행
                breeding_(x, y)

# 3. 제초제 살포 위치 선정 함수 정의
def select_index() :
    # 3-1. 선정 위치 변수 생성
    final_x = final_y = 0
    # 3-2. 박멸되는 나무 수 생성
    max_remove_cnt = -int(1e9)
    # 3-3. 제초제 살포 위치 리스트 생성
    final_herbicide_index = []
    # 3-4.
    for x in range(n) :
        for y in range(n) :
            # 3-4-1. 현재 위치에 나무가 없는 경우 예외 처리
            if graph[x][y] <= 0 : continue
            # 3-4-2. 현재 위치에서 박멸될 나무 수 변수, 현재 위치에서 제초제 살포 위치 리스트 생성
            now_remove_cnt, now_herbicide_index = graph[x][y], [(x, y)]
            # 3-4-3.
            for dir_x, dir_y in [(-1, -1), (-1, 1), (1, 1), (1, -1)] :
                for multiple in range(1, k+1) :
                    nx, ny = x + dir_x * multiple, y + dir_y * multiple
                    # 범위를 벗어나는 경우 예외 처리
                    if nx < 0 or nx >= n or ny < 0 or ny >= n : break
                    # 해당 칸에 나무가 있을 경우
                    if graph[nx][ny] > 0 :
                        # 현재 위치에서 박멸될 나무 수 업데이트
                        now_remove_cnt += graph[nx][ny]
                        # 현재 위치에서 제초제 살포 위치 리스트 업데이트
                        now_herbicide_index.append((nx, ny))
                    # 해당 칸이 비었거나 벽이 있을 경우
                    else :
                        # 현재 위치에서 제초제 살포 위치 리스트 업데이트
                        now_herbicide_index.append((nx, ny))
                        # 현재 대각선 방향 이동 중단
                        break
            # 3-4-4. 현재 위치에 박멸될 나무가 더 많을 경우
            if max_remove_cnt < now_remove_cnt :
                # 선정 위치 변수 업데이트
                final_x, final_y = x, y
                # 박멸되는 나무 수 업데이트
                max_remove_cnt = now_remove_cnt
                # 제초제 살포 위치 리스트 업데이트
                final_herbicide_index = now_herbicide_index[:]
    # 3-5. 박멸되는 나무 수, 제초제 살포 위치 반환
    return max_remove_cnt, final_herbicide_index

# 4. 제초제 살포 함수 정의
def sprinkling(remove_cnt, herbicide_index) :
    global ans

    # 4-1. 총 박멸한 나무 수 업데이트
    ans += remove_cnt
    # 4-2.
    for x, y in herbicide_index :
        # 4-2-1. 제초제 살포
        herbicide[x][y] = c+1
        # 4-2-2. 해당 위치에 나무가 있을 경우 제거
        if graph[x][y] > 0 : graph[x][y] = 0

# 5. 제초제 잔량 업데이트 함수 정의
def update_herbicide() :
    # 5-1.
    for x in range(n) :
        for y in range(n) :
            # 제초제가 남아 있는 경우 업데이트
            if herbicide[x][y] : herbicide[x][y] -= 1

n, m, k, c = map(int, input().split())
graph = [list(map(int, input().split())) for _ in range(n)]

ans = 0
# 6. 제초제 리스트 생성
herbicide = [[ 0 for _ in range(n)] for _ in range(n) ]
# 7.
for _ in range(m) :
    # 7-1. 제초제 잔량 업데이트
    update_herbicide()
    # 7-2. 나무 성장
    grow()
    # 7-3. 번식
    breeding()
    # 7-4. 제초제 살포 위치 선정
    remove_cnt, herbicide_index = select_index()
    # 7-5. 제초제 살포
    sprinkling(remove_cnt, herbicide_index)
# 8. 결과 출력
print(ans)