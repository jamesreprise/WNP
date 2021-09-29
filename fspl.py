# Miscellaneous functions for Free Space Path Loss (FSPL).

import math

# Typical WiFi freq is 2.4GHz
MHZ = 2400

# FSPL(dB) = 20log10(d) + 20log10(f) - 27.55
# d, f are meters, megahertz
def fspl(d, f):
    if d == 0:
        return 0
    return (20 * math.log(d, 10)) + (20 * math.log(f, 10)) - 27.55

def euclid_dist(x, y):
    return math.sqrt((x[0] - y[0])**2 + (x[1] - y[1])**2)

def fspl_min(nodes, points):
    total_fspl = 0
    if len(nodes) == 0:
        return 0
    for point in points:
        min_dist = math.inf
        for node in nodes:
            dist = euclid_dist(node, point)
            if dist < min_dist:
                min_dist = dist
        # At a certain distance, the FSPL is acceptable.
        total_fspl += max(fspl(min_dist, MHZ), 20)
    return total_fspl / len(points)