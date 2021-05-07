from daifugo.game import DEBUG
import game
DEBUG = True


# 대부호 > 부호 > 빈민 > 평민
class _player:
    def __init__(self, 이름, 계급, 점수):
        self.이름 = 이름
        self.계급 = 계급
        self.점수 = 점수

    def set_score(self, winner):
        if winner[0].이름 == self.이름:
            self.점수 += 5
        elif winner[1].이름 == self.이름:
            self.점수 += 3
        elif winner[2].이름 == self.이름:
            self.점수 += 1
        elif winner[3].이름 == self.이름:
            self.점수 += 0

    def set_rank(self, winner):
        if winner[0].이름 == self.이름:
            self.계급 = "대부호"
        elif winner[1].이름 == self.이름:
            self.계급 = "부호"
        elif winner[2].이름 == self.이름:
            self.계급 = "평민"
        elif winner[3].이름 == self.이름:
            self.계급 = "빈민"

A = _player('A', '평민', 0)
B = _player('B', '평민', 0)
C = _player('C', '평민', 0)
D = _player('D', '평민', 0)

players = (A, B, C, D)
max = 0
round = 1

while (max < 18):
    if DEBUG: print("::::::::::대부호 게임 시작::::::::::\n")
    if DEBUG: print(round, "round를 시작하겠습니다\n")
    result = game.play_game(players)

    if DEBUG: print("게임이 종료되었습니다.\n")
    if DEBUG: print("\n----- 게임의 결과 -----\n")

    for i in range(4):
        _player.set_score(players[i], result)
        _player.set_rank(players[i], result)

    if DEBUG:print("{0}의 점수 = {1}, {2}의 계급 = {3}".format('A', A.점수, 'A', A.계급))
    if DEBUG:print("{0}의 점수 = {1}, {2}의 계급 = {3}".format('B', B.점수, 'B', B.계급))
    if DEBUG:print("{0}의 점수 = {1}, {2}의 계급 = {3}".format('C', C.점수, 'C', C.계급))
    if DEBUG:print("{0}의 점수 = {1}, {2}의 계급 = {3}".format('D', D.점수, 'D', D.계급))
    if DEBUG:print()

    for i in range(4):
        if players[i].점수 >= max:
            max = players[i].점수

    if DEBUG:print("최대 값:{0}\n".format(max))
    round += 1

if DEBUG:print("   대부호 게임 끝   ")
