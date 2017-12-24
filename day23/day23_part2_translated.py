from __future__ import print_function, division, absolute_import


"""
set b 65
set c b
jnz a 2
jnz 1 5
mul b 100
sub b -100000
set c b
sub c -17000
    set f 1
    set d 2
        set e 2
            set g d
            mul g e
            sub g b
            # g = d * e - b
            # if d * e == b, set flag to zero (factor of b found -> we're looking for primes!)
            jnz g 2
            set f 0
            sub e -1
            set g e
            sub g b
            jnz g -8
        sub d -1
        set g d
        sub g b
        jnz g -13
    jnz f 2
    sub h -1 # if flag is 1, b is prime, increment h
    set g b
    sub g c
    jnz g 2
    jnz 1 3
    sub b -17  # b increments to c in steps of 17
    jnz 1 -23  # This is looping b up through
"""


def is_prime(n):
    for i in range(2, n//2+2):
        if (n % i) == 0:
            break
    else:
        return True
    return False

def solve_simplified():
    h = 0
    for b in range(106500, 123500 + 1, 17):
        if not is_prime(b):
            h += 1
    print('h =', h)

if __name__ == '__main__':
    solve_simplified()