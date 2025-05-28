from manim import *
import numpy as np
import random as Rand
import math
from collections import deque


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
    edges_list = [(1, 2), (1, 3), (3, 4), (3, 5), (4, 6), (4, 8), (4, 9), (6, 10), (6, 11), (6, 12), (8, 13), (8, 14), (8, 15), (9, 16), (9, 17), (9, 18)] 
    edges_dict = {1: (2, 3), 3: (4, 5), 4: (6, 8, 9), 6: (10, 11, 12), 8: (13, 14, 15), 9: (16, 17, 18)}
    labels = {1:MathTex('').flip(axis=UP),2:MathTex('-6').flip(axis=UP),3:MathTex('').flip(axis=UP),4:MathTex('').flip(axis=UP),5:MathTex('3').flip(axis=UP),6:MathTex('').flip(axis=UP),8:MathTex('').flip(axis=UP),9:MathTex('').flip(axis=UP),10:MathTex('-8').flip(axis=UP),11:MathTex('1').flip(axis=UP),12:MathTex('-5').flip(axis=UP),13:MathTex('7').flip(axis=UP),14:MathTex('-2').flip(axis=UP),15:MathTex('-8').flip(axis=UP),16:MathTex('9').flip(axis=UP),17:MathTex('7').flip(axis=UP),18:MathTex('-4').flip(axis=UP),}
    scores = {1: None, 2: -6, 3: None, 4: None, 5: 3, 6: None, 8: None, 9: None, 10: -8, 11: 1, 12: -5, 13: 7, 14: -2, 15: -8, 16: 9, 17: 7, 18: -4}
    size = 19

    def __init__(self, avg_branching_factor=0, max_depth=0, fixed_depth=True):
        if avg_branching_factor == 0 or max_depth == 0:
            return
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
            label_string += str(label) + ":" + str(self.labels[label]) + ".flip(axis=UP)" + ","
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

def FillTree(tree: Tree, is_minimax=False, side_to_move=1, current_node=1):

    if is_minimax:
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

    else:
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
    RADIUS = 0.35
    VERTEX_CONFIG = {"stroke_width": 2, "stroke_color": WHITE, "radius": RADIUS, "color":BLACK, "fill_opacity": 1}
    LAYOUT_SCALE = (6, 3.5)
    
    def construct(self):
        internal_tree = Tree(2, 5, fixed_depth=False)
        print(internal_tree)
        displayed_tree = Graph([i for i in range(1, internal_tree.size)],
            internal_tree.edges_list,
            layout="tree",
            layout_config={"root_vertex":1},
            layout_scale=self.LAYOUT_SCALE,
            vertex_config=self.VERTEX_CONFIG,
            labels=internal_tree.labels
        ).flip(axis=UP).move_to(RIGHT*0.5)
        self.add(displayed_tree)
