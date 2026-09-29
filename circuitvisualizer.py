import matplotlib.pyplot as plt
import networkx as nx
import re


def tokenize(expression):

    expression = expression.upper()

    # Convert standard Boolean notation
    expression = expression.replace(".", " AND ")
    expression = expression.replace("+", " OR ")

    # Convert A' into NOT A
    expression = re.sub(
        r"([A-Z])'",
        r"NOT \1",
        expression
    )

    return re.findall(
        r'AND|OR|NOT|[A-Z]|\(|\)',
        expression
    )


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def eat(self, token=None):
        current = self.current()

        if token and current != token:
            raise ValueError(f"Expected {token}")

        self.position += 1
        return current

    def parse(self):
        return self.parse_or()

    def parse_or(self):
        node = self.parse_and()

        while self.current() == "OR":
            self.eat("OR")
            right = self.parse_and()
            node = ("OR", node, right)

        return node

    def parse_and(self):
        node = self.parse_not()

        while self.current() == "AND":
            self.eat("AND")
            right = self.parse_not()
            node = ("AND", node, right)

        return node

    def parse_not(self):

        if self.current() == "NOT":
            self.eat("NOT")
            return ("NOT", self.parse_not())

        return self.parse_primary()

    def parse_primary(self):

        token = self.current()

        if token == "(":
            self.eat("(")
            node = self.parse_or()
            self.eat(")")
            return node

        if token and re.fullmatch(r"[A-Z]", token):
            self.eat()
            return ("INPUT", token)

        raise ValueError("Invalid expression")


def expression_to_tree(expression):

    tokens = tokenize(expression)

    parser = Parser(tokens)

    tree = parser.parse()

    if parser.current() is not None:
        raise ValueError("Invalid expression")

    return tree


def draw_circuit(expression):

    tree = expression_to_tree(expression)

    graph = nx.DiGraph()

    counter = [0]

    def build_graph(node):

        node_type = node[0]

        # Input variable
        if node_type == "INPUT":

            name = node[1]

            graph.add_node(
                name,
                label=name,
                layer=0
            )

            return name

        # Logic gate
        counter[0] += 1

        gate_id = f"G{counter[0]}"

        graph.add_node(
            gate_id,
            label=node_type,
            layer=counter[0]
        )

        if node_type == "NOT":

            child = build_graph(node[1])

            graph.add_edge(child, gate_id)

        else:

            left = build_graph(node[1])
            right = build_graph(node[2])

            graph.add_edge(left, gate_id)
            graph.add_edge(right, gate_id)

        return gate_id

    output = build_graph(tree)

    graph.add_node(
        "OUTPUT",
        label="OUTPUT",
        layer=counter[0] + 1
    )

    graph.add_edge(output, "OUTPUT")

    # Draw graph
    plt.figure(figsize=(10, 5))

    positions = nx.multipartite_layout(
        graph,
        subset_key="layer",
        align="vertical"
    )

    labels = nx.get_node_attributes(graph, "label")

    nx.draw(
        graph,
        positions,
        labels=labels,
        node_size=2500,
        arrows=True,
        font_size=10
    )

    plt.title("Generated Logic Circuit")

    return plt