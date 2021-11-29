from plane.number import Field
from plane.vector import ProjectivePlane


def construct(field: Field):
    plane = ProjectivePlane(field)
    line_list = list(plane.get_point_list())

    for line in line_list:
        for normal in line_list:
            if line.is_orthogonal(normal):
                print(line, normal)
