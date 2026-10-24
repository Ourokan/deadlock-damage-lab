"""Damage-matrix helpers for the real match scripts (match metadata damage_matrix)."""


def at(s, k, n):
    """Damage-matrix arrays are cumulative per sample time but right-aligned: a source that starts later (an item
    bought mid game) has a shorter array whose first entry is the sample time len(times) - len(s)."""
    if not s:
        return 0
    i = k - (n - len(s))
    return s[i] if 0 <= i < len(s) else (0 if i < 0 else s[-1])


def win(s, k, n):
    """Amount added to cumulative array s in sample window k (of n)."""
    return at(s, k, n) - at(s, k - 1, n)
