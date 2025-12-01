# Heron's Method SMT Solver

This project uses Z3 SMT solver to prove properties and find counterexamples for Heron's method of approximating square roots.

## Heron's Method

The function implements Heron's method for approximating √x:

```python
def heron(x, init=1, iters=6):
    res = init
    for _ in range(iters):
        res = (x / res + res) / 2
    return res
```

## Problems Solved

### Problem 1
- **1a**: Find counterexample for |heron(x, init=1, iters=6) - √x| < 0.01 where 0 < x < 100
- **1b**: Prove |heron(x, init=1, iters=7) - √x| < 0.01 where 0 < x < 100

### Problem 2
- **2a**: Find counterexample for |heron(x, init=b, iters=1) - √x| > |heron(x, init=b, iters=2) - √x|
- **2b**: Prove the previous holds if b ≠ √x
- **2c**: Find maximal c for which |heron(x, init=b, iters=1) - √x| > c · |heron(x, init=b, iters=3) - √x|

### Problem 3
Given 0 < b1 < b2 and |√x - b1| = |√x - b2|, determine whether heron(x, iters=1, init=b1) or heron(x, iters=1, init=b2) is a better approximation.

## Installation

Install the Z3 solver:

```bash
pip install z3-solver
```

## Usage

Run the solver:

```bash
python heron_smt_solver.py
```

## Requirements

- Python 3.6+
- z3-solver
