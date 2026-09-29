import re
from itertools import product


def normalize_expression(expression):
    """
    Convert standard Boolean notation into
    AND / OR / NOT notation.
    """

    expr = expression.upper().strip()

    # AND: A.B → A AND B
    expr = expr.replace(".", " AND ")

    # OR: A+B → A OR B
    expr = expr.replace("+", " OR ")

    # NOT: A' → NOT A
    expr = re.sub(r"([A-Z])'", r"NOT \1", expr)

    return expr


def find_variables(expression):
    expression = normalize_expression(expression)

    return sorted(
        set(re.findall(r'\b[A-Z]\b', expression))
    )


def evaluate_expression(expression, values):

    expr = normalize_expression(expression)

    for variable, value in values.items():
        expr = re.sub(
            rf'\b{variable}\b',
            str(value),
            expr
        )

    expr = expr.replace("AND", " and ")
    expr = expr.replace("OR", " or ")
    expr = expr.replace("NOT", " not ")

    try:
        return int(bool(eval(expr)))
    except Exception as e:
        print("Evaluation error:", e)
        print("Expression:", expr)
        return None
def generate_truth_table(expression):

    expression = normalize_expression(expression)

    variables = find_variables(expression)
    rows = []

    combinations = product(
        [0, 1],
        repeat=len(variables)
    )

    for combination in combinations:

        values = dict(
            zip(variables, combination)
        )

        output = evaluate_expression(
            expression,
            values
        )

        row = values.copy()
        row["Output"] = output

        rows.append(row)

    return variables, rows


def calculate_logic_depth(expression):
    """
    Estimate logic depth based on Boolean operators.
    """

    expr = normalize_expression(expression)

    levels = []

    if "AND" in expr:
        levels.append(1)

    if "OR" in expr:
        levels.append(1)

    if "NOT" in expr:
        levels.append(1)

    if not levels:
        return 0

    depth = len(levels)

    return depth


def estimate_delay(expression):
    """
    Estimate propagation delay in nanoseconds.
    """

    expr = normalize_expression(expression)

    delay = 0

    if "AND" in expr:
        delay += 10

    if "OR" in expr:
        delay += 10

    if "NOT" in expr:
        delay += 5

    return delay
def count_gates(expression):
    """
    Count the number of logic gates.
    """

    expr = normalize_expression(expression)

    count = 0

    count += expr.count("AND")
    count += expr.count("OR")
    count += expr.count("NOT")

    return count

def validate_expression(expression):
    """
    Validate a Boolean expression.
    """

    if not expression.strip():
        return False, "Expression cannot be empty."

    # Check balanced parentheses
    if expression.count("(") != expression.count(")"):
        return False, "Unbalanced parentheses."

    # Try parsing the expression
    try:
        from circuitvisualizer import expression_to_tree

        expression_to_tree(normalize_expression(expression))
    except Exception:
        return False, "Invalid Boolean expression."

    return True, "Valid expression."