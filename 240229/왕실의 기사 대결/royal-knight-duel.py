import sys
from collections import deque
input = sys.stdin.readline

# 1. 기사 이동 가능 여부 함수 정의
def check(x1, y1, x2, y2) :
    # 1-1. 그래프를 벗어나는 경우(벽인 경우) False 반환
    if x1 < 1 or y1 < 1 or x2 > N - 1 or y2 > M - 1: return False
    # 1-2.
    for x in range(x1, x2 + 1) :
        for y in range(y1, y2 + 1) :
            # 해당 위치가 벽일 경우 False 반환
            if graph[x][y] == 2 : return False
    # 1-3. True 반환
    return True
# 2. 이동 함수 정의
def move(target, info, knight_graph, dir) :
    # 2-1. 업데이트용 딕셔너리, 조정이 필요한 기사 리스트, 밀려난 기사 번호 리스트 생성
    updated_info = info.copy()
    need = deque([target])
    array = []
    # 2-2.
    while need :
        # 2-2-1. 조정이 필요한 기사 꺼내기
        knight = need.popleft()
        x, y, h, w, k = info[knight]
        # 2-2-2. 기사 이동
        x1, y1, x2, y2 = x + dirs[dir][0], y + dirs[dir][1], x + h - 1 + dirs[dir][0], y + w - 1 + dirs[dir][1]
        # 2-2-3. 기사의 이동 위치가 벽일 경우 (False, 기존의 기사 정보 딕셔너리, 기사 위치 그래프, None 반환)
        if not check(x1, y1, x2, y2) : return [False, info, knight_graph, None]
        # 2-2-4. 기사 정보 업데이트
        updated_info[knight] = [x1, y1, h, w, k]
        # 2-2-5. 이동 위치에 다른 기사가 있을 경우
        for i in range(x1, x2+1) :
            for j in range(y1, y2+1) :
                if knight_graph[i][j] not in [0, knight] and knight_graph[i][j] not in need :
                    # 정보 업데이트
                    need.append(knight_graph[i][j])
                    array.append(knight_graph[i][j])
    # 2-3. 기사 위치 그래프 업데이트
    knight_graph = [[0 for _ in range(M)] for _ in range(N)]
    for knight in updated_info.keys() :
        x, y, h, w, k = updated_info[knight]
        x1, y1, x2, y2 = x, y, x + h - 1, y + w - 1
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                knight_graph[i][j] = knight
    # 2-4. (True, 업데이트된 기사 정보 딕셔너리, 밀려난 기사 번호 리스트 반환)
    return [True, updated_info, knight_graph, array]
# 3. 데미지 함수 정의
def damage(info, knight_graph, array) :
    # 3-1.
    for key in array :
        r, c, h, w, k = info[key]
        cnt = 0
        # 3-1-1. 함정 갯수 체크
        for i in range(r, r+h) :
            for j in range(c, c+w) :
                if graph[i][j] == 1 : cnt += 1
        # 3-1-2. 함정 갯수가 현재 체력보다 같거나 많을 경우 딕셔너리 정보 삭제
        if cnt >= k :
            for i in range(r, r+h) :
                for j in range(c, c+w) :
                    knight_graph[i][j] = 0
            del info[key]
        # 3-1-3. 이외의 경우 체력 감소
        else : info[key][-1] -= cnt
    # 3-2. 정보 반환
    return info, knight_graph
# 4. 명령 수행 함수 정의
def carryout(target, info, knight_graph, dir) :
    # 4-1. 이동
    change, info, knight_graph, array = move(target, info, knight_graph, dir)
    # 4-2. 이동한 경우 데미지 계산
    if change : info, knight_graph = damage(info, knight_graph, array)
    # 4-3. 기사 정보, 기사 위치 정보 반환
    return info, knight_graph

if __name__ == "__main__" :
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    l, n, q = map(int, input().split())
    # 5. 그래프 생성
    graph = [[0]] + [[0] + list(map(int, input().split())) for _ in range(l)]
    # 6. 기사 정보 딕셔너리 생성
    info = dict()
    for i in range(1, n+1) :
        info[i] = list(map(int, input().split()))
    N, M = len(graph), len(graph[-1])
    stand = info.copy()
    # 7. 기사 위치 그래프 생성
    knight_graph = [[0 for _ in range(M)] for _ in range(N)]
    for key in info.keys() :
        r, c, h, w, k = info[key]
        for i in range(r, r+h) :
            for j in range(c, c+w) :
                knight_graph[i][j] = key
    # 8.
    for _ in range(q) :
        target, dir = map(int, input().split())
        try :
            if info[target]:
                # 8-1. 명령 수행
                info, knight_graph = carryout(target, info, knight_graph, dir)
        except : pass
    # 9. 결과 출력
    ans = 0
    for knight in info.keys() : ans += stand[knight][-1] - info[knight][-1]
    print(ans)