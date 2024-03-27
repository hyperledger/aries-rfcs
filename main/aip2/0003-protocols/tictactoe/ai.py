import game
import random

def winnable_in_n_moves(line:list, cells, player:str):
    # Tells how many moves would get 3-in-a-row on a given
    # line, for a given player. Returns None if player
    # can't win, or 0 if player has already won.
    n = 3
    for i in line:
        cell = cells[i]
        if cell == player:
            n -= 1
        elif cell is None:
            pass
        else:
            return None
    return n

def next_move(g:game.Game, player:str, randomize=True):
    '''
    Return the best cell for the player to pick, given current
    game state--or None if the game has already been won.
    '''
    player = player.upper()
    turn = g.whose_turn()
    if turn and (player != turn):
        raise Exception("It isn't player %s's turn." % player)
    cells = g.cells
    # First, figure out which line each player is closest
    # to winning on. If someone already *has* won, then
    # return None.
    bests = ([4,None],[4,None])
    candidate_lines = game.LINES
    if randomize:
        candidate_lines = random.shuffle(candidate_lines[0:])
    for line in game.LINES:
        ns = [
            winnable_in_n_moves(line, cells, player),
            winnable_in_n_moves(line, cells, game.other_player(player))
        ]
        for i in [0,1]:
            n = ns[i]
            # If someone already won, there is no next move.
            if n == 0:
                return None
            # If this player can't win with this line, then it
            # can't be the basis for one of their best choices.
            if n is None:
                continue
            # If this line is closer to winning, or if it's
            # equally close to winning compared to a previously
            # seen line, but this one includes the center square
            # but the previous best does not, pick this line.
            if n < bests[i][0] or \
                    ((4 in line) and (n == bests[i][0]) and
                     (bests[i][1] is None or (4 not in bests[i][1]))):
               bests[i][0] = n
               bests[i][1] = line
    # First, prefer something on my best line that blocks
    # my opponent on their best line.
    choices = None
    if bests[0][1] and bests[1][1]:
        choices = [x for x in bests[0][1] if x in bests[1][1]]
    # If I can't do that, then see who's winning. If me,
    # play offense by staying one step ahead (moving toward
    # my win). If them, play defense by blocking them.
    if not choices:
        if bests[0][0] <= bests[1][0]:
            line = bests[0][1]
        else:
            line = bests[1][1]
        # If we get here and line is None, then there is no
        # way to win the game. Just pick a random cell that's
        # left.
        if not line:
            choices = [x for x in range(9) if cells[x] is None]
        else:
            choices = [line[x] for x in [0,1,2] if cells[line[x]] is None]
    # If the center cell is one of our choices, always pick it.
    # Otherwise, return first of equally good alternatives.
    if 4 in choices:
        choice = 4
    else:
        choice = random.choice(choices) if randomize else choices[0]
    return game.idx_to_key(choice)
