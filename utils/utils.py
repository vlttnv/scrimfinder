def get_bit_combinations(bit_string):
    """
    Use for generating similar scrim times, represented as a bit string.

    Return combinations of all unique binary string, and set '1's 
    in the same places as those in the original bit string.

    E.g. Mon, Tue, Wed ("1110000") -> ["1110000", "1110001", "1110011"...]
    """

    import itertools as itools

    result = []

    all_ones = [i for i, ltr in enumerate(bit_string) if ltr == '1']

    n = len(bit_string)
    possiblities = ["".join(seq) for seq in itools.product("01", repeat=n)]
    for p in possiblities:
        s = []
        for char in p:
            s.append(char)
        for ones_index in all_ones:
            s[ones_index] = '1'
        new_s = ''.join(s)
        if new_s not in result:
            result.append(new_s)

    return result