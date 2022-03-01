import time

from backend.blockchain.cormachain import Cormachain
from backend.config import SECONDS

the_cormachain = Cormachain()

length_of_time_to_mine = []

for i in range(1000):
    print('===== Adding new block =====')
    print(f'Current difficulty {the_cormachain.get_last_block.difficulty}')
    start = time.time_ns()
    the_cormachain.add_block(i)
    time_took_to_mine = (time.time_ns() - start) / SECONDS
    length_of_time_to_mine.append(time_took_to_mine)
    print(f'It took {time_took_to_mine}ms to mine')
    print(f'Average to mine a block {sum(length_of_time_to_mine) / len(length_of_time_to_mine)}')
