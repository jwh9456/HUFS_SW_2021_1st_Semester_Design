
def straightsJoker(cards): #player가 조커를 가지고 있을 경우 straigth 가능한 수 알려주는 함수

    cards = sorted(cards, key=card_value) #카드 value 순으로 오름차순 정렬
    print(cards)
    num_cards = len(cards)
    retval = []

    #straight를 3장만 낼 수 있다고 정했기 때문에 3으로 고정이라 첫 for문 삭제

    if num_cards < 3:
        return retval

    for i in range(num_cards-2):
        if card_value(cards[i+2]) - card_value(cards[i]) + 1 == 3 and card_value(cards[i+2]) != 13: #조커 있지만 스트레이트인 경우
            retval.append(cards[i:i+3])
        if card_value(cards[i+1]) - card_value(cards[i]) + 1 == 3: #바로 옆이 2단계 위인 경우 조커 가운데로
            straight = []
            straight.append(cards[i])
            straight.append(cards[-1])
            straight.append(cards[i+1])
            retval.append(straight)
        if card_value(cards[i+1]) - card_value(cards[i]) + 1 == 2: #바로 옆이 한단계 위인 경우 조커가 양 옆에 올 수 있음
            if card_value(cards[i]) == 0:
                straight = []
                straight.append(cards[i])
                straight.append(cards[i + 1])
                straight.append(cards[-1])
                retval.append(straight)
            elif card_value(cards[i+1]) == 12:
                straight = []
                straight.append(cards[-1])
                straight.append(cards[i])
                straight.append(cards[i + 1])
                retval.append(straight)
            else:
                straight = []
                straight.append(cards[-1])
                straight.append(cards[i])
                straight.append(cards[i + 1])
                retval.append(straight)
                straight = []
                straight.append(cards[-1])
                straight.append(cards[i])
                straight.append(cards[i + 1])
                retval.append(straight)

    return retval
