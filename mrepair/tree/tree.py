
import re


class Tree:

    def __init__(self):

        self.nodes = []
        self.node_id = 1

        # Add root node
        self.nodes.append(Node(id='0',
                               name='root'))
        self.root = self.nodes[0]

    def add_node(self, id, name, parent=None):
        """
        Add a node to the tree.
        """

        # Append a Node to the array
        node = Node(id, name, parent)
        self.nodes.append(node)

        # Append a children to the parent
        parent.children.append(node)

        # increase node_id
        self.node_id += 1

        return

    def by_id(self, id):
        """
        Find a Node using its id. 
        """

        node = [n for n in self.nodes if n.id == id]

        return node[0]


class Node:

    def __init__(self, id, name, parent=None):

        # Basic parameters
        self.id = id
        self.name = name
        self.parent = parent
        self.children = []


def generate_tree(results):
    """
    Creates a tree from the results dictionary of the 
    RePair algorithm.
    """

    # Initialize the tree
    tree = Tree()

    # Isolate results
    indices = results['index']
    rules = results['Rule']
    exp_rules = results['Expanded Rule']

    # Iterate over the pairs
    for indice, rule, exp_rule in zip(indices, rules, exp_rules):

        # Try to match a number in the pair
        content = re.findall('[1-9][0-9]*', rule)

        # If there are no number, the pair is a root node
        if not content:
            tree.add_node(id=str(tree.node_id),
                          name=f"{indice}: {exp_rule}",
                          parent=tree.root)

        # Otherwise
        else:
            tree.add_node(id=str(tree.node_id),
                          name=f"{indice}: {exp_rule}",
                          parent=tree.by_id(id=content[0]))

    return tree


def generate_dot(tree):
    """
    Generates a dot file of a directed graph, i.e.:
    digraph graphname {
        a -> b -> c;
        b -> d;
    }
    """

    # Create and write on a .dot file
    with open('hierarchy.dot', 'w') as f:

        f.write('digraph hierarchy {\n')

        # Iterate over the nodes
        for node in tree.nodes:

            # If the node has children
            if node.children:
                for children in node.children:

                    f.write(f'"{node.name}" -> "{children.name}";\n')

        f.write('}\n')

    return


def compute_hierarchy(results):
    """
    Computes the underlying hierarchy from the results of the 
    RePair algorithm.

    Saves the hierarchy as a .dot file and also as a .png file
    if pydot is installed.
    """
    # Build tree
    tree = generate_tree(results)

    # Generate .dot file for tree visualization
    generate_dot(tree)

    # Generate an image from the .dot file
    try:
        import pydot
    except ImportError:
        print('Requires the pydot module.')
        return

    graphs = pydot.graph_from_dot_file('hierarchy.dot')
    graph = graphs[0]
    graph.write_png('hierarchy.png')

    return
