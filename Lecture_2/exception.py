import sys

try:
  x = int(input("x: "))
  y = int(input("y: "))
except ValueError:
  print("Error: Invalid input.")
  sys.exit(1) # 1 means error occured


try:
  result = x / y
except ZeroDivisionError:
  print("Error: Can't divide by zero.")
  sys.exit(1)


print(f"{x} / {y} = {result}")