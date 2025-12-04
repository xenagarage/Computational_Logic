from z3 import *

def heron_formula(x, init, iters):
    res = init
    for _ in range(iters):
        res = (x / res + res) / 2
    return res


def problem_1a():
    s = Solver()
    x = Real('x')
    sqrt_x = Real('sqrt_x')
    
    s.add(x > 0)
    s.add(x < 100)
    s.add(sqrt_x * sqrt_x == x)
    s.add(sqrt_x > 0) 
    
    heron_result = heron_formula(x, 1, 6)
    
    diff = heron_result - sqrt_x
    s.add(Or(diff >= 0.01, diff <= -0.01))
    
    if s.check() == sat:
        m = s.model()
        x_val = m[x]
        sqrt_x_val = m[sqrt_x]
        print(f"  x = {x_val} (≈ {float(x_val.as_fraction())})")
        print(f"  sqrt(x) = {sqrt_x_val} (≈ {float(sqrt_x_val.as_fraction())})")
        
        import math
        x_float = float(x_val.as_fraction())
        heron_val = heron_python(x_float, 1, 6)
        actual_sqrt = math.sqrt(x_float)
        error = abs(heron_val - actual_sqrt)
        print(f"  heron(x, 1, 6) ≈ {heron_val}")
        print(f"  |heron - sqrt(x)| ≈ {error}")
        print(f"  Error >= 0.01? {error >= 0.01}")
    else:
        print("No counterexample found")
    print()


def problem_1b():
    s = Solver()
    x = Real('x')
    sqrt_x = Real('sqrt_x')
    
    s.add(x > 0)
    s.add(x < 100)
    s.add(sqrt_x * sqrt_x == x)
    s.add(sqrt_x > 0) 
    
    heron_result = heron_formula(x, 1, 7)
    
    diff = heron_result - sqrt_x
    s.add(Or(diff >= 0.01, diff <= -0.01))
    
    result = s.check()
    if result == unsat:
        print("PROVED: No counterexample exists!")
        print("The claim |heron(x, init=1, iters=7) - sqrt(x)| < 0.01 is TRUE for all 0 < x < 100")
    elif result == sat:
        m = s.model()
        print("Counterexample found (claim is false):")
        print(f"  x = {m[x]}")
    else:
        print("Unknown (solver could not determine)")
    print()


def problem_2a():
    """
    Problem 2a: Find counterexample for |heron(x, init=b, iters=1) - sqrt(x)| > |heron(x, init=b, iters=2) - sqrt(x)|
    where 0 < x and 0 < b
    """
    print("=" * 80)
    print("Problem 2a: Find counterexample for |heron(x,b,1) - sqrt(x)| > |heron(x,b,2) - sqrt(x)|")
    print("=" * 80)
    
    s = Solver()
    x = Real('x')
    b = Real('b')
    sqrt_x = Real('sqrt_x')
    
    s.add(x > 0)
    s.add(b > 0)
    s.add(sqrt_x * sqrt_x == x)
    s.add(sqrt_x > 0)
    
    heron_1 = heron_formula(x, b, 1)
    heron_2 = heron_formula(x, b, 2)
    
    diff_1 = heron_1 - sqrt_x
    diff_2 = heron_2 - sqrt_x
    
    s.add(diff_1 * diff_1 <= diff_2 * diff_2)
    
    if s.check() == sat:
        m = s.model()
        x_val = m[x]
        b_val = m[b]
        sqrt_x_val = m[sqrt_x]
        print(f"Counterexample found!")
        print(f"  x = {x_val} (≈ {float(x_val.as_fraction())})")
        print(f"  b = {b_val} (≈ {float(b_val.as_fraction())})")
        print(f"  sqrt(x) = {sqrt_x_val} (≈ {float(sqrt_x_val.as_fraction())})")
        
        import math
        x_float = float(x_val.as_fraction())
        b_float = float(b_val.as_fraction())
        h1 = heron_python(x_float, b_float, 1)
        h2 = heron_python(x_float, b_float, 2)
        actual_sqrt = math.sqrt(x_float)
        err1 = abs(h1 - actual_sqrt)
        err2 = abs(h2 - actual_sqrt)
        print(f"  |heron(x,b,1) - sqrt(x)| ≈ {err1}")
        print(f"  |heron(x,b,2) - sqrt(x)| ≈ {err2}")
        print(f"  err1 > err2? {err1 > err2}")
        print(f"  err1 <= err2? {err1 <= err2} (counterexample)")
    else:
        print("No counterexample found (claim is always true)")
    print()


def problem_2b():
    """
    Problem 2b: Prove |heron(x, init=b, iters=1) - sqrt(x)| > |heron(x, init=b, iters=2) - sqrt(x)|
    when b != sqrt(x)
    """
    print("=" * 80)
    print("Problem 2b: Prove |heron(x,b,1) - sqrt(x)| > |heron(x,b,2) - sqrt(x)| when b != sqrt(x)")
    print("=" * 80)
    
    s = Solver()
    x = Real('x')
    b = Real('b')
    sqrt_x = Real('sqrt_x')
    
    s.add(x > 0)
    s.add(b > 0)
    s.add(sqrt_x * sqrt_x == x)
    s.add(sqrt_x > 0)
    s.add(b != sqrt_x)  
    
    heron_1 = heron_formula(x, b, 1)
    heron_2 = heron_formula(x, b, 2)
    
    diff_1 = heron_1 - sqrt_x
    diff_2 = heron_2 - sqrt_x
    
    s.add(diff_1 * diff_1 <= diff_2 * diff_2)
    
    result = s.check()
    if result == unsat:
        print("PROVED: No counterexample exists!")
        print("When b != sqrt(x), the error always decreases: |heron(x,b,1) - sqrt(x)| > |heron(x,b,2) - sqrt(x)|")
    elif result == sat:
        m = s.model()
        print("Counterexample found:")
        print(f"  x = {m[x]}, b = {m[b]}")
    else:
        print("Unknown")
    print()


def problem_2c():
    """
    Problem 2c: Find maximal c such that |heron(x,b,1) - sqrt(x)| > c * |heron(x,b,3) - sqrt(x)|
    when b != sqrt(x)
    """
    print("=" * 80)
    print("Problem 2c: Find maximal c for |heron(x,b,1) - sqrt(x)| > c * |heron(x,b,3) - sqrt(x)|")
    print("=" * 80)
    
    def can_prove_for_c(c_val):
        """Check if we can prove the claim for a given c value"""
        s = Solver()
        x = Real('x')
        b = Real('b')
        sqrt_x = Real('sqrt_x')
        
        s.add(x > 0)
        s.add(b > 0)
        s.add(sqrt_x * sqrt_x == x)
        s.add(sqrt_x > 0)
        s.add(b != sqrt_x)
        
        heron_1 = heron_formula(x, b, 1)
        heron_3 = heron_formula(x, b, 3)
        
        diff_1 = heron_1 - sqrt_x
        diff_3 = heron_3 - sqrt_x
        
        s.add(diff_1 * diff_1 <= c_val * c_val * diff_3 * diff_3)
        
        return s.check() == unsat
    
    low, high = 0.0, 1000.0
    best_c = 0.0
    
    print("Searching for maximal c using binary search...")
    for iteration in range(20):  
        mid = (low + high) / 2
        if can_prove_for_c(mid):
            best_c = mid
            low = mid
            print(f"  Iteration {iteration+1}: c = {mid:.6f} - PROVABLE")
        else:
            high = mid
            print(f"  Iteration {iteration+1}: c = {mid:.6f} - not provable")
    
    print(f"\nMaximal c found (approximately): {best_c:.6f}")
    print(f"This means: |heron(x,b,1) - sqrt(x)| > {best_c:.6f} * |heron(x,b,3) - sqrt(x)| for all valid x, b")
    print()


def problem_3():
    """
    Problem 3: Given 0 < b1 < b2 and |sqrt(x) - b1| = |sqrt(x) - b2|,
    which gives better approximation after 1 iteration?
    """
    print("=" * 80)
    print("Problem 3: Which is better: heron(x,1,b1) or heron(x,1,b2)?")
    print("Given: 0 < b1 < b2 and |sqrt(x) - b1| = |sqrt(x) - b2|")
    print("=" * 80)
    
    s = Solver()
    s.set("timeout", 30000)  # 30 second timeout
    
    x = Real('x')
    b1 = Real('b1')
    b2 = Real('b2')
    sqrt_x = Real('sqrt_x')
    
    s.add(x > 0)
    s.add(b1 > 0)
    s.add(b2 > 0)
    s.add(b1 < b2)
    s.add(sqrt_x * sqrt_x == x)
    s.add(sqrt_x > 0)
    
    # |sqrt_x - b1| = |sqrt_x - b2|
    # Since b1 < b2, this means b1 < sqrt_x < b2 and sqrt_x = (b1 + b2) / 2
    s.add(b1 < sqrt_x)
    s.add(sqrt_x < b2)
    s.add(sqrt_x == (b1 + b2) / 2)
    
    # heron for both
    heron_b1 = heron_formula(x, b1, 1)
    heron_b2 = heron_formula(x, b2, 1)
    
    diff_b1 = heron_b1 - sqrt_x
    diff_b2 = heron_b2 - sqrt_x
    
    print("Testing if b1 always gives better approximation...")
    s.push()
    s.add(diff_b1 * diff_b1 >= diff_b2 * diff_b2)
    
    result = s.check()
    if result == unsat:
        print("PROVED: heron(x, init=b1, iters=1) is always better!")
        print("(smaller b1 gives better approximation)")
        s.pop()
    elif result == sat:
        print("b1 is not always better, checking if b2 is always better...")
        s.pop()
        
        s.push()
        s.add(diff_b2 * diff_b2 >= diff_b1 * diff_b1)
        
        result2 = s.check()
        if result2 == unsat:
            print("PROVED: heron(x, init=b2, iters=1) is always better!")
            print("(larger b2 gives better approximation)")
        elif result2 == sat:
            m = s.model()
            print("Neither is always better (depends on specific values)")
            print(f"Example: x={m[x]}, b1={m[b1]}, b2={m[b2]}, sqrt_x={m[sqrt_x]}")
        else:
            print("Solver returned unknown")
        s.pop()
    else:
        print(f"Solver timeout or unknown result: {result}")
        s.pop()
    
    print()


def heron_python(x, init, iters):
    res = init
    for _ in range(iters):
        res = (x / res + res) / 2
    return res


def main():
    
    problem_1a()
    problem_1b()
    
    problem_2a()
    problem_2b()
    problem_2c()
    
    problem_3()

if __name__ == "__main__":
    main()
