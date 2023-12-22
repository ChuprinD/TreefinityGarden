def blend_colors(color1, color2, ratio):
    r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
    g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
    b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
    return f'#{r:02x}{g:02x}{b:02x}'


def natural_coloring(depth, max_depth):
    green = (34, 139, 34)
    brown = (139, 69, 19)
    return blend_colors(green, brown, depth / max_depth)


def default_coloring(depth, max_depth):
    return '#000000'


def pink_coloring(depth, max_depth):
    carnation_pink = (254, 141, 198)
    karry = (254, 209, 199)
    return blend_colors(carnation_pink, karry, depth / max_depth)


def neon_coloring(depth, max_depth):
    hot_magenta = (255, 0, 212)
    deep_sky_blue = (0, 221, 255)
    return blend_colors(deep_sky_blue, hot_magenta, depth / max_depth)


def ukrainian_coloring(depth, max_depth):
    light_blue = (0, 191, 255)
    yellow = (255, 186, 0)
    return blend_colors(light_blue, yellow, depth / max_depth)


def red_white_coloring(depth, max_depth):
    white = (255, 255, 255)
    cherry_red = (121, 6, 4)
    return blend_colors(white, cherry_red, depth / max_depth)


def gold_coloring(depth, max_depth):
    tangerine = (217, 163, 0)
    dandelion = (253, 207, 94)
    return blend_colors(tangerine, dandelion, depth / max_depth)


def green_black_coloring(depth, max_depth):
    green = (76, 187, 23)
    black = (1, 1, 1)
    return blend_colors(green, black, depth / max_depth)


COLORINGS = {'natural_coloring': natural_coloring, 'pink_coloring': pink_coloring,
             'neon_coloring': neon_coloring, 'default_coloring': default_coloring,
             'ukrainian_coloring': ukrainian_coloring, 'red_white_coloring': red_white_coloring,
             'gold_coloring': gold_coloring, 'green_black_coloring': green_black_coloring}


def get_coloring_by_name(name):
    return COLORINGS[name]