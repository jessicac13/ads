from math import factorial

def erlang_b(k, rho):
    numerator = (rho ** k) / factorial(k)
    denominator = sum((rho ** n) / factorial(n) for n in range(k + 1))
    return numerator / denominator

k = 9
rho = 5

prob_block = erlang_b(k, rho)
print(f"Probabilidade de bloqueio (Erlang-B): {prob_block:.4f}")
