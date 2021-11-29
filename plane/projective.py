from plane.number import Field
from plane.vector import ProjectivePlane


def construct(field: Field):
    plane = ProjectivePlane(field)
    line_list = list(plane.get_line_list())
    for line in line_list:
        print(line)
