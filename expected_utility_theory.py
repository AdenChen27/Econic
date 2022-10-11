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
    # "axis_config": {"include_numbers": True}
}


class UtilityIntro(Scene):
    """
    Utilty Introduction

    derive utility-wealth function from indifference curve
    """
    def construct(self):
        # W-U plane for utility-wealth function
        plane = Axes(**AX_CONFIG).shift(LEFT*2)
        labels = plane.get_axis_labels(x_label="W", y_label="U")

        # utility function over wealth u(w)
        ufunc = plane.plot(lambda x: x**.7)
        
        self.add(plane, labels)
        self.add(ufunc)

