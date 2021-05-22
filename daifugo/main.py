#!/usr/bin/env python3
import asyncio

from agents.random_agent import RandomAgent
from game.president import President

if __name__ == "__main__":
    game = President([
        *(RandomAgent() for _ in range(4))
    ])

    # Start the game
    asyncio.run(game.play(250, 20))
