import re

"""
Find all 6 digit numbers, within a range, where:
    (Part 1):
        - The digits never decrease (from left to right)
        - There is at least one repeat (two adjacent digits that are same)
    (Part 2):
        - Same as part 1, but also there has to be at least one *double*
            - ie., 123444 was valid for part 1 but is not valid for part 2,
              because the repeat is not a double
            - 111122 meets the part 2 criteria

Taking out the "repeat" constraint, the problem is just "find all of the
numbers w/in the given range s.t. the digits never decrease".
    - Given a number, we can get the next number in sequence using 
      the following recursive algorithm:
        - if the sixth digit is < 9, just increment it by 1
        - otherwise, go to the fifth digit
            - if fifth digit < 9, increment by 1
                - then reset sixth digit to equal the new fifth digit
            - else, go to 4th digit, etc. etc.
    - ex: get_next_number(256699):
        -> 25669_
        -> 2566__
        -> 2567__
        -> 256777

Then, after getting the next "never decreasing" number in the sequence,
we can check if the repeat constraint is met and throw the number out
if it is not.
"""

def get_sequence(start, end, digits=6, part=1):
    sequence = []
    number = first_valid_number(start)
    while number <= end:
        if part == 1:
            if len(set(number)) < digits:
                sequence.append(number)
        else:
            if has_double(number):
                sequence.append(number)
        number = get_next_number(number)
    return sequence

def get_next_number(number, digits_to_fill=0):
    # If < 9, just increment by 1
    # Fill in digits that need to be reset, if they exist
    last_digit = int(number[-1])
    if last_digit < 9:
        next_digit = str(last_digit + 1)
        return number[:-1] + next_digit * (digits_to_fill + 1)
    else:
        # This digit needs to be reset, so move back one
        return get_next_number(number[:-1], digits_to_fill + 1)

def first_valid_number(start):
    valid_start = prev = start[0]
    for i in range(1, len(start)):
        curr = start[i]
        if curr < prev:
            valid_start = valid_start + prev
        else:
            valid_start = valid_start + curr
            prev = curr
    return valid_start



def has_double(number):
    counts = {}
    for num in number:
        counts[num] = counts.get(num, 0) + 1
    if 2 in counts.values():
        return True
    return False


def run(start, end):
    sequence1 = get_sequence(str(start), str(end), part=1)
    sequence2 = get_sequence(str(start), str(end), part=2)
    print("Answer to part 1: {}".format(len(sequence1)))
    print("Answer to part 2: {}".format(len(sequence2)))


def main():
    run(256310, 732736)

main()