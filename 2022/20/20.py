#!/usr/bin/env python3

from time import perf_counter


Digit = tuple[int, int]

DECRYPTION_KEY = 811589153


def encrypt(numbers: list[Digit], cipher: list[Digit] | None = None) -> list[Digit]:
    if cipher is None:
        cipher = numbers.copy()

    for digit in numbers:
        val = digit[0]
        idx = cipher.index(digit)
        del cipher[idx]

        new_idx = (idx + val) % (len(numbers) - 1)
        cipher.insert(new_idx, digit)

    return cipher


def get_coords(numbers: list[Digit]) -> tuple[int, int, int]:
    numbers_raw = [digit[0] for digit in numbers]
    idx_0 = numbers_raw.index(0)
    return (
        numbers_raw[(idx_0 + 1000) % len(numbers)],
        numbers_raw[(idx_0 + 2000) % len(numbers)],
        numbers_raw[(idx_0 + 3000) % len(numbers)],
    )


def proc(input_file: str) -> tuple[int, int]:
    with open(input_file, "r") as file:
        numbers_int = [int(num) for num in file.readlines()]

    numbers = [(val, i) for i, val in enumerate(numbers_int)]
    encrypted = encrypt(numbers)
    coords = get_coords(encrypted)
    part_a = sum(coords)
    numbers = [(DECRYPTION_KEY * val, i) for i, val in enumerate(numbers_int)]
    encrypted: list[Digit] | None = None
    for i in range(10):
        encrypted = encrypt(numbers, encrypted)
    coords = get_coords(encrypted)
    part_b = sum(coords)
    return part_a, part_b


if __name__ == "__main__":
    fn1 = "../data/day20/test.txt"
    fn2 = "../data/day20/input.txt"

    tic = perf_counter()

    part_1a, part_1b = proc(fn1)
    part_2a, part_2b = proc(fn2)

    toc = perf_counter()
    time_us = round((toc - tic), 1)

    print(f"{part_1a=}, {part_1b=}, {part_2a=}, {part_2b=} ({time_us}s)")
