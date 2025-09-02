from manim import *
from tree import *
import numpy as np
import random as Rand
from collections import deque

RADIUS = 0.35
VERTEX_CONFIG = {"stroke_width": 2, "stroke_color": WHITE, "radius": RADIUS, "color":BLACK, "fill_opacity": 1}
LAYOUT_SCALE = (6, 3)

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
    

class Minimax(Scene):
    def construct(self):
        self.next_section("section_1", skip_animations=True)
        tex = Tex("Minimax and alpha-beta pruning")
        tex[0][10:15].set_color(RED)
        tex[0][16:20].set_color(BLUE)
        self.play(Write(tex), run_time=3.4)
        self.wait(0.5)
        self.play(tex.animate.shift(UP*3), run_time=1.5)
        self.wait(0.5)
        cue_template = Text("#")
        cue = cue_template.copy()
        self.play(Write(cue))
        self.wait(2)
        self.wait(7.5)
        self.play(Indicate(tex[0][10:20]), run_time=2)
        self.wait(0.4)
        self.wait(7.8)


        self.next_section("section_2", skip_animations=True)

        minimax_tex = tex[0][0:7]
        remaining_tex = tex[0][7:]

        player_template = VGroup(Circle(radius=0.25, fill_opacity=0.5, stroke_width=0).shift(UP*0.75), Sector(radius=0.5, angle=180*DEGREES, fill_opacity=0.5)).center()
        player1 = player_template.copy().set_color(RED).shift(LEFT*2.5)
        player2 = player_template.copy().set_color(BLUE).shift(RIGHT*2.5)

        turn_arrows = VGroup(
            CurvedArrow(start_point=[-1.5,-0.5,0], end_point=[1.5,-0.5,0], color=RED), 
            CurvedArrow(start_point=[1.5,0.5,0], end_point=[-1.5,0.5,0], color=BLUE)
        )

        info = Text("i", color=BLUE_A, font_size=80, weight=ULTRAHEAVY)
        circle_surround = Circle(color=BLUE_D, fill_opacity=0.5).surround(info)
        perfect_information = VGroup(info, circle_surround).shift(LEFT*0.75)

        base = Rectangle(width=2, height=0.3, color=YELLOW, fill_opacity=1).shift(DOWN*2.5)
        post = Rectangle(width=0.3, height=3, color=YELLOW, fill_opacity=1).next_to(base, UP)
        beam = Rectangle(width=6, height=0.3, color=YELLOW, fill_opacity=1).next_to(post, UP)
        cap = Circle(radius=0.3, color=YELLOW, fill_opacity=1).next_to(post, UP, buff=-0.15)
        left_hook = Line(beam.get_left() + RIGHT*0.3, beam.get_left() + DOWN*1.5 + RIGHT*0.3, color=WHITE).set_z_index(-1)
        right_hook = Line(beam.get_right() + LEFT*0.3, beam.get_right() + DOWN*1.5 + LEFT*0.3, color=WHITE).set_z_index(-1)
        left_bowl = Arc(radius=1, angle=PI, color=YELLOW, fill_opacity=1).shift(left_hook.get_end() + DOWN*0.2).rotate(PI)
        right_bowl = Arc(radius=1, angle=PI, color=YELLOW, fill_opacity=1).shift(right_hook.get_end() + DOWN*0.2).rotate(PI)
        scales = VGroup(base, post, beam, cap, left_hook, right_hook, left_bowl, right_bowl).move_to([0, -1.5, 0])
        scales_icon = scales.copy().set(height=0.8).center().shift(RIGHT*0.75)

        score = ValueTracker(0.5)
        red_circle = always_redraw(lambda: Circle(radius=score.get_value(), color=RED, fill_opacity=1).next_to(left_bowl, UP, buff=0))
        blue_circle = always_redraw(lambda: Circle(radius=1-score.get_value(), color=BLUE, fill_opacity=1).next_to(right_bowl, UP, buff=0))

        self.play(LaggedStart(AnimationGroup(FadeOut(remaining_tex), FadeOut(cue)), minimax_tex.animate.move_to(tex.get_center()), lag_ratio=0.5), run_time=3)
        self.wait(3.8)
        self.play(DrawBorderThenFill(player1), DrawBorderThenFill(player2), run_time=0.8)
        self.play(Create(turn_arrows))
        self.play(Write(perfect_information[0]), DrawBorderThenFill(perfect_information[1]), run_time=1.3)
        self.play(FadeIn(scales_icon), run_time=1.5)
        self.wait()
        self.play(
            LaggedStart(
                AnimationGroup(
                    player1.animate.move_to([-2.7, -2.8, 0]),
                    player2.animate.move_to([2.7, -2.8, 0]), 
                    FadeOut(turn_arrows, perfect_information),
                    ReplacementTransform(scales_icon, scales),
                ),
                AnimationGroup(
                    Create(red_circle),
                    Create(blue_circle)
                ),
                lag_ratio=0.5
            ),
            run_time=2
        )
        self.wait(1.4)
        #(player, score, angle, hook_shift, run_time, wait)
        animation_sets = [(0, 0.75, 0.2, 0.5, 2, 0.1), (0, 0.25, -0.4, -1, 2, 10), (0, 0.1, -0.1, -0.25, 3, 0.1), 
                          (1, 0.15, 0.05, 0.15, 1, 0.2), (2, 0.1, -0.05, -0.15, 1, 0.2), (1, 0.25, 0.1, 0.25, 1, 0.2), (2, 0.15, -0.05, -0.1, 1, 0.2), 
                          (1, 0.35, 0.15, 0.25, 1, 0.2), (2, 0.15, -0.15, -0.25, 1, 0.2),] 
        for animation_set in animation_sets:
            match animation_set[0]:
                case 0: player = Dot(radius=0)
                case 1: player = player1
                case 2: player = player2
            self.play(
                player.animate.scale(6/5),
                score.animate.set_value(animation_set[1]),
                Rotate(beam, angle=animation_set[2], about_point=post.get_top()),
                left_hook.animate.shift(DOWN*animation_set[3]),
                right_hook.animate.shift(UP*animation_set[3]),
                left_bowl.animate.shift(DOWN*animation_set[3]),
                right_bowl.animate.shift(UP*animation_set[3]),
                run_time=animation_set[4]
            )
            self.play(player.animate.scale(5/6), run_time=animation_set[5])
        self.wait(0.5)


        self.next_section("section_3", skip_animations=True)

        minimax_code = '''def Minimax(depth, current_position, is_maximiser):
    if depth == 0:
        return Evaluate(current_position)

    MakeMove(current_position) #generates children_position
    if is_maximiser:
        best_so_far = -math.inf
        for children_position in current_position:
            best_so_far = max(best_so_far, Minimax(depth - 1, children_position, False))
    else:
        best_so_far = math.inf
        for children_position in current_position:
            best_so_far = min(best_so_far, Minimax(depth - 1, children_position, True))

    return best_so_far'''
        base_minimax_code = Code(
            code_string=minimax_code,
            language="python",
            add_line_numbers=False,
            background="rectangle",
            paragraph_config={"width":10, "height":6}
        )
        rendered_minimax_code = base_minimax_code.copy()
        
        self.play(*[FadeOut(submobject) for submobject in self.mobjects])
        self.play(
            Succession(
                Create(rendered_minimax_code.background), 
                Write(VGroup(rendered_minimax_code.code_lines[0][i] for i in [0,1,2,3,4,5,6,7,8,9,10,11,49,50]))
            ),
            run_time=2.4
        )
        self.wait(0.35)
        self.play(Write(VGroup(rendered_minimax_code.code_lines[0][i] for i in [12,13,14,15,16,17])), run_time=1.4)
        self.play(Write(VGroup(rendered_minimax_code.code_lines[0][i] for i in range(19,36))), run_time=1.4)
        self.wait(0.5)
        self.play(Write(VGroup(rendered_minimax_code.code_lines[0][i] for i in range(37,49))), run_time=1.3)

        self.wait(3)
        self.play(FadeIn(rendered_minimax_code.code_lines[4]), run_time=3)
        self.wait(3.3)
        self.wait(1.1)
        self.play(Write(rendered_minimax_code.code_lines[2]), run_time=2.9)
        self.play(Write(rendered_minimax_code.code_lines[1]), run_time=2.1)
        self.wait(7.6)

        self.play(FadeIn(rendered_minimax_code.code_lines[5:15]), run_time=2.7)
        self.wait()
        self.play(Indicate(VGroup(rendered_minimax_code.code_lines[8][43:88])), Indicate(VGroup(rendered_minimax_code.code_lines[12][43:87])))
        scale = 1.1
        self.play(rendered_minimax_code.code_lines[5:9].animate.scale(scale))
        for i in range(4):
            if i % 2 == 0:
                self.play(rendered_minimax_code.code_lines[9:13].animate.scale(scale), rendered_minimax_code.code_lines[5:9].animate.scale(1/scale))
            else:
                self.play(rendered_minimax_code.code_lines[9:13].animate.scale(1/scale), rendered_minimax_code.code_lines[5:9].animate.scale(scale))
        self.play(rendered_minimax_code.code_lines[5:9].animate.scale(1/scale))


        self.next_section("section_4", skip_animations=True)

        def Minimax(displayed_tree: Graph, internal_tree: Tree, current_node: int, is_maximiser: bool):
            displayed_node = displayed_tree[current_node]

            if current_node not in internal_tree.edges_dict: #checks if current_node is a leaf
                return internal_tree.scores[current_node]
            
            if is_maximiser:
                best_so_far = -10
                for children_node in internal_tree.edges_dict[current_node]:
                    self.play(ShowPassingFlash(displayed_tree.edges[(current_node, children_node)].copy().set_stroke(width=5,color=YELLOW)))
                    child_score = Minimax(displayed_tree, internal_tree, children_node, False)
                    best_so_far = max(best_so_far, child_score)
            else:
                best_so_far = 10
                for children_node in internal_tree.edges_dict[current_node]:
                    self.play(ShowPassingFlash(displayed_tree.edges[(current_node, children_node)].copy().set_stroke(width=5,color=YELLOW)))
                    child_score = Minimax(displayed_tree, internal_tree, children_node, True)
                    best_so_far = min(best_so_far, child_score)
            self.play(Write(MathTex(NumToStr(best_so_far)).move_to(displayed_node), scale=1.5))
            return best_so_far
        
        internal_tree = Tree("minimax")
        displayed_tree_base = Graph(
            vertices=[i for i in range(1,internal_tree.size)],
            edges=internal_tree.edges_list,
            layout="tree",
            layout_config={"root_vertex":1},
            layout_scale=(3, 3),
            vertex_config=VERTEX_CONFIG,
            labels=internal_tree.labels
        ).flip(axis=UP).move_to(RIGHT*3.5)
        displayed_tree = displayed_tree_base.copy()
        for vertex in displayed_tree.vertices.values():
            vertex[1].set_opacity(0)
        max_text = Tex("Max", color=RED).move_to([0.6,0,0]).align_to(displayed_tree[1], UP)
        min_text = Tex("Min", color=BLUE).move_to([0.6,0,0]).align_to(displayed_tree[2], UP)
        line = Line(start=[0,5,0], end=[0,-5,0])

        self.play(rendered_minimax_code.animate.scale(0.5).shift(LEFT*3.5), Create(line), run_time=2)
        self.play(Create(displayed_tree), Write(max_text), Write(min_text), run_time=1.5)
        self.wait(1.5)
        self.play(*[Indicate(edge) for edge in displayed_tree.edges.values()], run_time=0.9)
        self.play(*[Indicate(vertex) for vertex in list(displayed_tree.vertices.values())[1:]], run_time=1.1)
        self.wait(1.4)
        self.play(Indicate(displayed_tree.vertices[1]), run_time=1.2)
        self.wait(2.6)
        self.play(LaggedStart(Indicate(displayed_tree[i]) for i in range(4,8)), lag_ratio=0.35, run_time=2.2)
        self.wait(1.8)
        self.play(*[vertex[1].animate.set_opacity(1) for vertex in displayed_tree.vertices.values()], run_time=2.2)
        self.wait()
        Minimax(displayed_tree, internal_tree, 1, True)
        self.wait(4.2)
        self.play(displayed_tree[4][1].animate.set_color(RED))
        self.wait(2.3)
        self.play(displayed_tree.edges[(1,3)].animate.set_color(YELLOW), displayed_tree.edges[(3,7)].animate.set_color(YELLOW))
        self.wait(1.2)
        self.play(displayed_tree.edges[(2,4)].animate.set_color(RED))
        self.wait(2.5)
        self.wait(3.6)
        minimax_tree = VGroup(displayed_tree, *[mobject for mobject in self.mobjects[27:30]], max_text, min_text)
        self.play(
            LaggedStart(
                AnimationGroup(
                    minimax_tree.animate.set_opacity(0), 
                    FadeOut(line)
                ),
                rendered_minimax_code.animate.scale(2).shift(RIGHT*3.5), 
                lag_ratio=0.25
            ),
            run_time=1.8
        )
        minimax_tree[0] = displayed_tree_base.copy().set_opacity(0)
        self.wait(1.3)


        self.next_section("section_5", skip_animations=True)

        redundant_code = VGroup(*rendered_minimax_code.code_lines[5:13].copy()).scale(1.1).center()
        feature = VGroup(Dot(color=RED).shift(LEFT*0.75), Tex("Feature", font_size=24, color=RED))
        feature_1 = feature.copy().next_to(redundant_code[0][19])
        feature_2 = feature.copy().next_to(redundant_code[4][8])
        self.play(
            VGroup(*rendered_minimax_code.code_lines[0:5]).animate.set_opacity(0),
            VGroup(*rendered_minimax_code.code_lines[13:15]).animate.set_opacity(0), 
            VGroup(*rendered_minimax_code.code_lines[5:13]).animate.scale(1.1).center(), 
            Transform(rendered_minimax_code.background, SurroundingRectangle(redundant_code, **Code.default_background_config)),
            run_time=1.5
        )
        self.wait(4)
        self.play(FadeIn(feature_1), FadeIn(feature_2), run_time=1.6)
        self.wait(1.5)
        self.play(
            feature_1.animate.align_to(rendered_minimax_code.code_lines[6], UL).shift(DOWN*0.25), 
            FadeOut(feature_2),
            rendered_minimax_code.code_lines[5].animate.set_opacity(0),
            rendered_minimax_code.code_lines[9].animate.set_opacity(0),
            VGroup(*rendered_minimax_code.code_lines[6:9]).animate.shift(DOWN*0.5), 
            VGroup(*rendered_minimax_code.code_lines[10:13]).animate.shift(UP*0.5),
            run_time=2
        )
        self.wait()

        rendered_minimax_code_2 = base_minimax_code.copy()
        absolute_score_arrow = Arrow(
            start=rendered_minimax_code_2.code_lines[2][-1].get_right(), 
            end=rendered_minimax_code_2.code_lines[2][-1].get_right()+RIGHT*2,
            max_tip_length_to_length_ratio=0.15
        )
        absolute_score_text = Tex("Absolute score", font_size=24).next_to(absolute_score_arrow)
        absolute_score = VGroup(absolute_score_arrow, absolute_score_text)
        score_equation = Tex("My score = -Opponent score").shift(UP*2.5)
        negamax_code = '''def Negamax(depth, current_position):
    if depth == 0:
        return RelativeEvaluate(current_position)

    MakeMove(current_position) #generates children_position
        best_so_far = -math.inf
        for children_position in current_position:
            best_so_far = max(best_so_far, -Negamax(depth - 1, children_position))

    return best_so_far'''
        base_negamax_code = Code(
            code_string=negamax_code,
            language="python",
            add_line_numbers=False,
            background="rectangle",
            paragraph_config={"width":10, "height":6}
        )
        rendered_negamax_code = base_negamax_code.copy()
        self.play(ReplacementTransform(rendered_minimax_code, rendered_minimax_code_2), FadeOut(feature_1))
        self.wait(1.2)
        self.play(Succession(Create(absolute_score_arrow), Write(absolute_score_text)), run_time=2)
        self.wait(3.4)
        self.play(Transform(absolute_score_text, Tex("Relative score", font_size=24).next_to(absolute_score_arrow)), run_time=1.6)
        self.wait(9.5)
        self.play(Write(score_equation), run_time=3)
        self.wait(2.2)
        self.play(
            FadeOut(score_equation), 
            FadeOut(absolute_score, target_position=rendered_minimax_code.code_lines[2][23], scale=0.5),
            run_time=1.4
        )
        self.play(ReplacementTransform(rendered_minimax_code_2, rendered_negamax_code), run_time=2.2)
        self.wait(4)

        self.next_section("section_6", skip_animations=False)
        line = Line(start=[0,5,0], end=[0,-5,0])
        negamax_tree = minimax_tree.copy().set_opacity(1)
        negamax_tree[1] = MathTex("4").move_to(minimax_tree[1])
        negamax_tree[2] = MathTex("-2").move_to(minimax_tree[2])
        negamax_tex = Tex("Negamax").to_corner(UR)
        self.play(rendered_negamax_code.animate.scale(0.5).shift(LEFT*3.5), Create(line), run_time=2.5)
        self.play(Create(negamax_tree[0:-2]), Write(negamax_tree[-2]), Write(negamax_tree[-1]), Write(negamax_tex), run_time=2.1)
        self.wait(1.4)
        self.play(
            Transform(negamax_tree[1], MathTex("-4").move_to(minimax_tree[1])), 
            Transform(negamax_tree[2], MathTex("2").move_to(minimax_tree[2])), 
            Transform(negamax_tex, Tex("Minimax").to_corner(UR)),
            run_time=2
        )
        self.wait(0.3)
        self.play(
            Transform(negamax_tree[1], MathTex("4").move_to(minimax_tree[1])), 
            Transform(negamax_tree[2], MathTex("-2").move_to(minimax_tree[2])), 
            Transform(negamax_tex, Tex("Negamax").to_corner(UR)),
            run_time=2
        )

        self.wait(1.7)
        negamax_tree[0].set_z_index(-1)
        self.play(LaggedStart(*[Indicate(negamax_tree[0][node]) for node in negamax_tree[0].vertices], lag_ratio=0.25), run_time=1.7)
        self.wait(5.2)
        self.play(FadeOut(*self.mobjects))
        cue = cue_template.copy()
        self.play(Write(cue))
        self.wait(4.6)
        self.play(Unwrite(cue))
        self.wait(6.5)

        self.next_section("section_7", skip_animations=False)
        

class AB(Scene):
    def construct(self):
        self.next_section("Intro_to_ab", skip_animations=False)

        # chapter_3 = Tex(r"\textbf{\underline{\Large Chapter 3}}\\")
        # ab_chapter_text = Tex(r"Alpha-Beta Pruning", substrings_to_isolate=("Alpha","Beta")).next_to(chapter_3, DOWN)
        # self.play(FadeIn(chapter_3, scale=3), FadeIn(ab_chapter_text, shift=UP*2, scale=3), run_time=3)
        # self.wait(0.5)
        # self.play(FadeOut(chapter_3), ab_chapter_text.animate.set_color_by_tex(r"Alpha", RED).set_color_by_tex(r"Beta", BLUE).move_to((0,0,0)), run_time=2)
        # self.wait(5)

        # self.next_section("explain_ab", skip_animations=False)

        # alpha_text_1 = Tex("Alpha: Best score maximiser has guaranteed", substrings_to_isolate=("Alpha", "maximiser")).shift(UP).scale(1.2)
        # alpha_text_1.set_color_by_tex(r"Alpha", RED)
        # alpha_text_1.set_color_by_tex(r"maximiser", RED)
        # beta_text_1 = Tex("Beta: Best score minimiser has guaranteed", substrings_to_isolate=("Beta", "minimiser")).shift(DOWN).scale(1.2)
        # beta_text_1.set_color_by_tex(r"Beta", BLUE)
        # beta_text_1.set_color_by_tex(r"minimiser", BLUE)
        # ab_group_1 = VGroup(alpha_text_1, beta_text_1)

        # alpha_text_2 = Tex("Alpha: Best score side-to-move has guaranteed", substrings_to_isolate=("Alpha", "side-to-move")).shift(UP).scale(1.2)
        # alpha_text_2.set_color_by_tex(r"Alpha", RED)
        # beta_text_2 = Tex("Beta: Best score opponent has guaranteed", substrings_to_isolate=("Beta", "opponent")).shift(DOWN).scale(1.2)
        # beta_text_2.set_color_by_tex(r"Beta", BLUE)
        # ab_group_2 = VGroup(alpha_text_2, beta_text_2)

        # beta_text_3 = Tex("Beta: Maximum score opponent will allow us to have", substrings_to_isolate=("Beta", "opponent")).shift(DOWN).scale(1.2)
        # beta_text_3.set_color_by_tex(r"Beta", BLUE)

        # minimax_text = Tex("Minimax", font_size=96).to_edge(UP)
        # negamax_text = Tex("Negamax", font_size=96).to_edge(UP)

        # self.play(Write(minimax_text), TransformMatchingTex(ab_chapter_text, ab_group_1), run_time=4)
        # self.wait(5.5)
        # self.wait(2)
        # self.play(ReplacementTransform(minimax_text, negamax_text))
        # self.wait(5.2)
        # self.play(ReplacementTransform(ab_group_1, ab_group_2), run_time=4)
        # self.wait(3.8)
        # self.play(ReplacementTransform(ab_group_2[1], beta_text_3), run_time=3)
        # self.wait(5)      

        alpha_beta_tex = Tex("Alpha-beta pruning").shift(UP*3)
        alpha_beta_tex[0][0:5].set_color(RED)
        internal_tree = Tree()
        internal_tree.edges_list = [(1, 2), (1, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (3, 9), (3, 10), (4, 11), (4, 12), (4, 13), (5, 14), (5, 15), (6, 16), (6, 17), (7, 18), (7, 19), (7, 20), (7, 21), (7, 22), (8, 23), (8, 24), (8, 25), (8, 26), (9, 27), (9, 28), (9, 29), (10, 30), (10, 31), (10, 32), (10, 33), (11, 34), (11, 35), (12, 36), (12, 37), (12, 38), (12, 39), (12, 40), (12, 41), (13, 42), (13, 43), (13, 44), (13, 45), (13, 46), (13, 47), (13, 48), (14, 49), (14, 50), (14, 51), (14, 52), (14, 53), (14, 54), (14, 55), (15, 56), (15, 57), (15, 58), (16, 59), (16, 60), (16, 61), (16, 62), (16, 63), (17, 64), (17, 65), (17, 66), (18, 67), (18, 68), (18, 69), (19, 70), (19, 71), (19, 72), (19, 73), (19, 74), (19, 75), (19, 76), (19, 77), (19, 78), (19, 79), (19, 80), (19, 81), (20, 82), (20, 83), (21, 84), (21, 85), (21, 86), (22, 87), (22, 88), (22, 89), (22, 90), (23, 91), (23, 92), (23, 93), (23, 94), (24, 95), (24, 96), (24, 97), (24, 98), (24, 99), (25, 100), (25, 101), (25, 102), (25, 103), (25, 104), (26, 105), (26, 106), (27, 107), (27, 108), (27, 109), (28, 110), (28, 111), (29, 112), (29, 113), (29, 114), (29, 115), (30, 116), (30, 117), (31, 118), (31, 119), (31, 120), (32, 121), (33, 122), (33, 123), (33, 124)]
        internal_tree.edges_dict = {1: (2, 3), 2: (4, 5, 6, 7, 8), 3: (9, 10), 4: (11, 12, 13), 5: (14, 15), 6: (16, 17), 7: (18, 19, 20, 21, 22), 8: (23, 24, 25, 26), 9: (27, 28, 29), 10: (30, 31, 32, 33), 11: (34, 35), 12: (36, 37, 38, 39, 40, 41), 13: (42, 43, 44, 45, 46, 47, 48), 14: (49, 50, 51, 52, 53, 54, 55), 15: (56, 57, 58), 16: (59, 60, 61, 62, 63), 17: (64, 65, 66), 18: (67, 68, 69), 19: (70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81), 20: (82, 83), 21: (84, 85, 86), 22: (87, 88, 89, 90), 23: (91, 92, 93, 94), 24: (95, 96, 97, 98, 99), 25: (100, 101, 102, 103, 104), 26: (105, 106), 27: (107, 108, 109), 28: (110, 111), 29: (112, 113, 114, 115), 30: (116, 117), 31: (118, 119, 120), 32: (121,), 33: (122, 123, 124)}
        internal_tree.labels={1:MathTex('-1').flip(axis=UP),2:MathTex('7').flip(axis=UP),3:MathTex('1').flip(axis=UP),4:MathTex('-6').flip(axis=UP),5:MathTex('-6').flip(axis=UP),6:MathTex('-7').flip(axis=UP),7:MathTex('-3').flip(axis=UP),8:MathTex('7').flip(axis=UP),9:MathTex('-1').flip(axis=UP),10:MathTex('8').flip(axis=UP),11:MathTex('6').flip(axis=UP),12:MathTex('9').flip(axis=UP),13:MathTex('8').flip(axis=UP),14:MathTex('6').flip(axis=UP),15:MathTex('8').flip(axis=UP),16:MathTex('7').flip(axis=UP),17:MathTex('7').flip(axis=UP),18:MathTex('8').flip(axis=UP),19:MathTex('9').flip(axis=UP),20:MathTex('3').flip(axis=UP),21:MathTex('').flip(axis=UP),22:MathTex('').flip(axis=UP),23:MathTex('9').flip(axis=UP),24:MathTex('9').flip(axis=UP),25:MathTex('7').flip(axis=UP),26:MathTex('-7').flip(axis=UP),27:MathTex('8').flip(axis=UP),28:MathTex('9').flip(axis=UP),29:MathTex('1').flip(axis=UP),30:MathTex('-8').flip(axis=UP),31:MathTex('').flip(axis=UP),32:MathTex('').flip(axis=UP),33:MathTex('').flip(axis=UP),34:MathTex('-6').flip(axis=UP),35:MathTex('3').flip(axis=UP),36:MathTex('-9').flip(axis=UP),37:MathTex('-3').flip(axis=UP),38:MathTex('6').flip(axis=UP),39:MathTex('-7').flip(axis=UP),40:MathTex('6').flip(axis=UP),41:MathTex('-8').flip(axis=UP),42:MathTex('7').flip(axis=UP),43:MathTex('2').flip(axis=UP),44:MathTex('6').flip(axis=UP),45:MathTex('-1').flip(axis=UP),46:MathTex('8').flip(axis=UP),47:MathTex('2').flip(axis=UP),48:MathTex('-8').flip(axis=UP),49:MathTex('-6').flip(axis=UP),50:MathTex('1').flip(axis=UP),51:MathTex('2').flip(axis=UP),52:MathTex('-3').flip(axis=UP),53:MathTex('9').flip(axis=UP),54:MathTex('3').flip(axis=UP),55:MathTex('6').flip(axis=UP),56:MathTex('-1').flip(axis=UP),57:MathTex('-8').flip(axis=UP),58:MathTex('-6').flip(axis=UP),59:MathTex('3').flip(axis=UP),60:MathTex('-2').flip(axis=UP),61:MathTex('-3').flip(axis=UP),62:MathTex('-7').flip(axis=UP),63:MathTex('4').flip(axis=UP),64:MathTex('-7').flip(axis=UP),65:MathTex('7').flip(axis=UP),66:MathTex('-3').flip(axis=UP),67:MathTex('-8').flip(axis=UP),68:MathTex('-2').flip(axis=UP),69:MathTex('-7').flip(axis=UP),70:MathTex('0').flip(axis=UP),71:MathTex('-5').flip(axis=UP),72:MathTex('-5').flip(axis=UP),73:MathTex('2').flip(axis=UP),74:MathTex('3').flip(axis=UP),75:MathTex('0').flip(axis=UP),76:MathTex('-3').flip(axis=UP),77:MathTex('2').flip(axis=UP),78:MathTex('4').flip(axis=UP),79:MathTex('-2').flip(axis=UP),80:MathTex('-9').flip(axis=UP),81:MathTex('1').flip(axis=UP),82:MathTex('-3').flip(axis=UP),83:MathTex('4').flip(axis=UP),84:MathTex('-3').flip(axis=UP),85:MathTex('6').flip(axis=UP),86:MathTex('9').flip(axis=UP),87:MathTex('-9').flip(axis=UP),88:MathTex('0').flip(axis=UP),89:MathTex('1').flip(axis=UP),90:MathTex('7').flip(axis=UP),91:MathTex('-9').flip(axis=UP),92:MathTex('-8').flip(axis=UP),93:MathTex('1').flip(axis=UP),94:MathTex('7').flip(axis=UP),95:MathTex('5').flip(axis=UP),96:MathTex('-3').flip(axis=UP),97:MathTex('2').flip(axis=UP),98:MathTex('7').flip(axis=UP),99:MathTex('-9').flip(axis=UP),100:MathTex('1').flip(axis=UP),101:MathTex('-1').flip(axis=UP),102:MathTex('-7').flip(axis=UP),103:MathTex('9').flip(axis=UP),104:MathTex('7').flip(axis=UP),105:MathTex('7').flip(axis=UP),106:MathTex('9').flip(axis=UP),107:MathTex('-8').flip(axis=UP),108:MathTex('7').flip(axis=UP),109:MathTex('3').flip(axis=UP),110:MathTex('-2').flip(axis=UP),111:MathTex('-9').flip(axis=UP),112:MathTex('2').flip(axis=UP),113:MathTex('-1').flip(axis=UP),114:MathTex('3').flip(axis=UP),115:MathTex('1').flip(axis=UP),116:MathTex('9').flip(axis=UP),117:MathTex('8').flip(axis=UP),118:MathTex('6').flip(axis=UP),119:MathTex('-5').flip(axis=UP),120:MathTex('6').flip(axis=UP),121:MathTex('8').flip(axis=UP),122:MathTex('1').flip(axis=UP),123:MathTex('5').flip(axis=UP),124:MathTex('-3').flip(axis=UP),}
        internal_tree.scores = {1: -1, 2: 7, 3: 1, 4: -6, 5: -6, 6: -7, 7: -3, 8: 7, 9: -1, 10: 8, 11: 6, 12: 9, 13: 8, 14: 6, 15: 8, 16: 7, 17: 7, 18: 8, 19: 9, 20: 3, 21: None, 22: None, 23: 9, 24: 9, 25: 7, 26: -7, 27: 8, 28: 9, 29: 1, 30: -8, 31: None, 32: None, 33: None, 34: -6, 35: 3, 36: -9, 37: -3, 38: 6, 39: -7, 40: 6, 41: -8, 42: 7, 43: 2, 44: 6, 45: -1, 46: 8, 47: 2, 48: -8, 49: -6, 50: 1, 51: 2, 52: -3, 53: 9, 54: 3, 55: 6, 56: -1, 57: -8, 58: -6, 59: 3, 60: -2, 61: -3, 62: -7, 63: 4, 64: -7, 65: 7, 66: -3, 67: -8, 68: -2, 69: -7, 70: 0, 71: -5, 72: -5, 73: 2, 74: 3, 75: 0, 76: -3, 77: 2, 78: 4, 79: -2, 80: -9, 81: 1, 82: -3, 83: 4, 84: -3, 85: 6, 86: 9, 87: -9, 88: 0, 89: 1, 90: 7, 91: -9, 92: -8, 93: 1, 94: 7, 95: 5, 96: -3, 97: 2, 98: 7, 99: -9, 100: 1, 101: -1, 102: -7, 103: 9, 104: 7, 105: 7, 106: 9, 107: -8, 108: 7, 109: 3, 110: -2, 111: -9, 112: 2, 113: -1, 114: 3, 115: 1, 116: 9, 117: 8, 118: 6, 119: -5, 120: 6, 121: 8, 122: 1, 123: 5, 124: -3}    
        internal_tree.size = 125

        crosses = VGroup()
        def Negamax(internal_tree: Tree, displayed_tree: Graph, current_node: int, side_to_move: int, alpha:int, beta:int):
            best_so_far = -10
            beta_cutoff = False

            if current_node not in internal_tree.edges_dict: #checks if current_node is a leaf
                best_so_far = max(best_so_far, internal_tree.scores[current_node])
                return best_so_far

            best_so_far = -10
            for children_node in internal_tree.edges_dict[current_node]:
                best_so_far = max(best_so_far, -Negamax(internal_tree, displayed_tree, children_node, -side_to_move, -beta, -alpha))
                alpha = max(best_so_far, alpha)
                internal_tree.scores[current_node] = best_so_far
                internal_tree.labels[current_node] = MathTex(f"{best_so_far}").flip(axis=UP)
                if best_so_far > beta:
                    beta_cutoff = True
                    break

            if beta_cutoff == True:
                children_node += 1
                while(children_node in internal_tree.edges_dict[current_node]):
                    crosses.add((Cross(scale_factor=RADIUS-0.1).move_to(displayed_tree.edges[(current_node, children_node)])))
                    children_node += 1
                return best_so_far

            return best_so_far

        displayed_tree = Graph([i for i in range(1, internal_tree.size)],
            internal_tree.edges_list,
            layout="tree",
            layout_config={"root_vertex":1},
            layout_scale=(6,2.5),
            vertex_config=VERTEX_CONFIG,
            labels=internal_tree.labels
        ).flip(axis=UP).shift(DOWN*0.5)
        Negamax(internal_tree, displayed_tree, 1, 1, -10, 10)

        alpha_beta_tex[0][6:10].set_color(BLUE)
        opponent_POV = Tex("Opponent POV:").to_corner(UL).shift(DOWN*1.5+RIGHT*0.5)
        blist = BulletedList("Don't allow position", "Get rekt").next_to(opponent_POV, DOWN).shift(RIGHT)
        # dont_allow = Tex("Don't allow position").next_to(opponent_POV, DR)
        # get_rekt = Tex("Get rekt").next_to(dont_allow, DOWN)
        self.play(Succession(Write(alpha_beta_tex), Create(displayed_tree)), run_time=3)
        self.wait(2.1)
        self.play(Create(crosses), run_time=2.4)
        self.wait(2.8)
        self.play(Indicate(displayed_tree[1][1]), run_time=2.3)
        self.wait(3.3)
        self.play(Indicate(displayed_tree[20][1]), run_time=2.2)
        self.play(Indicate(crosses[7:9]))
        self.wait(0.8)
        self.play(Uncreate(crosses), Uncreate(displayed_tree))
        self.play(Write(opponent_POV))
        self.play(Write(blist[0]), run_time=2)
        self.wait(0.7)
        self.play(Write(blist[1]), run_time=2)
        self.wait(4.5)
        self.next_section("window_ab", skip_animations=False)

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
        alpha = alpha_beta_tex[0][0:5].copy()
        beta = alpha_beta_tex[0][6:10].copy()
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
        self.play(*[FadeOut(mobject) for mobject in self.mobjects], ReplacementTransform(alpha, alpha_tex), ReplacementTransform(beta, beta_tex), run_time=2)
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

        self.next_section("ab_code", skip_animations=True)

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

        if best_so_far >= beta:
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
        self.wait(1.2)
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

        RECT=0
        ALPHA_TEX=1
        BETA_TEX=2
        NEGATIVE_ALPHA_TEX=3
        NEGATIVE_BETA_TEX=4
        global_window_group_list = []
        global_crosses_list = []

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
            else:
                AnimateAlphaBeta(parent_node, current_node)
            best_so_far = -10

            if current_node not in internal_tree.edges_dict: #checks if current_node is a leaf
                best_so_far = internal_tree.scores[current_node]
                color = RED
                dot = Dot(radius=0.04, color=color).next_to(displayed_tree[current_node]).shift((0,(RADIUS/10)*(best_so_far),0))
                dot.move_to((global_window_group_list[current_node][RECT].get_x(), dot.get_y(), 0))
                dot_tex = Tex(f"{best_so_far}", font_size=10, color=color).next_to(dot, LEFT)
                dot_group = VGroup(dot, dot_tex)
                displayed_best_so_far = MathTex(NumToStr(best_so_far)).move_to(displayed_node)
                self.play(ReplacementTransform(displayed_best_so_far.copy(), dot_group))
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
                    self.wait(3)
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
                    return best_so_far
                if current_node == 9:
                    self.next_section("beta_cutoff", skip_animations=True)
                    dot = Dot(radius=0.04, color=RED).next_to(displayed_tree[parent_node]).shift((0,(RADIUS/10)*(-best_so_far),0))
                    dot.move_to((global_window_group_list[parent_node][RECT].get_x(), dot.get_y(), 0))
                    eight_tex = Tex("8", font_size=10, color=RED).next_to(dot, LEFT)
                    dot_group = VGroup(dot, eight_tex)
                    six_tex = Tex("6 for us", substrings_to_isolate=("6",)).move_to((-1,2.5,0))
                    six_tex.set_color_by_tex("6", YELLOW)
                    six_arrow = Arrow(
                        start=six_tex.get_bottom(), 
                        end=displayed_tree[2].get_left(), 
                        max_tip_length_to_length_ratio=0.1, 
                        max_stroke_width_to_length_ratio=2.5
                    )
                    six_group = VGroup(six_arrow, six_tex)

                    self.play(
                        ShowPassingFlash(displayed_tree.edges[(parent_node, current_node)].copy().reverse_direction().set_stroke(width=5,color=YELLOW)),
                        ReplacementTransform(displayed_best_so_far.copy(), dot_group)
                    )
                    self.wait(3.9)
                    self.play(
                        Write(six_group),
                        displayed_tree.edges[(1,2)].animate.set_color(YELLOW),
                        displayed_tree.edges[(1,3)].animate.set_color(YELLOW),
                        displayed_tree.edges[(3,4)].animate.set_color(YELLOW),
                        displayed_tree.edges[(4,6)].animate.set_color(YELLOW),
                        displayed_tree.edges[(6,9)].animate.set_color(YELLOW),
                        displayed_tree[9][1].animate.set_color(YELLOW),
                        run_time=1.5
                    )
                    self.wait(4.2)
                    self.wait(6.7)
                    self.play(
                        Unwrite(six_group), 
                        dot_group.animate.set_color(BLUE), 
                        displayed_tree.edges[(1,2)].animate.set_color(WHITE),
                        displayed_tree.edges[(1,3)].animate.set_color(WHITE),
                        displayed_tree.edges[(3,4)].animate.set_color(WHITE),
                        displayed_tree.edges[(4,6)].animate.set_color(WHITE),
                        displayed_tree.edges[(6,9)].animate.set_color(WHITE),
                        displayed_tree[9][1].animate.set_color(WHITE),
                        run_time=1.5
                    )
                    self.wait(0.5)
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
                    global_crosses_list.append(Cross(scale_factor=RADIUS-0.1).move_to(displayed_tree.edges[(current_node, children_node)]))
                    self.play(Create(global_crosses_list[-1]))
                    children_node += 1
                            
            AnimateReturnAlphaBeta(parent_node, current_node, best_so_far, displayed_best_so_far, exact)

            return best_so_far
                
        internal_tree = Tree(type="ab")
        displayed_tree = Graph([i for i in range(1, internal_tree.size)],
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
        self.wait(5)


        self.next_section("ab_properties", skip_animations=True)

        fail_high_text = Tex("Fail high", font_size=24, color=BLUE)
        fail_low_text = Tex("Fail low", font_size=24, color=RED)
        exact_text = Tex("Exact", font_size=24, color=GREEN)
        not_searched_text = Tex("Not searched", font_size=24)
        question_marks = []

        window_tracker = ValueTracker(2)
        exact_window = always_redraw(lambda: Rectangle(height=window_tracker.get_value()*2, width=3, stroke_width=1, color=GREEN_E, fill_opacity=0.3))
        non_exact_windows = always_redraw(
            lambda: VGroup(
                Rectangle(height=4-window_tracker.get_value(), width=3, stroke_width=1, color=RED, fill_opacity=0.2).shift(UP*(2+(window_tracker.get_value())/2)),Rectangle(height=4-window_tracker.get_value(), width=3, stroke_width=1, color=RED, fill_opacity=0.2).shift(DOWN*(2+(window_tracker.get_value())/2))
                )
            ),
        alpha_tex = always_redraw(lambda: MathTex(r"\alpha", color=RED).next_to(exact_window,LEFT).shift(DOWN*window_tracker.get_value()))
        beta_tex = always_redraw(lambda: MathTex(r"\beta", color=BLUE).next_to(exact_window,LEFT).shift(UP*window_tracker.get_value()))
        dot = Dot()
        def dot_updater(mobj):
            if -window_tracker.get_value() <= mobj.get_center()[1] < window_tracker.get_value():
                mobj.set_color(GREEN)
            else:
                mobj.set_color(RED)
        dot.add_updater(dot_updater)
        score_dots = VGroup(
            dot.copy().move_to((0, dot_y, 0)).set_color(GREEN if -2 < dot_y < 2 else RED) 
            for dot_y in [0, -1, -0.5, -1.2, 3, 3.8, 1.5, -2.5, -1.8, 2.1, -1.9, 1.2, 0.5, 0.8, -2.8, -3.8, -3, 1]
        )

        self.wait(3.4)
        self.play(*[Circumscribe(displayed_tree[i], fade_out=True) for i in [9,13,17]], run_time=1.5)
        self.wait(1.2)
        self.play(*[Indicate(global_crosses_list[i], fade_out=True) for i in [0,1,2]], run_time=1.5)
        self.wait(1.1)
        self.wait(9.3)
        for node in range(9,18):
            displayed_tree[node][1].save_state()
            question_marks.append(Tex("?").move_to(displayed_tree[node][1]))
        self.play(*[Transform(displayed_tree[node][1], question_marks[node-9]) for node in range(9,18)])    
        self.wait(3.5)
        self.wait(2.9)
        for node in range(9,18):
            displayed_tree[node][1].restore().set_opacity(0.5)
        self.play(*[Write(displayed_tree[node][1]) for node in range(9,18)], *[question_marks[node].animate.set_opacity(0.75) for node in range(9)])
        self.wait(3.2)
        self.play(*[Restore(displayed_tree[node][1]) for node in range(9,18)], *[Uncreate(question_marks[node]) for node in range(9)])
        self.wait(1.3)
        self.play(
            Write(fail_high_text.copy().next_to(displayed_tree[7], UP).shift(LEFT*0.5)), 
            Write(fail_high_text.copy().next_to(displayed_tree[3], UP).shift(RIGHT*0.2)), 
            *[Write(fail_high_text.copy().next_to(displayed_tree[i], UP)) for i in [6,8]], 
            Write(fail_low_text.copy().next_to(displayed_tree[4], UP)),
            *[Write(fail_low_text.copy().next_to(displayed_tree[i], DOWN)) for i in [9,13,17]], 
            *[Write(exact_text.copy().next_to(displayed_tree[i], UP)) for i in [1,2]],
            *[Write(exact_text.copy().next_to(displayed_tree[i], DOWN)) for i in [12,15,16]], 
            Write(not_searched_text.copy().next_to(displayed_tree[5], DOWN).shift(LEFT*0.1)),
            *[Write(not_searched_text.copy().next_to(displayed_tree[i], DOWN)) for i in [10,11,14]], 
            run_time=3
        )
        self.wait(15.2)
        self.clear()
        self.play(
            DrawBorderThenFill(exact_window), 
            DrawBorderThenFill(non_exact_windows[0]), 
            Write(alpha_tex), 
            Write(beta_tex),
            Create(score_dots),
            window_tracker.animate.set_value(2)
        )
        self.play(window_tracker.animate.set_value(1), run_time=2.5)
        self.wait(3.25)
        
        true_score = VGroup(Dot(color=YELLOW).move_to([0, 0.8, 0]), Tex("True score", color=YELLOW, font_size=24).next_to(Dot(), UP*0.25))
        ab_displayed_tree = FillTree(Tree(type="asp"), is_minimax=False, alphabeta=True)
        exact_asp_ab_displayed_tree = FillTree(Tree(type="asp"), is_minimax=False, alphabeta=True, alpha=-2, beta=3)
        non_exact_asp_ab_displayed_tree = FillTree(Tree(type="asp"), is_minimax=False, alphabeta=True, alpha=-8, beta=-7)
        
        self.clear()
        self.play(Write(ab_displayed_tree), run_time=1.2)
        self.wait(8.3)
        self.play(ReplacementTransform(ab_displayed_tree, exact_asp_ab_displayed_tree), run_time=1.5)
        self.wait(2.8)
        self.wait(6.6)
        self.play(
            ReplacementTransform(exact_asp_ab_displayed_tree[0][3][1], Dot(radius=0).move_to(exact_asp_ab_displayed_tree[0][3])), 
            ReplacementTransform(exact_asp_ab_displayed_tree[1], non_exact_asp_ab_displayed_tree[1]),
            run_time=1.5
        )
        self.wait(8.4)
        self.clear()
        window_tracker.set_value(2)
        exact_window.update(1/self.camera.frame_rate)
        non_exact_windows[0].update(1/self.camera.frame_rate)
        alpha_tex.update(1/self.camera.frame_rate)
        beta_tex.update(1/self.camera.frame_rate)
        score_dots.update(1/self.camera.frame_rate)
        self.play(
            DrawBorderThenFill(exact_window), 
            DrawBorderThenFill(non_exact_windows[0]), 
            Write(alpha_tex), 
            Write(beta_tex),
            Create(score_dots),
            Create(true_score)
        )
        self.play(window_tracker.animate.set_value(1), run_time=2.5)
        self.wait(3.1)


class PVS(Scene):
    def construct(self):
        self.next_section("section_1", skip_animations=False)
        alpha_value = ValueTracker(-1)
        beta_value = ValueTracker(1)
        right_shift = ValueTracker(0)

        exact_window = always_redraw(
            lambda: Rectangle(
                height=(beta_value.get_value()-alpha_value.get_value()),
                width=3, 
                stroke_width=1, 
                color=GREEN_E, 
                fill_opacity=0.3
            ).shift(RIGHT*right_shift.get_value()+UP*(beta_value.get_value()+alpha_value.get_value())/2)
        )
        non_exact_windows = always_redraw(
            lambda: VGroup(
                Rectangle(
                    height=4-beta_value.get_value(), 
                    width=3, 
                    stroke_width=1, 
                    color=RED, 
                    fill_opacity=0.2
                ).shift(UP*(2+(beta_value.get_value())/2)+RIGHT*right_shift.get_value()),
                Rectangle(
                    height=4+alpha_value.get_value(), 
                    width=3, 
                    stroke_width=1, 
                    color=RED, 
                    fill_opacity=0.2
                ).shift(UP*(-2+(alpha_value.get_value())/2)+RIGHT*right_shift.get_value())
            )
        ),
        alpha_tex = always_redraw(lambda: MathTex(r"\alpha", color=RED).next_to(exact_window, DL))
        beta_tex = always_redraw(lambda: MathTex(r"\beta", color=BLUE).next_to(exact_window, UL))
        dot = Dot()
        def dot_updater(mobj):
            if alpha_value.get_value() <= mobj.get_center()[1] < beta_value.get_value():
                mobj.set_color(GREEN)
            else:
                mobj.set_color(RED)
        dot.add_updater(dot_updater)      
        score_dots = VGroup(
            dot.copy().move_to((0, dot_y, 0))
            for dot_y in [-3.8, -3, -2.8, -2.5, -1.9, -1.8, -1.2, -1, -0.5, 0, 0.5, 1, 1.2, 1.5, 2.1, 3, 3.8]
        )
        
        ab_window = VGroup(exact_window, non_exact_windows[0], alpha_tex, beta_tex)

        score_dots.update(1/self.camera.frame_rate)
        true_score = VGroup(Dot(color=YELLOW).move_to([0,0.8,0]), Tex("True score", color=YELLOW, font_size=24).next_to(Dot(), UP*0.25))
        question_mark = Tex("?", color=YELLOW)
        moving_exact_dot_tracker = ValueTracker(-1)
        moving_exact_dot = always_redraw(lambda: Dot(color=YELLOW, fill_opacity=0.5).move_to([0,moving_exact_dot_tracker.get_value(),0]))
        principal_variation_search_text = Tex("Principal Variation Search", substrings_to_isolate=("P","V","S",))
        pvs_text = Tex("PVS", substrings_to_isolate=("P","V","S",))

        self.add(exact_window, non_exact_windows[0], alpha_tex, beta_tex, score_dots, true_score)
        self.wait(3.2)
        self.play(Wiggle(true_score))
        self.wait(3.9)
        self.play(LaggedStart(*[Indicate(score_dots[i]) for i in range(7,11)], Indicate(true_score), lag_ratio=0.3, run_time=2))
        self.wait(1.4)
        self.wait(4.5)
        exact_dots = VGroup(score_dots[7:11], true_score)

        self.play(ReplacementTransform(exact_dots, question_mark), run_time=2)
        self.wait()
        self.play(ReplacementTransform(question_mark, moving_exact_dot), run_time=1.8)
        self.wait(0.8)
        self.play(moving_exact_dot_tracker.animate.set_value(0.8), run_time=2)
        self.remove(moving_exact_dot)
        self.play(ReplacementTransform(Group(*self.mobjects[:-7]), principal_variation_search_text), run_time=1.6)
        self.wait(0.3)
        self.play(ReplacementTransform(principal_variation_search_text, pvs_text), run_time=0.9)
        self.wait()
        self.play(Unwrite(pvs_text), run_time=0.5)

        # self.play(*[Unwrite(submobject) for submobject in self.mobjects[:-2]])
        # ab_question = Tex(r"What is the highest score in our $\alpha\beta$ window?")
        # ab_question[0][26].set_color(RED)
        # ab_question[0][27].set_color(BLUE)
        # pvs_question = Tex(r"Are there any exact scores which beat $\alpha$?")
        # pvs_question[0][-2].set_color(RED)
        # self.play(Write(ab_question), run_time=4.9)
        # self.wait(4.5)
        # self.play(ReplacementTransform(ab_question, pvs_question), run_time=1.9)
        # self.wait()
        # yes_answer = Tex("Return as true score").move_to([-3.5,-2,0])
        # yes_arrow = Arrow(start=pvs_question.get_bottom()+[0,2,0], end=[-4,-1,0])
        # yes = Tex("Yes").next_to(yes_arrow, LEFT)
        # no_answer = Tex(r"What is the highest score\\in our $\alpha\beta$ window?").move_to([3.5,-2,0])
        # no_answer[0][26].set_color(RED)
        # no_answer[0][27].set_color(BLUE)
        # no_arrow = Arrow(start=pvs_question.get_bottom()+[0,2,0], end=[4,-1,0])
        # no = Tex("No").next_to(no_arrow, RIGHT)
        # self.play(
        #     Succession(
        #         pvs_question.animate.shift(UP*2), 
        #         AnimationGroup(Write(yes_arrow), Write(no_arrow)), 
        #         AnimationGroup(Write(yes), Write(no)), 
        #         lag_ratio=0.75
        #     ),
        #     run_time=1.5
        # )
        # self.wait(0.3)
        # self.play(Write(yes_answer),  Write(no_answer), run_time=2.9)
        # principal_variation_search_text = Tex("Principal Variation Search", substrings_to_isolate=("P","V","S",)).to_edge(UP)
        # pvs_text = Tex("PVS", substrings_to_isolate=("P","V","S",)).to_edge(UP)
        # self.wait(1)
        # self.play(Write(principal_variation_search_text), run_time=1.6)
        # self.wait(0.3)
        # self.play(ReplacementTransform(principal_variation_search_text, pvs_text), run_time=0.9)
        # self.wait(1.5)

        self.next_section("section_2", skip_animations=False)

        pvs_code = '''def Negamax(depth, current_node, side_to_move, alpha, beta):
    if depth == 0:
        return GetScore(current_node) * side_to_move

    best_so_far = -math.inf
    for child_node in current_node:
        if child_node == current_node[0]:
            score = -Negamax(depth - 1, child_node, -side_to_move, -beta, -alpha)
        else:
            score = -Negamax(depth - 1, child_node, -side_to_move, -alpha-0.01, -alpha)
            if alpha < score <= beta:
                score = -Negamax(depth - 1, child_node, -side_to_move, -beta, -alpha)
        
        best_so_far = max(score, best_so_far)
                
        if best_so_far > alpha:
            alpha = best_so_far

        if best_so_far >= beta:
            break
        
    return best_so_far'''
        
        rendered_pvs_code = Code(
            code_string=pvs_code,
            language="python",
            add_line_numbers=False,
            background="window",
            paragraph_config={"width": 10, "height": 6}
        ).scale(0.5).shift(LEFT*3.5)

        right_shift.set_value(3.5)
        alpha_value.set_value(-1.5)
        beta_value.set_value(1.5)

        ab_window.update(1/self.camera.frame_rate)

        pvs_dots = VGroup(
            *[dot.copy().move_to((3.5, dot_y, 0))
            for dot_y in [0, -1.5, -3]],
            Dot(color=YELLOW).move_to([3.5, 2.5, 0])
        )
        pvs_dots.update(1/self.camera.frame_rate)

        graph = Graph([1,2,3,4,5,6,7,8,9,10,11,12,13,14],
                {(1,2), (1,3), (1,4), (2,5), (2,6), (2,7), (3,8), (3,9), (3,10), (3,11), (4,12) ,(4,13), (4,14)},
                layout="tree",
                layout_config={"root_vertex":1},
                layout_scale=(3,3),
                labels=False
            )
        labeleddot = LabeledDot(stroke_width=2, stroke_color=WHITE, radius=0.35, color=BLACK, fill_opacity=1, label="")
        displayed_tree_template = VGroup(
            graph, 
            labeleddot.copy().move_to(graph.vertices[1]), 
            labeleddot.copy().move_to(graph.vertices[2]), 
            labeleddot.copy().move_to(graph.vertices[3]), 
            labeleddot.copy().move_to(graph.vertices[4])
        ).shift(RIGHT*3.5)

        full_window_template = Rectangle(width=0.35, height=0.6, stroke_width=1, fill_opacity=0.5).set_color(GREEN).next_to(graph.vertices[3], LEFT*1.5).shift(UP*0.1)
        parent_window_template = Rectangle(width=0.35, height=0.25, stroke_width=1, fill_opacity=0.5).set_color(GREEN).next_to(graph.vertices[1], LEFT*1.5).shift(UP*0.25/2)
        null_window = Rectangle(width=0.35, height=0.01, stroke_width=1, fill_opacity=0.5).set_color(GREEN)
        null_windows_template = VGroup(null_window.copy().next_to(graph.vertices[4], LEFT*1.5), null_window.copy().next_to(graph.vertices[2], LEFT*1.5)) 

        alpha = Tex(r"$\alpha$?").next_to(graph.vertices[1], UP*1.5)
        alpha[0][0].set_color(RED)

        displayed_tree = displayed_tree_template.copy()
        full_window = full_window_template.copy()
        parent_window = full_window.copy().next_to(graph.vertices[1], LEFT*1.5).shift(DOWN*0.1/2)


        self.play(
            Succession(
                Create(Line(start=[0,5,0], end=[0,-5,0])), 
                AnimationGroup(Write(rendered_pvs_code), Write(displayed_tree), DrawBorderThenFill(parent_window)),
                lag_ratio=0.75
            )
        )
        self.wait(0.5)
        self.play(
            ShowPassingFlash(graph.edges[(1,3)].copy().set_stroke(width=5, color=YELLOW)), 
            DrawBorderThenFill(full_window), 
            *[Indicate(rendered_pvs_code.code_lines[i]) for i in [6,7]], 
            run_time=2
        )
        self.wait(2.5)
        self.play(Write(alpha), run_time=1.4)
        self.wait(0.5)

        self.play(FadeOut(displayed_tree), FadeOut(alpha), FadeOut(parent_window), ReplacementTransform(full_window, ab_window), run_time=1.3)
        self.play(Write(pvs_dots[0]), alpha_value.animate.set_value(0), run_time=1.6)
        self.play(Succession(*[Write(pvs_dots[i]) for i in range(1,3)]), lag_ratio=0.75)
        self.wait(0.7)
        self.play(Write(pvs_dots[3], run_time=0.7))
        self.wait(1.6)
        self.play(Unwrite(pvs_dots[3], run_time=0.7))
        self.wait()

        self.remove(*[pvs_dot for pvs_dot in pvs_dots])
        displayed_tree = displayed_tree_template.copy()
        full_window = full_window_template.copy()
        parent_window = parent_window_template.copy()
        null_windows = null_windows_template.copy()
        self.play(FadeIn(displayed_tree), FadeIn(full_window), ReplacementTransform(ab_window, parent_window), run_time=1.7)
        self.wait(0.7)
        self.play(*[ReplacementTransform(parent_window.copy(), window) for window in null_windows], run_time=1.2)
        self.wait(0.2)
        self.play(Indicate(rendered_pvs_code.code_lines[9][67:78]), run_time=1.2)
        self.wait(1.3)
        self.play(Indicate(rendered_pvs_code.code_lines[9][80:86]), run_time=1.2)
        self.wait(7.6)

        self.next_section("section_3", skip_animations=False)
        null_dots_1 = VGroup(Dot(color=RED, radius=0.04).move_to([null_windows[0].get_center()]).shift([0,dot_y,0]) for dot_y in [-0.1, 0.3])
        null_dots_2 = VGroup(Dot(color=RED, radius=0.04).move_to([null_windows[1].get_center()]).shift([0,dot_y,0]) for dot_y in [-0.35, -0.3, -0.2])
        parent_dot_bottom = Dot(color=RED, radius=0.04).move_to(parent_window).shift(DOWN*0.3)
        parent_dot_top = Dot(color=RED, radius=0.04).move_to(parent_window).shift(UP*0.2)
        bound_score_bottom = VGroup(parent_dot_bottom, Arrow(start=parent_dot_bottom.get_center(), end=parent_dot_bottom.get_center()+[0,-0.25,0], color=RED))
        bound_score_top = VGroup(parent_dot_top, Arrow(start=parent_dot_top.get_center(), end=parent_dot_top.get_center()+[0,0.25,0], color=RED))
        window_bound_score_bottom = VGroup(Dot(color=RED), Arrow(start=[0,0,0], end=[0,-1,0], buff=0, color=RED)).move_to([3.5, -3, 0])
        window_bound_score_top = VGroup(Dot(color=RED), Arrow(start=[0,0,0], end=[0,1,0], buff=0, color=RED)).move_to([3.5, 2.5, 0])

        self.play(Write(null_dots_1))
        self.wait()
        self.play(
            ShowPassingFlash(graph.edges[(1,4)].copy().reverse_direction().set_stroke(width=5, color=YELLOW)),
            ReplacementTransform(null_dots_1[-1].copy(), parent_dot_bottom)
        )
        self.play(Write(null_dots_2))
        self.wait()
        self.play(
            ShowPassingFlash(graph.edges[(1,2)].copy().reverse_direction().set_stroke(width=5, color=YELLOW)),
            ReplacementTransform(null_dots_2[-1].copy(), parent_dot_top)
        )
        self.wait(1.4)
        self.wait(0.7)
        self.play(ReplacementTransform(parent_dot_bottom, bound_score_bottom), ReplacementTransform(parent_dot_top, bound_score_top))
        self.wait(2.3)


        self.play(
            FadeOut(displayed_tree), 
            FadeOut(full_window), 
            FadeOut(null_windows), 
            FadeOut(null_dots_1), 
            FadeOut(null_dots_2),
            ReplacementTransform(parent_window, ab_window),
            ReplacementTransform(bound_score_bottom, window_bound_score_bottom),
            ReplacementTransform(bound_score_top, window_bound_score_top),
            run_time=1.3
        )
        self.wait(1.5)
        self.play(Indicate(window_bound_score_bottom), Indicate(window_bound_score_top), run_time=2.1)
        self.wait(3.7)

        self.next_section("section_4", skip_animations=False)
        self.wait(1.8)
        self.play(window_bound_score_top.animate.shift(DOWN).set_color(GREEN), run_time=1.4)
        self.wait()
        self.play(Indicate(rendered_pvs_code.code_lines[10:12]), run_time=1.7)
        self.play(
            Circumscribe(rendered_pvs_code.code_lines[11][71:85]), 
            Unwrite(window_bound_score_bottom), 
            Unwrite(window_bound_score_top), 
            alpha_value.animate.set_value(-1.5),
            beta_value.animate.set_value(1.5),
            run_time=1.3
        )
        dots = [Dot(color=GREEN if -1.5 <= dot_y < 1.5 else RED).move_to([3.5, dot_y, 0]) for dot_y in [-2.5, 1, -0.6, 0.2, -2, -3, -3.4, -2.3, -1.5, 0.8, -1, 0, -0.8]]
        self.wait()
        self.play(Succession(*[Write(dot) for dot in dots], run_time=12.5))
        self.wait(0.5)
        self.play(Flash(dots[1]))
        self.wait(0.8)





# with tempconfig({"quality": "medium_quality", "disable_caching": True}):
#     scene = AnimateTree()
#     scene.render()
