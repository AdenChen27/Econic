from manim import *
from demand_curve import IndifferenceCurve, BudgetConstraint

AX_HEIGHT = 10
AX_WIDTH = 10
AX_SCALE = 2
AX_CONFIG = {
    "x_range": [0, AX_WIDTH, 1], 
    "y_range": [0, AX_HEIGHT, 1], 
    "x_length": AX_WIDTH/AX_SCALE, 
    "y_length": AX_HEIGHT/AX_SCALE, 
    "tips": False,
    "axis_config": {"include_numbers": True}
}

WU_PLANE_CONFIG = {
    "x_range": [0, AX_WIDTH, 1], 
    "y_range": [0, AX_HEIGHT, 1], 
    "x_length": AX_WIDTH/AX_SCALE, 
    "y_length": AX_HEIGHT/AX_SCALE, 
    "tips": False,
    "axis_config": {"include_numbers": True}, 
    "y_axis_config": {"scaling": LogBase(custom_labels=True)}
}


PX = 2 # price for good x and y
PY = 2
BUDGET = 12 # budget


class UtilityIntro(Scene):
    """
    Utilty Introduction

    derive utility-wealth function from indifference curve
    """
    def construct(self):
        # Qx-Qy plane, for budget constraints and indifference curves
        plane = Axes(**AX_CONFIG).shift(LEFT*3)
        labels = plane.get_axis_labels(x_label="Q_x", y_label="Q_y")

        # W-U plane for utility-wealth function
        # plane2 = Axes(**WU_PLANE_CONFIG).shift(RIGHT*3)
        plane2 = Axes(**AX_CONFIG).shift(RIGHT*3)
        labels2 = plane2.get_axis_labels(x_label="W", y_label="U")

        # budget (wealth) tracker
        b_tracker = ValueTracker(BUDGET)

        # budget constraint 
        bc = BudgetConstraint(PX, PY, BUDGET)
        bc_graphs = bc.get_all_graphs(plane)
        bc_graphs.add_updater(
            lambda l: l.become(BudgetConstraint(PX, PY, b_tracker.get_value()).get_all_graphs(plane))
        )
        
        # displaying current budget and maxium utility
        b_var = Variable(BUDGET, "B(W)", num_decimal_places=2)
        u_var = Variable(BUDGET, "U^*", num_decimal_places=2)

        Group(b_var, u_var).arrange(DOWN).shift(LEFT*1.5 + UP*2.5)
        
        b_var.add_updater(lambda v: v.tracker.set_value(
            b_tracker.get_value()
        ))

        u_var.add_updater(lambda v: v.tracker.set_value(
            BudgetConstraint(PX, PY, b_tracker.get_value()).u
        ))

        # dot on utility-wealth function
        dot = Dot().add_updater(lambda d: d.move_to(plane2.c2p(
            b_tracker.get_value(), 
            BudgetConstraint(PX, PY, b_tracker.get_value()).u**2
        )))
        
        self.add(plane, labels)
        self.add(plane2, labels2)
        self.add(bc_graphs, b_var, u_var, dot)

        b_values = (BUDGET*2, BUDGET/5, BUDGET)
        for b in b_values:
            self.play(
                b_tracker.animate.set_value(b), 
                run_time=2
            )

        # self.wait()
