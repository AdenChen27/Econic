from manim import *
from demand_curve import IndifferenceCurve

AX_HEIGHT = 10
AX_WIDTH = 10
AX_SCALE = 2
AX_CONFIG_1st_QUADRANT = {
    "x_range": [0, AX_WIDTH, 1], 
    "y_range": [0, AX_HEIGHT, 1], 
    "x_length": AX_WIDTH/AX_SCALE, 
    "y_length": AX_HEIGHT/AX_SCALE, 
    "tips": False,
    "axis_config": {"include_ticks": False}
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
        self.P = .5
        self.plane = plane
        self.f = lambda x: 2*x**self.P

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

    Animation #0: showing u(w)
    Animation #1: diminishing marginal utility of wealth
        showing utility change for [w, w+1] (w = w_tracker)
    Animation #2: showing expected utility for bet: 50% +100; 50% -100
    Animation #3: showing expected utility for bet: 50% +110; 50% -100
    Animation #4: showing expected utility for choices: 100% -750 or 75% -1000
    """
    def construct(self):
        self.init() # +{u_graph} -> {u_graph}
        # self.animation_1() # no change
        # self.animation_2() # no change
        # self.animation_3() # no change
        # self.animation_4() # no change

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

        # W-U plane for utility-wealth function
        plane = Axes(**AX_CONFIG_1st_QUADRANT).shift(LEFT*2)
        labels = plane.get_axis_labels(x_label="W", y_label="U")

        # utility function over wealth u(w)
        u_w = UtilityOverWealth(plane)
        u_graph = u_w.get_graph(plane)

        # Animation #0: showing u(w)
        self.add(plane, labels)
        self.add(u_graph)
        self.plane, self.u_w, self.u_graph = plane, u_w, u_graph
        self.protected_mobjects = [self.plane, self.u_graph]

    def animation_1(self):
        # Animation #1: diminishing marginal utility of wealth
        #   showing utility change for [w, w+1] (w = w_tracker)
        plane, u_w, u_graph = self.plane, self.u_w, self.u_graph
        p2c, c2p = plane.p2c, plane.c2p

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

        self.remove_mobjects(w_tracker, to_x_axis_line_0, to_x_axis_line_1, h_line, brace)
        # self.clean()

    def animation_2(self):
        # Animation #2: showing expected utility for bet: 50% +100; 50% -100
        plane, u_w, u_graph = self.plane, self.u_w, self.u_graph
        p2c, c2p = plane.p2c, plane.c2p
        # dots: 
        # L: bet lost; M: current state; R: bet won
        # M2: mid point of L and R -- expected utility
        Lx = 1
        Rx = 7
        Mx = (Lx + Rx)/2
        L = Dot(u_w.get_pos(x=Lx))
        M = Dot(u_w.get_pos(x=Mx), color=GREEN)
        R = Dot(u_w.get_pos(x=Rx))
        M2 = Dot(c2p(Mx, (u_w.f(Lx) + u_w.f(Rx))/2), color=YELLOW)

        self.add(DashedLine(u_w.get_pos(x=Lx), u_w.get_pos(x=Rx)))
        self.add(L, M, R, M2)
        self.add(Text("-100").scale(.5).next_to(L, UP/2))
        self.add(Text("+100").scale(.5).next_to(R, UP/2))

        self.clean()

    def animation_3(self):
        # Animation #3: showing expected utility for bet: 50% +110; 50% -100
        plane, u_w, u_graph = self.plane, self.u_w, self.u_graph
        p2c, c2p = plane.p2c, plane.c2p
        # dots: 
        # L: bet lost; I: initial state; R: bet won
        # M2: mid point of L and R -- expected utility
        Lx = 1
        Rx = 7 + 3/10
        Ix = 4
        Mx = (Lx + Rx)/2

        L = Dot(u_w.get_pos(x=Lx))
        I = Dot(u_w.get_pos(x=Ix), color=GREEN)
        R = Dot(u_w.get_pos(x=Rx))
        M2 = Dot(c2p(Mx, (u_w.f(Lx) + u_w.f(Rx))/2), color=YELLOW)

        self.add(DashedLine(u_w.get_pos(x=Lx), u_w.get_pos(x=Rx)))
        self.add(L, I, R, M2)
        self.add(Text("-100").scale(.5).next_to(L, UP/2))
        self.add(Text("+110").scale(.5).next_to(R, UP/2))
        self.add(Text("W = +0").scale(.4).set_color(GREEN).next_to(I, UP/2))
        self.add(Text("W = +5").scale(.4).set_color(YELLOW).next_to(M2, RIGHT/2))

        self.clean()

    def animation_4(self):
        # Animation #4: showing expected utility for choices: 100% -750 or 75% -1000
        plane, u_w, u_graph = self.plane, self.u_w, self.u_graph
        p2c, c2p = plane.p2c, plane.c2p
        # dots: 
        # I: initial state
        # C1: choice 1 (100% -750)
        # C2: choice 2 (75% -1000) and lost (-1000)
        # C3: choice 2 (75% -1000) expected state
        Ix = 10
        x_1000 = 1
        x_750 = x_1000 + (Ix - x_1000)/4
        

        I = Dot(u_w.get_pos(x=Ix))
        C1 = Dot(u_w.get_pos(x=x_750), color=GREEN)
        C2 = Dot(u_w.get_pos(x=x_1000))
        C3 = Dot(c2p(x_750, u_w.f(x_1000) + (u_w.f(Ix) - u_w.f(x_1000))/4), color=YELLOW)

        self.add(DashedLine(u_w.get_pos(x=Ix), u_w.get_pos(x=x_1000)))
        self.add(DashedLine(
            c2p(x_750, 2), 
            c2p(x_750, 5)
        ))
        self.add(I, C1, C2, C3)
        self.add(Text("W = 0").scale(.4).next_to(I, DOWN/2))
        self.add(Text("W = -750").scale(.4).next_to(C1, DR/2))
        self.add(Text("W = -1000").scale(.4).next_to(C2, DR/2).shift(LEFT/3))

        self.add(Text("C", color=GREEN).scale(.4).next_to(C1, UL/2))
        self.add(Text("D", color=YELLOW).scale(.4).next_to(C3, DL/2))

        self.clean()


class NeoClassicalEndowmentEffect(Scene):
    # Neoclassical explanation for endowment effect (Hanemann, 1991)
    # essentially DMU of wealth
    # WTP < WTA
    def construct(self):
        # Wealth-Good plane
        plane = Axes(**AX_CONFIG_1st_QUADRANT).shift(LEFT*2)
        labels = plane.get_axis_labels(x_label="x", y_label="W")
        self.add(plane, labels)

        ic = IndifferenceCurve(3)
        ic2 = IndifferenceCurve(4) # with an extra unit of x
        ic_graph = ic.get_graph(plane)
        ic_graph2 = ic2.get_graph(plane)

        # D
        # A B
        #   C
        a_pos = ic.get_pos(plane, x=2)
        b_pos = ic2.get_pos(plane, y=ic.f(2))
        c_pos = ic.get_pos(plane, x=ic2.get_x(ic.f(2)))
        d_pos = ic2.get_pos(plane, x=2)

        label_a = Text("A").scale(.5).next_to(a_pos, DL/2)
        label_b = Text("B").scale(.5).next_to(b_pos, UR/2)
        label_c = Text("A'", color=YELLOW).scale(.5).next_to(c_pos, DL/2)
        label_d = Text("B'", color=YELLOW).scale(.5).next_to(d_pos, UR/2)
        # label_d2 = Text("B").scale(.5).next_to(dot2, UR/2)
        # label_d3 = Text("C").scale(.5).next_to(dot3, UR/2)

        dot_a = Dot(a_pos)
        dot_b = Dot(b_pos) # same wealth, one more unit of good x
        dot_c = Dot(a_pos, color=YELLOW) # move from A to C
        dot_d = Dot(b_pos, color=YELLOW) # move from B to D

        self.add(dot_a, dot_b, label_a, label_b)
        self.add(ic_graph, ic_graph2)

        # A -> B (C -> B)
        arrow_cb = Arrow(c_pos, b_pos, buff=0.1, color=BLUE)
        arrow_ab = Arrow(a_pos, b_pos, buff=0.1, color=BLUE)
        self.play(FadeIn(arrow_ab))
        self.add(dot_c)
        self.play(
            dot_c.animate.move_to(c_pos), 
            ReplacementTransform(arrow_ab, arrow_cb), 
            FadeIn(label_c)
        )

        # B -> A (B -> D)
        arrow_da = Arrow(d_pos, a_pos, buff=0.1, color=BLUE)
        arrow_ba = Arrow(b_pos, a_pos, buff=0.1, color=BLUE)
        self.play(FadeIn(arrow_ba))
        self.add(dot_d)
        self.play(
            dot_d.animate.move_to(d_pos), 
            ReplacementTransform(arrow_ba, arrow_da), 
            FadeIn(label_d)
        )

        self.wait()






class ProspectTheoryUtility(Scene):
    """
    Utility function in prospect theory
    """
    def construct(self):
        plane = Axes(**AX_CONFIG).shift(LEFT*2)
        # wealth - reference point
        labels = plane.get_axis_labels(x_label=r"c-r", y_label="U")

        u_graph = plane.plot(lambda x: x**.7 if x>=0 else -2*(-x)**.7)
        # u_graph = plane.plot(lambda x: x)
        
        self.add(plane, labels)
        self.add(u_graph)



# markowitz utility function


