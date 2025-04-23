from manim import *
from tree import *
import numpy as np
import random as Rand
from collections import deque

class AnimateTree(Scene):
    VERTEX_CONFIG = {"stroke_width": 2, "stroke_color": WHITE, "radius": 0.35, "color":BLACK, "fill_opacity": 1}
    LAYOUT_SCALE = (6, 3.5)
    def construct(self):
        #Generates the tree
        depth = 3
        avg_branching_factor = 2
        
        internal_tree = Tree(avg_branching_factor, depth)
        tree_size = len(internal_tree.edges_list)

        displayed_tree = Graph([i for i in range(1, tree_size + 2)],
            internal_tree.edges_list,
            layout="tree",
            layout_config={"root_vertex":1},
            layout_scale=self.LAYOUT_SCALE,
            vertex_config=self.VERTEX_CONFIG,
            labels=internal_tree.labels
        ).move_to(RIGHT*0.5)

        run_time = (tree_size + 2)/3

        self.play(Write(displayed_tree, run_time=run_time))
        self.wait()
        
        # #Introduces alpha and beta
        self.next_section()
        for i in range(1, tree_size+2):
            node = displayed_tree[tree_size+2-i]
            text = MathTex(r"{{\alpha}} = -\infty \\ {{\beta}} = \infty").scale(0.35).next_to(node, LEFT*0.15)
            text.set_color_by_tex("alpha", RED)
            text.set_color_by_tex("beta", BLUE)

            self.play(Create(text, run_time = 0.2))
