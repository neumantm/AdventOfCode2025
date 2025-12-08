
from dataclasses import dataclass
from functools import reduce
from math import sqrt
from sqlite3 import connect
from turtle import right
from typing import Any, Generator, Self
from xmlrpc.client import Boolean


def remove_if_present(list: list, e: Any):
    if e in list:
        list.remove(e)


Coord = tuple[int, int, int]


def distance(c1: Coord, c2: Coord) -> float:
    return sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2 + (c1[2] - c2[2])**2)


def split_by_axis(points: list[Coord], axis: int) -> tuple[list[Coord], Coord, list[Coord]]:
    middle = len(points) // 2
    sorted_points = sorted(points, key=lambda x: x[axis])
    return (sorted_points[:middle], sorted_points[middle], sorted_points[middle + 1:])


def greater_than_by_axix(point1: Coord, point2: Coord, axis: int) -> Boolean:
    return point1[axis] > point2[axis]


# @dataclass
# class Block3:
#     min_corner: Coord # inclusive
#     max_corner: Coord # exclusive

#     is_leaf: Boolean

#     children: list[Self] | None
#     points_inside: list[Coord] | None

#     def get_points_recursive(self) -> list[Coord]:
#         if self.is_leaf:
#             return self.points_inside if self.points_inside is not None else []
#         else:
#             res: list[Coord] = []
#             for child in (self.children if self.children is not None else []):
#                 res.extend(child.get_points_recursive())
#             return res

# class BlockTree3:


# KDTree not the correct datastructure for this problem
# @dataclass
# class KDTree3Node:
#     axis: int
#     location: Coord
#     left_child: Self | None
#     right_child: Self | None
#     parent: Self | None


# class KDTree3:
#     root: KDTree3Node

#     def __init__(self, points: list[Coord]):
#         self.root = self._build_tree(points, 0)

#     def _build_tree(self, points: list[Coord], depth: int) -> KDTree3Node:
#         axis = depth % 3
#         left_points, pivot, right_points = split_by_axis(points, axis)
#         left_child = None if len(left_points) == 0 else self._build_tree(left_points, depth + 1)
#         right_child = None if len(right_points) == 0 else self._build_tree(right_points, depth + 1)
#         new_node = KDTree3Node(axis, pivot, left_child, right_child, None)
#         if left_child is not None:
#             left_child.parent = new_node
#         if right_child is not None:
#             right_child.parent = new_node
#         return new_node

#     def find_nearest_neighbour_to(self, search_point: Coord):
#         def _recurse_to_leaf(node: KDTree3Node, depth: int) -> KDTree3Node:
#             if greater_than_by_axix(search_point, node.location, node.axis):
#                 return node if node.right_child is None else _recurse_to_leaf(node.right_child, depth + 1)
#             else:
#                 return node if node.left_child is None else _recurse_to_leaf(node.left_child, depth + 1)

#         current_best_dist: float | None = None
#         current_best_node: KDTree3Node | None = None

#         node_to_check: KDTree3Node | None = _recurse_to_leaf(self.root, 0)

#         while node_to_check is not None:
#             dist = distance(node_to_check.location, search_point)
#             if node_to_check != search_point and (current_best_dist is None or dist < current_best_dist):
#                 current_best_dist = dist
#                 current_best_node = node_to_check
#             if current_best_dist > abs(node_to_check.location[node_to_check.axis] - search_point[node_to_check.axis]):
#                 pass
#             node_to_check = node_to_check.parent




class Graph:
    nodes: list[Coord]
    edges: list[tuple[Coord, Coord]]

    def __init__(self, p_nodes: list[Coord], p_edges: list[tuple[Coord, Coord]]) -> None:
        self.nodes = p_nodes
        self.edges = p_edges

    def __repr__(self) -> str:
        return f"Graph(nodes={self.nodes}, edges={self.edges})"

    def has_edge(self, c1: Coord, c2: Coord) -> Boolean:
        return (c1, c2) in self.edges or (c2, c1) in self.edges

    def get_any_edge_with(self, c1: Coord, excep: list[tuple[Coord, Coord]] = []) -> tuple[Coord, Coord] | None:
        return next((e for e in self.edges if (e[0] == c1 or e[1] == c1) and e not in excep), None)

    def get_all_edges_with(self, c1: Coord) -> list[tuple[Coord, Coord]]:
        return [e for e in self.edges if e[0] == c1 or e[1] == c1]

    # Naiiv implementation is to slow, we use kd tree
    # def find_next_shortest_edge(self) -> None:
    #     shortest_dist: float | None = None
    #     shortest_edge: tuple[Coord, Coord] | None = None

    #     for i, n1 in enumerate(self.nodes):
    #         for j, n2 in enumerate(self.nodes):
    #             if i == j:
    #                 continue
    #             if self.has_edge(n1, n2):
    #                 continue
    #             dist = distance(n1, n2)
    #             if shortest_dist is None or dist < shortest_dist:
    #                 shortest_dist = dist
    #                 shortest_edge = (n1, n2)
    #     if shortest_edge is None:
    #         raise ValueError("Did not find next shortest edge")
    #     self.edges.append(shortest_edge)

    def get_connected_subgraphs(self) -> "list[Graph]":
        remaining_nodes = self.nodes.copy()
        res: list[Graph] = []

        while len(remaining_nodes) > 0:
            print(f"Getting subgraphs: {len(remaining_nodes)} / {len(self.nodes)} remaining")
            node = remaining_nodes.pop()
            possible_edge = self.get_any_edge_with(node)
            if possible_edge is None:
                res.append(Graph([node], []))
                continue

            remove_if_present(remaining_nodes, possible_edge[0])
            remove_if_present(remaining_nodes, possible_edge[1])
            nodes_for_subgraph = set([possible_edge[0], possible_edge[1]])
            edges_for_subgraph = [possible_edge]

            while possible_edge is not None:
                possible_edge = None
                for other_node in nodes_for_subgraph:
                    possible_edge = self.get_any_edge_with(other_node, excep=edges_for_subgraph)
                    if possible_edge is not None:
                        remove_if_present(remaining_nodes, possible_edge[0])
                        remove_if_present(remaining_nodes, possible_edge[1])
                        nodes_for_subgraph.add(possible_edge[0])
                        nodes_for_subgraph.add(possible_edge[1])
                        edges_for_subgraph.append(possible_edge)
                        break
            res.append(Graph(list(nodes_for_subgraph), edges_for_subgraph))

        return res

    def is_fully_connected(self) -> Boolean:
        remaining_nodes = self.nodes.copy()
        node = remaining_nodes.pop()
        connected_nodes = set([node])
        while len(remaining_nodes) > 0:
            found_new = False
            for other_node in connected_nodes:
                possible_edges = self.get_all_edges_with(other_node)
                if len(possible_edges) > 0:
                    for possible_edge in possible_edges:
                        if possible_edge[0] not in connected_nodes:
                            remove_if_present(remaining_nodes, possible_edge[0])
                            connected_nodes.add(possible_edge[0])
                            found_new = True
                        if possible_edge[1] not in connected_nodes:
                            remove_if_present(remaining_nodes, possible_edge[1])
                            connected_nodes.add(possible_edge[1])
                            found_new = True
                if found_new:
                    break
            if not found_new:
                return False
        return True


def calc_all_possible_edges(nodes: list[Coord]) -> Generator[tuple[Coord, Coord], None, None]:
    for i, n1 in enumerate(nodes):
        for j, n2 in enumerate(nodes):
            if i >= j:
                continue
            yield (n1, n2)


def load_input() -> list[str]:
    with open("input.txt") as f:
        return f.readlines()


def load_coords(input: list[str]) -> list[Coord]:
    def load_coord_line(line: str) -> Coord:
        line_coord_list = [int(c) for c in line.split(",")]
        return (line_coord_list[0], line_coord_list[1], line_coord_list[2])
    return [load_coord_line(line) for line in input]


def main():
    SHORTEST_N_TO_FIND = 10
    input = load_input()
    coords = load_coords(input)

    all_edges = list(calc_all_possible_edges(coords))
    edges_sorted_by_length = sorted(all_edges, key=lambda e: distance(e[0], e[1]))
    shortest_n_edges = edges_sorted_by_length[:SHORTEST_N_TO_FIND]

    print(edges_sorted_by_length[27])
    print(edges_sorted_by_length[28])
    print(edges_sorted_by_length[29])

    graph = Graph(coords, shortest_n_edges)
    # for i in range(SHORTEST_N_TO_FIND):
    #     print(f"find shortest: {i}/{SHORTEST_N_TO_FIND}")
    #     graph.find_next_shortest_edge()

    subgraphs = graph.get_connected_subgraphs()
    subgraphs.sort(key=lambda x: len(x.nodes), reverse=True)
    #print(subgraphs)
    multiplied_sizes = reduce(lambda a,b: a*b, [len(x.nodes) for x in subgraphs[:3]], 1)
    print(f"{multiplied_sizes=}")

    # B

    binary_search_pivot = len(edges_sorted_by_length) // 2
    binary_search_left_end = 0
    binary_search_right_end = len(edges_sorted_by_length) - 1

    first_edge_to_completely_connect: tuple[Coord, Coord] | None = None
    while first_edge_to_completely_connect is None:
        print(f"Binary searching: {binary_search_left_end} - {binary_search_right_end} (pivot: {binary_search_pivot})")
        if Graph(coords, edges_sorted_by_length[:binary_search_pivot + 1]).is_fully_connected(): # inclusive the pivot
            binary_search_right_end = binary_search_pivot
        else:
            binary_search_left_end = binary_search_pivot + 1
        binary_search_pivot = (binary_search_left_end + binary_search_right_end) // 2
        if binary_search_left_end == binary_search_right_end:
            first_edge_to_completely_connect = edges_sorted_by_length[binary_search_left_end]

    print(f"{first_edge_to_completely_connect=}")
    print(f"Product: {first_edge_to_completely_connect[0][0] * first_edge_to_completely_connect[1][0]}")

if __name__ == "__main__":
    main()
