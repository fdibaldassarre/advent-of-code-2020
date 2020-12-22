#!/usr/bin/env python3


from collections import deque


def read_input():
    with open("input") as hand:
        for line in hand:
            yield line.strip()


def read_decks():
    player_1 = list()
    player_2 = list()
    read_player_2 = False
    for line in read_input():
        if line == "":
            continue
        if line.startswith("Player"):
            if line == "Player 2:":
                read_player_2 = True
            continue
        else:
            if read_player_2:
                player_2.append(int(line))
            else:
                player_1.append(int(line))
    return deque(player_1), deque(player_2)


def play_combat(decks):
    player1, player2 = decks
    while len(player1) > 0 and len(player2) > 0:
        card1 = player1.popleft()
        card2 = player2.popleft()
        if card1 > card2:
            player1.extend([card1, card2])
        else:
            player2.extend([card2, card1])
    return player1 if len(player1) > 0 else player2


def compute_winner_score(winner):
    score = 0
    for pos, card in enumerate(winner):
        value = len(winner) - pos
        score += card * value
    return score


def compute_configuration(player1, player2):
    p1_ser = ",".join(map(str, player1))
    p2_ser = ",".join(map(str, player2))
    return "%s-%s", (p1_ser, p2_ser)


def play_combat_recursive(decks):
    player1, player2 = decks
    previous_configurations = set()
    while True:
        configuration = compute_configuration(player1, player2)
        if configuration in previous_configurations:
            player1_wins = True
            break
        previous_configurations.add(configuration)
        card1 = player1.popleft()
        card2 = player2.popleft()
        if len(player1) >= card1 and len(player2) >= card2:
            new_deck_1 = deque([player1[n] for n in range(card1)])
            new_deck_2 = deque([player2[n] for n in range(card2)])
            player1_wins_round, _ = play_combat_recursive((new_deck_1, new_deck_2))
        else:
            if card1 > card2:
                player1_wins_round = True
            else:
                player1_wins_round = False
        if player1_wins_round:
            player1.extend([card1, card2])
        else:
            player2.extend([card2, card1])
        # Check winner
        if len(player1) == 0:
            player1_wins = False
            break
        elif len(player2) == 0:
            player1_wins = True
            break
    return player1_wins, (player1, player2)


def solve1(decks):
    winner = play_combat(decks)
    return compute_winner_score(winner)


def solve2(decks):
    player1_wins, final_decks = play_combat_recursive(decks)
    player1, player2 = final_decks
    winner = player1 if player1_wins else player2
    return compute_winner_score(winner)


if __name__ == "__main__":
    decks = read_decks()
    solution1 = solve1(decks)
    print("Solution 1: %d" % solution1)
    decks = read_decks()
    solution2 = solve2(decks)
    print("Solution 2: %d" % solution2)
