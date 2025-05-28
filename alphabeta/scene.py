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

        self.play(*[FadeOut(edge) for edge in displayed_minimax_tree.edges.values()], run_time=2)
        self.play(*[FadeOut(mobject) for mobject in self.mobjects], run_time=3)

class AnimateNegamaxTree(Scene):
    RADIUS = 0.35
    VERTEX_CONFIG = {"stroke_width": 2, "stroke_color": WHITE, "radius": RADIUS, "color":BLACK, "fill_opacity": 1}
    LAYOUT_SCALE = (6, 3)
    
    def Negamax(self, displayed_tree: Graph, internal_tree: Tree, current_node: int):
        displayed_node = displayed_tree[current_node]

        if current_node not in internal_tree.edges_dict: #checks if current_node is a leaf
            return internal_tree.scores[current_node]
        

        best_so_far = -10
        initial_score_above_node = MathTex(r"-\infty")
        for children_node in internal_tree.edges_dict[current_node]:
            self.play(Indicate(displayed_tree.edges[(current_node, children_node)]))
            child_score = self.Negamax(displayed_tree, internal_tree, children_node)
            compared_score_above_node = MathTex(NumToStr(best_so_far) + r"\ vs\ " + NumToStr(child_score)).next_to(displayed_node, UP)
            best_so_far = max(best_so_far, -child_score)
            self.play(Transform(initial_score_above_node, compared_score_above_node))
            self.wait(0.3)
            self.play(Transform(initial_score_above_node, MathTex(NumToStr(best_so_far)).next_to(displayed_node, UP)))

        self.play(Unwrite(initial_score_above_node))
        self.play(FadeIn(MathTex(NumToStr(best_so_far)).move_to(displayed_node), scale=1.5))
        return best_so_far
    
    def construct(self):

        avg_branching_factor = 2
        max_depth = 5

        internal_tree = Tree()
        FillTree(internal_tree, is_minimax=False)
        displayed_negamax_tree = Graph([i for i in range(1, internal_tree.size)],
            internal_tree.edges_list,
            layout="tree",
            layout_config={"root_vertex":1},
            layout_scale=self.LAYOUT_SCALE,
            vertex_config=self.VERTEX_CONFIG,
            labels=internal_tree.labels
        ).flip(axis=UP).move_to(RIGHT*0.5)

        minimax_tree = GetMinimaxTree(internal_tree)
        FillTree(minimax_tree, is_minimax=True)
        displayed_minimax_tree = Graph([i for i in range(1, minimax_tree.size)],
            minimax_tree.edges_list,
            layout="tree",
            layout_config={"root_vertex":1},
            layout_scale=self.LAYOUT_SCALE,
            vertex_config=self.VERTEX_CONFIG,
            labels=minimax_tree.labels
        ).flip(axis=UP).move_to(RIGHT*0.5)

        maximiser_group = [VGroup(Rectangle(color=RED, height=8/max_depth, width=14+2/9, fill_opacity=0.5, stroke_width=0).shift((0, rect_offset*8/max_depth, 0)).set_z_index(-100), Tex("Max", color=RED).move_to((-6.5, rect_offset*8/max_depth, 0))) for rect_offset in range(-max_depth, max_depth) if rect_offset%2==0]

        minimiser_group = [VGroup(Rectangle(color=BLUE, height=8/max_depth, width=14+2/9, fill_opacity=0.5, stroke_width=0).shift((0, rect_offset*8/max_depth, 0)).set_z_index(-100), Tex("Min", color=BLUE).move_to((-6.5, rect_offset*8/max_depth, 0))) for rect_offset in range(-max_depth, max_depth) if rect_offset%2==1]

        self.next_section("Tree")
        self.play(Write(displayed_minimax_tree), *[Write(maximiser) for maximiser in maximiser_group], *[Write(minimiser) for minimiser in minimiser_group])
        self.wait(2)

        me_group = [VGroup(Rectangle(color=GRAY_B, height=8/max_depth, width=14+2/9, fill_opacity=0.5, stroke_width=0).shift((0, rect_offset*8/max_depth, 0)).set_z_index(-100), Tex("Me", color=WHITE).move_to((-6.5, rect_offset*8/max_depth, 0))) for rect_offset in range(-max_depth, max_depth) if rect_offset%2==0]

        opponent_group = [VGroup(Rectangle(color=GRAY_C, height=8/max_depth, width=14+2/9, fill_opacity=0.5, stroke_width=0).shift((0, rect_offset*8/max_depth, 0)).set_z_index(-100), Tex("Opponent", color=BLACK).move_to((-6, rect_offset*8/max_depth, 0))) for rect_offset in range(-max_depth, max_depth) if rect_offset%2==1]

        self.play(*[ReplacementTransform(maximiser, me) for maximiser, me in zip(maximiser_group, me_group)], *[ReplacementTransform(minimiser, opponent) for minimiser, opponent in zip(minimiser_group, opponent_group)], ReplacementTransform(displayed_minimax_tree, displayed_negamax_tree))
        self.wait(2)

        my_POV = VGroup(Rectangle(color=GRAY_B, height=8, width=14+2/9, fill_opacity=0.5, stroke_width=0).set_z_index(-100), Tex("My perspective", color=WHITE).to_corner(UL))
        opponent_POV = VGroup(Rectangle(color=GRAY_C, height=8, width=14+2/9, fill_opacity=0.5, stroke_width=0).set_z_index(-100), Tex("Opponent perspective", color=BLACK).to_corner(UL))

        top_rect = me_group[-2].copy()
        my_POV_tree = Tree()
        FillTree(my_POV_tree, is_minimax=True)
        displayed_my_POV_tree = Graph([i for i in range(1, my_POV_tree.size)],
            my_POV_tree.edges_list,
            layout="tree",
            layout_config={"root_vertex":1},
            layout_scale=self.LAYOUT_SCALE,
            vertex_config=self.VERTEX_CONFIG,
            labels=my_POV_tree.labels
        ).flip(axis=UP).move_to(RIGHT*0.5)
        print(my_POV_tree)
        
        displayed_negamax_tree_orig = displayed_negamax_tree.copy()
        self.play(ReplacementTransform(top_rect, my_POV), ReplacementTransform(displayed_negamax_tree, displayed_my_POV_tree), *[FadeOut(me) for me in me_group if me != top_rect], *[FadeOut(opponent) for opponent in opponent_group])
        self.wait()
        
        opponent_POV_tree = my_POV_tree
        for node in opponent_POV_tree.scores:
            opponent_POV_tree.scores[node] *= -1 
            opponent_POV_tree.labels[node] = MathTex(NumToStr(opponent_POV_tree.scores[node])).flip(axis=UP)
        print(opponent_POV_tree)
        displayed_opponent_POV_tree = Graph([i for i in range(1, opponent_POV_tree.size)],
            opponent_POV_tree.edges_list,
            layout="tree",
            layout_config={"root_vertex":1},
            layout_scale=self.LAYOUT_SCALE,
            vertex_config=self.VERTEX_CONFIG,
            labels=opponent_POV_tree.labels
        ).flip(axis=UP).move_to(RIGHT*0.5)
        self.play(ReplacementTransform(my_POV, opponent_POV), ReplacementTransform(displayed_my_POV_tree, displayed_opponent_POV_tree))
        top_rect = opponent_group[-2]
        self.wait()

        self.play(ReplacementTransform(opponent_POV, top_rect), ReplacementTransform(displayed_opponent_POV_tree, displayed_negamax_tree_orig), *[FadeIn(me) for me in me_group], *[FadeIn(opponent) for opponent in opponent_group if opponent != top_rect])

        self.wait()
        self.play(*[FadeOut(submobject) for submobject in self.mobjects])

class AnimateNegamaxCode(Scene):
    def construct(self):
        #Chapter 2: Negamax
        chapter_2 = Tex(r"\textbf{\underline{\Large Chapter 2}}\\~\\ Negamax")
        self.play(FadeIn(chapter_2, scale=3), run_time=3)
        self.wait(0.5)
        self.play(FadeOut(chapter_2), run_time=2)

        minimax_code = '''def Minimax(depth, current_node, is_maximiser: bool):
    if depth == 0:
        return GetScore(current_node)

    if is_maximiser:
        best_so_far = -math.inf
        for children_node in current_node:
            best_so_far = max(best_so_far, Minimax(depth - 1, children_node, False))
    else:
        best_so_far = math.inf
        for children_node in current_node:
            best_so_far = min(best_so_far, Minimax(depth - 1, children_node, True))

    return best_so_far'''

        rendered_minimax_code = Code(
            code_string=minimax_code,
            language="python",
            add_line_numbers=False,
            background="window",
            paragraph_config={"width": 10, "height": 6}
        )

        self.play(DrawBorderThenFill(rendered_minimax_code))
        self.wait(2)

        self.play(Indicate(rendered_minimax_code.code_lines[1:3]))
        self.wait()

        self.play(Indicate(rendered_minimax_code.code_lines[4:8]))
        self.play(Indicate(rendered_minimax_code.code_lines[8:12]))
        self.wait()

        max_text = Tex("Max", color=RED).next_to(rendered_minimax_code, UP).align_to(rendered_minimax_code, LEFT).set_z_index(-150)
        min_text = Tex("Min", color=BLUE).next_to(rendered_minimax_code, DOWN).align_to(rendered_minimax_code, LEFT).set_z_index(-150)
        max_code = rendered_minimax_code.code_lines[4:8].copy()
        min_code = rendered_minimax_code.code_lines[8:12].copy()
        self.play(ReplacementTransform(max_code, max_text), ReplacementTransform(min_code, min_text))
        self.wait()

        self.play(Indicate(rendered_minimax_code.code_lines[7]), Indicate(rendered_minimax_code.code_lines[11]))
        self.wait()


        minimax_code_ab = '''def Minimax(depth, current_node, is_maximiser: bool, alpha=-math.inf, beta=math.inf):
    if depth == 0:
        return GetScore(current_node)

    if is_maximiser:
        best_so_far = -math.inf
        for children_node in current_node:
            best_so_far = max(best_so_far, Minimax(depth - 1, children_node, False))
            alpha = max(best_so_far, alpha)
            if alpha >= beta:
                return best_so_far
    else:
        best_so_far = math.inf
        for children_node in current_node:
            best_so_far = min(best_so_far, Minimax(depth - 1, children_node, True))
            beta = min(best_so_far, beta)
            if alpha >= beta:
                return best_so_far

    return best_so_far'''
        
        rendered_minimax_code_ab = Code(
            code_string=minimax_code_ab,
            language="python",
            add_line_numbers=False,
            background="window",
            paragraph_config={"width": 10, "height": 6}
        )

        self.play(ReplacementTransform(rendered_minimax_code, rendered_minimax_code_ab), FadeOut(min_text), FadeOut(max_text))
        self.wait()
        self.play(Indicate(rendered_minimax_code_ab.code_lines[8]), Indicate(rendered_minimax_code_ab.code_lines[15]))
        self.wait()

        stm_negamax_code = '''def Negamax(depth, current_node, side_to_move):
    if depth == 0:
        return GetScore(current_node) * side_to_move

    best_so_far = -math.inf
    for children_node in current_node:
        best_so_far = max(best_so_far, -Negamax(depth - 1, children_node, -side_to_move))

    return best_so_far'''
        
        rendered_stm_negamax_code = Code(
            code_string=stm_negamax_code,
            language="python",
            add_line_numbers=False,
            background="window",
            paragraph_config={"width": 10, "height": 6}
        )
        
        self.play(ReplacementTransform(rendered_minimax_code_ab, rendered_stm_negamax_code))
        self.wait()

        self.play(Indicate(rendered_stm_negamax_code.code_lines[6][-51:-2]))
        self.wait()

        max_text = Tex("Max", color=RED).next_to(rendered_stm_negamax_code, UP).align_to(rendered_stm_negamax_code, LEFT).set_z_index(-150)
        min_text = Tex("Min", color=BLUE).next_to(rendered_stm_negamax_code, DOWN).align_to(rendered_stm_negamax_code, LEFT).set_z_index(-150)
        self.play(FadeIn(max_text), FadeIn(min_text))
        self.wait()
        self.play(max_text.animate.move_to(rendered_stm_negamax_code).set_z_index(-150), min_text.animate.move_to(rendered_stm_negamax_code).set_z_index(-150))

        self.wait()
        self.play(Indicate(rendered_stm_negamax_code.code_lines[0][-14:-2]), Indicate(rendered_stm_negamax_code.code_lines[2][-12:]), Indicate(rendered_stm_negamax_code.code_lines[6][-14:-2]))

        no_stm_negamax_code = '''def Negamax(depth, current_node):
    if depth == 0:
        return GetRelativeScore(current_node)

    best_so_far = -math.inf
    for children_node in current_node:
        best_so_far = max(best_so_far, -Negamax(depth - 1, children_node))

    return best_so_far'''
        
        rendered_no_stm_negamax_code = Code(
            code_string=no_stm_negamax_code,
            language="python",
            add_line_numbers=False,
            background="window",
            paragraph_config={"width": 10, "height": 6}
        )
        
        self.wait()
        self.play(Transform(rendered_stm_negamax_code, rendered_no_stm_negamax_code))
        self.wait()
        
class AdditionalNegamaxScene(Scene):
    def construct(self):
        minimax_code_ab = '''def Minimax(depth, current_node, is_maximiser: bool, alpha=-math.inf, beta=math.inf):
    if depth == 0:
        return GetScore(current_node)

    if is_maximiser:
        best_so_far = -math.inf
        for children_node in current_node:
            best_so_far = max(best_so_far, Minimax(depth - 1, children_node, False))
            alpha = max(best_so_far, alpha)
            if alpha >= beta:
                return best_so_far
    else:
        best_so_far = math.inf
        for children_node in current_node:
            best_so_far = min(best_so_far, Minimax(depth - 1, children_node, True))
            beta = min(best_so_far, beta)
            if alpha >= beta:
                return best_so_far

    return best_so_far'''
        
        rendered_minimax_code_ab = Code(
            code_string=minimax_code_ab,
            language="python",
            add_line_numbers=False,
            background="window",
            paragraph_config={"width": 10, "height": 6}
        )

        self.add(rendered_minimax_code_ab)
        self.wait()
        self.play(Indicate(rendered_minimax_code_ab.code_lines[9:11]), Indicate(rendered_minimax_code_ab.code_lines[16:18]))
        self.wait()
    
class AnimateABNegamax(Scene):
    def construct(self):
        self.next_section("Intro", skip_animations=True)


        chapter_3 = Tex(r"\textbf{\underline{\Large Chapter 3}}\\")
        ab_chapter_text = Tex(r"Alpha-Beta Pruning", substrings_to_isolate=("Alpha","Beta")).next_to(chapter_3, DOWN)
        self.play(FadeIn(chapter_3, scale=3), FadeIn(ab_chapter_text, shift=UP*2, scale=3), run_time=3)
        self.wait(0.5)
        self.play(FadeOut(chapter_3), ab_chapter_text.animate.set_color_by_tex(r"Alpha", RED).set_color_by_tex(r"Beta", BLUE).move_to((0,0,0)), run_time=2)
        self.wait(5)

        self.next_section("explain_ab", skip_animations=True)



        alpha_text_1 = Tex("Alpha: Best score maximiser has guaranteed", substrings_to_isolate=("Alpha", "maximiser")).shift(UP).scale(1.2)
        alpha_text_1.set_color_by_tex(r"Alpha", RED)
        alpha_text_1.set_color_by_tex(r"maximiser", RED)
        beta_text_1 = Tex("Beta: Best score minimiser has guaranteed", substrings_to_isolate=("Beta", "minimiser")).shift(DOWN).scale(1.2)
        beta_text_1.set_color_by_tex(r"Beta", BLUE)
        beta_text_1.set_color_by_tex(r"minimiser", BLUE)
        ab_group_1 = VGroup(alpha_text_1, beta_text_1)

        alpha_text_2 = Tex("Alpha: Best score side-to-move has guaranteed", substrings_to_isolate=("Alpha", "side-to-move")).shift(UP).scale(1.2)
        alpha_text_2.set_color_by_tex(r"Alpha", RED)
        beta_text_2 = Tex("Beta: Best score opponent has guaranteed", substrings_to_isolate=("Beta", "opponent")).shift(DOWN).scale(1.2)
        beta_text_2.set_color_by_tex(r"Beta", BLUE)
        ab_group_2 = VGroup(alpha_text_2, beta_text_2)

        beta_text_3 = Tex("Beta: Maximum score opponent will allow us to have", substrings_to_isolate=("Beta", "opponent")).shift(DOWN).scale(1.2)
        beta_text_3.set_color_by_tex(r"Beta", BLUE)

        minimax_text = Tex("Minimax", font_size=96).to_edge(UP)
        negamax_text = Tex("Negamax", font_size=96).to_edge(UP)

        self.play(Write(minimax_text), TransformMatchingTex(ab_chapter_text, ab_group_1), run_time=4)
        self.wait(5.5)
        self.wait(2)
        self.play(ReplacementTransform(minimax_text, negamax_text))
        self.wait(5.2)
        self.play(ReplacementTransform(ab_group_1, ab_group_2), run_time=4)
        self.wait(3.8)
        self.play(ReplacementTransform(ab_group_2[1], beta_text_3), run_time=3)
        self.wait(5)

        self.next_section("window_ab", skip_animations=True)



        arrow_tip_length = 0.25
        rect = Rectangle(height=4, width=3, stroke_width=1).set_color(GREEN)

        #Windows
        exact_window = rect.copy().set_fill(GREEN_E, opacity=0.3)
        non_exact_windows = [
            Rectangle(height=2, width=3, stroke_width=1).shift(UP*3).set_color(RED).set_fill(RED, opacity=0.2), 
            Rectangle(height=2, width=3, stroke_width=1).shift(DOWN*3).set_color(RED).set_fill(RED, opacity=0.2)
            ]
        TOP_WINDOW = 0
        BOTTOM_WINDOW = 1

        #Flashing arrows
        def ArrowAnimation(pos, direction, arrow_width=0.5, arrow_length = 0.8, arrow_tip_length = 0.4, arrow_shown_size = 0.25,run_time=1):
            (arrow_aligned_edge, rect_aligned_edge) = (UP, DOWN) if direction == -1 else (DOWN, UP)
            arrow = Polygon(
                (-arrow_width/2,0,0),
                (arrow_width/2,0,0),
                (arrow_width/2,arrow_length*direction,0),
                (arrow_width,arrow_length*direction,0),
                (0,(arrow_tip_length+arrow_length)*direction,0),
                (-arrow_width,arrow_length*direction,0),
                (-arrow_width/2,arrow_length*direction,0)
            ).move_to(pos, aligned_edge=arrow_aligned_edge).set_fill(WHITE, opacity=1)
            intersection_shift = ValueTracker()
            intersection_rectangle = Rectangle(height=arrow_shown_size, width=2*arrow_width)
            arrow_animation = always_redraw(lambda: Intersection(arrow, 
                                                                 intersection_rectangle.move_to(
                                                                     pos+(0,intersection_shift.get_value(),0),
                                                                     aligned_edge=rect_aligned_edge)).set_fill(WHITE, opacity=1))
            self.add(arrow_animation)
            self.play(
                intersection_shift.animate.set_value((arrow_tip_length+arrow_length+arrow_shown_size)*direction), 
                run_time=run_time
                )
        
        #Text
        alpha_tex = MathTex(r"\alpha", color=RED).next_to(rect, DOWN)
        beta_tex = MathTex(r"\beta", color=BLUE).next_to(rect, UP)
        exact_text = Tex("Exact scores", font_size=48).move_to((4.8,1,0))
        non_exact_text = Tex("Non-exact scores", font_size=48).move_to((4.8,1,0))
        true_score_text = Tex("True score", font_size=48, color=GREEN).next_to(exact_window, RIGHT)
        upper_bound_score_text = Tex("Upper bound", font_size=48, color=RED).next_to(non_exact_windows[BOTTOM_WINDOW], RIGHT)
        lower_bound_score_text = Tex("Lower bound", font_size=48, color=RED).next_to(non_exact_windows[TOP_WINDOW], RIGHT)
                
        #Arrows
        exact_arrow = Arrow(
            stroke_width=1.5, 
            tip_length=arrow_tip_length, 
            start=exact_text.get_bottom()+(0,-0.2,0), 
            end=exact_window.get_right()
        )
        non_exact_arrow = [
            Arrow(
                stroke_width=1.5, 
                tip_length=arrow_tip_length,
                start=non_exact_text.get_top()+(0,0.2,0), 
                end=exact_window.get_right()+(0,3,0)
            ), 
            Arrow(
                stroke_width=1.5, 
                tip_length=arrow_tip_length, 
                start=non_exact_text.get_bottom()+(0,-0.2,0), 
                end=exact_window.get_right()+(0,-3,0)
            )
        ]

        #Updaters
        dot_tracker = ValueTracker(0)
        score_dot = Dot().add_updater(lambda m: m.move_to((0, dot_tracker.get_value(), 0)))

        #Animations
        self.play(*[FadeOut(mobject) for mobject in self.mobjects], Transform(alpha_text_2[0], alpha_tex), Transform(beta_text_3[0], beta_tex), run_time=2)
        self.add(alpha_tex, beta_tex)
        self.play(GrowFromCenter(rect))
        self.play(FadeTransform(rect, exact_window))
        self.play(Wiggle(alpha_tex, scale_value=1.5), run_time=1.9)
        self.play(Wiggle(beta_tex, scale_value=1.5), run_time=2)
        self.play(SpiralIn(score_dot.set_z_index(10)))
        self.play(dot_tracker.animate.set_value(1.7), run_time=1.7)
        self.wait(0.5)
        self.play(
            LaggedStart(
                dot_tracker.animate.set_value(-1.1), 
                AnimationGroup(
                    Write(exact_text), 
                    GrowArrow(exact_arrow)
                ), 
                lag_ratio=0.25, 
                run_time=1.5
            )
        )
        self.wait(0.2)
        self.play(
            LaggedStart(
                AnimationGroup(
                    dot_tracker.animate.set_value(-3.6), 
                    DrawBorderThenFill(non_exact_windows[TOP_WINDOW]), 
                    DrawBorderThenFill(non_exact_windows[BOTTOM_WINDOW]), 
                    FadeOut(exact_window), 
                    alpha_tex.animate.move_to(exact_window.get_corner(DL)).shift(LEFT*0.5), 
                    beta_tex.animate.move_to(exact_window.get_corner(UL)).shift(LEFT*0.5)
                ),
                AnimationGroup(
                    ReplacementTransform(exact_text, non_exact_text), 
                    ReplacementTransform(exact_arrow, non_exact_arrow[0]), 
                    ReplacementTransform(exact_arrow.copy(), non_exact_arrow[1])
                ), 
            lag_ratio=0.2
            )
        )
        self.play(dot_tracker.animate.set_value(-2.5), run_time=0.8, rate_func=rate_functions.ease_in_sine)
        self.play(dot_tracker.animate.set_value(2.8), run_time=0.4, rate_func=rate_functions.linear)
        self.play(dot_tracker.animate.set_value(3.2), run_time=0.7, rate_func=rate_functions.ease_out_sine)
        self.wait(0.3)
        self.play(FadeIn(exact_window), dot_tracker.animate.set_value(0), FadeOut(non_exact_arrow[0]), FadeOut(non_exact_arrow[1]), run_time=1.6)
        self.play(ReplacementTransform(non_exact_text, true_score_text), run_time=1.7)
        self.wait(2)
        self.play(Write(upper_bound_score_text), Write(lower_bound_score_text), run_time=2.5)
        self.wait(1.5)
        self.play(dot_tracker.animate.set_value(-2.5), run_time=1.6)
        self.wait()
        self.play(Wiggle(upper_bound_score_text), run_time=1.9)
        self.wait(1.7)
        ArrowAnimation(score_dot.get_center()+0.15*DOWN, -1)
        self.wait(1.4)
        self.play(dot_tracker.animate.set_value(2.5), run_time=1.3)
        self.wait(0.2)
        ArrowAnimation(score_dot.get_center()+0.15*UP, 1)
        self.wait(1.2)
        self.wait(2.9)
        self.play(FadeOut(score_dot), run_time=1.6)
        self.wait(1.2)
        self.play(*[non_exact_window.animate.set_fill(opacity=0.5) for non_exact_window in non_exact_windows], run_time=1.6)
        self.wait(1.4)
        dot_tracker.set_value(0)
        self.play(FadeIn(score_dot), run_time=1.4)
        self.wait()
        self.play(ShowPassingFlash(exact_window.copy().set_fill(opacity=0).set_stroke(GREEN,5), time_width=0.2), run_time=1.3)
        self.wait(1.2)
        self.play(Unwrite(score_dot), *[non_exact_window.animate.set_fill(opacity=0.2) for non_exact_window in non_exact_windows])
        self.wait(5)

        self.next_section("fail_low_fail_high", skip_animations=True)

        #Score dots
        score_dots_exact = VGroup(
            Dot((0, -1.0, 0)),
            Dot((0, -2.9, 0)),
            Dot((0, -1.1, 0)),
            Dot((0, -3.3, 0)),
            Dot((0, 0.7, 0)),
            Dot((0, 1.3, 0)),
            Dot((0, -0.2, 0)),
            Dot((0, -2.3, 0)),
        )
        score_dots_fail_high = VGroup(
            Dot((0, -2.8, 0)),
            Dot((0, 1.5, 0)),
            Dot((0, -2.5, 0)),
            Dot((0, -1.7, 0)),
            Dot((0, 2.8, 0)),
        )
        score_dots_fail_low = VGroup(
            Dot((0, -3.0, 0)),
            Dot((0, -2.9, 0)),
            Dot((0, -3.9, 0)),
            Dot((0, -2.1, 0)),
            Dot((0, -3.4, 0)),
        )

        #Text
        fail_low_text = Tex("Fail low", font_size=48, color=RED).to_corner(UL)
        fail_high_text = Tex("Fail high", font_size=48, color=BLUE).to_corner(UL)
        stop_searching_text = Tex("Stop searching").move_to((4.5,1.2,0))

        #Arrow
        stop_searching_arrow = Arrow(start=stop_searching_text.get_left(), end=score_dots_fail_high[-1].get_corner(DR))

        #Animation
        self.play(LaggedStart(*[SpiralIn(dot) for dot in score_dots_exact], lag_ratio=0.5), run_time=2.8)
        self.wait(0.2)
        self.play(Flash(score_dots_exact[5]), run_time=0.8)
        self.wait(0.2)
        self.play(FadeOut(score_dots_exact), run_time=0.8)
        self.play(LaggedStart(*[SpiralIn(dot) for dot in score_dots_fail_low], lag_ratio=0.5), run_time=1.7)
        self.wait(0.2)
        self.play(LaggedStart(Flash(score_dots_fail_low[3]), Write(fail_low_text), FadeOut(score_dots_fail_low), lag_ratio=0.75), run_time=2.3)
        self.wait(0.2)
        self.play(LaggedStart(*[SpiralIn(dot) for dot in score_dots_fail_high], lag_ratio=0.5), run_time=1.7)
        self.wait(0.2)
        self.play(LaggedStart(Flash(score_dots_fail_high[-1]), ReplacementTransform(fail_low_text, fail_high_text), lag_ratio=0.75), run_time=2.3)
        self.wait()
        self.play(Write(stop_searching_arrow), run_time=1.9)
        self.play(Write(stop_searching_text), run_time=1.9)
        self.wait(2)
        self.play(ShowPassingFlash(non_exact_windows[TOP_WINDOW].copy().set_stroke(width=5).set_fill(opacity=0)), run_time=1.3)
        self.wait(2.3)
        self.play(LaggedStart(*[score_dots_fail_high[i].animate(rate_func=rate_functions.wiggle).shift(RIGHT*0.2) for i in [1,3,2,0]]), run_time=2.4)
        self.wait(4)
        self.play(Flash(score_dots_fail_high[-1]), run_time=1.5)
        self.wait(5)
        self.play(score_dots_fail_high[:-1].animate.set_opacity(0.2), run_time=1.5)
        self.wait(0.7)
        ArrowAnimation(score_dots_fail_high[-1].get_center()+UP*0.15, 1, run_time=1.8)
        self.wait(2.4)
        self.play(Wiggle(lower_bound_score_text), run_time=2)
        self.wait()
        self.play(Unwrite(score_dots_fail_high), Unwrite(stop_searching_arrow), Unwrite(stop_searching_text), Unwrite(fail_high_text))
        self.play(LaggedStart(*[SpiralIn(dot) for dot in score_dots_exact[:2]], lag_ratio=0.5), run_time=1.2)
        self.wait(2.5)
        self.play(LaggedStart(*[SpiralIn(dot) for dot in score_dots_exact[2:]], lag_ratio=0.5), run_time=3.6)
        self.wait(0.6)
        self.play(Flash(score_dots_exact[5]), run_time=1.5)
        self.wait(5)

        self.next_section("ab_code", skip_animations=False)

        code_negamax = '''def Negamax(depth, current_node, side_to_move):
    if depth == 0:
        return GetScore(current_node) * side_to_move

    best_so_far = -math.inf
    for child_node in current_node:
        best_so_far = max(best_so_far, -Negamax(depth - 1, child_node, -side_to_move))

    return best_so_far'''
        
        code_ab_1 = '''def Negamax(depth, current_node, side_to_move, alpha, beta):
    if depth == 0:
        return GetScore(current_node) * side_to_move

    best_so_far = -math.inf
    for child_node in current_node:
        best_so_far = max(best_so_far, -Negamax(depth - 1, child_node, -side_to_move))

    return best_so_far'''
        
        code_ab_2 = '''def Negamax(depth, current_node, side_to_move, alpha, beta):
    if depth == 0:
        return GetScore(current_node) * side_to_move

    best_so_far = -math.inf
    for child_node in current_node:
        best_so_far = max(best_so_far, -Negamax(depth - 1, child_node, -side_to_move, alpha,   beta))
 
    return best_so_far'''
        
        code_ab_3 = '''def Negamax(depth, current_node, side_to_move, alpha, beta):
    if depth == 0:
        return GetScore(current_node) * side_to_move

    best_so_far = -math.inf
    for child_node in current_node:
        best_so_far = max(best_so_far, -Negamax(depth - 1, child_node, -side_to_move, -beta, -alpha))

        if best_so_far > alpha:
            alpha = best_so_far

        if best_so_far > beta:
            break
        
    return best_so_far'''
        
        rendered_code_negamax = Code(
            code_string=code_negamax,
            language="python",
            add_line_numbers=False,
            background="rectangle",
            paragraph_config={"width": 10, "height": 6}
        )

        rendered_code_ab_1 = Code(
            code_string=code_ab_1,
            language="python",
            add_line_numbers=False,
            background="rectangle",
            paragraph_config={"width": 10, "height": 6}
        )

        rendered_code_ab_2 = Code(
            code_string=code_ab_2,
            language="python",
            add_line_numbers=False,
            background="rectangle",
            paragraph_config={"width": 10, "height": 6}
        )

        rendered_code_ab_3 = Code(
            code_string=code_ab_3,
            language="python",
            add_line_numbers=False,
            background="rectangle",
            paragraph_config={"width": 10, "height": 6}
        )

        alpha = rendered_code_ab_2.code_lines[6][-16:-10]
        beta = rendered_code_ab_2.code_lines[6][-8:-2]
        alpha_path = ArcBetweenPoints(start=alpha[-1].get_corner(DR), end=beta[-1].get_corner(DR))
        beta_path = ArcBetweenPoints(start=beta[-1].get_corner(DR), end=alpha[-1].get_corner(DR))
        alpha_path = alpha_path.shift(alpha.get_center() - alpha_path.get_start())
        beta_path = beta_path.shift(beta.get_center() - beta_path.get_start())
        alpha_clone = rendered_code_ab_3.code_lines[6][-7:-2]
        beta_clone = rendered_code_ab_3.code_lines[6][-14:-10]
        alpha_negative_clone = rendered_code_ab_3.code_lines[6][-8]
        beta_negative_clone = rendered_code_ab_3.code_lines[6][-15]

        self.clear()
        self.wait(0.2)
        self.add(rendered_code_negamax)
        self.wait(3.4)
        self.play(ReplacementTransform(rendered_code_negamax, rendered_code_ab_1), run_time=2)
        self.wait(3.6)
        self.play(ReplacementTransform(rendered_code_ab_1, rendered_code_ab_2), run_time=2)
        self.wait(0.7)
        self.wait(2.4)
        self.play(MoveAlongPath(alpha, alpha_path), MoveAlongPath(beta, beta_path), run_time=1.4)

        alpha_negative_sign = rendered_code_ab_2.code_lines[6][-30].copy().next_to(alpha[1], LEFT, buff=0.02)
        beta_negative_sign = rendered_code_ab_2.code_lines[6][-30].copy().next_to(beta[2], LEFT, buff=0.02)
        
        self.play(Write(alpha_negative_sign), Write(beta_negative_sign), run_time=1.4)
        self.wait()
        self.play(Indicate(beta), Indicate(beta_negative_sign), run_time=2)
        self.wait()
        self.play(Indicate(alpha), Indicate(alpha_negative_sign), run_time=2)
        self.wait(5)
        self.play(
            rendered_code_ab_2.background.animate.stretch(1.5, 1), 
            Transform(beta, beta_clone),
            Transform(alpha, alpha_clone),
            Transform(beta_negative_sign, beta_negative_clone),
            Transform(alpha_negative_sign, alpha_negative_clone),
            rendered_code_ab_2.code_lines[:-1].animate.move_to((0, (rendered_code_ab_2.height*1.5 - rendered_code_ab_2.code_lines.height)/2-0.0935, 0)),
            rendered_code_ab_2.code_lines[-1].animate.move_to((rendered_code_ab_2.code_lines[-1].get_x(), rendered_code_ab_3.code_lines[-1].get_y(), 0))
        )
        self.play(Write(rendered_code_ab_3.code_lines[-8:-5]), run_time=2)
        self.wait(1.4)
        self.play(Circumscribe(rendered_code_ab_3.code_lines[-7][11:], buff=0.02, stroke_width=1))
        self.wait(1.6)
        self.wait(8.6)
        self.play(Indicate(rendered_code_ab_3.code_lines[-6]))
        self.wait(0.6)
        self.play(Write(rendered_code_ab_3.code_lines[-4:-2], run_time=2))
        self.wait()
        self.wait()
        self.play(Indicate(rendered_code_ab_3.code_lines[-3]))
        self.wait(2)
        self.wait(5)


        self.next_section("ab_tree", skip_animations=True)

        RADIUS = 0.35
        VERTEX_CONFIG = {"stroke_width": 2, "stroke_color": WHITE, "radius": RADIUS, "color":BLACK, "fill_opacity": 1}
        LAYOUT_SCALE = (6, 3)

        RECT=0
        ALPHA_TEX=1
        BETA_TEX=2
        NEGATIVE_ALPHA_TEX=3
        NEGATIVE_BETA_TEX=4
        global_window_group_list = []

        def ABNegamax(displayed_tree: Graph, internal_tree: Tree, parent_node:int, current_node: int, side_to_move: int, alpha=-10, beta=10):
            
            def AddWindow(displayed_node, current_node, alpha, beta):
                window_height = (RADIUS/10)*abs(beta-alpha)

                window = Rectangle(width=RADIUS, height=window_height, stroke_width=1, fill_opacity=0.5).set_color(
                    GREEN).next_to(displayed_node, LEFT*0.5).shift((0,(RADIUS/10)*((alpha+beta)/2),0))
                
                (alpha_pos, beta_pos) = (window.get_bottom()+0.1*DOWN, window.get_top()+0.1*UP) if alpha < beta else (window.get_top()+0.1*UP, window.get_bottom()+0.1*DOWN)
                
                
                alpha_tex = MathTex(fr"\alpha:{NumToStr(alpha)}", substrings_to_isolate=(r"\alpha",":","-")).scale(0.35).move_to(alpha_pos)
                alpha_tex.set_color_by_tex(r"\alpha", RED)
                beta_tex = MathTex(fr"\beta:{NumToStr(beta)}", substrings_to_isolate=(r"\beta",":","-")).scale(0.35).move_to(beta_pos)
                beta_tex.set_color_by_tex(r"\beta", BLUE)
                negative_alpha_tex = MathTex(fr"-\alpha:{NumToStr(beta)}", substrings_to_isolate=(r"\alpha",":","-")).scale(0.35).move_to(beta_pos)
                negative_alpha_tex.set_color_by_tex(r"\alpha", RED)
                negative_beta_tex = MathTex(fr"-\beta:{NumToStr(alpha)}", substrings_to_isolate=(r"\beta",":","-")).scale(0.35).move_to(alpha_pos)
                negative_beta_tex.set_color_by_tex(r"\beta", BLUE)

                window_group = VGroup(window, alpha_tex, beta_tex, negative_alpha_tex, negative_beta_tex)
                global_window_group_list[current_node] = window_group

            def AnimateAlphaBeta(parent_node, child_node, run_time=1):
                current_window_group = global_window_group_list[parent_node].copy()
                child_window_group = global_window_group_list[child_node]

                self.play(
                    ShowPassingFlash(displayed_tree.edges[(parent_node, child_node)].copy().set_stroke(width=5,color=YELLOW)),
                    ReplacementTransform(current_window_group[RECT], child_window_group[RECT]),
                    TransformMatchingTex(current_window_group[ALPHA_TEX], child_window_group[BETA_TEX]),
                    TransformMatchingTex(current_window_group[BETA_TEX], child_window_group[ALPHA_TEX]),
                    run_time=run_time
                )

            def AnimateReturnAlphaBeta(parent_node, child_node, best_so_far, displayed_best_so_far, exact=False, run_time=1):
                if parent_node == child_node:
                    return
                
                orig_parent_window_group = global_window_group_list[parent_node]
                new_parent_window_group = global_window_group_list[parent_node+internal_tree.size]

                color = RED if best_so_far > 0 else BLUE
                dot = Dot(radius=0.04, color=color).next_to(displayed_tree[parent_node]).shift((0,(RADIUS/10)*(-best_so_far),0))
                dot.move_to((orig_parent_window_group[RECT].get_x(), dot.get_y(), 0))
                dot_tex = Tex(f"{-best_so_far}", font_size=10, color=color).next_to(dot, LEFT)
                dot_group = VGroup(dot, dot_tex)

                if exact:
                    self.play(
                        ShowPassingFlash(displayed_tree.edges[(parent_node, child_node)].copy().reverse_direction().set_stroke(width=5,color=YELLOW)),
                        Write(
                            Line(
                                start=orig_parent_window_group[RECT].get_corner(DL), 
                                end=orig_parent_window_group[RECT].get_corner(DR), 
                                color=GREEN).set_z_index(-10)
                        ),
                        Transform(orig_parent_window_group[RECT], new_parent_window_group[RECT]),
                        ReplacementTransform(displayed_best_so_far.copy(), dot_group),
                        run_time=run_time
                    )
                else:
                    self.play(
                        ShowPassingFlash(displayed_tree.edges[(parent_node, child_node)].copy().reverse_direction().set_stroke(width=5,color=YELLOW)),
                        ReplacementTransform(displayed_best_so_far.copy(), dot_group), 
                        run_time=run_time
                    )

            displayed_node = displayed_tree[current_node]
            AddWindow(displayed_node, current_node, alpha, beta)
            exact = False

            #Start negamaxing
            if current_node == 1:
                self.wait(8)
                self.play(Write(global_window_group_list[current_node][RECT]))
                self.wait()
                self.play(Write(global_window_group_list[current_node][ALPHA_TEX]))
                self.wait()
                self.play(Write(global_window_group_list[current_node][BETA_TEX]))
                self.wait(10.7)
            elif current_node == 2:
                current_window_group = global_window_group_list[parent_node].copy()
                child_window_group = global_window_group_list[current_node]

                self.play(
                    ShowPassingFlash(displayed_tree.edges[(parent_node, current_node)].copy().set_stroke(width=5,color=YELLOW)),
                    ReplacementTransform(current_window_group[RECT], child_window_group[RECT]),
                    current_window_group[ALPHA_TEX].animate.move_to(child_window_group[BETA_TEX]),
                    current_window_group[BETA_TEX].animate.move_to(child_window_group[ALPHA_TEX]),
                    run_time=1.5
                )
                self.play(
                    TransformMatchingTex(current_window_group[ALPHA_TEX], child_window_group[NEGATIVE_ALPHA_TEX]),
                    TransformMatchingTex(current_window_group[BETA_TEX], child_window_group[NEGATIVE_BETA_TEX]),
                    run_time=1.5
                )
                self.play(
                    TransformMatchingTex(child_window_group[NEGATIVE_ALPHA_TEX], child_window_group[BETA_TEX]),
                    TransformMatchingTex(child_window_group[NEGATIVE_BETA_TEX], child_window_group[ALPHA_TEX]),
                    run_time=1.5
                )
                self.wait(1.7)
            else:
                AnimateAlphaBeta(parent_node, current_node)
            best_so_far = -10

            if current_node not in internal_tree.edges_dict: #checks if current_node is a leaf
                best_so_far = internal_tree.scores[current_node]
                displayed_best_so_far = MathTex(NumToStr(best_so_far)).move_to(displayed_node)
                if best_so_far > alpha and best_so_far < beta:
                    exact = True
                AddWindow(displayed_tree[parent_node], parent_node+internal_tree.size, -best_so_far, -alpha)
                if current_node == 2:
                    dot = Dot(radius=0.04, color=RED).next_to(displayed_tree[parent_node]).shift((0,(RADIUS/10)*(-best_so_far),0))
                    dot.move_to((global_window_group_list[parent_node][RECT].get_x(), dot.get_y(), 0))
                    six_tex = Tex("6", font_size=10, color=RED).next_to(dot, LEFT)
                    dot_group = VGroup(dot, six_tex)
                    self.play(
                        ShowPassingFlash(displayed_tree.edges[(parent_node, current_node)].copy().reverse_direction().set_stroke(width=5,color=YELLOW)),
                        ReplacementTransform(displayed_best_so_far.copy(), dot_group)
                    )
                    self.wait(1.7)
                    self.play(Indicate(global_window_group_list[parent_node][ALPHA_TEX]), run_time=1.9)
                    self.wait(6.3)
                    line_start = global_window_group_list[parent_node][RECT].get_corner(DL)
                    line_end = global_window_group_list[parent_node][RECT].get_corner(DR)
                    self.play(
                        ReplacementTransform(global_window_group_list[parent_node][RECT], global_window_group_list[parent_node+internal_tree.size][RECT]),
                        run_time=2
                    )
                    self.wait(1.2)
                    self.play(GrowFromCenter(
                            Line(
                                start=line_start,
                                end=line_end, 
                                color=GREEN
                            )
                        ),
                        run_time=1.5
                    )
                    self.wait(2.8)
                    self.next_section("beta_cutoff", skip_animations=True)
                    return best_so_far

                    dot = Dot(radius=0.04, color=RED).next_to(displayed_tree[parent_node]).shift((0,(RADIUS/10)*(-best_so_far),0))
                    dot.move_to((global_window_group_list[parent_node][RECT].get_x(), dot.get_y(), 0))
                    six_tex = Tex("6", font_size=16, color=RED).next_to(dot, DOWN, buff=0.08)
                    dot_group = VGroup(dot, six_tex)
                    self.play(
                        ShowPassingFlash(displayed_tree.edges[(parent_node, current_node)].copy().reverse_direction().set_stroke(width=5,color=YELLOW)),
                        ReplacementTransform(displayed_best_so_far.copy(), dot_group)
                    )
                    self.wait(1.7)
                    self.play(Indicate(global_window_group_list[parent_node][ALPHA_TEX]), run_time=1.9)
                    self.wait(6.3)
                    line_start = global_window_group_list[parent_node][RECT].get_corner(DL)
                    line_end = global_window_group_list[parent_node][RECT].get_corner(DR)
                    self.play(
                        ReplacementTransform(global_window_group_list[parent_node][RECT], global_window_group_list[parent_node+internal_tree.size][RECT]),
                        run_time=2
                    )
                    self.wait(1.2)
                    self.play(GrowFromCenter(
                            Line(
                                start=line_start,
                                end=line_end, 
                                color=GREEN
                            )
                        ),
                        run_time=1.5
                    )
                    self.wait(2.8)
                    self.next_section("beta_cutoff")
                    return best_so_far
                AnimateReturnAlphaBeta(parent_node, current_node, best_so_far, displayed_best_so_far, exact)
                return best_so_far
            
            for children_node in internal_tree.edges_dict[current_node]:
                best_so_far = max(best_so_far, -ABNegamax(displayed_tree, internal_tree, current_node, children_node, -side_to_move, -beta, -alpha))
                AddWindow(displayed_node, current_node+internal_tree.size, -best_so_far, beta)
                if best_so_far > alpha:
                    alpha = best_so_far
                    exact = True
                beta_cutoff = False
                if alpha >= beta:
                    beta_cutoff = True
                    exact = False
                    break
                
            displayed_best_so_far = MathTex(NumToStr(best_so_far)).move_to(displayed_node)
            self.play(FadeIn(displayed_best_so_far, scale=1.5))

            if beta_cutoff:
                children_node += 1
                while(children_node in internal_tree.edges_dict[current_node]):
                    self.play(Create(Cross(scale_factor=RADIUS-0.1).move_to(displayed_tree.edges[(current_node, children_node)])) )
                    children_node += 1
                            
            AnimateReturnAlphaBeta(parent_node, current_node, best_so_far, displayed_best_so_far, exact)

            return best_so_far
                

        internal_tree = Tree()
        displayed_tree = Graph([i for i in range(1, internal_tree.size) if i !=7],
            internal_tree.edges_list,
            layout="tree",
            layout_config={"root_vertex":1},
            layout_scale=LAYOUT_SCALE,
            vertex_config=VERTEX_CONFIG,
            labels=internal_tree.labels
        ).flip(axis=UP).move_to(RIGHT*0.5)

        self.play(*[FadeOut(submobject) for submobject in self.mobjects], run_time=3.5)
        self.play(Write(displayed_tree))

        global_window_group_list = [None for _ in range(1, 2*(internal_tree.size+1))]
        ABNegamax(displayed_tree, internal_tree, parent_node=1, current_node=1, side_to_move=1)



# with tempconfig({"quality": "medium_quality", "disable_caching": True}):
#     scene = AnimateTree()
#     scene.render()