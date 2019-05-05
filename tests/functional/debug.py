from cairocffi import Context
from shapely.geometry import LineString


def draw_line_string(cairo_context: Context, line_string: LineString):
    start = True
    for x, y in line_string.coords:
        if start:
            cairo_context.move_to(x, y)
        else:
            cairo_context.line_to(x, y)

        start = False
