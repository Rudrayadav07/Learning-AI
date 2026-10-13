import ast
import operator
import os
import re
from typing import Any

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise ValueError("GROQ_API_KEY is not set. Add it to your .env file.")

client = Groq(api_key=API_KEY)
MODEL = "openai/gpt-oss-120b"


def get_product_price(product: str) -> int:
    """Return the price for a known product name."""
    products = {
        "iPhone 17": 1000,
        "iPhone 15": 500,
        "iPhone 13": 700,
    }
    return products.get(product.strip(), 0)


def _safe_eval(node: ast.AST) -> Any:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.BinOp):
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        ops = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.FloorDiv: operator.floordiv,
            ast.Mod: operator.mod,
            ast.Pow: operator.pow,
        }
        if type(node.op) not in ops:
            raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
        return ops[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp):
        operand = _safe_eval(node.operand)
        ops = {
            ast.UAdd: operator.pos,
            ast.USub: operator.neg,
            ast.Not: operator.not_,
        }
        if type(node.op) not in ops:
            raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
        return ops[type(node.op)](operand)

    if isinstance(node, ast.Tuple):
        return tuple(_safe_eval(item) for item in node.elts)

    if isinstance(node, ast.List):
        return [_safe_eval(item) for item in node.elts]

    raise ValueError(f"Unsupported expression: {ast.dump(node)}")


def calculator(expression: str) -> Any:
    """Evaluate a restricted arithmetic expression safely."""
    if not isinstance(expression, str):
        return "Calc error!"

    sanitized_expression = expression.strip()
    if not sanitized_expression:
        return "Calc error!"

    try:
        parsed = ast.parse(sanitized_expression, mode="eval")
        result = _safe_eval(parsed.body)
        if isinstance(result, complex):
            return "Calc error!"
        return result
    except Exception:
        return "Calc error!"


TOOLS = {
    "get_product_price": get_product_price,
    "calculator": calculator,
}

SYSTEM_PROMPT = """
You are a shopping assistant.

You have access to these tools:
- get_product_price(product)
- calculator(expression)

Important rules:
1. Decide what you need to do next.
2. Call exactly ONE tool at a time.
3. After writing an Action, stop immediately.
4. Never make up tool results.
5. Wait for the Observation before deciding the next step.
6. When the task is complete, provide a Final Answer.

Use this format:
Thought: <your reasoning>
Action: tool_name(argument)

When done:
Final Answer: <your answer>

Examples:
Action: get_product_price("iPhone 17")
Action: calculator("5000 - 1000")

Do not use keyword arguments like get_product_price(product="iPhone 17").
"""


def parse_action(response: str):
    """Extract the single tool call from the model output."""
    if not response:
        return None, None

    match = re.search(r"Action:\s*(\w+)\((.*?)\)", response, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return None, None

    tool_name = match.group(1)
    raw_argument = match.group(2).strip()

    if raw_argument.startswith(("\"", "'")) and raw_argument.endswith(("\"", "'")):
        argument = raw_argument[1:-1]
    else:
        try:
            argument = ast.literal_eval(raw_argument)
        except (ValueError, SyntaxError):
            argument = raw_argument

    return tool_name, argument


def execute_tool(tool_name: str, tool_input: Any) -> Any:
    tool = TOOLS.get(tool_name)
    if tool is None:
        return f"Tool not found: {tool_name}"
    return tool(tool_input)


def run_agent(question: str, max_steps: int = 5) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]

    for step in range(max_steps):
        print(f"\n-----------------\nSTEP {step + 1}\n------------------")
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.2,
        )

        result = (response.choices[0].message.content or "").strip()
        print(result)

        if re.search(r"Final Answer:\s*", result, flags=re.IGNORECASE):
            return result

        tool_name, tool_input = parse_action(result)
        if tool_name is None:
            return "The model did not provide a valid tool action."

        observation = execute_tool(tool_name, tool_input)
        print(f"Observation: {observation}")

        messages.append({"role": "assistant", "content": result})
        messages.append({"role": "user", "content": f"Observation: {observation}"})

    return "The agent could not complete the task within the allowed steps."


if __name__ == "__main__":
    prompt = """
    I have 5000 rs. What is the price of iPhone 17?
    And how much money will I have left?
    """

    final_answer = run_agent(prompt)
    print("\n" + final_answer)
