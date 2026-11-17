# tiny-chess-v23

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/haidildariell/tiny-chess-v23/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/haidildariell/tiny-chess-v23/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

An entry for the make.fun bounty **tiny-chess-01** — the strongest chess
engine that fits in 4 KB of Python, built in a recorded session so it is
eligible for the paid places.

`main.py` (3,917 bytes) is a self-unpacking engine built with the kit's
official `makefun compress` from the readable `src.py` (the compressed
entry stays under the 4,096-byte cap): a 0x88 board,
incremental Zobrist hashing with a transposition table, principal-variation
search with aspiration windows, check extensions, killer and history move
ordering, and a capture / evasion quiescence search. It searches a fixed
budget of 150,000 nodes per move — deterministic: no wall clock, no
unseeded randomness, no model calls — so every trial replays move for
move. It speaks the bounty protocol over HTTP: it polls the game server,
parses each position, and answers with its move in UCI form.

Run it with the game server's URL in the environment:

```
MAKEFUN_ENV_URL=http://127.0.0.1:<port> python3 -P -s main.py
```

## Practice trials (engine v19–v20, kit practice gauntlet)

| Trial | Elo | W / D / L | Time loss |
|------:|----:|----------:|----------:|
| 0 | 1,545 | 4 / 1 / 1 | 0 |
| 1 | 1,364 | — | 0 |
| 2 | 1,545 | 4 / 1 / 1 | 0 |

Re-validated after rebuilding `main.py` with `makefun compress`
(trial 0 re-run, 2026-11-17, 844 s wall): Elo 1,545, 4 W / 1 D / 1 L,
0 time loss — identical to the builder's trial 0.

Trial 2 (engine v20, 2026-11-17, 709 s wall): history table widened to
the full 17-bit move code (was 14-bit, so promotion moves sharing
from/to squares collided in one slot). Same result on the practice
gauntlet: Elo 1,545, 4 W / 1 D / 1 L, 0 time loss.

Trial 0 re-run of the packed `main.py` as submitted (engine v23,
2026-11-18, 682 s wall): Elo 1,451, 4 W / 0 D / 2 L, 0 time loss —
still clearly above the standing v18 entry (practice Elo 1,279).

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
