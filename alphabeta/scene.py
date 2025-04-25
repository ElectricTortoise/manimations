from manim import *
from tree import *
import numpy as np
import random as Rand
from collections import deque

def NumToStr(num):
    if num == math.inf:
        return r"\infty"
    elif num == -math.inf:
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

    #Negamax search algorithm
    def Search(self, displayed_tree: Graph, internal_tree: Tree, text_list: list, current_node: int, side_to_move: int, alpha=-math.inf, beta=math.inf):

        def WriteAlphaBeta(text_list, node, text: Mobject):
            if text_list[node] == None:
                text_list[node] = text
                self.play(Write(text))
            else:
                self.play(Transform(text_list[current_node], text))

        bestSoFar = alpha

        #Display parent's ab values
        displayed_node = displayed_tree[current_node]
        text = MakeAlphaBeta(alpha, beta).scale(0.35).next_to(displayed_node, LEFT*0.15)
        WriteAlphaBeta(text_list, current_node, text)

        if current_node not in internal_tree.edges_dict: #checks if current_node is a leaf
            bestSoFar = internal_tree.scores[current_node] * side_to_move
            if bestSoFar > alpha:
                alpha = bestSoFar
            text = MakeAlphaBeta(alpha, beta).scale(0.35).next_to(displayed_node, LEFT*0.15)
            WriteAlphaBeta(text_list, current_node, text)
            return bestSoFar
        
        for children_node in internal_tree.edges_dict[current_node]:
            self.play(Indicate(displayed_tree.edges[(current_node, children_node)]))

            bestSoFar = max(bestSoFar, -self.Search(displayed_tree, internal_tree, text_list, children_node, -side_to_move, -beta, -alpha))
            if bestSoFar > alpha:
                alpha = bestSoFar
            if alpha >= beta:
                self.play(Write(MathTex(NumToStr(bestSoFar*side_to_move)).move_to(displayed_node)))
                self.play(Create(Cross(scale_factor=self.RADIUS).move_to(displayed_node)))
                return bestSoFar
            
            text = MakeAlphaBeta(alpha, beta).scale(0.35).next_to(displayed_node, LEFT*0.15)
            self.play(Indicate(displayed_tree.edges[(current_node, children_node)]))
            WriteAlphaBeta(text_list, current_node, text)
        
        self.play(Write(MathTex(NumToStr(bestSoFar*side_to_move)).move_to(displayed_node)))

        return bestSoFar
            
    def construct(self):
        #Generates the tree
        depth = 4
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

        run_time = (internal_tree.size)/3

        self.play(Write(displayed_tree, run_time=run_time))
        self.wait()
        
        #Starts searching
        self.next_section()
        text_list = [None, MakeAlphaBeta(-math.inf, math.inf).scale(0.35).next_to(displayed_tree[1], LEFT*0.15)]
        self.play(Write(text_list[1]))
        for internal_node in range(1, internal_tree.size):
            text = None
            text_list.append(text)
        self.Search(displayed_tree, internal_tree, text_list, current_node=1, side_to_move=1)


# with tempconfig({"quality": "medium_quality", "disable_caching": True}):
#     scene = AnimateTree()
#     scene.render()