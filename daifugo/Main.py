import game as g
import common as c
import interactive as playerInstance


print("######## 대부호 카드 게임 시작 ########")

while 1 :
    print("게임을 시작합니다.")
    print(g.get_deck())
    print("패를 생성합니다.")
    deal = g.deal()
    g.play_game(4)
    # print(deal)
    # i = 1
    # for hands in deal :
    #     print("player {0}의 핸드 손패 : {1}".format(i,hands))
    #     if '3D' in hands : print("player {0}가 먼저 시작합니다.".format(i))
    #     i += 1
    break;




# testset=['3H','4H','5H','7H','8H','9C','8C','2H','BB']

# print(g.deal(4))
# print(c.generate_plays(testset))