import asyncio
import time

from dataclasses import dataclass
from random import choice

from utils import get_logger


logger = get_logger('async', 'INFO', './logs/async.log')


TABLES_GAME = 24
TIME_FACTOR = 1_000


@dataclass
class Player:
    name: str
    remaining_moves: int
    unit_of_time_to_move: int

    async def move(self) -> None:
        if self.remaining_moves > 0:
            await asyncio.sleep(self.unit_of_time_to_move / TIME_FACTOR)
            self.remaining_moves -= 1


@dataclass
class Game:
    name: str
    main_player: Player
    opponent: Player

    @property
    def is_game_over(self) -> bool:
        return not bool(self.main_player.remaining_moves + self.opponent.remaining_moves)

    async def play(self) -> None:
        players = (self.main_player, self.opponent)

        for player in players:
            logger.info(f'{self.name}: {player.name} is thinking...')
            await player.move()
            logger.info(f'{self.name}: {player.name} moved')


@dataclass
class ChessExhibition:
    games: list[Game]

    async def run(self) -> None:
        while not self.is_exhibition_over:
            plays = (game.play() for game in self.games if not game.is_game_over)
            await asyncio.gather(*plays)

    @property
    def is_exhibition_over(self) -> bool:
        for game in self.games:
            if not game.is_game_over:
                return False
        return True


async def prepare_chess_exhibition() -> ChessExhibition:
    names = ('James', 'Bruce', 'Alfred', 'Li', 'Oswald', 'Eduard', 'Harby')
    last_names = ('Gordon', 'Wayne', 'Pennyworth', 'Tomquins', 'Cobblepot', 'Nigma', 'Bullock')

    games = [
        Game(
            name=f'Table {i}',
            main_player=Player(name='Judit Polgár', remaining_moves=30, unit_of_time_to_move=5),
            opponent=Player(name=f'{choice(names)} {choice(last_names)}', remaining_moves=30, unit_of_time_to_move=55)
        )
        for i in range(1, TABLES_GAME + 1)
    ]

    return ChessExhibition(games)



async def main() -> None:
    chess_exhibition = await prepare_chess_exhibition()
    await chess_exhibition.run()
    


if __name__ == '__main__':
    start_point = time.perf_counter()
    asyncio.run(main())
    end_point = time.perf_counter()

    logger.info(f'Executed in: {end_point - start_point} seconds')
