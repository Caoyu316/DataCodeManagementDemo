# Historical examples from class/lecture02.qmd. Predict before running.
x = -4
if x < 0:
    x = -x
if x % 2 == 0:
    print(f"{x} is even")

x = 0
if x == 0:
    print("zero")
elif x % 2 == 0:
    print("even")
else:
    print("odd")

for number in range(1,7):
    print(number)

for i in range(1, 21):
    if i % 15 == 0: print("FizzBuzz")
    elif i % 3 == 0: print("Fizz")
    elif i % 5 == 0: print("Buzz")
    else: print(i)
