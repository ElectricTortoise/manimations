from manim import *
import numpy as np
import random as Rand
import math
from collections import deque

class Tree:
    edges_list = [(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7), (3, 8), (3, 9), (3, 10), (4, 11), (4, 12), (4, 13)] 
    edges_dict = {1: (2, 3, 4), 2: (5, 6), 3: (7, 8, 9, 10), 4: (11, 12, 13)}
    labels = {1: MathTex('').flip(axis=UP), 2: MathTex('').flip(axis=UP), 3: MathTex('').flip(axis=UP), 4: MathTex('').flip(axis=UP), 5: MathTex('-2').flip(axis=UP), 6: MathTex('6').flip(axis=UP), 7: MathTex('-8').flip(axis=UP), 8: MathTex('9').flip(axis=UP), 9: MathTex('-4').flip(axis=UP), 10: MathTex('7').flip(axis=UP), 11: MathTex('3').flip(axis=UP), 12: MathTex('5').flip(axis=UP), 13: MathTex('-9').flip(axis=UP)}
    scores = {1: None, 2: None, 3: None, 4: None, 5: -2, 6: 6, 7: -8, 8: 9, 9: -4, 10: 7, 11: 3, 12: 5, 13: -9}
    size = len(edges_list) + 2

    # def __init__(self, avg_branching_factor, max_depth):
    #     self.edges_list, self.edges_dict = GenerateEdges(avg_branching_factor, max_depth)
    #     self.labels, self.scores = GetLabels(self.edges_dict)
    #     self.size = len(self.edges_list) + 2

    def __str__(self):
        return f"{self.edges_list} \n{self.edges_dict} \n{self.labels} \n{self.scores}"


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
            branchingFactor = 2

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
