# The Great Wall Game Solver

## Project Description

This project solves **The Great Wall Game**, a solitaire board game invented by Hua and Shen. The game is played on an `n × n` grid with `n` stones, each placed randomly in the grid with no more than one stone per square. A player can move any stone to an adjacent unoccupied square (horizontally or vertically) in a single move. The goal is to line up all `n` stones in a straight line (horizontally, vertically, or diagonally) using the fewest number of moves.

Given a starting configuration of stones, this program calculates the minimum number of moves required to form such a line.

## Problem Statement

For a given `n × n` grid and a random placement of `n` stones, determine the fewest number of moves needed to line up the stones into a straight line (horizontally, vertically, or diagonally).

### Input

- The input consists of multiple cases.
- Each case starts with an integer `n` (1 ≤ `n` ≤ 15), representing the grid size and the number of stones.
- The next line contains `2n` integers specifying the row and column positions of each stone.
- The input ends with a single `0`, indicating no more cases.

### Output

- For each case, the output shows the case number and the minimum number of moves needed to line up the `n` stones in a straight line.


## Solution Approach

To solve the problem, the following approach is used:

1. **Input Parsing:** Read multiple cases and parse each case's stone positions.
2. **Move Calculation:** For each case, compute the minimum number of moves required to align all the stones into a straight line (horizontally, vertically, or diagonally).
3. **Optimization:** The algorithm ensures that the number of moves is minimized by checking all possible lines and determining the minimum number of shifts required.
4. **Edge Cases:** Handle edge cases, such as stones already aligned (0 moves), and ensure correct output formatting.



