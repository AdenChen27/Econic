"""
Utility func: u = x^p + y
"""

from manim import *

S_HEIGHT = 8
S_WIDTH = 14
P = .82



class IndifferenceCurve:
    # utility function: u = x^p + y
    # y = -x^p + u
    def __init__(self, ax, u, p=P):
        self.p = p
        self.u = u
        
        self.f = lambda x: -x**p + u
        self.x_range = [0, min(u**(1/p), S_WIDTH)]

        self.graph = ax.plot(self.f, x_range=self.x_range, use_smoothing=False, color=BLUE)


class BudgetConstraint:
    def __init__(self, ax, px, py, budget):
        # prices for good x and y
        self.ax = ax
        self.px = px
        self.py = py
        self.budget = budget

        # graph
        k = -px/py
        b = budget/py
        self.k, self.b = k, b
        self.f = lambda x: x*k + b
        x_range = [0, budget/px]
        self.graph = ax.plot(self.f, x_range=x_range, use_smoothing=False)

        # indifference curve
        t = (k/-P)**(1/(P-1))
        u = b + k*t + t**P
        self.ic = IndifferenceCurve(self.ax, u)
        
        self.tan_pos = t, self.f(t)
        self.tan_dot = self.get_dot(t)

        # graphs
        self.graphs = VGroup(self.graph, self.ic.graph, self.tan_dot)

    def get_dot(self, x):
        y = self.f(x)
        return Dot(point=self.ax.coords_to_point(x, y))



class DemandCurveOrigin(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0, S_WIDTH, 1],
            y_range=[0, S_HEIGHT, 1],
            x_length=S_WIDTH/1.5,
            y_length=S_HEIGHT/1.5,
            tips=False,
            # axis_config={"include_numbers": True},
        ).add_coordinates()

        labels = ax.get_axis_labels(x_label="Q_x", y_label="Q_y")
        self.add(ax, labels)

        # prices for good x and y, and budget
        PX = 2
        PY = 1.5
        B = 12
        bc = BudgetConstraint(ax, PX, PY, B)

        tracker = ValueTracker(PY)
        # tracker = ValueTracker(PX)

        def updater(z):
            new_bc = BudgetConstraint(ax, PX, tracker.get_value(), B)
            # new_bc = BudgetConstraint(ax, tracker.get_value(), PY, B)
            z.become(new_bc.graphs)

        bc.graphs.add_updater(updater)
        self.play(Create(bc.graphs))

        # changing PX
        """
        demand_curve = ax.plot(
            lambda px: -P*px**P + bc.b, 
            x_range=[.1, S_WIDTH], 
            color=YELLOW_B
        )

        px_values = (.8, )
        for px in px_values:
            self.play(
                tracker.animate.set_value(px), 
                Create(demand_curve), 
                run_time=2
            )
        
        self.wait(1)
        """

        # changing PY
        # the actural demand curve
        A = (PX/P)**(1/(P-1))
        demand_curve = ax.plot(
            lambda x: -PX*A*(x/A)**P + B*(x/A)**(P-1), 
            x_range=[.1, min(B/PX, S_WIDTH)], 
            color=YELLOW_B
        )

        self.play(
            tracker.animate.set_value(3.2), 
            Create(demand_curve), 
            run_time=2
        )
        self.wait(.5)

        bc.graphs.remove_updater(updater)
        self.play(
            FadeOut(bc.graphs), 
            Create(Text("D").next_to(demand_curve.get_end(), UP)), 
        )

        self.wait(1)





