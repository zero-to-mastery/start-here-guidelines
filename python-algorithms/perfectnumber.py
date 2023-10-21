def is_perfect_number(num):
    divisors = [1]
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            divisors.extend([i, num // i])
    return sum(divisors) == num

def find_perfect_numbers_in_range(start, end):
    perfect_numbers = []
    for number in range(start, end + 1):
        if is_perfect_number(number):
            perfect_numbers.append(number)
    return perfect_numbers

start_range = 1  # Change this to the starting range you want to search
end_range = 10000  # Change this to the ending range you want to search

perfect_numbers = find_perfect_numbers_in_range(start_range, end_range)

if perfect_numbers:
    print("Perfect numbers in the range {} to {}: {}".format(start_range, end_range, perfect_numbers))
else:
    print("No perfect numbers found in the range {} to {}.".format(start_range, end_range))
