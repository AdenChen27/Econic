from manim import *

AX_HEIGHT = 10
AX_WIDTH = 10
AX_SCALE = 2
AX_CONFIG = {
    "x_range":[0, AX_WIDTH, 1], 
    "y_range":[0, AX_HEIGHT, 1], 
    "x_length":AX_WIDTH/AX_SCALE, 
    "y_length":AX_HEIGHT/AX_SCALE, 
    "tips":False,
}

PX = 2 # price for good x and y
PY = 2
BUDGET = 12 # budget


class IndifferenceCurve:
    # utility function: u = sqrt(x*y)
    # y = u^2/x
    def __init__(self, u):
        self.u = u
        self.f = lambda x: u**2/x
        self.x_range = [self.u**2/AX_HEIGHT, AX_WIDTH]

    def get_graph(self, plane, **config):
        return plane.plot(self.f, x_range=self.x_range, use_smoothing=False, **config)
        # return plane.plot(self.f, x_range=self.x_range, use_smoothing=False, **config)

    def get_coords(self, x=None, y=None):
        # return coordinates of a dot on the budget constraint line
        # given the x or y position of the dot
        if x is not None and y is not None:
            return (x, y)
        if x is not None:
            return (x, self.f(x))
        if y is not None:
            return (self.u**2/y, y)
        return None
    
    def get_pos(self, plane, x=None, y=None):
        # return position of a dot on the budget constraint line relative to given plane
        # given the x or y position of the dot
        return plane.c2p(*self.get_coords(x, y))


class BudgetConstraint:
    def __init__(self, px, py, budget):
        # prices for good x and y
        self.px = px
        self.py = py
        self.budget = budget

        # graph
        k = -px/py
        b = budget/py
        self.k, self.b = k, b
        self.f = lambda x: x*k + b
        self.x_range = [max((AX_HEIGHT - b)/k, 0), min(self.budget/self.px, AX_WIDTH)]

        # indifference curve
        self.u = b/(2*np.sqrt(-k))
        
        # optimal (tangent) point
        _x = budget/px/2
        self.tan_pos = _x, self.f(_x)

    def get_coords(self, x=None, y=None):
        # return coordinates of a dot on the budget constraint line
        # given the x or y position of the dot
        if x is not None and y is not None:
            return (x, y)
        if x is not None:
            return (x, self.f(x))
        if y is not None:
            return ((y - self.b)/self.k, y)
        return None
    
    def get_pos(self, plane, x=None, y=None):
        # return position of a dot on the budget constraint line relative to given plane
        # given the x or y position of the dot
        return plane.c2p(*self.get_coords(x, y))

    def get_graph(self, plane):
        return plane.plot(self.f, x_range=self.x_range, use_smoothing=False)

    def get_ic(self, plane):
        return IndifferenceCurve(self.u)

    def get_ic_graph(self, plane):
        return self.get_ic(plane).get_graph(plane, color=BLUE)

    def get_all_graphs(self, plane):
        bc_graph = self.get_graph(plane)
        ic_graph = self.get_ic_graph(plane)
        optimal_point_dot = Dot(point=plane.c2p(*self.tan_pos))
        
        return VGroup(bc_graph, ic_graph, optimal_point_dot)


class BudgetConstraintIntro(Scene):
    """
    Budget Constraint Introduction

    showing how budget constraint change in response to the change in price of good x (px)
    dot with fixed Qy on budget constraint, moving with the budget constraint line
    (showing that Qx increases when Px decreases; lower price = more goods)
    """
    def construct(self):
        # Qx-Qy plane
        plane = NumberPlane(**AX_CONFIG).shift(LEFT*2)
        labels = plane.get_axis_labels(x_label="Q_x", y_label="Q_y")
        self.add(plane, labels)

        bc = BudgetConstraint(PX, PY, BUDGET)

        p_tracker = ValueTracker(PX)

        bc_graph = bc.get_graph(plane)
        bc_graph.add_updater(
            lambda l: l.become(BudgetConstraint(p_tracker.get_value(), PY, BUDGET).get_graph(plane))
        )

        # Animation #1
        dot = Dot(bc_graph.get_start()).add_updater(
            lambda d: d.move_to(bc.get_pos(plane, x=x_tracker.get_value()))
        )

        self.add(bc_graph, dot)

        x_tracker = ValueTracker(0)
        # x_values = (bc.x_range[1], bc.get_coords(y=2)[0])
        x_values = (bc.x_range[1], bc.x_range[1]/2)
        for x in x_values:
            self.play(
                x_tracker.animate.set_value(x), 
                run_time=2
            )
        self.wait()

        # Animation #2
        # a dot on the budget constraint line with Qy = 2
        init_dot_pos = bc.get_pos(plane, y=2)
        dot.clear_updaters()
        dot.add_updater(lambda d: d.move_to(
            BudgetConstraint(p_tracker.get_value(), PY, BUDGET).get_pos(plane, y=2)
        ))

        # line from dot to y axis (Q_y)
        dot_to_y_ax_line = plane.get_lines_to_point(init_dot_pos)[0].set_color(YELLOW)
        dot_to_y_ax_line.add_updater(lambda l: l.put_start_and_end_on(
            plane.c2p(0, 2), 
            BudgetConstraint(p_tracker.get_value(), PY, BUDGET).get_pos(plane, y=2)
        ))

        # Variable displaying current price
        p_var = Variable(bc.px, "P_x", num_decimal_places=3)
        q_var = Variable(bc.tan_pos[0], 'Q_x', num_decimal_places=3)

        # Group(p_var, q_var).arrange(DOWN)
        p_var.add_updater(lambda v: v.tracker.set_value(p_tracker.get_value()))
        q_var.add_updater(lambda v: v.tracker.set_value(
            BudgetConstraint(p_tracker.get_value(), PY, BUDGET).tan_pos[0]
        ))

        # p_arrow denoting the direction price is changing (up = price increasing)
        # q_arrow denoting the direction of change for quantity
        p_arrow_is_up = True
        p_arrow = Arrow(start=ORIGIN, end=UP)
        q_arrow = Arrow(start=UP, end=ORIGIN).set_color(YELLOW)
        Group(p_var, p_arrow).arrange(RIGHT).shift(UR*2 + RIGHT*.5)
        Group(q_var, q_arrow).arrange(RIGHT).next_to(Group(p_var, p_arrow), DOWN)
        
        self.play(FadeIn(p_var), FadeIn(p_arrow), FadeIn(q_var), FadeIn(q_arrow))
        self.add(dot_to_y_ax_line)

        p_values = (10, BUDGET/AX_WIDTH, 2)
        for p in p_values:
            # update p_arrow direction
            if (p_tracker.get_value() < p) != p_arrow_is_up: 
                p_arrow_is_up = ~p_arrow_is_up
                self.play(
                    Rotate(p_arrow, angle=PI), 
                    Rotate(q_arrow, angle=PI)
                )

            self.play(
                p_tracker.animate.set_value(p), 
                run_time=2
            )

        self.wait()


class IndifferenceCurveIntro(Scene):
    """
    Indifference Curve Introduction
    
    Animation #1: dot moving along a fixed indifference curve
    Animation #2: dot moving with a movning indifference curve
    """
    def construct(self):
        plane = NumberPlane(**AX_CONFIG).shift(LEFT*2)
        labels = plane.get_axis_labels(x_label="Q_x", y_label="Q_y")

        # indifference curve
        ic = IndifferenceCurve(3)
        ic_graph = ic.get_graph(plane)
        
        self.add(plane, labels, ic_graph)

        dot = Dot(ic_graph.get_start()).add_updater(
            lambda d: d.move_to(ic.get_pos(plane, x=x_tracker.get_value()))
        )

        # Variables showing quantities of goods x and y, and utility
        dot_coords = (ic.x_range[0], ic.f(ic.x_range[0]))
        u_var = Variable(ic.u, 'U', num_decimal_places=3)
        qx_var = Variable(dot_coords[0], "Q_x", num_decimal_places=3)
        qy_var = Variable(dot_coords[1], 'Q_y', num_decimal_places=3)

        Group(u_var, qx_var, qy_var).arrange(DOWN).shift(UR*2 + RIGHT*.5)
        qx_var.add_updater(lambda v: v.tracker.set_value(x_tracker.get_value()))
        qy_var.add_updater(lambda v: v.tracker.set_value(
            ic.f(x_tracker.get_value())
        ))

        self.add(dot)
        self.add(u_var, qx_var, qy_var)

        x_tracker = ValueTracker(dot_coords[0])
        x_values = (ic.x_range[1], ic.u)
        for x in x_values:
            self.play(
                x_tracker.animate.set_value(x), 
                run_time=2
            )
        self.wait()

        # Animation #2: dot moving with a moving indifference curve
        # clear updaters for Animation #1
        [m.clear_updaters() for m in (dot, qx_var, qy_var, ic_graph)]

        self.play(
            FadeOut(qx_var), FadeOut(qy_var), u_var.animate().shift(DOWN * 1.5)
        )

        dot.add_updater(
            lambda d: d.move_to(plane.c2p(u_tracker.get_value(), u_tracker.get_value()))
        )

        ic_graph.add_updater(
            lambda l: l.become(IndifferenceCurve(u_tracker.get_value()).get_graph(plane))
        )

        u_var.add_updater(
            lambda v: v.tracker.set_value(u_tracker.get_value()**2)
        )
        
        u_tracker = ValueTracker(ic.u)
        u_values = [7, 1, 3]
        for u in u_values:
            self.play(
                u_tracker.animate.set_value(u), 
                run_time=2
            )
        self.wait()


class IndifferenceCurveIntro2(Scene):
    """
    Indifference Curve Introduction 2
    
    comparing points on indifference curve, 
    showing diminishing marginal utility for consumption of good x
    """
    def construct(self):
        plane = Axes(**AX_CONFIG).shift(LEFT*2)
        labels = plane.get_axis_labels(x_label="Q_x", y_label="Q_y")
        self.add(plane, labels)

        ic = IndifferenceCurve(3)
        ic_graph = ic.get_graph(plane)
        self.add(ic_graph)
        
        dot1 = Dot(point=ic.get_pos(plane, x=1))
        dot2 = Dot(point=ic.get_pos(plane, x=3))
        dot3 = Dot(point=ic.get_pos(plane, y=1))
        label_d1 = Text("A").scale(.5).next_to(dot1, UR/2)
        label_d2 = Text("B").scale(.5).next_to(dot2, UR/2)
        label_d3 = Text("C").scale(.5).next_to(dot3, UR/2)

        line_x1 = Arrow(ic.get_pos(plane, x=1), plane.c2p(3, 9), buff=0).set_color(GREEN)
        line_y1 = Arrow(plane.c2p(3, 9), ic.get_pos(plane, x=3), buff=0).set_color(RED)
        label_x1 = Text("+2X").scale(.5).next_to(line_x1, DOWN).set_color(GREEN)
        label_y1 = Text("-6Y").scale(.5).next_to(line_y1, RIGHT).set_color(RED)

        line_x2 = Arrow(ic.get_pos(plane, x=3), plane.c2p(9, 3), buff=0).set_color(GREEN)
        line_y2 = Arrow(plane.c2p(9, 3), ic.get_pos(plane, y=1), buff=0).set_color(RED)
        label_x2 = Text("+6X").scale(.5).next_to(line_x2, UP).set_color(GREEN)
        label_y2 = Text("-2Y").scale(.5).next_to(line_y2, LEFT).set_color(RED)

        # explanations before simplifying equation
        _explanation_1 = MathTex(r"A \rightarrow B: 2X=6Y").scale(.75).shift(UR*2 + RIGHT*.5)
        _explanation_2 = MathTex(r"B \rightarrow C: 6X=2Y").scale(.75).next_to(_explanation_1, DOWN)
        # explanations after simplifying equation
        explanation_1 = MathTex(r"A \rightarrow B: X=2Y").scale(.75).shift(UR*2 + RIGHT*.5)
        explanation_2 = MathTex(r"B \rightarrow C: X= \frac{1} {3} Y").scale(.75).next_to(explanation_1, DOWN)

        self.play(*(FadeIn(e) for e in (dot1, dot2, dot3, label_d1, label_d2, label_d3)))

        self.play(*(FadeIn(e) for e in (line_x1, line_y1, label_x1, label_y1)))
        self.play(FadeIn(_explanation_1))
        self.play(Transform(_explanation_1, explanation_1))
        self.wait()

        self.play(*(FadeIn(e) for e in (line_x2, line_y2, label_x2, label_y2)))
        self.play(FadeIn(_explanation_2))
        self.wait()
        
        self.play(Transform(_explanation_2, explanation_2))
        self.wait()

        # self.play(*(FadeOut(e) for e in (
        #     dot1, dot2, dot3, label_d1, label_d2, label_d3, 
        #     line_x1, line_y1, label_x1, label_y1, _explanation_1, 
        #     line_x2, line_y2, label_x2, label_y2, _explanation_2
        # )))


class IndifferenceCurveIntro3(Scene):
    """
    Indifference Curve Introduction 3
    
    comparing how much of good Y would one trade 
    for a unit of good X on each point on the indifference curve
    Animation #3: showing MRS for each point on the indifference curve
    """
    def construct(self):
        plane = Axes(**AX_CONFIG).shift(LEFT*2)
        labels = plane.get_axis_labels(x_label="Q_x", y_label="Q_y")
        self.add(plane, labels)

        ic = IndifferenceCurve(3)
        ic_graph = ic.get_graph(plane)
        self.add(ic_graph)

        dot = Dot(ic_graph.get_start()).add_updater(
            lambda d: d.move_to(ic.get_pos(plane, x=x_tracker.get_value()))
        )

        # Variables showing quantities of goods x and y, and utility
        dot_coords = (ic.x_range[0], ic.f(ic.x_range[0]))
        u_var = Variable(ic.u, 'U', num_decimal_places=3)
        qx_var = Variable(dot_coords[0], "Q_x", num_decimal_places=3)
        qy_var = Variable(dot_coords[1], 'Q_y', num_decimal_places=3)

        Group(u_var, qx_var, qy_var).arrange(DOWN).shift(UR*2 + RIGHT*.5)
        qx_var.add_updater(lambda v: v.tracker.set_value(x_tracker.get_value()))
        qy_var.add_updater(lambda v: v.tracker.set_value(
            ic.f(x_tracker.get_value())
        ))

        self.add(dot)
        self.add(u_var, qx_var, qy_var)

        x_tracker = ValueTracker(dot_coords[0])
        x_values = (ic.x_range[1], ic.u)
        for x in x_values:
            self.play(
                x_tracker.animate.set_value(x), 
                run_time=2
            )
        self.wait()




        # Animation #?: multiple indifference curves, color showing utility (darker = higher utility)
        # U_MAX = 10
        # for u in np.linspace(0.1, U_MAX, 200):
        #     L = 30
        #     H = 255
        #     # hex_val = hex(int(L + (H - L)/U_MAX**.5*u**.5))[2:] # hex value for each r, g, and b
        #     hex_val = hex(int(H - (H - L)/U_MAX**.5*u**.5))[2:] # hex value for each r, g, and b
        #     if len(hex_val) == 1:
        #         hex_val = "0" + hex_val
        #     rgb_color = "#" + hex_val*3 # color in rgb hex
        #     ic_graph = IndifferenceCurve(u).get_graph(plane, color=rgb_color)
        #     self.add(ic_graph)


class DerivingDemandCurve(Scene):
    """
    Deriving Demand Curve

    showing how budget constraint and highest indifference curve 
    respond to changes in price of good x (px) and plotting 
    the derived demand curve on a Price-Quantity plane 
    """
    def construct(self):
        # Qx-Qy plane, for budget constraints and indifference curves
        plane = NumberPlane(**AX_CONFIG).shift(LEFT*3)
        labels = plane.get_axis_labels(x_label="Q_x", y_label="Q_y")

        # Q-P plane for good x, for budget constraints and indifference curves
        plane2 = NumberPlane(**AX_CONFIG).shift(RIGHT*3)
        labels2 = plane2.get_axis_labels(x_label="Q_x", y_label="P_x")

        # add number planes
        self.add(plane, labels)
        self.add(plane2, labels2)

        # graphs on plane
        bc = BudgetConstraint(PX, PY, BUDGET)

        p_tracker = ValueTracker(PX)
        # self.p_tracker = p_tracker
        bc_graphs = bc.get_all_graphs(plane)
        bc_graphs.add_updater(
            lambda l: l.become(BudgetConstraint(p_tracker.get_value(), PY, BUDGET).get_all_graphs(plane))
        )

        # Variables displaying values of Px and Qx
        p_var = Variable(bc.px, "P_x", num_decimal_places=3)
        q_var = Variable(bc.tan_pos[0], 'Q_x', num_decimal_places=3)

        Group(p_var, q_var).arrange(DOWN).shift(LEFT + UP*2.5)
        p_var.add_updater(lambda v: v.tracker.set_value(p_tracker.get_value()))
        q_var.add_updater(lambda v: v.tracker.set_value(
            BudgetConstraint(p_tracker.get_value(), PY, BUDGET).tan_pos[0]
        ))

        self.play(FadeIn(bc_graphs), FadeIn(p_var), FadeIn(q_var))

        # demand curve on the Q-P plane 
        self.last_dot_pos = (bc.tan_pos[0], bc.px)
        self.demand_curve = VGroup()
        self.demand_curve.add(Line(
            plane2.c2p(*self.last_dot_pos), plane2.c2p(*self.last_dot_pos)
        ))

        def demand_dot(): # (Q, P)
            px = p_tracker.get_value()
            qx = BudgetConstraint(px, PY, BUDGET).tan_pos[0]
            self.last_dot_pos = (qx, px)
            return Dot(point=plane2.coords_to_point(qx, px))

        def demand_curve():
            last_line = self.demand_curve[-1]
            # print(last_line.get_end(), self.last_dot_pos)
            new_line = Line(last_line.get_end(), plane2.c2p(*self.last_dot_pos), color=YELLOW_D)
            self.demand_curve.add(new_line)
            return self.demand_curve

        demand_dot = always_redraw(demand_dot)
        demand_curve = always_redraw(demand_curve)
        self.add(demand_dot, demand_curve)

        # animation: BC and IC moves as Px moves
        px_values = (9, BUDGET/AX_WIDTH/2, PX)
        for px in px_values:
            self.play(
                p_tracker.animate.set_value(px), 
                run_time=2
            )

        self.wait()


