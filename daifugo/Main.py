#import daifugo.game as g
import daifugo.common as c
import players.interactive as playerInstance


print("######## 대부호 카드 게임 시작 ########")




testset=['3H','4H','5H','7H','8H','9C','8C','2H','BB']


print(c.generate_plays(testset))