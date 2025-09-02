from manim import *
import numpy as np
import random as Rand
import math
from collections import deque

def NumToStr(num):
    if num == 10:
        return r"\infty"
    elif num == -10:
        return r"-\infty"
    else:
        return str(num)
    
def GenerateTree(avgBranchingFactor, max_depth, fixed_depth: bool):
    edges_list = []
    edges_dict = {}
    children = []
    node_counter = 2  # 1 is the root 1 is current node
    queue = deque()
    queue.append((1, 1))  # (nodeID, currentDepth)

    #Generate edges
    while queue:
        parentID, depth = queue.popleft()

        if depth >= max_depth:
            continue

        branchingFactor = np.random.poisson(avgBranchingFactor)

        if fixed_depth:
            while (branchingFactor == 0):
                branchingFactor = np.random.poisson(avgBranchingFactor)

        elif not fixed_depth:
            while (branchingFactor == 1):
                branchingFactor = np.random.poisson(avgBranchingFactor)

        for _ in range(branchingFactor):
            childID = node_counter
            node_counter += 1
            if parentID in edges_dict:
                children.append(childID)
            else:
                children = [childID]
            edges_dict[parentID] = children
            edges_list.append((parentID, childID))
            queue.append((childID, depth + 1))

    for edge in edges_dict:
        edges_dict[edge] = tuple(edges_dict[edge])

    #Generate labels
    labels = {}
    scores = {}
    if len(list(edges_dict.keys())) == 0:
        return edges_list, edges_dict, {1: MathTex("")}, {1: None}
    max_node = edges_dict[list(edges_dict.keys())[-1]][-1]
    for nodeID in range(1, max_node+1):
        if nodeID in edges_dict: #parent node
            labels[nodeID] = MathTex("").flip(axis=UP)
            scores[nodeID] = None
        else: #child node
            score = Rand.randint(-9, 9)
            labels[nodeID] = MathTex(f"{score}").flip(axis=UP)
            scores[nodeID] = score

    return edges_list, edges_dict, labels, scores

class Tree:
    edges_list = [] 
    edges_dict = {}
    labels = {}
    scores = {}
    size = 0

    def __init__(self, type="ab"):
        match type:
            case "minimax":
                self.edges_list=[(1,2),(1,3),(2,4),(2,5),(3,6),(3,7)]
                self.edges_dict = {1: (2, 3), 2: (4, 5), 3: (6, 7)}
                self.labels = {1:MathTex('').flip(axis=UP),2:MathTex('').flip(axis=UP),3:MathTex('').flip(axis=UP),4:MathTex('6').flip(axis=UP),5:MathTex('-4').flip(axis=UP),6:MathTex('7').flip(axis=UP),7:MathTex('2').flip(axis=UP),}
                self.scores = {1: None, 2: None, 3: None, 4: 6, 5: -4, 6: 7, 7: 2}
                self.size = 8
            case "ab":
                self.edges_list = [(1, 2), (1, 3), (3, 4), (3, 5), (4, 6), (4, 7), (4, 8), (6, 9), (6, 10), (6, 11), (7, 12), (7, 13), (7, 14), (8, 15), (8, 16), (8, 17)] 
                self.edges_dict = {1: (2, 3), 3: (4, 5), 4: (6, 7, 8), 6: (9, 10, 11), 7: (12, 13, 14), 8: (15, 16, 17)}
                self.labels = {1:MathTex('').flip(axis=UP),2:MathTex('-6').flip(axis=UP),3:MathTex('').flip(axis=UP),4:MathTex('').flip(axis=UP),5:MathTex('3').flip(axis=UP),6:MathTex('').flip(axis=UP),7:MathTex('').flip(axis=UP),8:MathTex('').flip(axis=UP),9:MathTex('-4').flip(axis=UP),10:MathTex('9').flip(axis=UP),11:MathTex('7').flip(axis=UP),12:MathTex('7').flip(axis=UP),13:MathTex('-4').flip(axis=UP),14:MathTex('9').flip(axis=UP),15:MathTex('9').flip(axis=UP),16:MathTex('7').flip(axis=UP),17:MathTex('-4').flip(axis=UP),}
                self.scores = {1: None, 2: -6, 3: None, 4: None, 5: 3, 6: None, 7: None, 8: None, 9: -4, 10: 9, 11: 7, 12: 7, 13: -4, 14: 9, 15: 9, 16: 7, 17: -4}
                self.size = 18
            case "asp":
                self.edges_list = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (4, 9), (8, 10), (8, 11), (8, 12), (8, 13), (8, 14), (9, 15), (9, 16), (9, 17)] 
                self.edges_dict = {1: (2, 3), 2: (4, 5), 3: (6, 7), 4: (8, 9), 8: (10, 11, 12, 13, 14), 9: (15, 16, 17)}
                self.labels = {1: MathTex('').flip(axis=UP), 2: MathTex('').flip(axis=UP), 3: MathTex('').flip(axis=UP), 4: MathTex('').flip(axis=UP), 5: MathTex('-1').flip(axis=UP), 6: MathTex('6').flip(axis=UP), 7: MathTex('2').flip(axis=UP), 8: MathTex('').flip(axis=UP), 9: MathTex('').flip(axis=UP), 10: MathTex('3').flip(axis=UP), 11: MathTex('4').flip(axis=UP), 12: MathTex('-9').flip(axis=UP), 13: MathTex('7').flip(axis=UP), 14: MathTex('2').flip(axis=UP), 15: MathTex('-6').flip(axis=UP), 16: MathTex('6').flip(axis=UP), 17: MathTex('7').flip(axis=UP),}
                self.scores = {1: None, 2: None, 3: None, 4: None, 5: -1, 6: 6, 7: 2, 8: None, 9: None, 10: 3, 11: 4, 12: -9, 13: 7, 14: 2, 15: -6, 16: 6, 17: 7}
                self.size = 18

    def RandomTree(self, avg_branching_factor, max_depth, fixed_depth=False):
        num_leaves = 0
        leaf_offset = max(0, max_depth - 4)
        if fixed_depth:
            leaf_offset = 0
        while num_leaves < (8 + leaf_offset) or num_leaves > (10 + leaf_offset):
            num_leaves = 0
            self.edges_list, self.edges_dict, self.labels, self.scores = GenerateTree(avg_branching_factor, max_depth, fixed_depth)
            for node in self.scores:
                if self.scores[node] is not None:
                    num_leaves += 1
        self.size = len(self.edges_list) + 2

    def __str__(self):
        label_string = ""
        open_brace = "{"
        close_brace = "}"
        for label in self.labels:
            label_string += str(label) + ":" + str(self.labels[label]) + ","
        return f"edges_list = {self.edges_list} \nedges_dict = {self.edges_dict} \nlabels = {open_brace}{label_string}{close_brace} \nscores = {self.scores} \nsize = {self.size}"

def GetMinimaxTree(tree: Tree, side_to_move=1, current_node=1):
    minimax_tree = tree
    if current_node not in minimax_tree.edges_dict: #checks if current_node is a leaf
        minimax_tree.scores[current_node] *= side_to_move
        return minimax_tree
    
    for children_node in minimax_tree.edges_dict[current_node]:
        GetMinimaxTree(minimax_tree, side_to_move*-1, children_node)
    
    max_node = minimax_tree.edges_dict[list(minimax_tree.edges_dict.keys())[-1]][-1]
    for nodeID in range(1, max_node+1):
        if nodeID in minimax_tree.edges_dict: #parent node
            pass
        else:
            minimax_tree.labels[nodeID] = MathTex(f"{minimax_tree.scores[nodeID]}").flip(axis=UP)
    return minimax_tree

def FillTree(tree: Tree, is_minimax=False, alphabeta=False, PVS=False, side_to_move=1, current_node=1, alpha=-10, beta=10):
    RADIUS = 0.35
    VERTEX_CONFIG = {"stroke_width": 2, "stroke_color": WHITE, "radius": RADIUS, "color":BLACK, "fill_opacity": 1}
    LAYOUT_SCALE = (6, 3.5)

    if is_minimax and not alphabeta:
        def Minimax(internal_tree: Tree, current_node: int, is_maximiser: bool):

            if current_node not in internal_tree.edges_dict: #checks if current_node is a leaf
                internal_tree.labels[current_node] = MathTex(f"{internal_tree.scores[current_node]}").flip(axis=UP)
                return internal_tree.scores[current_node]

            if is_maximiser:
                best_so_far = -10
                for children_node in internal_tree.edges_dict[current_node]:
                    best_so_far = max(best_so_far, Minimax(internal_tree, children_node, False))
                    internal_tree.scores[current_node] = best_so_far
                    internal_tree.labels[current_node] = MathTex(f"{best_so_far}").flip(axis=UP)
            else:
                best_so_far = 10
                for children_node in internal_tree.edges_dict[current_node]:
                    best_so_far = min(best_so_far, Minimax(internal_tree, children_node, True))
                    internal_tree.scores[current_node] = best_so_far
                    internal_tree.labels[current_node] = MathTex(f"{best_so_far}").flip(axis=UP)

            return best_so_far
        
        Minimax(tree, current_node, True)
        displayed_tree = Graph([i for i in range(1, tree.size)],
            tree.edges_list,
            layout="tree",
            layout_config={"root_vertex":1},
            layout_scale=LAYOUT_SCALE,
            vertex_config=VERTEX_CONFIG,
            labels=tree.labels
        ).flip(axis=UP).move_to(RIGHT*0.5)
        return displayed_tree

    elif not is_minimax and not alphabeta:
        def Negamax(internal_tree: Tree, current_node: int, side_to_move: int):

            if current_node not in internal_tree.edges_dict: #checks if current_node is a leaf
                return internal_tree.scores[current_node] 

            best_so_far = -10
            for children_node in internal_tree.edges_dict[current_node]:
                best_so_far = max(best_so_far, -Negamax(internal_tree, children_node, -side_to_move))
                internal_tree.scores[current_node] = best_so_far
                internal_tree.labels[current_node] = MathTex(f"{best_so_far}").flip(axis=UP)

            return best_so_far
        
        Negamax(tree, current_node, side_to_move)
        displayed_tree = Graph([i for i in range(1, tree.size)],
            tree.edges_list,
            layout="tree",
            layout_config={"root_vertex":1},
            layout_scale=LAYOUT_SCALE,
            vertex_config=VERTEX_CONFIG,
            labels=tree.labels
        ).flip(axis=UP).move_to(RIGHT*0.5)
        return displayed_tree

    elif not is_minimax and alphabeta:
        windows_group = VGroup()
        crosses = VGroup()

        def MakeWindow(displayed_node, best_so_far, alpha, beta, initial=False):
            window_height = (RADIUS/10)*abs(beta-alpha)

            window = Rectangle(width=RADIUS, height=window_height, stroke_width=1, fill_opacity=0.5).set_color(
                GREEN).next_to(displayed_node, LEFT*0.5).shift((0,(RADIUS/10)*((alpha+beta)/2),0))
            
            (alpha_pos, beta_pos) = (window.get_bottom()+0.1*DOWN, window.get_top()+0.1*UP) if alpha < beta else (window.get_top()+0.1*UP, window.get_bottom()+0.1*DOWN)
            
            alpha_tex = MathTex(fr"\alpha:{NumToStr(alpha)}", substrings_to_isolate=(r"\alpha",":","-")).scale(0.35).move_to(alpha_pos)
            alpha_tex.set_color_by_tex(r"\alpha", RED)
            beta_tex = MathTex(fr"\beta:{NumToStr(beta)}", substrings_to_isolate=(r"\beta",":","-")).scale(0.35).move_to(beta_pos)
            beta_tex.set_color_by_tex(r"\beta", BLUE)

            if initial:
                return VGroup(window, alpha_tex, beta_tex)

            else:
                color = RED if best_so_far < beta else BLUE
                dot = Dot(radius=0.04, color=color).next_to(displayed_node, LEFT*0.5).shift((0,(RADIUS/10)*(best_so_far),0))
                dot.move_to((window.get_x(), dot.get_y(), 0))
                dot_tex = Tex(f"{best_so_far}", font_size=10, color=color).next_to(dot, LEFT)
                return VGroup(dot, dot_tex)

        def Negamax(internal_tree: Tree, current_node: int, side_to_move: int, alpha:int, beta:int):

            displayed_tree_for_positioning = Graph([i for i in range(1, internal_tree.size)],
                internal_tree.edges_list,
                layout="tree",
                layout_config={"root_vertex":1},
                layout_scale=LAYOUT_SCALE,
                vertex_config=VERTEX_CONFIG,
                labels={1:MathTex(''), 2:MathTex(''), 3:MathTex(''), 4:MathTex(''), 5:MathTex('-1'), 6:MathTex('6'), 7:MathTex('2'), 8:MathTex(''), 9:MathTex(''), 10:MathTex('4'), 11:MathTex('3'), 12:MathTex('-9'), 13:MathTex('7'), 14:MathTex('2'), 15:MathTex('-6'), 16:MathTex('6'), 17:MathTex('7'),}
            ).flip(axis=UP).move_to(RIGHT*0.5)
            best_so_far = -10
            displayed_node = displayed_tree_for_positioning[current_node]
            beta_cutoff = False

            windows_group.add(MakeWindow(displayed_node, internal_tree.scores[current_node], alpha, beta, initial=True))
            if current_node not in internal_tree.edges_dict: #checks if current_node is a leaf
                windows_group.add(MakeWindow(displayed_node, internal_tree.scores[current_node], alpha, beta))
                best_so_far = max(best_so_far, internal_tree.scores[current_node])
                return best_so_far

            best_so_far = -10
            for children_node in internal_tree.edges_dict[current_node]:
                best_so_far = max(best_so_far, -Negamax(internal_tree, children_node, -side_to_move, -beta, -alpha))
                alpha = max(best_so_far, alpha)
                internal_tree.scores[current_node] = best_so_far
                internal_tree.labels[current_node] = MathTex(f"{best_so_far}").flip(axis=UP)
                windows_group.add(MakeWindow(displayed_node, best_so_far, alpha, beta))
                if best_so_far > beta:
                    beta_cutoff = True
                    break

            if beta_cutoff == True:
                children_node += 1
                while(children_node in internal_tree.edges_dict[current_node]):
                    windows_group.add((Cross(scale_factor=RADIUS-0.1).move_to(displayed_tree_for_positioning.edges[(current_node, children_node)])))
                    children_node += 1
                return best_so_far

            return best_so_far
        
        # if alpha == -10 and beta == 10:
        Negamax(tree, current_node=current_node, side_to_move=side_to_move, alpha=alpha, beta=beta)
        # else:
        #     while True:
        #         asp_tree = tree
        #         score = Negamax(tree, current_node=current_node, side_to_move=side_to_move, alpha=alpha, beta=beta)
        #         if score <= alpha:
        #             alpha -= 1
        #         elif score > beta:
        #             beta += 1
        #         else:
        #             windows_group = VGroup(Circle(color=BLACK, fill_opacity=1).set_z_index(-100))
        #             Negamax(asp_tree, current_node=current_node, side_to_move=side_to_move, alpha=alpha, beta=beta)
        #             displayed_tree = Graph([i for i in range(1, tree.size)],
        #                 tree.edges_list,
        #                 layout="tree",
        #                 layout_config={"root_vertex":1},
        #                 layout_scale=LAYOUT_SCALE,
        #                 vertex_config=VERTEX_CONFIG,
        #                 labels=tree.labels
        #             ).flip(axis=UP).move_to(RIGHT*0.5)

        #            return VGroup(displayed_tree, windows_group)
            
        displayed_tree = Graph([i for i in range(1, tree.size)],
                tree.edges_list,
                layout="tree",
                layout_config={"root_vertex":1},
                layout_scale=LAYOUT_SCALE,
                vertex_config=VERTEX_CONFIG,
                labels=tree.labels
            ).flip(axis=UP).move_to(RIGHT*0.5)

        return VGroup(displayed_tree, windows_group)



#Perfect move ordering (beta cutoff demo)
    # edges_list = [(1, 2), (1, 3), (3, 4), (3, 5), (4, 6), (4, 7), (5, 8), (5, 9), (6, 10), (6, 11), (7, 12), (7, 13), (7, 14), (9, 15), (9, 16)] 
    # edges_dict = {1: (2, 3), 3: (4, 5), 4: (6, 7), 5: (8, 9), 6: (10, 11), 7: (12, 13, 14), 9: (15, 16)}
    # labels = {1:MathTex('').flip(axis=UP),2:MathTex('0').flip(axis=UP),3:MathTex('').flip(axis=UP),4:MathTex('').flip(axis=UP),5:MathTex('').flip(axis=UP),6:MathTex('').flip(axis=UP),7:MathTex('').flip(axis=UP),8:MathTex('8').flip(axis=UP),9:MathTex('').flip(axis=UP),10:MathTex('-9').flip(axis=UP),11:MathTex('-4').flip(axis=UP),12:MathTex('-4').flip(axis=UP),13:MathTex('6').flip(axis=UP),14:MathTex('1').flip(axis=UP),15:MathTex('-3').flip(axis=UP),16:MathTex('-7').flip(axis=UP),}
    # scores = {1: None, 2: 0, 3: None, 4: None, 5: None, 6: None, 7: None, 8: 8, 9: None, 10: -9, 11: -4, 12: -4, 13: 6, 14: 1, 15: -3, 16: -7}
    # size = 17

#Perfect move ordering again
    # edges_list = [(1, 2), (1, 3), (3, 4), (3, 5), (4, 6), (4, 7), (4, 8), (4, 9), (6, 10), (6, 11), (6, 12), (8, 13), (8, 14), (8, 15), (9, 16), (9, 17)] 
    # edges_dict = {1: (2, 3), 3: (4, 5), 4: (6, 7, 8, 9), 6: (10, 11, 12), 8: (13, 14, 15), 9: (16, 17)}
    # labels = {1:MathTex('').flip(axis=UP),2:MathTex('-6').flip(axis=UP),3:MathTex('').flip(axis=UP),4:MathTex('').flip(axis=UP),5:MathTex('3').flip(axis=UP),6:MathTex('').flip(axis=UP),7:MathTex('0').flip(axis=UP),8:MathTex('').flip(axis=UP),9:MathTex('').flip(axis=UP),10:MathTex('-8').flip(axis=UP),11:MathTex('1').flip(axis=UP),12:MathTex('-5').flip(axis=UP),13:MathTex('-2').flip(axis=UP),14:MathTex('8').flip(axis=UP),15:MathTex('6').flip(axis=UP),16:MathTex('-1').flip(axis=UP),17:MathTex('-6').flip(axis=UP),}
    # scores = {1: None, 2: -6, 3: None, 4: None, 5: 3, 6: None, 7: 0, 8: None, 9: None, 10: -8, 11: 1, 12: -5, 13: -2, 14: 8, 15: 6, 16: -1, 17: -6}
    # size = 18


class DisplayTree(Scene):
    def construct(self):
        # while True:
        internal_tree = Tree(type="asp")
        #internal_tree.RandomTree(1.5, 5)
        ab_internal_tree = internal_tree
        exact_asp_ab_internal_tree = internal_tree
        non_exact_asp_ab_internal_tree = internal_tree

        ab_displayed_tree = FillTree(ab_internal_tree, is_minimax=False, alphabeta=True)
        exact_asp_ab_displayed_tree = FillTree(exact_asp_ab_internal_tree, is_minimax=False, alphabeta=True, alpha=-2, beta=3)
        non_exact_asp_ab_displayed_tree = FillTree(non_exact_asp_ab_internal_tree, is_minimax=False, alphabeta=True, alpha=-8, beta=-7)

        self.add(ab_displayed_tree)
        self.wait(2)
        self.play(ReplacementTransform(ab_displayed_tree, exact_asp_ab_displayed_tree))
        self.wait()
        self.play(ReplacementTransform(exact_asp_ab_displayed_tree, non_exact_asp_ab_displayed_tree))
        self.wait()
        print(internal_tree)

        # internal_tree = Tree()
        # print(internal_tree)
        # RADIUS = 0.35
        # VERTEX_CONFIG = {"stroke_width": 2, "stroke_color": WHITE, "radius": RADIUS, "color":BLACK, "fill_opacity": 1}
        # LAYOUT_SCALE = (6, 3.5)
        # displayed_tree = FillTree(internal_tree, is_minimax=False,)
        # self.add(displayed_tree)

