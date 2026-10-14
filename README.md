# DCOMP320 Stack Implementation Assignment

 # Project description

This Python program reads mathematical expressions from `input.txt`, evaluates each expression using stack data structures, and writes the answers to `output.txt`. It supports addition, subtraction, multiplication, division, parentheses, decimal values, negative numeric values, and normal operator-precedence rules.

## Files

 `stack_evaluator.py` - Python source code.
 `input.txt` - sample expressions used for testing.
 `output.txt` - results generated from the sample input.
 `test_stack_evaluator.py` - automated unit tests.
 `DCOMP320_Stack_Implementation_Report.docx` - printable assignment report.

# Requirements

- Python 3.9 or a newer version.
- No external packages are required to run the program.

# How to run the program

1. Put `stack_evaluator.py` and `input.txt` in the same folder.
2. Open Command Prompt, Terminal, or the VS Code terminal in that folder.
3. Run the following command:

   bash
   python stack_evaluator.py
   

4. Open `output.txt` to view the generated answers.

On some computers, the command may be `python3 stack_evaluator.py`.

## Input-file structure

- Place one mathematical expression on each line.
- Place a line containing only hyphens, such as `-----`, between expressions.
- Spaces are optional.

Example:

text
3 + 5 * 2
-----
(8 / 4) + 7 * 2
```

## Output-file structure

Each expression is replaced by its calculated result. Separator lines and blank lines are preserved.

text
13
-----
16
```

# Assumptions and limitations

- Supported operators are `+`, `-`, `*`, and `/`.
- Parentheses must match correctly.
- A unary positive or negative sign is supported when directly followed by a number, such as `-5` or `(-2 + 6)`.
- Exponents, square roots, variables, and mathematical functions are not supported.
- Invalid expressions and division by zero produce an error message in `output.txt`; they do not stop the remaining expressions from being processed.

# Running the tests

Run:

```bash
python -m unittest test_stack_evaluator.py -v
```

All tests should display `ok`.