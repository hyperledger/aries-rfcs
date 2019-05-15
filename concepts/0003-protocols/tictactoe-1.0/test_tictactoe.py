import unittest
import sys
import os
import random

import game
import ai

class GameTest(unittest.TestCase):
    def setUp(self):
        self.game = game.Game()
    def test_first(self):
        self.assertEqual(None, self.game.first)
        self.game['b3'] = 'x'
        self.assertEqual('X', self.game.first)
    def test_turns_enforced(self):
        self.game['b1'] = 'o'
        ok = True
        try:
            self.game['b2'] = 'o'
            ok = False
        except:
            pass
        if not ok:
            self.fail('Expected game not to allow two turns in row by same person.')
    def test_get_item_from_empty(self):
        self.assertEqual(None, self.game['a1'])
    def test_simple_set_item(self):
        self.game['a1'] = 'x'
        self.assertEqual('X', self.game['a1'])
        self.game['c3'] = 'o'
        self.assertEqual('O', self.game['c3'])
        self.game['b2'] = 'X'
        self.assertEqual('X', self.game['b2'])
        self.game['a3'] = 'O'
        self.assertEqual('O', self.game['a3'])
    def test_set_item_with_bad_value(self):
        bad_values = ['',None,'*','0',1,0]
        for bad in bad_values:
            self.game = game.Game() # reset state
            with self.assertRaises(ValueError):
                self.game['a1'] = bad
    def test_bad_key(self):
        bad_keys = ['1a','a4','d1','a1 ',' a1','a0','a01',11,None,'a12','aa1']
        for bad in bad_keys:
            with self.assertRaises(KeyError):
                self.game[bad]
    def test_cant_clobber_existing_cell(self):
        self.game['c3'] = 'o'
        with self.assertRaises(Exception):
            self.game['c3'] = 'x'
    def test_winner1(self):
        self.game['b2'] = 'o'
        self.game['a2'] = 'x'
        self.game['b1'] = 'o'
        self.game['b3'] = 'x'
        self.game['c3'] = 'o'
        self.assertEqual(None, self.game.winner())
    def test_winner2(self):
        self.game['a1'] = 'x'
        self.game['b2'] = 'o'
        self.game['b1'] = 'x'
        self.game['a2'] = 'o'
        self.game['c2'] = 'x'
        self.assertEqual(None, self.game.winner())
        self.game['c3'] = 'o'
        self.game['c1'] = 'x'
        self.assertEqual('X', self.game.winner())
    def test_bad_idx_to_key(self):
        bad_idx = [0,9,-1,'0',None,'a','a1']
        for bad in bad_idx:
            with self.assertRaises(ValueError):
                game.idx_to_key(bad_idx)
    def test_good_idx_to_key(self):
        def all_good_idx():
            for r in '123':
                for c in 'ABC':
                    yield c + r
        expected = 0
        for idx in all_good_idx():
            self.assertEqual(idx, game.idx_to_key(expected))
            expected += 1
    def test_good_other_player(self):
        opposites = 'xXoO'
        for player in opposites:
            opposite = opposites[(opposites.index(player) + 2) % 4].upper()
            self.assertEqual(opposite, game.other_player(player))
    def test_bad_other_player(self):
        bad_players = ['fred',None,'',0,1,-1,'xx','xo','Ox']
        for bad in bad_players:
            with self.assertRaises(ValueError):
                game.other_player(bad)
    def test_load_and_dump(self):
        moves = 'X:B2,O:C3,X:B1,O:B3,X:A3'.split(',')
        self.game.load(moves)
        dumped = self.game.dump()
        self.assertEqual(len(dumped), len(moves))
        for m in moves:
            self.assertTrue(m in dumped)

class AITest(unittest.TestCase):
    def test_line_winnable(self):
        for line in game.LINES:
            cells = [None]*9
            self.assertEqual(3, ai.winnable_in_n_moves(line, cells, 'x'))
            self.assertEqual(3, ai.winnable_in_n_moves(line, cells, 'o'))
            cells[line[0]] = 'X'
            self.assertEqual(2, ai.winnable_in_n_moves(line, cells, 'X'))
            self.assertEqual(None, ai.winnable_in_n_moves(line, cells, 'O'))
            cells[line[0]] = 'O'
            cells[line[1]] = 'O'
            self.assertEqual(None, ai.winnable_in_n_moves(line, cells, 'X'))
            self.assertEqual(1, ai.winnable_in_n_moves(line, cells, 'O'))
            cells[line[0]] = 'X'
            cells[line[1]] = 'X'
            cells[line[2]] = 'X'
            self.assertEqual(0, ai.winnable_in_n_moves(line, cells, 'X'))
            self.assertEqual(None, ai.winnable_in_n_moves(line, cells, 'O'))
    def test_first_move(self):
        g = game.Game()
        self.assertEqual('B2', ai.next_move(g, 'x'))
    def test_head_to_head(self):
        # Make the AI play against itself a bunch of times. Randomize which
        # side starts. Every game should take a full 9 moves, and every gamee
        # should end with a draw.
        for i in range(100):
            g = game.Game()
            player = random.choice('XO')
            n = 0
            while True:
                cell = ai.next_move(g, player)
                g[cell] = player
                n += 1
                w = g.winner()
                if w:
                    if w != g.first or n != 9:
                        self.fail('Game won unexpectedly:\n%s.' % str(g))
                    break
                if n == 9:
                    break
                player = game.other_player(player)

if __name__ == '__main__':
    unittest.main()
