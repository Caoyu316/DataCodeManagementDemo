# Historical examples from class/lecture02.qmd. Predict before running.
x <- -4
if (x < 0) {
  x <- -x
}
if (x %% 2 == 0) {
  cat(x, "is even\n")
}

x <- 0
if (x == 0) {
  cat("zero\n")
} else if (x %% 2 == 0) {
  cat("even\n")
} else {
  cat("odd\n")
}

for (number in 1:6) {
  print(number)
}

for (i in 1:20) {
  if (i %% 15 == 0) cat("FizzBuzz\n")
  else if (i %% 3 == 0) cat("Fizz\n")
  else if (i %% 5 == 0) cat("Buzz\n")
  else cat(i, "\n")
}
