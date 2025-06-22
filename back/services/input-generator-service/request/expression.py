import ast
import operator as op
from error import VariableNotFoundError

operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}

def safe_eval(expr, variables=None):
    variables = variables or {}

    def _eval(node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise TypeError("숫자만 허용됨")
        elif isinstance(node, ast.Name):
            if node.id in variables:
                return variables[node.id][0]
            raise VariableNotFoundError(node.id, f"정의되지 않은 변수: {node.id}")
        elif isinstance(node, ast.BinOp):
            return operators[type(node.op)](_eval(node.left), _eval(node.right))
        elif isinstance(node, ast.UnaryOp):
            return operators[type(node.op)](_eval(node.operand))
        else:
            raise TypeError(f"허용되지 않은 표현식: {type(node)}")

    parsed = ast.parse(expr, mode='eval')
    return _eval(parsed.body)

def safe_eval_helper(variables, find_dict, key, default_value):
    if default_value is None and key not in find_dict:
        raise ValueError(f"default_value가 None임에도 찾는 dictionary에 {key}가 없습니다.")
    return safe_eval(str(find_dict.get(key, default_value)).replace("$", ""), variables)

def safe_eval_helper_by_key(variables, key, default_value):
    if default_value is None and key not in variables:
        raise ValueError(f"variable에 {key}가 없습니다.")
    return safe_eval(variables.get(key, default_value), variables)
