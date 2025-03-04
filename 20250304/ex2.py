def gcd(a: int, b: int) -> int:
    """計算兩數的最大公因數"""
    if b == 0:
        return a
    return gcd(b, a % b)

# 測試
x, y = 7, 49
print(f"GCD of {x} and {y} is {gcd(x, y)}")

x, y = 11, 121
print(f"GCD of {x} and {y} is {gcd(x, y)}")