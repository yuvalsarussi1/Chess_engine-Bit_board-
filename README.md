# Chess Bitboard Engine

## Overview
A chess engine built using bitboards. Supports all chess rules, move generation, and a simple engine with minimax search.

## Features
- Full chess rules (castling, en passant, promotion)
- Bitboard move generation
- Minimax with alpha-beta pruning
- Evaluation heuristics (material + positional)
- Perft testing for validation
- Playable in terminal (PvP and PvE)

## Usage
Run perft test:
```bash
python main_terminal.py

## play vs engine
python player_vs_engine.py


## example:
  a b c d e f g h
 +-----------------+
8 | r n b q k b n r | 8
7 | p p p p p p p p | 7
6 | . . . . . . . . | 6
5 | . . . . . . . . | 5
4 | . . . . . . . . | 4
3 | . . . . . . . . | 3
2 | P P P P P P P P | 2
1 | R N B Q K B N R | 1
 +-----------------+
  a b c d e f g h



