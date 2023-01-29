#!/usr/bin/env python3

import string
import sys
from time import perf_counter


def get_priority(char: str) -> int:
    if char in string.ascii_lowercase:
        # ord("a") = 97
        offset = 96
    else:
        # ord("A") = 65, plus the 26 extra pts for uppercase
        offset = 38
    return ord(char) - offset


def sum_duplicates(rucksacks: list[str]) -> int:
    total = 0
    for rucksack in rucksacks:
        midpt = len(rucksack) // 2
        l, r = rucksack[:midpt], rucksack[midpt:]
        duplicate = list(set(l).intersection(r))[0]
        total += get_priority(duplicate)

    return total


if __name__ == "__main__":
    fn1 = "../data/day3/test.txt"
    fn2 = "../data/day3/input.txt"
    input_file = fn2
    with open(input_file, "r") as file:
        rucksacks = [line.strip() for line in file.readlines()]

    tic = perf_counter()
    result = sum_duplicates(rucksacks)
    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    print(f"{result=} ({time_us}µs)")
