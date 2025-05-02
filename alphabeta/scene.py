from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
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

class Intro(Scene):
    def construct(self):
        intro = Tex("Minimax", font_size=96).shift(UP*2)
        self.play(Write(intro), run_time=2.5)
        bullets = (Tex(r"Zero-sum games\\Optimal play"))
        self.play(Write(bullets), run_time=4.8)
        self.wait(8.5)
        agenda = Tex(r"\underline{Today's agenda}", font_size=96).to_corner(UL)
        self.play(Unwrite(intro), Unwrite(bullets))

        self.play(Write(agenda))
        first_point = (Tex(r"-Flaw in minimax")).next_to(agenda, DOWN*1.5).align_to(agenda, LEFT)
        second_point = (Tex(r"-Variant of minimax")).next_to(first_point, DOWN).align_to(agenda, LEFT)
        third_point = (Tex(r"-Minimax optimisations")).next_to(second_point, DOWN).align_to(agenda, LEFT)
        self.play(Write(first_point), run_time=2.5)
        self.wait(3)
        self.play(Write(second_point), run_time=4.5)
        self.play(Write(third_point), run_time=3)

        self.play(Unwrite(agenda), Unwrite(first_point), Unwrite(second_point), Unwrite(third_point), run_time=5)

class AnimateMinimax(Scene):
    RADIUS = 0.35
    VERTEX_CONFIG = {"stroke_width": 2, "stroke_color": WHITE, "radius": RADIUS, "color":BLACK, "fill_opacity": 1}
    LAYOUT_SCALE = (6, 3)

    def Minimax(self, displayed_tree: Graph, internal_tree: Tree, current_node: int, is_maximiser: bool):
        displayed_node = displayed_tree[current_node]

        if current_node not in internal_tree.edges_dict: #checks if current_node is a leaf
            return internal_tree.scores[current_node]
        

        if is_maximiser:
            initial_score_above_node = MathTex(r"-\infty")
            self.play(Write(initial_score_above_node.next_to(displayed_node, UP)))
            best_so_far = -10
            for children_node in internal_tree.edges_dict[current_node]:
                self.play(Indicate(displayed_tree.edges[(current_node, children_node)]))
                child_score = self.Minimax(displayed_tree, internal_tree, children_node, False)
                compared_score_above_node = MathTex(NumToStr(best_so_far) + r"\ vs\ " + NumToStr(child_score)).next_to(displayed_node, UP)
                best_so_far = max(best_so_far, child_score)
                self.play(Transform(initial_score_above_node, compared_score_above_node))
                self.wait(0.3)
                self.play(Transform(initial_score_above_node, MathTex(NumToStr(best_so_far)).next_to(displayed_node, UP)))
        else:
            best_so_far = 10
            initial_score_above_node = MathTex(r"\infty")
            self.play(Write(initial_score_above_node.next_to(displayed_node, UP)))
            for children_node in internal_tree.edges_dict[current_node]:
                self.play(Indicate(displayed_tree.edges[(current_node, children_node)]))
                child_score = self.Minimax(displayed_tree, internal_tree, children_node, True)
                compared_score_above_node = MathTex(NumToStr(best_so_far) + r"\ vs\ " + NumToStr(child_score)).next_to(displayed_node, UP)
                best_so_far = min(best_so_far, child_score)
                self.play(Transform(initial_score_above_node, compared_score_above_node))
                self.wait(0.3)
                self.play(Transform(initial_score_above_node, MathTex(NumToStr(best_so_far)).next_to(displayed_node, UP)))

        self.play(Unwrite(initial_score_above_node))
        self.play(FadeIn(MathTex(NumToStr(best_so_far)).move_to(displayed_node), scale=1.5))
        return best_so_far
            
    def construct(self):
        
        #Chapter 1: Minimax
        chapter_1 = Tex(r"\textbf{\underline{\Large Chapter 1}}\\~\\ Minimax")
        self.play(FadeIn(chapter_1, scale=3), run_time=3)
        self.wait(0.5)
        self.play(FadeOut(chapter_1), run_time=2)

        avg_branching_factor = 2
        max_depth = 5
        internal_tree = Tree()
        print(internal_tree)
        minimax_tree = GetMinimaxTree(internal_tree)

        displayed_minimax_tree = Graph([i for i in range(1, minimax_tree.size)],
            minimax_tree.edges_list,
            layout="tree",
            layout_config={"root_vertex":1},
            layout_scale=self.LAYOUT_SCALE,
            vertex_config=self.VERTEX_CONFIG,
            labels=minimax_tree.labels
        ).flip(axis=UP).move_to(RIGHT*0.5)

        self.play(Write(displayed_minimax_tree))
        self.wait()
        
        self.play(*[Indicate(displayed_minimax_tree[node]) for node in range(1, minimax_tree.size)])
        self.wait(3.4)

        print(displayed_minimax_tree.edges)
        self.play(*[Indicate(edge) for edge in displayed_minimax_tree.edges.values()])
        self.wait(5.5)

        self.play(*[Indicate(displayed_minimax_tree[node][1]) for node in range(1, minimax_tree.size) if minimax_tree.scores[node] is not None])
        self.wait(22)

        maximiser_group = [VGroup(Rectangle(color=RED, height=8/max_depth, width=14+2/9, fill_opacity=0.5, stroke_width=0).shift((0, rect_offset*8/max_depth, 0)).set_z_index(-100), Tex("Max", color=RED).move_to((-6.5, rect_offset*8/max_depth, 0))) for rect_offset in range(-max_depth, max_depth) if rect_offset%2==0]

        minimiser_group = [VGroup(Rectangle(color=BLUE, height=8/max_depth, width=14+2/9, fill_opacity=0.5, stroke_width=0).shift((0, rect_offset*8/max_depth, 0)).set_z_index(-100), Tex("Min", color=BLUE).move_to((-6.5, rect_offset*8/max_depth, 0))) for rect_offset in range(-max_depth, max_depth) if rect_offset%2==1]

        
        self.play(*[Write(maximiser) for maximiser in maximiser_group], *[Write(minimiser) for minimiser in minimiser_group])

        self.Minimax(displayed_minimax_tree, internal_tree, current_node=1, is_maximiser=True)

        self.play(*[FadeOut(mobject) for mobject in self.mobjects], run_time=5)


class AnimateNegamax(Scene):
    RADIUS = 0.35
    VERTEX_CONFIG = {"stroke_width": 2, "stroke_color": WHITE, "radius": RADIUS, "color":BLACK, "fill_opacity": 1}
    LAYOUT_SCALE = (6, 3)
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

    def ABNegamax(self, displayed_tree: Graph, internal_tree: Tree, text_list: list, current_node: int, side_to_move: int, alpha=-10, beta=10):

        def WriteAlphaBeta(text_list, node, text: Mobject):
            if text_list[node] == None:
                text_list[node] = text
                return Write(text)
            else:
                return Transform(text_list[current_node], text)

        if current_node == 1:
            text = MakeAlphaBeta(alpha, beta).scale(0.35).next_to(displayed_tree[1], LEFT*0.15)
            self.play(WriteAlphaBeta(text_list, 1, text))

        best_so_far = -10

        #Display parent's ab values
        displayed_node = displayed_tree[current_node]

        if current_node not in internal_tree.edges_dict: #checks if current_node is a leaf
            best_so_far = internal_tree.scores[current_node]
            if best_so_far > alpha:
                alpha = best_so_far
            text = MakeAlphaBeta(alpha, beta).scale(0.35).next_to(displayed_node, LEFT*0.15)
            self.play(WriteAlphaBeta(text_list, current_node, text))
            self.AddRectangle(displayed_node, current_node, alpha, beta)
            return best_so_far
        
        for children_node in internal_tree.edges_dict[current_node]:
            text = MakeAlphaBeta(-beta, -alpha).scale(0.35).next_to(displayed_tree[children_node], LEFT*0.15)
            self.play(Indicate(displayed_tree.edges[(current_node, children_node)]), WriteAlphaBeta(text_list, children_node, text))

            best_so_far = max(best_so_far, -self.ABNegamax(displayed_tree, internal_tree, text_list, children_node, -side_to_move, -beta, -alpha))
            if best_so_far > alpha:
                alpha = best_so_far

            text = MakeAlphaBeta(alpha, beta).scale(0.35).next_to(displayed_node, LEFT*0.15)
            self.play(Indicate(displayed_tree.edges[(current_node, children_node)]), WriteAlphaBeta(text_list, current_node, text))
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
        pass
        #Negamax
        # self.next_section()
        # displayed_tree = Graph([i for i in range(1, internal_tree.size)],
        #     internal_tree.edges_list,
        #     layout="tree",
        #     layout_config={"root_vertex":1},
        #     layout_scale=self.LAYOUT_SCALE,
        #     vertex_config=self.VERTEX_CONFIG,
        #     labels=internal_tree.labels
        # ).flip(axis=UP).move_to(RIGHT*0.5)

        # self.play(Write(displayed_tree))

        # text_list = [None for _ in range(1, internal_tree.size)]
        # self.RECTANGLE_GROUP = [None for _ in range(1, internal_tree.size)]
        #self.ABNegamax(displayed_tree, internal_tree, text_list, current_node=1, side_to_move=1)

        #Window part
        # self.next_section()
        # self.play(*[ReplacementTransform(text, rectangle_group) for text, rectangle_group in zip(text_list, self.RECTANGLE_GROUP)])



# with tempconfig({"quality": "medium_quality", "disable_caching": True}):
#     scene = AnimateTree()
#     scene.render()