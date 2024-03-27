import re

import game
import ai

MOVE_MSG_TYPE = 'did:sov:SLfEi9esrjzybysFxQZbfq;spec/tictactoe/1.0/move'
RESULTS_MSG_TYPE = 'did:sov:SLfEi9esrjzybysFxQZbfq;spec/tictactoe/1.0/results'

TYPES = [
    MOVE_MSG_TYPE,
    RESULTS_MSG_TYPE
]

def load_game(moves):


def handle(wc, agent):
    try:
        t = wc.obj['@type']
        if t == MOVE_MSG_TYPE:
            them = wc.obj.get('ill_be', '')
            if them and isinstance(them, str) and len(them) == 1 and them in 'XO':
                them = them.strip().upper()
            else:
                raise Exception('Expected "ill_be" to contain either "X" or "O".')
            moves = wc.obj.get('moves', [])
            if not isinstance(moves, list) or len(moves) > 9:
                raise Exception('Expected "moves" to be a list of at most 9 items.')
            g = game.Game()
            g.load(moves)
            w = g.winner()
            if w:
                agent.trans.send('{"@type": "result", "outcome": "%s won."}')
            me = game.other_player(them)
            if g.whose_turn()

            if them == 'X':
                g.load(wc.obj['moves'])
                choice = ai.next_move(g, me)
                g[choice] = me
            agent.trans.send('{"@type": "%s"}' % MOVE_MSG_TYPE, wc.sender)
    except Exception as e:
        agent.trans.send('{"@type": "problem-report", "explain_ltxt": "%s"}', wc.sender)
    return True