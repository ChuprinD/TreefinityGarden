def linear_interpolation(x, x1, y1, x2, y2):
    # performs linear interpolation for value x between (x1, y1) and (x2, y2)
    return y1 + (y2 - y1) * ((x - x1) / (x2 - x1))
