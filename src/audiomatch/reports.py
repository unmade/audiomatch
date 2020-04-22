from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, Tuple

CONFIDENCE_SCORE = 0.61


def console(matches: Dict[Tuple[Path, Path], float]) -> None:
    """Print similar audio to standard output"""
    similars = _join(_adjancency_list(matches))
    lines = ["\n".join(str(node) for node in similar) for similar in sorted(similars)]

    if lines:
        sys.stdout.write("These files sound similar:\n\n")
        sys.stdout.write("\n\n---\n\n".join(lines))
    else:
        sys.stdout.write("No matches found.")

    sys.stdout.write("\n\n")


def _join(graph):
    """
    Groups all adjacent nodes into a unified list.

    For example, for matches '{(a, b): 0.7, (b, c): 0.8}' result will be '[a, b, c]'
    """
    return [
        sorted(similar)
        for node, edges in graph.items()
        if (similar := _traverse(graph, node))
    ]


def _adjancency_list(matches):
    """Returns an adjacency list for matches with a given score or higher"""
    graph = {}
    for pair, score in matches.items():
        if score > CONFIDENCE_SCORE:
            a, b = pair
            graph.setdefault(a, []).append(b)
            graph.setdefault(b, []).append(a)
    return graph


def _traverse(graph, node, visited=[]):
    """Returns list of all direct/indirect adjacent nodes for a given node"""
    nodes = []
    if node in visited:
        return nodes
    visited.append(node)
    nodes.append(node)
    for adjacent in graph[node]:
        nodes.extend(_traverse(graph, adjacent))
    return nodes
