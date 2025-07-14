import logging

logger = logging.getLogger(__name__)

def evaluate_rpn(expr: str, debug: bool = False) -> float:
    """
    Evaluate a Reverse Polish Notation (RPN) expression.
    Args:
        expr (str): The RPN expression, e.g. "3 4 +"
        debug (bool): If True, print debug information during calculation
    Returns:
        float: The result of the calculation
    Raises:
        ValueError: If the expression is invalid
        ZeroDivisionError: If division by zero occurs
    """
    ops = expr.strip().split()
    stack: list[float] = []

    logger.info(f"Starting evaluation of expression: {expr}")
    if debug:
        logger.debug(f"Expression tokens: {ops}")

    for token in ops:
        if debug:
            logger.debug(f"Processing token: {token}, Current stack: {stack}")

        if token in {"+", "-", "*", "/"}:
            try:
                b, a = stack.pop(), stack.pop()
                logger.debug(f"Popped operands: a={a}, b={b}")
            except IndexError:
                logger.error(f"Invalid expression: not enough operands for operator {token}")
                raise ValueError(f"Invalid expression: not enough operands for operator {token}")
            
            try:
                if token == "+":
                    result = a + b
                elif token == "-":
                    result = a - b
                elif token == "*":
                    result = a * b
                else:  # "/"
                    if b == 0:
                        logger.error("Division by zero attempted")
                        raise ZeroDivisionError("Division by zero")
                    result = a / b
                
                stack.append(result)
                logger.debug(f"Operation: {a} {token} {b} = {result}")
                logger.debug(f"Stack after operation: {stack}")
            except Exception as e:
                logger.error(f"Error during calculation: {str(e)}")
                raise
        else:
            try:
                num = float(token)
                stack.append(num)
                logger.debug(f"Pushed number to stack: {num}")
            except ValueError:
                logger.error(f"Invalid token encountered: {token}")
                raise ValueError(f"Invalid token: {token}")

    if len(stack) != 1:
        logger.error(f"Invalid expression: stack has {len(stack)} items after evaluation")
        raise ValueError("Invalid expression: too many operands")
    
    result = stack[0]
    logger.info(f"Expression evaluation completed: {expr} = {result}")
    return result
