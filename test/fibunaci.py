fib = [0, 1]

for i in range(8):
    fib += [fib[-1] + fib[-2]]

print(fib)