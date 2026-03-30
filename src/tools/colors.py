colors = ["red", "blue", "green", "yellow", "cyan", "magenta", "orange", "purple"]

def int_to_color(i: int) -> str:
    if i < 0:
        raise ValueError("Color index must be non-negative")
    if i >= 8:
        raise ValueError("Color index must be less than 8")
    return colors[i % len(colors)]
