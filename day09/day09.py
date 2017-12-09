from __future__ import print_function, division, absolute_import


def solve(input):
    """
    Solve the Day 9 puzzle.

    Given a text string
    - *groups* is defined by a sequence enclosed in curly braces { }.
    - *garbage* is defined by a sequence enclosed in angle brackets < >.
    - the meaning of any character is negated if preceded by !

    Part 1:  Provide the 'score' of the text string where each group gets
    a score of 1 greater than it's enclosing group.  The outermost group
    has a score of 1.

    Part 2:  Count the characters *between* garbage brackets, unless the
    character is ! or negated by !.

    Solution method:

    Proceed through the string, keeping track of the depth of curly braces.
    Each time we encounter a { that is neither garbage nor negated, it starts
    a new group and the depth is incremented.  The score is then incremented by
    that depth.

    For part 2, if the current character is *between* garbage brackets, not
    ! and not negated, increment the garbage count by 1.

    Parameters
    ----------
    input : str
        the string stream

    Returns
    -------
    score : int
        The score of our stream input
    garbage_count : int
        The number of characters in garbage that are not negated nor !
    """
    score = 0
    brace_depth = 0
    garbage = False
    negate = False
    garbage_count = 0
    allow_add = True

    for character in input:
        if character == '{' and not garbage and not negate:
            brace_depth += 1
            score += brace_depth
        elif character == '}' and not garbage and not negate:
            brace_depth -= 1
        elif character == '<' and not garbage and not negate:
            garbage = True
            allow_add = False
        elif character == '>' and garbage and not negate:
            garbage = False
            allow_add = False
        else:
            allow_add = True

        if character == '!' and not negate:
            negate = True
        else:
            if garbage and not negate and allow_add:
                garbage_count += 1
            negate = False

    return score, garbage_count


if __name__ == '__main__':

    print(solve('{}'))
    print(solve('{{{}}}'))
    print(solve('{{},{}}'))
    print(solve('{{{},{},{{}}}}'))
    print(solve('{<a>,<a>,<a>,<a>}'))
    print(solve('{{<ab>},{<ab>},{<ab>},{<ab>}}'))
    print(solve('{{<!!>},{<!!>},{<!!>},{<!!>}}'))
    print(solve('{{<a!>},{<a!>},{<a!>},{<ab>}}'))

    print()

    print(solve('<>'))  # 0
    print(solve('<random characters>'))  # 17
    print(solve('<<<<>'))  # 3
    print(solve('<{!>}>'))  # 2
    print(solve('<!!>'))  # 0
    print(solve('<!!!>>'))  # 0
    print(solve('<{o"i!a,<{i<a>'))  # 10

    print()

    with open('input.txt', 'r') as f:
        input = f.read()

    print(solve(input)) # 10800, 4522
