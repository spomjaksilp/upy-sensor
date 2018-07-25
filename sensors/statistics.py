"""
statistics are defined here.
"""

def mean(samples):
    s_sum = 0
    for s in samples:
        s_sum += s
    return s_sum/len(samples)