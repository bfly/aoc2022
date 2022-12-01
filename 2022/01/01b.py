#!/usr/bin/env python3

import logging
import sys
from time import perf_counter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    handlers=[logging.StreamHandler()],
    datefmt="%H:%M:%S",
)


def get_most_calories(lines: list[str]) -> int:
    calories_each = []
    current_calories = 0
    lines.append("\n")

    for line in lines:
        if line == "\n":
            calories_each.append(current_calories)
            current_calories = 0
        else:
            current_calories += int(line)

    result = sum(sorted(calories_each)[-3:])
    return result


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "./test.txt"
    tic = perf_counter()
    with open(input_file, "r") as file:
        lines = file.readlines()

    result = get_most_calories(lines)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    logging.info(f"{result=} ({time_us}µs)")