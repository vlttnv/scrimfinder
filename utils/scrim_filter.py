def scrim_days_combinations(bit_string):
    """
    Generate all unique combinations of binary of length n, matching all the
    required scrim days.

    Return an array of similar scrim days, represented as bit strings.

    Example:

    "1110000" represents that team A can only play on Mon, Tue, and Wed.

    The result would be ["1110000", "1110001", "1110011", ...], meaning that 
    team A can play against any team whose scrim days match the above result
    """

    import itertools as itools

    indices_scrim_days = [i for i, bit in enumerate(bit_string) if bit == '1']

    n = len(bit_string)
    all_binaries = [''.join(seq) for seq in itools.product('01', repeat=n)]

    matched_scrim_days = []
    for binary in all_binaries:
        bits_list = list(binary)
        contains_any_scrim_day = False
        for i in indices_scrim_days:
            if bits_list[i] == "1":
                contains_any_scrim_day = True
        if contains_any_scrim_day:
            combination = ''.join(bits_list)
            if combination not in matched_scrim_days:
                matched_scrim_days.append(combination)
    return matched_scrim_days