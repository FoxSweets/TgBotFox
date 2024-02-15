from typing import Tuple
import os
from random import randint as rnd

async def get_word(path_files: str) -> tuple[str, str]:
    path = f"data/{path_files}"

    if os.path.exists(path):
        with open("data/word_list.txt", "r", encoding="UTF-8") as word_list:
            lines = word_list.readlines()
            random_num: int = rnd(0, len(lines) - 1)
            random_word = lines[random_num].strip().lower()

            random_num_spy: int = rnd(0, len(lines) - 1)
            while random_num == random_num_spy:
                random_num_spy: int = rnd(0, len(lines) - 1)

            random_word_spy = lines[random_num_spy].strip().lower()

        return random_word, random_word_spy