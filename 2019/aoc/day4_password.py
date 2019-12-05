"""
--- Day 4: Secure Container ---
You arrive at the Venus fuel depot only to discover it's protected by a password. The Elves had written the password on a sticky note, but someone threw it out.

However, they do remember a few key facts about the password:

It is a six-digit number.
The value is within the range given in your puzzle input.
Two adjacent digits are the same (like 22 in 122345).
Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
Other than the range rule, the following are true:

111111 meets these criteria (double 11, never decreases).
223450 does not meet these criteria (decreasing pair of digits 50).
123789 does not meet these criteria (no double).
How many different passwords within the range given in your puzzle input meet these criteria?

Your puzzle input is 158126-624574.
"""


def password_count(code_range):
    count = 0
    for i in range(code_range[0], code_range[1]+1):
        # assuming they're all six digits
        code = str(i)

        # check that each number does not decrease, and repeat requirement
        prev_ch = code[0]
        decrease, double = False, False
        repeat_count = 0
        for ch in code[1:]:
            if prev_ch < ch:
                prev_ch = ch
                if repeat_count == 1:
                    double = True
                repeat_count = 0
            elif prev_ch == ch:
                repeat_count += 1
            else:
                # don't worry about repeat, b/c we fail
                decrease = True
                break 

        if (repeat_count == 1 or double) and not decrease:
            count += 1
    return count


if __name__ == '__main__':
    code_range = [158126, 624574]
    print(password_count(code_range))
