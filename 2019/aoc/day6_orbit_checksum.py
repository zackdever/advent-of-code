class Node:
    def __init__(self, data):
        self.data = data
        self.children = []


def total_depth(tree, depth=0):
    total = 0
    depth += 1
    for child in tree.children:
        total += depth
        total += total_depth(child, depth)
    return total


def orbit_checksum(orbits):
    """Return the total number of direct and indirect orbits.

    orbits: ['WGB)S14', 'WN4)27C', ..., '18L)M18']
    There's a special object, the universal Center of Mass, (COM).
    Every other object orbits around exactly one other object.

    This can be represented by a n-ary tree, with COM as the root.
    The total number of orbits is the sum of the depth of each node.
    
    Also seems kind of graphy... because I have a list of edges...
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
        node1.children.append(node2)

    return total_depth(nodes['COM'])


if __name__ == '__main__':
    fp = './input/day6.txt'
    with open(fp) as f:
        orbits = [l.strip() for l in f.readlines()]
    print('Orbit checksum: {}'.format(orbit_checksum(orbits)))
