import sys
input = sys.stdin.readline

# 1. 술래와 도망자 간 거리 계산 함수 정의
def distance(x, y) :
    # 1-1. 거리 반환
    return abs(tagger_x - x) + abs(tagger_y - y)
# 2. 도망자 이동 함수 정의
def move_runaway() :
    # 2-1. 도망자 이동 함수 정의
    for runaway in runaways :
        x, y = information[runaway]["location"]
        # 2-1-1. 술래와의 거리가 3 초과일 경우 continue
        if distance(x, y) > 3 :
            continue
        # 2-1-2. 다음 위치 설정
        dir_x, dir_y = information[runaway]["dir"]
        nx, ny = x + dir_x, y + dir_y
        # 2-1-3. 맵을 벗어난 경우
        if nx < 1 or nx > n or ny < 1 or ny > n :
            # 방향 전환 후 다음 위치 재설정
            dir_x *= -1
            dir_y *= -1
            information[runaway]["dir"] = (dir_x, dir_y)
            nx, ny = x + dir_x, y + dir_y
        # 2-1-4. 다음 위치에 술래가 없는 경우
        if (nx, ny) != (tagger_x, tagger_y) :
            # 이동
            information[runaway]["location"] = (nx, ny)
            graph[(x, y)].remove(runaway)
            graph[(nx, ny)].append(runaway)
# 3. 시계 방향 회전 함수 정의
def mode_clockwise() :
    global mode, tagger_x, tagger_y, tagger_dir, cnt, rotate_cnt, how
    # 3-1. 마지막 라인에 있는 경우
    if tagger_y == 1 :
        # 3-1-1. 이동
        tagger_x -= 1
        # 3-1-2. (1, 1)에 도착한 경우
        if (tagger_x, tagger_y) == (1, 1) :
            # 모드 변경
            mode = "counterclockwise"
            # 방향 변경
            tagger_dir = 2
    # 3-2. 이외의 경우
    else :
        tagger_x += dirs[tagger_dir][0]
        tagger_y += dirs[tagger_dir][1]
        cnt += 1
        # 이동 방향이 틀어지는 지점일 경우 방향 변동
        if cnt == how :
            tagger_dir = (tagger_dir + 1) % 4
            # 이동 칸 수 증가 시
            rotate_cnt -= 1
            if rotate_cnt == 0 :
                rotate_cnt = 2
                if tagger_y != 1 : how += 1
            cnt = 0
# 4. 반시계 방향 함수 정의
def mode_counterclockwise() :
    global mode, tagger_x, tagger_y, tagger_dir, cnt, rotate_cnt, how
    # 4-1. 첫 라인에 있는 경우
    if tagger_x != n and tagger_y == 1 :
        # 4-1-1. 이동
        tagger_x += 1
        # 4-1-2. 첫 라인의 끝에 도달한 경우
        if tagger_x == n :
            tagger_dir -= 1
    # 4-2. 이외의 경우
    else :
        tagger_x += dirs[tagger_dir][0]
        tagger_y += dirs[tagger_dir][1]
        # 4-2-1. 중심 지점에 도착한 경우
        if (tagger_x, tagger_y) == (n // 2 + 1, n // 2 + 1) :
            # 모드 변경
            mode = "clockwise"
            # 방향 변경
            tagger_dir = 0
            rotate_cnt = 2
        # 4-2-2. 이외의 경우
        else :
            cnt += 1
            # 이동 방향이 틀어지는 지점일 경우 방향 변동
            if cnt == how :
                tagger_dir = (tagger_dir - 1) % 4
                # 이동 칸 수 증가 시
                rotate_cnt -= 1
                if rotate_cnt == 0 :
                    rotate_cnt = 2
                    if tagger_y != 1 : how -= 1
                cnt = 0
# 5. 시야 내 도망자 검거 함수
def checkmate() :
    global score
    # 5-1.
    for i in range(3) :
        # 5-1-1. 시야 인덱스 설정
        cx, cy = tagger_x + dirs[tagger_dir][0] * i, tagger_y + dirs[tagger_dir][1] * i
        # 5-1-2. 맵을 벗어나는 경우
        if cx < 1 or cx > n or cy < 1 or cy > n : break
        # 5-1-3. 해당 위치에 나무가 있을 경우
        try :
            if trees[(cx, cy)] : continue
        # 5-1-4. 해당 위치에 나무가 없을 경우
        except :
            # 해당 위치에 사람이 있을 경우
            for runaway in graph[(cx, cy)] :
                # 스코어 업데이트
                score += round
                # 남아있는 도망자 리스트 업데이트
                runaways.remove(runaway)
            else :
                graph[(cx, cy)] = []

# 6. 술래 이동 함수 정의
def move_tagger() :
    # 6-1. 술래 이동
    mode_clockwise() if mode == "clockwise" else mode_counterclockwise()
    # 6-2. 도망자 검거
    checkmate()

if __name__ == "__main__" :
    n, m, h, k = map(int, input().split())
    # 7. 도망자 정보 딕셔너리 생성
    # 8. 그래프 내 도망자 정보 생성
    information = {}
    graph = {}
    for i in range(1, n + 1) :
        for j in range(1, n + 1) :
            graph[(i, j)] = []
    for idx in range(m) :
        x, y, dir = map(int, input().split())
        information[idx] = {"location" : (x, y), "dir" : (0, 1)} if dir == 1 else {"location" : (x, y), "dir" : (1, 0)}
        graph[(x, y)].append(idx)
    # 9. 현재 남아있는 도망자 리스트 생성
    runaways = list(range(m))
    # 10. 나무 위치 정의
    trees = {}
    for _ in range(h) :
        trees[tuple(map(int, input().split()))] = True
    # 11. 술래 위치 정의
    tagger_x, tagger_y = n // 2 + 1, n // 2 + 1
    # 12. 술래 방향 변수 생성
    tagger_dir = 0
    # 13. 술래 회전 방향 변수 생성
    mode = "clockwise"
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    # 14. 시계 방향 이동 시
    cnt, rotate_cnt, how = 0, 2, 1
    score = 0
    # 15.
    for round in range(1, k+1) :
        # 15-1. 도망자 이동
        move_runaway()
        # 15-2. 술래 이동
        move_tagger()
        # 15-3. 도망자가 없을 경우 탈출
        if not runaways : break
    # 16. 결과 출력
    print(score)