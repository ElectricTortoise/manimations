from manim import *
import numpy as np
import random as Rand
import math
from collections import deque

class Tree:
    edges_list = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (3, 8), (4, 9), (4, 10), (5, 11), (5, 12), (6, 13), (6, 14), (7, 15), (7, 16), (8, 17), 
    (8, 18)]
    edges_dict = {1: (2, 3), 2: (4, 5), 3: (6, 7, 8), 4: (9, 10), 5: (11, 12), 6: (13, 14), 7: (15, 16), 8: (17, 18)}
    labels = {1:MathTex('').flip(axis=UP),2:MathTex('').flip(axis=UP),3:MathTex('').flip(axis=UP),4:MathTex('').flip(axis=UP),5:MathTex('').flip(axis=UP),6:MathTex('').flip(axis=UP),7:MathTex('').flip(axis=UP),8:MathTex('').flip(axis=UP),9:MathTex('8').flip(axis=UP),10:MathTex('-1').flip(axis=UP),11:MathTex('3').flip(axis=UP),12:MathTex('1').flip(axis=UP),13:MathTex('0').flip(axis=UP),14:MathTex('-8').flip(axis=UP),15:MathTex('2').flip(axis=UP),16:MathTex('6').flip(axis=UP),17:MathTex('7').flip(axis=UP),18:MathTex('8').flip(axis=UP),}
    scores = {1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None, 9: 8, 10: -1, 11: 3, 12: 1, 13: 0, 14: -8, 15: 2, 16: 6, 17: 7, 18: 8}
    size = 19

    def __init__(self, avg_branching_factor=0, max_depth=0):
        if avg_branching_factor == 0 or max_depth == 0:
            return
        num_leaves = 0
        while num_leaves < 8 or num_leaves > 10:
            num_leaves = 0
            self.edges_list, self.edges_dict = GenerateEdges(avg_branching_factor, max_depth)
            self.labels, self.scores = GetLabels(self.edges_dict)
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


def GenerateEdges(avgBranchingFactor, maxDepth):
    edges_list = []
    edges_dict = {}
    children = []
    node_counter = 2  # 1 is the root 1 is current node
    queue = deque()
    queue.append((1, 1))  # (nodeID, currentDepth)

    while queue:
        parentID, depth = queue.popleft()

        if depth >= maxDepth:
            continue

        branchingFactor = np.random.poisson(avgBranchingFactor)
        if branchingFactor <= 1:
            branchingFactor = Rand.choice((2,3))

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

    return edges_list, edges_dict

def GetLabels(edges_dict):
    labels = {}
    scores = {}
    if len(list(edges_dict.keys())) == 0:
        return {1: MathTex("")}, {1: None}
    max_node = edges_dict[list(edges_dict.keys())[-1]][-1]
    for nodeID in range(1, max_node+1):
        if nodeID in edges_dict: #parent node
            labels[nodeID] = MathTex("").flip(axis=UP)
            scores[nodeID] = None
        else: #child node
            score = Rand.randint(-9, 9)
            labels[nodeID] = MathTex(f"{score}").flip(axis=UP)
            scores[nodeID] = score
    return labels, scores


# edges_list = [(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7), (3, 8), (3, 9), (3, 10), (4, 11), (4, 12), (4, 13)] 
# edges_dict = {1: (2, 3, 4), 2: (5, 6), 3: (7, 8, 9, 10), 4: (11, 12, 13)}
# labels = {1: MathTex('').flip(axis=UP), 2: MathTex('').flip(axis=UP), 3: MathTex('').flip(axis=UP), 4: MathTex('').flip(axis=UP), 5: MathTex('-2').flip(axis=UP), 6: MathTex('6').flip(axis=UP), 7: MathTex('-8').flip(axis=UP), 8: MathTex('9').flip(axis=UP), 9: MathTex('-4').flip(axis=UP), 10: MathTex('7').flip(axis=UP), 11: MathTex('3').flip(axis=UP), 12: MathTex('5').flip(axis=UP), 13: MathTex('-9').flip(axis=UP)}
# scores = {1: None, 2: None, 3: None, 4: None, 5: -2, 6: 6, 7: -8, 8: 9, 9: -4, 10: 7, 11: 3, 12: 5, 13: -9}
# size = len(edges_list) + 2

# print(Tree(2,4))