import sys
input = sys.stdin.readline

# 1. 토끼 선정 함수 정의
def select_rabbit() :
    # 1-1 우선 순위 토끼 번호 반환
    return sorted(rabbit.values(), key = lambda x : [x[4], (x[1] + x[2]), x[1], x[2], x[0]])[0][0]
# 2. 토끼 방향 선정 함수 정의
def select_rabbit_dir(pid) :
    x, y, d = rabbit[pid][1:4]
    # 2-1. 방향 별 다음 위치 리스트 생성
    next_index = []
    # 2-2. 
    for i in range(4) :
        # 2-2-1. 상하로 움직이는 경우
        if i < 2 :
            ny = y
            # 남은 칸 계산
            mod = x - 1 if i == 0 else n - x
            # 가야 하는 칸 계산
            step = d % (2 * (n-1))
            # 남은 칸 >= 가야 하는 칸
            if mod >= step :
                nx = x + step * dirs[i][0]
            # 이외의 경우
            else :
                step -= mod
                # 위쪽 방향인 경우
                if i == 0 : nx = 1 + step if step <= n - 1 else n - (step - (n - 1))
                # 아래쪽 방향인 경우
                else : nx = n - step if step <= n - 1 else 1 + (step - (n - 1))
        # 2-2-2. 좌우로 움직이는 경우
        else :
            nx = x
            # 남은 칸 게산
            mod = y - 1 if i == 2 else m - y
            # 가야 하는 칸 계산
            step = d % (2 * (m-1))
            # 남은 칸 >= 가야 하는 칸
            if mod >= step :
                ny = y + step * dirs[i][1]
            # 이외의 경우
            else :
                step -= mod
                # 왼쪽 방향인 경우
                if i == 2 : ny = 1 + step if step <= m - 1 else m - (step - (m - 1))
                # 오른쪽 방향인 경우
                else : 
                    ny = m - step if step <= m - 1 else 1 + (step - (m))
        next_index.append((nx, ny))
    # 2-3. 우선 순위에 따른 다음 위치 반환
    fx, fy = sorted(next_index, key = lambda x : [-(x[0] + x[1]), -x[0], -x[1]])[0]
    rabbit[pid][1], rabbit[pid][2] = fx, fy
    # return sorted(next_index, key = lambda x : [-(x[0] + x[1]), -x[0], -x[1]])[0]
# 3. 토끼 점수 획득 함수 정의
def get_score(pid) :
    add = sum(rabbit[pid][1:3])
    # 3-1. 선택된 토끼를 제외한 나머지 토끼 점수 획득
    for id in rabbit.keys() :
        if id != pid : 
            rabbit[id][5] += add 
# 4. 토끼 이동 함수 정의
def move() :
    # 4-1. 토끼 선정
    pid = select_rabbit()
    # 4-2. 토끼 이동
    select_rabbit_dir(pid)
    # 4-3. 선정된 토끼 점프 횟수 업데이트
    rabbit[pid][4] += 1
    # 4-4. 해당 경주에 점프한 토끼 리스트 업데이트
    if pid not in potential : potential.append(pid)
    # 4-5. 토끼 점수 획득
    get_score(pid)
# 5. 토끼 이동거리 변경 함수 정의
def correction(pid, l) :
    # 5-1. 토끼 이동거리 변경
    rabbit[pid][3] *= l
# 6. 추가 점수 부여 함수 정의
def get_additional_score() :
    # 6-1. 추가 점수를 부여받은 토끼의 정보 리스트 생성
    potential_rabbit_info = [value for key, value in rabbit.items() if key in potential]
    # 6-2. 추가 점수를 부여
    pid = sorted(potential_rabbit_info, key = lambda x : [-(x[1] + x[2]), -x[1], -x[2], -x[0]])[0][0]
    rabbit[pid][5] += s
# 7. 최고의 토끼 선정 함수 정의
def winner() :
    # 7-1. 최고점 반환
    return max(list(zip(*rabbit.values()))[5])

if __name__ == "__main__" :
    q = int(input())
    START, RACE, CHANGE, END = 100, 200, 300, 400
    # 방향 정보 리스트 생성
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for _ in range(q) :
        command = list(map(int, input().split()))
        # 시작 명령인 경우
        if command[0] == START :
            n, m, p = command[1:4]
            # 토끼 정보 딕셔너리 생성
            rabbit = {}
            for i in range(4, len(command), 2) :
                pid, d = command[i:i+2]
                rabbit[pid] = [pid, 1, 1, d, 0, 0]
        # 경주 진행 명령인 경우
        elif command[0] == RACE :
            k, s = command[1:]
            potential = []
            #
            for _ in range(k) :
                # 경주 진행
                move()
            # 추가 점수 부야
            get_additional_score()
        # 이동 거리 변경 명령인 경우
        elif command[0] == CHANGE :
            pid, l = command[1:]
            correction(pid, l)
        # 최고의 토끼 선정 함수일 경우
        else :
            print(winner())