from manim import *

AX_HEIGHT = 10
AX_WIDTH = 10
AX_SCALE = 2
AX_CONFIG = {
    "x_range": [0, AX_WIDTH, 1], 
    "y_range": [0, AX_HEIGHT, 1], 
    "x_length": AX_WIDTH/AX_SCALE, 
    "y_length": AX_HEIGHT/AX_SCALE, 
    "tips": False,
    "axis_config": {"include_ticks": False}
}




# class DemandCurveLinear:
#     # demand function: P = a - b*Q
#     def __init__(self, a, b):
#         self.a = a
#         self.b = b
#         self.f = lambda x: a - b*x
#         self.x_range = [0, a/b]

#     def get_graph(self, plane, **config):
#         return plane.plot(self.f, x_range=self.x_range, use_smoothing=False, **config)

#     def get_x(self, y):
#         return self.u**2/y

#     def get_coords(self, x=None, y=None):
#         # return coordinates of a dot on the indifference curve
#         # given the x or y position of the dot
#         if x is not None and y is not None:
#             return (x, y)
#         if x is not None:
#             return (x, self.f(x))
#         if y is not None:
#             return (self.get_x(y), y)
#         return None
    
#     def get_pos(self, plane, x=None, y=None):
#         # return position of a dot on the indifference curve relative to given plane
#         # given the x or y position of the dot
#         return plane.c2p(*self.get_coords(x, y))


# class SupplyCurveLinear:
#     # supply function: P = a + b*Q

#     def __init__(self, a, b):
#         self.a = a
#         self.b = b
#         self.f = lambda x: a + b*x
#         self.x_range = [0, AX_WIDTH]

#     def get_graph(self, plane, **config):
#         return plane.plot(self.f, x_range=self.x_range, use_smoothing=False, **config)


class LinearFunction:
    # y = k*x + b
    def __init__(self, plane, k, b, x_range=None):
        self.plane = plane
        self.f = lambda x: k*x + b
        self.get_x = lambda y: (y - b)/k
        if x_range is None:
            # TODO: default: keep everything in (0, 0) to (AX_HEIGHT, AXWIDTH)
            self.x_range = [0, AX_WIDTH]
            pass
        else:
            self.x_range = x_range

    def get_graph(self, **config):
        return self.plane.plot(self.f, x_range=self.x_range, use_smoothing=False, **config)

    def get_coords(self, x=None, y=None):
        # return coordinates of a dot on the indifference curve
        # given the x or y position of the dot
        if x is not None and y is not None:
            return (x, y)
        if x is not None:
            return (x, self.f(x))
        if y is not None:
            return (self.get_x(y), y)
        return None
    
    def get_pos(self, x=None, y=None):
        # return position of a dot on the indifference curve relative to given plane
        # given the x or y position of the dot
        return self.plane.c2p(*self.get_coords(x, y))



class DemandCurveIntro(Scene):
    """
    Demand Curve Introduction


    # Animation #1: moving along the demand curve
    # Animation #2: demand curve shifting
    """
    def construct(self):
        self.init() # +{dc_graph, sc_graph} -> {u_graph}
        # self.animation_1() # no change
        self.animation_2() # no change

    def clean(self):
        for m in self.mobjects:
            if m not in self.protected_mobjects:
                self.remove(m)

    def add_mobjects(self, *args, animation=FadeIn, **kwargs):
        if self.FADE_ANIMATION_OFF and animation == FadeIn:
            animation = None
        if animation is None:
            self.add(*args)
        else:
            self.play(animation(Group(*args)), **kwargs)

    def remove_mobjects(self, *args, animation=FadeOut, **kwargs):
        if self.FADE_ANIMATION_OFF and animation == FadeOut:
            animation = None
        if animation is not None:
            self.play(animation(Group(*args)), **kwargs)
        self.remove(*args)

    def init(self):
        self.FADE_ANIMATION_OFF = False

        plane = Axes(**AX_CONFIG).shift(LEFT*2)
        plane_labels = plane.get_axis_labels(x_label="Q", y_label="P")
        self.add(plane, plane_labels)

        dc = LinearFunction(plane, -1, 10, [3, 7])
        # sc = LinearFunction(1, 0, [3, 7])

        dc_graph = dc.get_graph()
        dc_label = Text("D").scale(.5).next_to(plane.c2p(7, 3))
        # sc_graph = sc.get_graph(plane)

        self.add(dc_graph, dc_label)

        self.plane, self.dc, self.dc_graph, self.dc_label = plane, dc, dc_graph, dc_label
        # self.sc, self.sc_graph = sc, sc_graph
        self.protected_mobjects = [self.plane, self.dc_graph, plane_labels, dc_label]

    def animation_1(self):
        # Animation #1: moving along the demand curve
        plane, dc, dc_graph, dc_label = self.plane, self.dc, self.dc_graph, self.dc_label
        x_tracker = ValueTracker(3.5)
        
        line_to_x_axis = DashedLine().add_updater(lambda l: l.put_start_and_end_on(
            dc.get_pos(x=x_tracker.get_value()), 
            plane.c2p(x_tracker.get_value(), 0)
        ))
        dot = Dot().add_updater(
            lambda d: d.move_to(dc.get_pos(x=x_tracker.get_value()))
        )
        q_label = Text("Q").scale(.5).add_updater(
            lambda t: t.next_to(plane.c2p(x_tracker.get_value(), 0), DOWN)
        )
        self.add(line_to_x_axis, q_label, dot)

        for x in [6.5, 3.5]:
            self.play(x_tracker.animate.set_value(x), run_time=2)

        self.clean()

    def animation_2(self):
        # Animation #2: demand curve shifting
        plane, dc, dc_graph, dc_label = self.plane, self.dc, self.dc_graph, self.dc_label
        self.play(dc_graph.animate.shift(RIGHT), dc_label.animate.shift(RIGHT))
        self.play(dc_graph.animate.shift(LEFT*2), dc_label.animate.shift(LEFT*2))
        self.play(dc_graph.animate.shift(RIGHT), dc_label.animate.shift(RIGHT))

        





