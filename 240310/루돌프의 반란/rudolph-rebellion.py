import sys
input = sys.stdin.readline

# 1. 루돌프와 산타의 최소 거리 계산 함수 정의
def calculate_dist(who) :
    target_x, target_y = santa[who]["idx"]
    # 1-1. 거리, 방향 변수 생성
    update_dist, update_dir = float("INF"), 0
    # 1-2.
    for dir, (dir_x, dir_y) in enumerate(dirs_r) :
        nrr, nrc = rr + dir_x, rc + dir_y
        # 1-2-1. 거리 계산
        dist = (nrr - target_x)**2 + (nrc - target_y)**2
        # 1-2-1. 거리가 가까워질 경우 거리, 방향 변수 업데이트
        if dist < update_dist :
            update_dist, update_dir = dist, dir
    # 1-3. 거리, 방향 반환
    return update_dir
# 2. 루돌프 이동 함수 정의
def move_roodolph() :
    global rr, rc
    # 2-1. 최종 이동 방향, 거리, 최종 타겟 인덱스 변수 생성
    target = -1
    target_x, target_y = -1, -1
    update_dist = float("INF")
    # 2-2. 산타 타겟 설정
    for who in santa.keys() :
        x, y = santa[who]["idx"]
        # 2-2-1. 거리 계산
        dist = (rr - x)**2 + (rc - y)**2
        # 2-2-2. 거리 업데이트
        if dist <= update_dist :
            x, y = santa[who]["idx"]
            # 거리가 같을 경우 산타의 위치에 따라 업데이트
            if dist == update_dist :
                if target_x <= x :
                    if (target_x < x) or (target_x == x and target_y < y) :
                        target = who
                        target_x, target_y = x, y
            else :
                target = who
                target_x, target_y = x, y
                update_dist = dist
    # 2-3. 루돌프 이동 방향 설정
    dir = calculate_dist(target)
    # 2-4. 루돌프 이동
    nrr, nrc = rr + dirs_r[dir][0], rc + dirs_r[dir][1]
    # 2-5. 해당 위치에 산타가 있을 경우
    if graph[nrr][nrc] :
        # 2-5-1. 산타 기절 업데이트
        santa[graph[nrr][nrc]]["faint_stack"] = 2
        # 2-5-2. 충돌 시 산타 이동 함수 실행
        smash("r2s", graph[nrr][nrc], dir)
    graph[rr][rc] = 0
    graph[nrr][nrc] = -1
    rr, rc = nrr, nrc
# 3. 산타의 이동 방향 결정 함수 정의
def select_dir(who) :
    x, y = santa[who]["idx"]
    # 3-1. 거리, 방향 변수 생성
    update_dist, update_dir = (rr - x) ** 2 + (rc - y) ** 2, -1
    # 3-2.
    for dir, (dir_x, dir_y) in enumerate(dirs_s) :
        # 3-2-1. 다음 방향 설정
        nx, ny = x + dir_x, y + dir_y
        # 3-2-2. 예외 처리
        if nx < 0 or nx >= n or ny < 0 or ny >= n or graph[nx][ny] > 0: continue
        # 3-2-3. 거리 계산
        dist = (rr - nx)**2 + (rc - ny)**2
        # 3-2-4. 거리 업데이트
        if dist < update_dist :
            update_dist, update_dir = dist, dir
    # 3-3. 방향 반환
    return update_dir
# 4. 산타 이동 함수 정의
def move_santa() :
    # 4-1.
    for who in sorted(list(santa.keys())) :
        try :
            # 4-1-1. 산타 기절 시 continue
            if santa[who]["faint_stack"] :
                santa[who]["faint_stack"] -= 1
                continue
            # 4-1-2. 산타 이동 방향 선정
            dir = select_dir(who)
            x, y = santa[who]["idx"]
            if dir != -1 :
                nx, ny = x + dirs_s[dir][0], y + dirs_s[dir][1]
            else :
                nx, ny = x, y
            # 4-1-3. 이동 위치에 루돌프가 있는 경우
            if (nx, ny) == (rr, rc) :
                # 산타 기절 업데이트
                santa[who]["faint_stack"] = 1
                # 충돌 시 산타 이동 함수 실행
                smash("s2r", who, dir)
            # 4-1-4. 이외의 경우 산타 이동
            else :
                graph[x][y], graph[nx][ny] = 0, who
                santa[who]["idx"] = [nx, ny]
        except : pass
# 5. 충돌 시 산타 이동 함수 정의
def smash(way, who, dir) :
    x, y = santa[who]["idx"]
    # 5-1. 산타 점수 획득
    santa[who]['score'] += c if way == "r2s" else d
    # 5-2. 튕겨져 나갈 방향 설정
    if way == "r2s" :
        dir_x, dir_y = dirs_r[dir][0], dirs_r[dir][1]
    else :
        new_dir = (dir + 2) % len(dirs_s)
        dir_x, dir_y = dirs_s[new_dir][0], dirs_s[new_dir][1]
    # 5-3. 튕겨져 나갈 거리 설정
    how = c+1 if way == 'r2s' else d
    # 5-4. 튕겨진 위치 구하기
    santa[who]["idx"] = [x + dir_x * (how - 2), y + dir_y * (how - 2)]
    next = who
    # 5-5.
    while True :
        # 5-5-1. 다음 위치 정의
        mx, my = santa[next]["idx"][0], santa[next]["idx"][1]
        nx, ny = mx + dir_x, my + dir_y
        # 5-5-2. 다음 위치가 맵을 벗어날 경우
        if nx < 0 or nx >= n or ny < 0 or ny >= n :
            # 그래프 업데이트
            if who == next :
                graph[x][y] = 0
            else :
                graph[mx][my] = 0
            # 게임 탈락 처리
            leaving_out(who)
            # while문 탈출
            break
        # 5-5-3. 그래프 업데이트
        if who == next:
            graph[x][y] = 0
        else:
            graph[mx][my] = 0
        # 5-5-4. 산타 정보 업데이트
        santa[who]["idx"] = [nx, ny]
        # 5-5-5. 다른 산타가 있는 경우
        if graph[nx][ny] :
            # 다음 처리되어야 할 산타 지정
            next = graph[nx][ny]
            # 그래프 업데이트
            graph[nx][ny] = who
        # 5-5-6. 다음 위치에 아무도 없는 경우
        else :
            # 그래프 업데이트
            graph[nx][ny] = who
            # while문 탈출
            break
        who = next
# 6. 게임 탈락 처리 함수 정의
def leaving_out(who) :
    # 6-1. 해당 산타의 최종 점수 등록
    final_score[who] = santa[who]["score"]
    # 6-2. 산타 정보 제거
    del santa[who]
# 7, 추가 점수 부여 함수 정의
def give_extra_points() :
    # 7-1.
    for who in santa.keys() :
        # 추가 점수 부여
        santa[who]["score"] += 1

if __name__ == "__main__" :
    n, m, p, c, d = map(int, input().split())
    # 8. 그래프 생성
    graph = [[0 for _ in range(n)] for _ in range(n)]
    rr, rc = map(int, input().split())
    rr -= 1
    rc -= 1
    graph[rr][rc] = -1
    # 9. 산타 정보 생성
    santa = dict()
    for _ in range(1, p+1) :
        pn, sr, sc = map(int, input().split())
        santa[pn] = {"faint_stack" : 0, "idx" : [sr-1, sc-1], "score" : 0}
        graph[sr-1][sc-1] = pn
    # 10. 루돌프 이동 방향 변수 생성
    dirs_r = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    # 11. 산타 이동 방향 변수 생성
    dirs_s = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    # 12. 최종 점수 리스트 생성
    final_score = [0 for _ in range(p+1)]
    # 13.
    for _ in range(m) :
        # 13-1. 루돌프 이동
        move_roodolph()
        # 13-2. 산타 이동
        move_santa()
        # 13-3. 게임 종료 여부 판단
        if not santa : break
        # 13-4. 추가 점수 부여
        give_extra_points()
    # 14. 최종 점수 리스트 업데이트
    for who in santa.keys() :
        final_score[who] = santa[who]["score"]
    # 15. 결과 출력
    print(*final_score[1:])