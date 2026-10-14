
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, Union


Number = Union[int, float]


class Stack:
    """A simple Last-In, First-Out (LIFO) stack implementation."""

    def __init__(self) -> None:
        self._items: list = []

    def push(self, item) -> None:
        """Place an item on top of the stack."""
        self._items.append(item)

    def pop(self):
        """Remove and return the top item from the stack."""
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack")
        return self._items.pop()

    def peek(self):
        """Return the top item without removing it."""
        if self.is_empty():
            raise IndexError("Cannot peek at an empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        """Return True if the stack has no items."""
        return len(self._items) == 0

    def size(self) -> int:
        """Return the number of items currently stored in the stack."""
        return len(self._items)


TOKEN_PATTERN = re.compile(r"\d+(?:\.\d+)?|[()+\-*/]")

BINARY_OPERATORS = {"+", "-", "*", "/"}

UNARY_OPERATORS = {"u+", "u-"}

ALL_OPERATORS = BINARY_OPERATORS | UNARY_OPERATORS

PRECEDENCE = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "u+": 3,
    "u-": 3,
}

RIGHT_ASSOCIATIVE = {"u+", "u-"}


def tokenize_expression(expression: str) -> list[str]:
    """
    Split an expression into numbers, operators and parentheses.
    """

    expression = expression.strip()

    if not expression:
        raise ValueError("Expression is empty")

    tokens: list[str] = []

    position = 0

    for match in TOKEN_PATTERN.finditer(expression):

        skipped = expression[position:match.start()]

        if skipped.strip():
            raise ValueError(
                f"Invalid token near: {skipped.strip()!r}"
            )

        tokens.append(match.group())

        position = match.end()

    trailing = expression[position:]

    if trailing.strip():
        raise ValueError(
            f"Invalid token near: {trailing.strip()!r}"
        )

    if not tokens:
        raise ValueError("No valid tokens were found")

    return tokens


def is_number(token: str) -> bool:
    """
    Check whether a token represents a number.
    """

    try:
        float(token)
        return True

    except ValueError:
        return False


def infix_to_postfix(tokens: Iterable[str]) -> list[str]:
    """
    Convert an infix mathematical expression into postfix notation.

    Example:

    Infix:
        3 + 5 * 2

    Postfix:
        3 5 2 * +
    """

    output: list[str] = []

    operators = Stack()

    previous_kind = "start"

    for token in tokens:

        # --------------------------------------
        # NUMBER
        # --------------------------------------

        if is_number(token):

            if previous_kind in {"number", "right_paren"}:
                raise ValueError(
                    "Missing operator between values"
                )

            output.append(token)

            previous_kind = "number"

            continue

        # LEFT PARENTHESIS 

        if token == "(":

            if previous_kind in {"number", "right_paren"}:
                raise ValueError(
                    "Missing operator before '('"
                )

            operators.push(token)

            previous_kind = "left_paren"

            continue

       
        # RIGHT PARENTHESIS
        

        if token == ")":

            if previous_kind in {
                "start",
                "operator",
                "left_paren"
            }:
                raise ValueError(
                    "Unexpected ')' or empty parentheses"
                )

            found_left_parenthesis = False

            while not operators.is_empty():

                top = operators.pop()

                if top == "(":

                    found_left_parenthesis = True

                    break

                output.append(top)

            if not found_left_parenthesis:

                raise ValueError(
                    "Mismatched parentheses"
                )

            previous_kind = "right_paren"

            continue

        
        # OPERATORS
        

        if token in BINARY_OPERATORS:

            # Detect unary + and -
            #
            # Example:
            # -5 + 3
            #
            # Here '-' is a unary operator.

            if token in {"+", "-"} and previous_kind in {
                "start",
                "operator",
                "left_paren"
            }:

                if token == "+":
                    operator = "u+"

                else:
                    operator = "u-"

            else:

                if previous_kind not in {
                    "number",
                    "right_paren"
                }:

                    raise ValueError(
                        f"Operator {token!r} is in an invalid position"
                    )

                operator = token

            # Apply operator precedence

            while (
                not operators.is_empty()
                and operators.peek() in ALL_OPERATORS
            ):

                top = operators.peek()

                higher_precedence = (
                    PRECEDENCE[top]
                    > PRECEDENCE[operator]
                )

                same_precedence_left_assoc = (
                    PRECEDENCE[top]
                    == PRECEDENCE[operator]
                    and operator not in RIGHT_ASSOCIATIVE
                )

                if (
                    higher_precedence
                    or same_precedence_left_assoc
                ):

                    output.append(
                        operators.pop()
                    )

                else:

                    break

            operators.push(operator)

            previous_kind = "operator"

            continue

        raise ValueError(
            f"Unsupported token: {token!r}"
        )

 
    # Check expression ending
   

    if previous_kind in {
        "start",
        "operator",
        "left_paren"
    }:

        raise ValueError(
            "Expression ended unexpectedly"
        )

    # Move remaining operators to output
    

    while not operators.is_empty():

        top = operators.pop()

        if top in {"(", ")"}:

            raise ValueError(
                "Mismatched parentheses"
            )

        output.append(top)

    return output


def apply_binary_operator(
    left: float,
    right: float,
    operator: str
) -> float:

    """
    Perform a mathematical operation on two numbers.
    """

    if operator == "+":
        return left + right

    if operator == "-":
        return left - right

    if operator == "*":
        return left * right

    if operator == "/":

        if right == 0:

            raise ZeroDivisionError(
                "Division by zero is not allowed"
            )

        return left / right

    raise ValueError(
        f"Unsupported operator: {operator}"
    )


def evaluate_postfix(
    postfix_tokens: Iterable[str]
) -> float:

    """
    Evaluate a postfix mathematical expression
    using a stack.
    """

    values = Stack()

    for token in postfix_tokens:

       
        # NUMBER
       

        if is_number(token):

            values.push(
                float(token)
            )

            continue

       
        # UNARY OPERATORS
       

        if token in UNARY_OPERATORS:

            if values.size() < 1:

                raise ValueError(
                    "Not enough values for unary operator"
                )

            value = values.pop()

            if token == "u+":

                values.push(value)

            else:

                values.push(-value)

            continue

      
        # BINARY OPERATORS
       

        if token in BINARY_OPERATORS:

            if values.size() < 2:

                raise ValueError(
                    "Not enough values for binary operator"
                )

            right = values.pop()

            left = values.pop()

            result = apply_binary_operator(
                left,
                right,
                token
            )

            values.push(result)

            continue

        raise ValueError(
            f"Unexpected postfix token: {token!r}"
        )

    # A correct expression should have
    # exactly one final value remaining.

    if values.size() != 1:

        raise ValueError(
            "Invalid expression"
        )

    return values.pop()


def evaluate_expression(
    expression: str
) -> float:

    """
    Evaluate one complete mathematical expression.
    """

    tokens = tokenize_expression(
        expression
    )

    postfix = infix_to_postfix(
        tokens
    )

    result = evaluate_postfix(
        postfix
    )

    return result


def is_separator_line(
    line: str
) -> bool:

    """
    Check whether a line contains only hyphens.

    Example:

    -----
    """

    stripped = line.strip()

    return (
        bool(stripped)
        and set(stripped) == {"-"}
    )


def format_number(
    value: float
) -> str:

    """
    Format the answer so whole numbers
    do not display .0.

    Example:

    13.0 becomes 13
    2.5 remains 2.5
    """

    if value == 0:

        return "0"

    if value.is_integer():

        return str(
            int(value)
        )

    return (
        f"{value:.10f}"
        .rstrip("0")
        .rstrip(".")
    )


def process_file(
    input_path: str = "input.txt",
    output_path: str = "output.txt"
) -> None:

    """
    Read expressions from input.txt,
    calculate each expression,
    and write answers to output.txt.
    """

    source = Path(
        input_path
    )

    destination = Path(
        output_path
    )

    # Check if input file exists
    

    if not source.exists():

        raise FileNotFoundError(
            f"Input file not found: "
            f"{source.resolve()}\n"
            "Place input.txt in the same "
            "folder as this Python file."
        )

    output_lines: list[str] = []

    # ------------------------------------------
    # Read input file
    # ------------------------------------------

    with source.open(
        "r",
        encoding="utf-8"
    ) as input_file:

        for raw_line in input_file:

            line = raw_line.rstrip(
                "\n\r"
            )

            # ----------------------------------
            # BLANK LINE
            # ----------------------------------

            if not line.strip():

                output_lines.append("")

                print()

                continue

            # ----------------------------------
            # SEPARATOR LINE
            # ----------------------------------

            if is_separator_line(line):

                output_lines.append(
                    line
                )

                print(line)

                continue

            # ----------------------------------
            # MATHEMATICAL EXPRESSION
            # ----------------------------------

            try:

                result = evaluate_expression(
                    line
                )

                formatted = format_number(
                    result
                )

                output_lines.append(
                    formatted
                )

                print(
                    f"{line} = {formatted}"
                )

            except (
                ValueError,
                ZeroDivisionError
            ) as error:

                message = (
                    f"ERROR: {error}"
                )

                output_lines.append(
                    message
                )

                print(
                    f"{line} -> {message}"
                )

    # ------------------------------------------
    # WRITE RESULTS TO OUTPUT FILE
    # ------------------------------------------

    with destination.open(
        "w",
        encoding="utf-8"
    ) as output_file:

        output_file.write(
            "\n".join(output_lines)
        )

        if output_lines:

            output_file.write("\n")

    print(
        "\nResults written successfully to:"
    )

    print(
        destination.resolve()
    )


def main() -> None:
    """
    Main function used to start the program.
    """

    process_file(
        "input.txt",
        "output.txt"
    )


if __name__ == "__main__":
    main()