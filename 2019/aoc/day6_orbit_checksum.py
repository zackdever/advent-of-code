class Node:
    def __init__(self, data):
        self.data = data
        self.parent = None
        self._children = []

    def add_child(self, node):
        node.parent = self
        self._children.append(node)

    def get_children(self):
        return iter(self._children)


def build_tree(orbits):
    """
    A little weird structure here. Returns a dict of {'FOO': Node(...), ...},
    but each node has it's children addeded. Really is an adjency list graph.
    """
    nodes = {}
    for orbit in orbits:
        o1, o2 = orbit.split(')')
        if o1 not in nodes:
            nodes[o1] = Node(o1)
        if o2 not in nodes:
            nodes[o2] = Node(o2)
        node1 = nodes[o1]
        node2 = nodes[o2]
        node1.add_child(node2)
    return nodes


def build_depths(node, depths=None):
    depths = depths or {}
    if not node.parent:
        depths[node] = 0
    else:
        depths[node] = depths[node.parent] + 1
    for child in node.get_children():
        build_depths(child, depths)
    return depths

def total_depth(tree, depth=0):
    total = 0
    depth += 1
    for child in tree.get_children():
        total += depth
        total += total_depth(child, depth)
    return total


def orbit_checksum(orbits):
    """Part 1: Return the total number of direct and indirect orbits.

    orbits: ['WGB)S14', 'WN4)27C', ..., '18L)M18']
    There's a special object, the universal Center of Mass, (COM).
    Every other object orbits around exactly one other object.

    This can be represented by a n-ary tree, with COM as the root.
    The total number of orbits is the sum of the depth of each node.
    
    Also seems kind of graphy... because I have a list of edges...
    """
    tree = build_tree(orbits)
    depths = build_depths(tree['COM'])
    return sum(depths.values())


def min_orbital_transfers(orbits, start='YOU', end='SAN'):
    """Part 2
    And part 2 could use Dijkstra's algo, but it wouldn't be terribly
    efficient b/c the edges aren't weighted.

    HOWEVER, I think we can just go up the tree until we reach the same depth,
    and then if we're not at the same, node, keep going up on both until we do.
    """
    tree = build_tree(orbits)
    depths = build_depths(tree['COM'])
    start_node = tree['YOU'].parent
    end_node = tree['SAN'].parent

    transfers = 0
    while start_node != end_node:
        if depths[start_node] < depths[end_node]:
            end_node = end_node.parent
            transfers += 1
        elif depths[start_node] > depths[end_node]:
            start_node = start_node.parent
            transfers += 1
        else:
            start_node = start_node.parent
            end_node = end_node.parent
            transfers += 2

    return transfers



if __name__ == '__main__':
    fp = './input/day6.txt'
    with open(fp) as f:
        orbits = [l.strip() for l in f.readlines()]
    print('Orbit checksum: {}'.format(orbit_checksum(orbits)))
    print('Min orbital transfers: {}'.format(min_orbital_transfers(orbits)))
