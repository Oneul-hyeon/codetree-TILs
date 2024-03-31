import sys
from collections import deque
input = sys.stdin.readline

# 1. 공격자 선정 함수
def select_attacker() :
    # 1-1. 부서지지 않은 포탑 중 공격력이 가장 낮은 포탑 선정
    low_power = []
    power = int(1e9)
    for idx, info in turret.items() :
        if not low_power or power > info["power"] :
            low_power = [idx]
            power = info["power"]
        elif power == info["power"] :
            low_power.append(idx)
    # 1-2. 포탑이 1개일 경우 공격자 선정
    if len(low_power) == 1 : return low_power[0]
    # 1-3. 걸러진 포탑 중 가장 최근에 공격한 포탑 선정
    recent_attack = []
    time = -int(1e9)
    for idx in low_power :
        if not recent_attack or time < turret[idx]["time"] :
            recent_attack = [idx]
            time = turret[idx]["time"]
        elif time == turret[idx]["time"] :
            recent_attack.append(idx)
    # 1-4. 포탑이 1개일 경우 공격자 선정
    if len(recent_attack) == 1 : return recent_attack[0]
    # 1-5. 걸러진 포탑 중 행 + 열의 합이 큰 포탑 선정
    max_sum = []
    sum = -int(1e9)
    for idx in recent_attack :
        if not max_sum or sum < idx[0] + idx[1] :
            max_sum = [idx]
            sum = idx[0] + idx[1]
        elif sum == idx[0] + idx[1] :
            max_sum.append(idx) 
    # 1-6. 포탑이 1개일 경우 공격자 선정
    if len(max_sum) == 1 : return max_sum[0]
    # 1-7. 열 값이 가장 큰 포탑 공격자 선정
    return sorted(max_sum, key = lambda x : -x[1])[0]
# 2. 공격 대상자 선정 함수
def select_target(attacker) :
    # 2-1. 부서지지 않은 포탑 중 공격력이 가장 높은 포탑 선정
    max_power = []
    power = -int(1e9)
    for idx, info in turret.items() :
        if idx == attacker : continue
        if not max_power or power < info["power"] :
            max_power = [idx]
            power = info["power"]
        elif power == info["power"] :
            max_power.append(idx)
    # 2-2. 포탑이 1개일 경우 공격 대상 선정
    if len(max_power) == 1 : return max_power[0]
    # 2-3. 걸러진 포탑 중 가장 나중에 공격한 포탑 선정
    later_attack = []
    time = int(1e9)
    for idx in max_power :
        if not later_attack or time > turret[idx]["time"] :
            later_attack = [idx]
            time = turret[idx]["time"]
        elif time == turret[idx]["time"] :
            later_attack.append(idx)
    # 2-4. 포탑이 1개일 경우 공격 대상자 선정
    if len(later_attack) == 1 : return later_attack[0]
    # 2-5. 걸러진 포탑 중 행 + 열의 합이 작은 포탑 선정
    min_sum = []
    sum = int(1e9)
    for idx in later_attack :
        if not min_sum or sum > idx[0] + idx[1] :
            min_sum = [idx]
            sum = idx[0] + idx[1]
        elif sum == idx[0] + idx[1] :
            min_sum.append(idx) 
    # 2-6. 포탑이 1개일 경우 공격 대상자 선정
    if len(min_sum) == 1 : return min_sum[0]
    # 2-7. 열 값이 가장 작은 포탑 공격 대상자 선정
    return sorted(min_sum, key = lambda x : x[1])[0]
# 3. 레이저 공격 함수
def laser_attack_range(attacker, target) :
    global graph, turret
    x, y = attacker
    state = False
    # 3-1. 큐 생성 후 현재 위치 삽입
    queue = deque()
    queue.append((x, y))
    # 3-2. 경로 추적 리스트 생성
    route = [[False for _ in range(m)] for _ in range(m)]
    # 3-2.
    while queue :
        # 3-2-1. 위치 인덱스 반환
        x, y = queue.popleft()
        # 3-2-2.
        for dir_x, dir_y in [(0, 1), (1, 0), (0, -1), (-1, 0)] :
            # 다음 위치 설정
            nx, ny = (x + dir_x) % n, (y + dir_y) % m
            # 다음 위치가 부서지지 않은 포탑이면서 방문하지 않은 경우
            if graph[nx][ny] and not route[nx][ny] :
                # 경로 입력
                route[nx][ny] = (x, y)
                # 목표 타겟에 도달한 경우
                if (nx, ny) == target :
                    state = True
                    break
                # 큐에 다음 위치 삽입
                queue.append((nx, ny))
        # 3-2-3. 레이저 공격이 가능한 경우 while문 탈출
        if state : True
    # 3-3. 레이저 공격이 가능한 경우 포탑 공격
    if state :
        # 3-3-1. 공격 연관 포탑 리스트 생성
        attack_related_turret = [attacker]
        nx, ny = target
        # 3-3-2. 공격력 변수 생성
        power = turret[attacker]["power"]
        # 3-3-3. 
        while (nx, ny) != attacker :
            # 공격 연관 포탑 리스트 업데이트
            attack_related_turret.append((nx, ny))
            # 타겟 혹은 타겟 주변 포탑에 따른 공격력 설정
            if (nx, ny) == target : now_power = power
            else : now_power = power // 2
            # 포탑 공격
            graph[nx][ny] = graph[nx][ny] - now_power if graph[nx][ny] > now_power else 0
            if graph[nx][ny] : turret[(nx, ny)]["power"] -= now_power
            else : del turret[(nx, ny)]
            nx, ny = route[nx][ny]
        # 3-3-4. True 반환
        return attack_related_turret
    # 3-4. False 반환
    return False
# 4. 포탄 공격 범위 함수
def shell_attack_range(attacker, target) :
    global graph, turret
    x, y = target[0], target[1]
    # 4-1. 공격 연관 포탑 리스트 생성
    attack_related_turret = [attacker]
    # 4-2. 
    for dir_x, dir_y in [(0, 0), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)] :
        nx, ny = (x + dir_x) % n, (y + dir_y) % m
        # 4-2-1. 공격자가 아니면서 부서지지 않은 포탑인 경우
        if (nx, ny) != attacker and graph[nx][ny] :
            # 공격 연관 포탑 리스트 업데이트
            attack_related_turret.append((nx, ny))
            # 공격력 변수 생성
            power = turret[attacker]["power"]
            # 타겟 혹은 타겟 주변 포탑에 따른 공격력 설정
            if (nx, ny) == target : now_power = power
            else : now_power = power // 2
            # 포탑 공격
            graph[nx][ny] = graph[nx][ny] - now_power if graph[nx][ny] > now_power else 0
            if graph[nx][ny] : turret[(nx, ny)]["power"] -= now_power
            else : del turret[(nx, ny)]
    # 4-3.
    return attack_related_turret
# 5. 공격 함수
def attack(attacker, target) :
    # 5-1. 레이저 공격
    attack_related_turret = laser_attack_range(attacker, target)
    # 5-2. 레이저 공격이 불가능할 경우 포탄 공격
    if not attack_related_turret : attack_related_turret = shell_attack_range(attacker, target)
    # 5-3. 공격 연관 포탑 리스트 반환
    return attack_related_turret
# 6. 포탑 정비 함수 정의
def turret_maintenance(attacker, target, attack_related_turret) :
    global graph, turret
    # 6-1. 
    for idx, info in turret.items() :
        # 6-1-1. 공격과 관련있는 포탑의 경우 continue
        if idx in attack_related_turret : continue
        # 6-1-2. 포탑 정비
        x, y = idx
        graph[x][y] += 1
        turret[idx]["power"] += 1
    
if __name__ == "__main__" :
    n, m, k = map(int, input().split())
    graph = [list(map(int, input().split())) for _ in range(n)]
    # 7. 활성화 포탑 딕셔너리 생성
    turret = {}
    for i in range(n) :
        for j in range(m) :
            if graph[i][j] :
                turret[(i, j)] = {"power" : graph[i][j], "time" : 0}
    attacker = select_attacker()
    target = select_target(attacker)
    # 8. 
    for t in range(1, k+1) :
        # 8-1. 공격자 선정
        attacker = select_attacker()
        # 8-2. 공격 대상자 선정
        target = select_target(attacker)
        # 8-3. 공격자 공격력 상승
        turret[attacker]["power"] += n + m
        graph[attacker[0]][attacker[1]] += n + m
        # 8-4. 공격자 공격 시간 업데이트
        turret[attacker]["time"] = t
        # 8-5. 공격
        attack_related_turret = attack(attacker, target)
        # 8-6. 포탑 정비
        turret_maintenance(attacker, target, attack_related_turret)
        # 8-7. 포탑이 1개 남은 경우 for문 탈출
        if len(turret.keys()) == 1 : break
    # 9. 결과 출력
    ans = -int(1e9)
    for info in turret.values() :
        ans = max(ans, info["power"])
    print(ans)