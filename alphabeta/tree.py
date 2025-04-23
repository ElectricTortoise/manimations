from manim import *
import numpy as np
import random as Rand
from collections import deque

class Tree:
    edges_list = []
    edges_dict = {}
    labels = {}

    def __init__(self, avg_branching_factor, max_depth):
        self.edges_list, self.edges_dict = self.GenerateEdges(avg_branching_factor, max_depth)
        self.labels = self.GetLabels(self.edges_dict)

    def GenerateEdges(self, avgBranchingFactor, maxDepth):
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

            if branchingFactor == 1:
                continue

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

    def GetLabels(self, edges_dict):
        labels = {}
        if len(list(edges_dict.keys())) == 0:
            return {1: Tex("")}
        max_node = edges_dict[list(edges_dict.keys())[-1]][-1]
        for nodeID in range(1, max_node+1):
            if nodeID in edges_dict: #parent node
                labels[nodeID] = Tex("")
            else: #child node
                labels[nodeID] = Tex(f"{Rand.randint(-9, 9)}")
        return labels
            
    def __str__(self):
        return f"{self.edges_list} \n{self.edges_dict} \n{self.labels}"