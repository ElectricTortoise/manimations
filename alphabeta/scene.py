from manim import *
from tree import *
import numpy as np
import random as Rand
from collections import deque

def NumToStr(num):
    if num == 10:
        return r"\infty"
    elif num == -10:
        return r"-\infty"
    else:
        return str(num)

def MakeAlphaBeta(alpha, beta):
    alpha = NumToStr(alpha)
    beta = NumToStr(beta)
    text = MathTex(fr"\alpha:{alpha}\\\beta:{beta}",
                        substrings_to_isolate=(r"\alpha", r"\beta"))
    text.set_color_by_tex(r"\alpha", RED)
    text.set_color_by_tex(r"\beta", BLUE)
    return text

class AnimateTree(Scene):
    RADIUS = 0.35
    VERTEX_CONFIG = {"stroke_width": 2, "stroke_color": WHITE, "radius": RADIUS, "color":BLACK, "fill_opacity": 1}
    LAYOUT_SCALE = (6, 3.5)
    RECTANGLE_GROUP = []

    def AddRectangle(self, displayed_node, current_node, alpha, beta):
        rect_height = (self.RADIUS/10)*abs(beta-alpha)

        rect = Rectangle(width=0.35, height=rect_height, stroke_width=1, fill_opacity=0.5).set_color([RED,BLUE]).next_to(displayed_node, LEFT*0.3).shift((0,(self.RADIUS/10)*((alpha+beta)/2),0))
        
        (sheen_direction, alpha_pos, beta_pos) = (UP, rect.get_bottom()+0.1*DOWN, rect.get_top()+0.1*UP) if alpha < beta else (DOWN, rect.get_top()+0.1*UP, rect.get_bottom()+0.1*DOWN)
        rect.set_sheen_direction(sheen_direction)
        
        alpha_tex = MathTex(fr"\alpha:{NumToStr(alpha)}", substrings_to_isolate=(r"\alpha",)).scale(0.35).move_to(alpha_pos)
        alpha_tex.set_color_by_tex(r"\alpha", RED)
        beta_tex = MathTex(fr"\beta:{NumToStr(beta)}", substrings_to_isolate=(r"\beta",)).scale(0.35).move_to(beta_pos)
        beta_tex.set_color_by_tex(r"\beta", BLUE)

        rect_group = VGroup(rect, alpha_tex, beta_tex)
        self.RECTANGLE_GROUP[current_node] = rect_group

    #Negamax search algorithm
    def Search(self, displayed_tree: Graph, internal_tree: Tree, text_list: list, current_node: int, side_to_move: int, alpha=-10, beta=10):

        def WriteAlphaBeta(text_list, node, text: Mobject):
            if text_list[node] == None:
                text_list[node] = text
                self.play(Write(text))
            else:
                self.play(Transform(text_list[current_node], text))

        best_so_far = -10

        #Display parent's ab values
        displayed_node = displayed_tree[current_node]
        text = MakeAlphaBeta(alpha, beta).scale(0.35).next_to(displayed_node, LEFT*0.15)
        WriteAlphaBeta(text_list, current_node, text)

        if current_node not in internal_tree.edges_dict: #checks if current_node is a leaf
            best_so_far = internal_tree.scores[current_node]
            if best_so_far > alpha:
                alpha = best_so_far
            text = MakeAlphaBeta(alpha, beta).scale(0.35).next_to(displayed_node, LEFT*0.15)
            WriteAlphaBeta(text_list, current_node, text)
            self.AddRectangle(displayed_node, current_node, alpha, beta)
            return best_so_far
        
        for children_node in internal_tree.edges_dict[current_node]:
            self.play(Indicate(displayed_tree.edges[(current_node, children_node)]))

            best_so_far = max(best_so_far, -self.Search(displayed_tree, internal_tree, text_list, children_node, -side_to_move, -beta, -alpha))
            if best_so_far > alpha:
                alpha = best_so_far

            text = MakeAlphaBeta(alpha, beta).scale(0.35).next_to(displayed_node, LEFT*0.15)
            self.play(Indicate(displayed_tree.edges[(current_node, children_node)]))
            WriteAlphaBeta(text_list, current_node, text)
            beta_cutoff = False

            if alpha >= beta:
                beta_cutoff = True
                break
            
        self.play(FadeIn(MathTex(NumToStr(best_so_far)).move_to(displayed_node), scale=1.5))

        if beta_cutoff:
            children_node += 1
            while(children_node in internal_tree.edges_dict[current_node]):
                self.play(Create(Cross(scale_factor=self.RADIUS-0.1).move_to(displayed_tree.edges[(current_node, children_node)])) )
                children_node += 1
            
        self.AddRectangle(displayed_node, current_node, alpha, beta)

        return best_so_far
            
    def construct(self):
        #Generates the tree
        depth = 5
        avg_branching_factor = 2
        
        internal_tree = Tree()
        print(internal_tree)

        displayed_tree = Graph([i for i in range(1, internal_tree.size)],
            internal_tree.edges_list,
            layout="tree",
            layout_config={"root_vertex":1},
            layout_scale=self.LAYOUT_SCALE,
            vertex_config=self.VERTEX_CONFIG,
            labels=internal_tree.labels
        ).flip(axis=UP).move_to(RIGHT*0.5)

        self.play(Write(displayed_tree))
        self.wait()
        
        #Starts searching
        self.next_section()
        text_list = [None for _ in range(1, internal_tree.size)]
        self.RECTANGLE_GROUP = [None for _ in range(1, internal_tree.size)]
        self.Search(displayed_tree, internal_tree, text_list, current_node=1, side_to_move=1)

        #Window part
        self.next_section()
        self.play(*[ReplacementTransform(text, rectangle_group) for text, rectangle_group in zip(text_list, self.RECTANGLE_GROUP)])



# with tempconfig({"quality": "medium_quality", "disable_caching": True}):
#     scene = AnimateTree()
#     scene.render()