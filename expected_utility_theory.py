from manim import *

AX_HEIGHT = 10
AX_WIDTH = 10
AX_SCALE = 2
AX_CONFIG_1st_QUADRANT = {
    "x_range": [0, AX_WIDTH, 1], 
    "y_range": [0, AX_HEIGHT, 1], 
    "x_length": AX_WIDTH/AX_SCALE, 
    "y_length": AX_HEIGHT/AX_SCALE, 
    "tips": False,
    # "axis_config": {"include_numbers": True}
}

AX_CONFIG = {
    "x_range": [-AX_WIDTH//2, AX_WIDTH//2, 1], 
    "y_range": [-AX_HEIGHT//2, AX_HEIGHT//2, 1], 
    "x_length": AX_WIDTH/AX_SCALE, 
    "y_length": AX_HEIGHT/AX_SCALE, 
    "tips": False,
    # "axis_config": {"include_numbers": True}
}


class UtilityOverWealth:
    # utility function over wealth
    def __init__(self, plane):
        self.P = .7
        self.plane = plane
        self.f = lambda x: x**self.P

    def get_graph(self, plane, **config):
        return plane.plot(self.f, use_smoothing=False)

    def get_coords(self, x=None, y=None):
        # return coordinates of a dot on the utility function
        # given the x or y position of the dot
        if x is not None and y is not None:
            return (x, y)
        if x is not None:
            return (x, self.f(x))
        if y is not None:
            return (y**(1/self.P), y)
        return None
    
    def get_pos(self, x=None, y=None):
        # return position of a dot on the utility function relative to given plane
        # given the x or y position of the dot
        return self.plane.c2p(*self.get_coords(x, y))


class UtilityIntro(Scene):
    """
    Utilty Introduction

    # Animation #0: showing u(w)
    Animation #1: diminishing marginal utility of wealth
        showing utility change for [w, w+1] (w = w_tracker)
    """
    def construct(self):
        # W-U plane for utility-wealth function
        plane = Axes(**AX_CONFIG_1st_QUADRANT).shift(LEFT*2)
        labels = plane.get_axis_labels(x_label="W", y_label="U")
        p2c, c2p = plane.p2c, plane.c2p

        # utility function over wealth u(w)
        u_w = UtilityOverWealth(plane)
        ufunc = u_w.get_graph(plane)

        
        # Animation #0: showing u(w)
        self.add(plane, labels)
        self.add(ufunc)

        # Animation #1: diminishing marginal utility of wealth
        #   showing utility change for [w, w+1] (w = w_tracker)
        w_tracker = ValueTracker(0.1)

        def get_line_to_x_axis_pos(w):
            # return start and end positions of a line from given point to the x axis
            coords = u_w.get_coords(x=w)
            return c2p(*coords), c2p(coords[0], 0)

        def get_h_line_pos(w=None):
            # retrun start and end positions of horizontal line 
            # from end of brace (which marks marginal utility of next wealth unit)
            # to start of to_x_axis_line_1
            if w is None:
                w = w_tracker.get_value()
            return u_w.get_pos(x=w), c2p(w + 1, u_w.f(w))

        to_x_axis_line_0 = DashedLine().add_updater(lambda l: l.put_start_and_end_on(
            *get_line_to_x_axis_pos(w_tracker.get_value())
        ))
        to_x_axis_line_1 = DashedLine().add_updater(lambda l: l.put_start_and_end_on(
            *get_line_to_x_axis_pos(w_tracker.get_value() + 1)
        ))
        to_x_axis_line_0.update()
        to_x_axis_line_1.update()

        # horizontal dashed line connnecting to_x_axis_line_1 tp brace (defined below)
        h_line = DashedLine().add_updater(lambda l: l.put_start_and_end_on(
            *get_h_line_pos()
        ))

        # brace marking marginal utility of next wealth unit
        brace_stem = Line().add_updater(lambda l: l.put_start_and_end_on(
            c2p(w_tracker.get_value() + 1, u_w.f(w_tracker.get_value())), 
            u_w.get_pos(x=w_tracker.get_value() + 1)
        ))
        brace_top = Line(ORIGIN, RIGHT/5).add_updater(lambda l: l.move_to(brace_stem, UP))
        brace_bottom = Line(ORIGIN, RIGHT/5).add_updater(lambda l: l.move_to(brace_stem, DOWN))
        brace = Group(brace_stem, brace_top, brace_bottom).set_color(YELLOW)

        

        self.add(to_x_axis_line_0, to_x_axis_line_1, h_line, brace)

        w_values = [9, .1]
        for w in w_values:
            self.play(w_tracker.animate.set_value(w), run_time=2)



class ProspectTheoryUtility(Scene):
    """
    Utility function in prospect theory
    """
    def construct(self):
        plane = Axes(**AX_CONFIG).shift(LEFT*2)
        # wealth - reference point
        labels = plane.get_axis_labels(x_label=r"c-r", y_label="U")

        ufunc = plane.plot(lambda x: x**.7 if x>=0 else -2*(-x)**.7)
        # ufunc = plane.plot(lambda x: x)
        
        self.add(plane, labels)
        self.add(ufunc)



# markowitz utility function

