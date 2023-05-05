from random import randint

# Remember how to use this kind of variable?
count = 0


def main():
  print("Welcome to Recursion Fun")

  # aggienacci calculation
  value = eval(input("Enter a number to find it's aggienacci value: "))
  print("The aggienacci value of " + str(value) + " is " +
        str(round(aggienacci(value), 4)))

  print()

  # Recursive search and sort

  key = eval(input("Enter a number to search for: "))
  numList = []
  for i in range(200000):
    if randint(0, 2) == 0:
      numList.append(i)

  numPos = binarySearch(numList, key)

  if numPos == -1:
    print("Your number, " + str(key) + ", is not in the list")
  else:
    print("Your number, " + str(key) + ", is in the list at position " +
          str(numPos))

  print("Total recursive calls: " + str(count))


def aggienacci(x):
  if 0 <= x < 3:
    return x
  return (aggienacci(x - 3) + aggienacci(x - 2)) / aggienacci(x - 1)


def binarySearch(numList, key, start=0):
  global count
  if len(numList) == 0:
    return -1
  mid = len(numList) // 2
  if key == numList[mid]:
    return start + mid
  elif key > numList[mid]:
    count += 1
    return binarySearch(numList[mid + 1:], key, start=start + mid + 1)
  elif key < numList[mid]:
    count += 1
    return binarySearch(numList[:mid], key, start=start)
  else:
    return -1


main()
