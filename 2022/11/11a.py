#!/usr/bin/env python3

import sys
from time import perf_counter
from typing import Callable


class Monkey:
    def __init__(
        self,
        operation: Callable[[int], int],
        test: Callable[[int], int],
        items: list[int],
    ):
        self.operation = operation
        self.test = test
        self.items = items
        self.inspections = 0

    def inspect_items(self, monkeys: list["Monkey"]):
        while self.items:
            self.inspections += 1
            item = self.items.pop(0)
            item = self.operation(item)
            item = item // 3
            give_to = self.test(item)
            monkeys[give_to].items.append(item)


def parse_monkeys(lines: list[str]) -> list[Monkey]:
    monkeys = []

    for line in lines:
        match line.split():
            case ["Starting", "items:", *nums]:
                items_str = f"[{' '.join(nums)}]"
                items = eval(items_str)
            case ["Operation:", *_, op, num]:
                lambda_str = f"lambda old: old {op} {num}"
                operation = eval(lambda_str)  # don't try this at home!
            case ["Test:", *_, num]:
                divisor = num
            case ["If", "true:", *_, monkey_num]:
                if_true = monkey_num
            case ["If", "false:", *_, monkey_num]:
                lambda_str = (
                    f"lambda item: {if_true} if item % {divisor} == 0 else {monkey_num}"
                )
                test = eval(lambda_str)
                monkey = Monkey(operation, test, items)
                monkeys.append(monkey)

    return monkeys


if __name__ == "__main__":
    fn1 = "../data/day11/test.txt"
    fn2 = "../data/day11/input.txt"
    input_file = fn2
    with open(input_file, "r") as file:
        lines = [line.strip() for line in file.readlines()]

    tic = perf_counter()

    monkeys = parse_monkeys(lines)
    for i in range(20):
        for monkey in monkeys:
            monkey.inspect_items(monkeys)
    inspections = sorted([monkey.inspections for monkey in monkeys])
    monkey_business = inspections[-1] * inspections[-2]

    toc = perf_counter()
    time_us = round((toc - tic) * 1000000)

    print(f"{monkey_business=} ({time_us}µs)")
