from manimlib import *

ACCENT_COLOR = '#b51919'
SECONDARY_COLOR = '#000000'
TERTIARY_COLOR = '#5ac61e'


class LinedRegularPolygon():
    def __init__(self, n, line_to_edge=False, draw_lines=True):
        self.sides = n
        self.polygon = RegularPolygon(n).set_color(ACCENT_COLOR).scale(3)
        self.center_dot = Dot(self.polygon.get_center()
                              ).set_color(SECONDARY_COLOR)
        self.radius_braces = []
        self.radiuss = []
        self.lines = VGroup()
        if draw_lines:
            if line_to_edge:
                self.lines = self.create_lines_to_edges()
            else:
                self.lines = self.create_lines_to_vertices()
        self.group = VGroup(self.lines, self.center_dot, self.polygon)

    def create_lines_to_vertices(self):
        vertices = self.polygon.get_vertices()
        polygon_center = self.polygon.get_center()
        lines = VGroup(*(Line(polygon_center, vertice).set_color(SECONDARY_COLOR)
                       for vertice in vertices))
        return lines

    def create_lines_to_edges(self):
        polygon_center = self.polygon.get_center()
        edges = self.get_center_of_edges(0)
        lines = VGroup(
            *(Line(polygon_center, edge).set_color(SECONDARY_COLOR) for edge in edges))
        return lines

    def create_free_radius_brace(self, object, direction, radius, pure_objects=False):
        radius_brace = Brace(object, direction).set_color(SECONDARY_COLOR)
        radius_ = Tex(str(radius)).set_color(
            ACCENT_COLOR).next_to(radius_brace, direction)
        self.radius_braces.append(radius_brace)
        self.radiuss.append(radius_)
        self.group.add(radius_brace, radius_)
        if pure_objects:
            return [radius_brace, radius_]
        else:
            return [GrowFromCenter(radius_brace), Write(radius_)]

    def create_radius_brace(self, radius):
        line = self.lines.submobjects[0]
        normal_direction = line.copy()
        normal_direction.rotate(-PI/2)
        normal_direction_vector = normal_direction.get_unit_vector()
        radius_brace = Brace(
            line, -normal_direction_vector).set_color(SECONDARY_COLOR)
        radius_ = Tex(str(radius)).set_color(ACCENT_COLOR).move_to(radius_brace.get_center(
        ) + normal_direction_vector * [-0.5, -0.5, 0]).set_stroke(ACCENT_COLOR, 3)
        self.radius_braces.append(radius_brace)
        self.radiuss.append(radius_)
        self.group.add(radius_brace, radius_)
        return [GrowFromCenter(radius_brace), FadeIn(radius_)]

    def fade_out_radius_braces(self):
        animations = [*[FadeOut(brace) for brace in self.radius_braces],
                      *[FadeOut(radius) for radius in self.radiuss]]
        for brace in self.radius_braces:
            self.group.remove(brace)
        for radius in self.radiuss:
            self.group.remove(radius)
        self.radius_braces = []
        self.radiuss = []
        return animations

    def get_edges(self):
        vertices = self.polygon.get_vertices()
        edges = []
        for i in range(len(vertices)):
            if i < len(vertices)-1:
                p1, p2 = [vertices[i], vertices[i+1]]
            else:
                p1, p2 = [vertices[-1], vertices[0]]
            edges.append(Line(p1, p2))
        return edges

    def get_center_of_edges(self, buff=SMALL_BUFF*3):
        vertices = self.polygon.get_vertices()
        coords_vertices = []
        for i in range(len(vertices)):
            if i < len(vertices)-1:
                p1, p2 = [vertices[i], vertices[i+1]]
            else:
                p1, p2 = [vertices[-1], vertices[0]]
            guide_line = Line(p1, p2)
            side = guide_line.get_center()
            normal_direction = guide_line.copy()
            normal_direction.rotate(-PI/2)
            vector_normal_direction = normal_direction.get_unit_vector()
            direction = Dot(side).shift(
                vector_normal_direction*buff).get_center()
            coords_vertices.append(direction)

        return coords_vertices


class first(Scene):
    def construct(self):
        self.wait(4)
        circle = Circle().scale(3).set_stroke(TERTIARY_COLOR)
        circle_radius_line = Line(circle.get_center(), circle.get_edge_center(RIGHT)).set_stroke(SECONDARY_COLOR)
        self.play(ShowCreation(circle_radius_line))
        self.wait()
        self.play(Rotate(circle_radius_line, 2 * PI, about_edge=LEFT), ShowCreation(circle), run_time=2)
        self.play
        self.wait(5)
        
        polygons = [LinedRegularPolygon(4, draw_lines=False)]
        polygons[0].group.rotate(-PI / 4)
        self.play(ShowCreation(polygons[0].group))
        self.wait(2.3)
        polygons[0].lines = polygons[0].create_lines_to_vertices()
        polygons[0].group.add(polygons[0].lines)
        self.play(ShowCreation(polygons[0].lines), run_time=2)
        self.wait(8)

        polygons.append(LinedRegularPolygon(6))
        self.play(ReplacementTransform(polygons[0].group, polygons[1].group))
        self.wait(6)

        polygons.append(LinedRegularPolygon(7))
        self.play(ReplacementTransform(polygons[1].group, polygons[2].group))
        self.wait(4)

        up_to = 30  # Go up to a N sided polygon
        for n_sides in range(8, up_to + 1):
            index = n_sides - 5
            polygons.append(LinedRegularPolygon(n_sides))
            self.play(ReplacementTransform(
                polygons[index - 1].group, polygons[index].group), run_time=4/n_sides)
        self.wait()


class second(Scene):
    def construct(self):
        polygon = LinedRegularPolygon(30)
        self.add(polygon.group)
        self.wait(2)
        square = LinedRegularPolygon(4)
        square.group.remove(square.lines)
        square.group.rotate(-PI/4)
        self.play(ReplacementTransform(polygon.group, square.group))
        self.wait(2)
        self.play(square.group.animate.shift(UP))
        perimeter = Tex(
            r'\text{perimetro}', '=2+2+2+2').set_color(SECONDARY_COLOR).scale(1.5).to_edge(DOWN)
        perimeter.set_color_by_tex_to_color_map({
            r'\text{perimetro}': ACCENT_COLOR
        })
        width_brace = always_redraw(Brace, square.polygon, DOWN)
        always(width_brace.set_color, SECONDARY_COLOR)
        width = Tex('2').set_color(SECONDARY_COLOR)
        always(width.next_to, width_brace, DOWN)
        self.play(GrowFromCenter(width_brace), Write(width))
        self.wait(4)
        self.play(square.group.animate.scale(0.5))

        height_brace = always_redraw(Brace, square.polygon, RIGHT)
        always(height_brace.set_color, SECONDARY_COLOR)
        height_2_brace = always_redraw(Brace, square.polygon, LEFT)
        always(height_2_brace.set_color, SECONDARY_COLOR)
        width_2_brace = always_redraw(Brace, square.polygon, UP)
        always(width_2_brace.set_color, SECONDARY_COLOR)
        height = width.copy()
        width_2 = width.copy()
        height_2 = width.copy()
        always(height.next_to, height_brace, RIGHT)
        always(width_2.next_to, width_2_brace, UP)
        always(height_2.next_to, height_2_brace, LEFT)

        self.play(GrowFromCenter(width_2_brace), GrowFromCenter(height_brace), GrowFromCenter(
            height_2_brace), Write(width_2), Write(height), Write(height_2))
        self.wait(3)
        self.play(Write(perimeter))        
        self.wait(3)


class third(Scene):
    def construct(self):
        square = LinedRegularPolygon(4)
        square.group.remove(square.lines)
        square.group.rotate(-PI/4)
        square.group.shift(UP)
        square.group.scale(0.5)
        perimeter = Tex(
            r'\text{perimetro}', '=2+2+2+2').set_color(SECONDARY_COLOR).scale(1.5).to_edge(DOWN)
        perimeter.set_color_by_tex_to_color_map({
            r'\text{perimetro}': ACCENT_COLOR
        })
        width_brace = always_redraw(Brace, square.polygon, DOWN)
        always(width_brace.set_color, SECONDARY_COLOR)
        width = Tex('2').set_color(SECONDARY_COLOR)
        always(width.next_to, width_brace, DOWN)
        height_brace = always_redraw(Brace, square.polygon, RIGHT)
        always(height_brace.set_color, SECONDARY_COLOR)
        height_2_brace = always_redraw(Brace, square.polygon, LEFT)
        always(height_2_brace.set_color, SECONDARY_COLOR)
        width_2_brace = always_redraw(Brace, square.polygon, UP)
        always(width_2_brace.set_color, SECONDARY_COLOR)
        height = width.copy()
        width_2 = width.copy()
        height_2 = width.copy()
        always(height.next_to, height_brace, RIGHT)
        always(width_2.next_to, width_2_brace, UP)
        always(height_2.next_to, height_2_brace, LEFT)
        self.add(square.group, width, height, width_2, height_2, width_brace,
                 width_2_brace, height_brace, height_2_brace, perimeter)
        self.wait(3)

        new_square = LinedRegularPolygon(4)
        new_square.group.rotate(-PI/4)
        new_square.group.remove(new_square.lines)
        circle = Circle().scale(2.11).set_stroke(TERTIARY_COLOR)

        self.play(FadeOut(width), FadeOut(width_2), FadeOut(width_2_brace), FadeOut(width_brace), FadeOut(height), FadeOut(height_2), FadeOut(
            height_brace), FadeOut(height_2_brace), ShowCreation(circle), ReplacementTransform(square.group, new_square.group), FadeOut(perimeter))

        self.wait(3)

        self.play(
            *new_square.create_free_radius_brace(new_square.get_edges()[1], UP, 2))

        self.wait()

        self.play(Indicate(new_square.group))

        self.wait(3)
        perimeter.to_corner(RIGHT + UP)
        self.play(new_square.group.animate.to_edge(LEFT),
                  circle.animate.to_edge(LEFT), Write(perimeter))

        self.wait(3)
        new_perimeter = Tex('perimetro_q', '=8').set_color(SECONDARY_COLOR)
        new_perimeter.scale(1.5).to_corner(RIGHT + UP)
        new_perimeter.set_color_by_tex_to_color_map(
            {'perimetro_q': ACCENT_COLOR})
        self.play(TransformMatchingTex(perimeter, new_perimeter))
        self.wait(3)

        circle_perimeter_inequality = Tex('perimetro_q', '>', 'perimetro_c').set_color(
            SECONDARY_COLOR).scale(1.5).to_corner(RIGHT + UP).shift(DOWN)
        circle_perimeter_inequality.set_color_by_tex_to_color_map({
            'perimetro_q': ACCENT_COLOR,
            'perimetro_c': TERTIARY_COLOR,
        })
        self.play(TransformFromCopy(
            new_perimeter, circle_perimeter_inequality))
        self.wait(3)

        new_circle_perimeter_inequality = Tex('8', '>', 'perimetro_c').set_color(
            SECONDARY_COLOR).scale(1.5).to_corner(RIGHT + UP).shift(DOWN)
        new_circle_perimeter_inequality.set_color_by_tex_to_color_map({
            '8': ACCENT_COLOR,
            'perimetro_c': TERTIARY_COLOR
        })
        self.play(TransformMatchingTex(
            circle_perimeter_inequality, new_circle_perimeter_inequality))
        self.wait(2)
        self.play(Indicate(new_circle_perimeter_inequality.submobjects[1]))
        self.wait(2)
        self.play(Indicate(new_circle_perimeter_inequality.submobjects[0]))
        self.wait(2)
        self.play(Indicate(new_circle_perimeter_inequality.submobjects[2]))
        self.wait(2)
        self.play(WiggleOutThenIn(new_circle_perimeter_inequality))


class fourth(Scene):
    def construct(self):
        square = LinedRegularPolygon(4)
        square.group.rotate(-PI/4)
        square.group.remove(square.lines)
        square.group.to_edge(LEFT)
        circle = Circle().scale(2.11).set_stroke(TERTIARY_COLOR)
        circle.to_edge(LEFT)
        perimeter_q = Tex('perimetro_q', '=8').set_color(SECONDARY_COLOR)
        perimeter_q.scale(1.5).to_corner(RIGHT + UP)
        perimeter_q.set_color_by_tex_to_color_map(
            {'perimetro_q': ACCENT_COLOR})
        circle_perimeter_inequality = Tex(
            '8', '>', 'perimetro_c').set_color(SECONDARY_COLOR)
        circle_perimeter_inequality.scale(
            1.5).to_corner(RIGHT + UP).shift(DOWN)
        circle_perimeter_inequality.set_color_by_tex_to_color_map({
            '8': ACCENT_COLOR,
            'perimetro_c': TERTIARY_COLOR,
        })
        self.add(*square.create_free_radius_brace(square.get_edges()
                 [1], UP, 2, True), circle, square.group, perimeter_q, circle_perimeter_inequality)
        self.wait(3)

        hexagon = LinedRegularPolygon(6)
        hexagon.group.scale(0.71)
        hexagon.polygon.set_stroke(SECONDARY_COLOR)
        hexagon.group.to_edge(LEFT)
        self.play(Transform(square.group, hexagon.group))
        self.wait(3)

        self.play(*hexagon.create_radius_brace('1'))
        self.wait(3)

        side_lengths = VGroup(*(Tex('1').set_color(SECONDARY_COLOR).move_to(edge)
                              for edge in hexagon.get_center_of_edges()))
        self.play(*hexagon.fade_out_radius_braces(), Write(side_lengths))
        self.wait(2)

        hexagon_perimeter = Tex('perimetro_h', '=1+1+1+1+1+1').set_color(
            SECONDARY_COLOR).scale(1).to_corner(RIGHT + UP).shift(DOWN * 2)
        self.play(TransformFromCopy(side_lengths, hexagon_perimeter))
        self.wait(2)
        self.play(ReplacementTransform(hexagon_perimeter, Tex('perimetro_h', '=6').set_color(
            SECONDARY_COLOR).scale(1.5).to_corner(RIGHT + UP).shift(DOWN * 2)))
        self.wait(3)
        self.play(Transform(circle_perimeter_inequality, Tex('perimetro_c', '>', 'perimetro_h').set_color(SECONDARY_COLOR).scale(1.5).to_corner(RIGHT + UP).shift(DOWN).set_color_by_tex_to_color_map({
            'perimetro_c': TERTIARY_COLOR,
        })))
        self.wait(2)
        self.play(Transform(circle_perimeter_inequality, Tex('perimetro_c', '>', '6').set_color(SECONDARY_COLOR).scale(1.5).to_corner(RIGHT + UP).shift(DOWN).set_color_by_tex_to_color_map({
            'perimetro_c': TERTIARY_COLOR,
        })))
        self.wait(2)
        self.play(Transform(circle_perimeter_inequality, Tex('8', '>', 'perimetro_c', '>', '6').set_color(SECONDARY_COLOR).scale(1.5).to_corner(RIGHT + UP).shift(DOWN).set_color_by_tex_to_color_map({
            'perimetro_c': TERTIARY_COLOR,
            '8': ACCENT_COLOR
        })))

class fifth(Scene):
    def construct(self):
        circle = Circle().scale(2.11).set_stroke(TERTIARY_COLOR)
        circle.to_edge(LEFT)
        perimeter_q = Tex('perimetro_q', '=8').set_color(SECONDARY_COLOR)
        perimeter_q.scale(1.5).to_corner(RIGHT + UP)
        perimeter_q.set_color_by_tex_to_color_map(
            {'perimetro_q': ACCENT_COLOR})
        circle_perimeter_inequality = Tex('8', '>', 'perimetro_c', '>', '6').set_color(SECONDARY_COLOR).scale(1.5).to_corner(RIGHT + UP).shift(DOWN).set_color_by_tex_to_color_map({
            'perimetro_c': TERTIARY_COLOR,
            '8': ACCENT_COLOR
        })
        hexagon = LinedRegularPolygon(6)
        hexagon.group.scale(0.71)
        hexagon.polygon.set_stroke(SECONDARY_COLOR)
        hexagon.group.to_edge(LEFT)
        side_lengths = VGroup(*(Tex('1').set_color(SECONDARY_COLOR).move_to(edge)
                              for edge in hexagon.get_center_of_edges()))
        hexagon_perimeter = Tex('perimetro_h', '=6').set_color(
            SECONDARY_COLOR).scale(1.5).to_corner(RIGHT + UP).shift(DOWN * 2)
        self.add(circle, perimeter_q, circle_perimeter_inequality, hexagon.group, side_lengths, hexagon_perimeter)
        self.wait(2)
        self.play(FadeOut(perimeter_q), FadeOut(hexagon_perimeter), FadeOut(hexagon.group), FadeOut(side_lengths), circle_perimeter_inequality.animate.scale(2, about_edge=RIGHT), circle.animate.to_edge(DOWN))
        circle_radius_line = Line(circle.get_center(), circle.get_edge_center(RIGHT)).set_color(SECONDARY_COLOR)
        self.play(ShowCreation(circle_radius_line))
        self.play(Rotate(circle_radius_line, 2 * PI, about_edge=LEFT), run_time=2)
        circle_radius = Tex('1').set_color(TERTIARY_COLOR).next_to(circle_radius_line, UP)
        self.play(Write(circle_radius))
        self.play(WiggleOutThenIn(circle_perimeter_inequality))
        self.wait(3)

