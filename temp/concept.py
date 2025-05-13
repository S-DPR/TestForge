# $v는 이전에 지정한 변수
# 입력포맷 : [ variable, line ]
# 입력포맷의 variable은 초기init
# line : { variable: [ var.. ], repeat: $v, format: { ... }, type: (str), line_repeat: $v }
# line.type은 graph나 line..
# var: { name: (str), type: (str), range: [int, int] }
# format: 뭐 이런저런 옵션들... 뭐 separator나 sequence..

import random
import ast
import operator as op
from collections import deque

operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,   # 소수까지 나오게
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}

def safe_eval(expr, variables=None):
    variables = variables or {}

    def _eval(node):
        if isinstance(node, ast.Constant):  # Python 3.8+
            if isinstance(node.value, (int, float)):
                return node.value
            raise TypeError("숫자만 허용됨")
        elif isinstance(node, ast.Name):
            if node.id in variables:
                return variables[node.id][0]
            raise ValueError(f"정의되지 않은 변수: {node.id}")
        elif isinstance(node, ast.BinOp):
            return operators[type(node.op)](_eval(node.left), _eval(node.right))
        elif isinstance(node, ast.UnaryOp):
            return operators[type(node.op)](_eval(node.operand))
        else:
            raise TypeError(f"허용되지 않은 표현식: {type(node)}")

    parsed = ast.parse(expr, mode='eval')
    return _eval(parsed.body)

def create_variables(variable_format):
    variables = {}
    for variable_format in variable_format:
        name = variable_format['name']
        types = variable_format['type']  # 일단 int/char만
        start, end = map(int, variable_format['range'])  # 당연히 시작과 끝 모두 int
        variables[name] = (random.randint(start, end), types)
    return variables

def type_line_data_generator(variables, sequence, config):
    line_data = []
    TYPE_FUNCTION = {
        'int': lambda val: val,
        'char': lambda val: chr(val)
    }
    for seq in sequence:
        if seq[0] == '$':
            value, types = variables[seq[1:]]
            line_data.append(TYPE_FUNCTION[types](value))
        else:
            line_data.append(seq)
    return [line_data] # 이중 배열로 반환이 generator들 기본 포맷으로 하자

def type_undirected_graph_data_generator(variables, sequence, config):
    def get_edge_count(is_perfect, is_tree, is_connect, config):
        possible = []
        if 'edge_count' in config:
            return safe_eval(config.get('edge_count', '1').replace("$", ""), variables)
        if is_perfect:
            possible.append(node_count*(node_count-1)//2)
        if is_tree:
            possible.append(node_count-1)
        if is_connect:
            possible.append(random.randint(node_count-1, node_count*(node_count-1)//2))
        else:
            possible.append(random.randint(0, node_count*(node_count-1)//2))
        return possible[0]

    def create_perfect_graph():
        graph = []
        start, end = 1, node_count
        if is_zero_start:
            start, end = 0, node_count-1
        for _s in range(start, end+1):
            for _e in range(_s+1, end+1):
                variables['_s'] = (_s, 'int')
                variables['_e'] = (_e, 'int')
                graph.extend(type_line_data_generator(variables, sequence, config))
        return graph

    # 초기 vis는 cur을 제외한 모든 노드가 한 번씩 들어간 데이터
    def create_tree(cur, vis):
        graph = []
        if len(vis) != node_count-1: # 루트가 아니라면
            is_leaf = random.randint(0, 1)
            if is_leaf or not vis: return graph
        while vis:
            nxt = vis.pop()
            variables['_s'] = (cur, 'int')
            variables['_e'] = (nxt, 'int')
            graph.extend(type_line_data_generator(variables, sequence, config))
            graph.extend(create_tree(nxt, vis))
        return graph

    def create_general_graph(left_edge_count):
        start, end = 1, node_count
        if is_zero_start:
            start, end = 0, node_count - 1
        nodes = [*range(start, end + 1)]
        all_nodes = set(nodes)
        random.shuffle(nodes)
        deq = deque([nodes.pop()])
        conn_graph = [set() for _ in ' '*(end+1)]
        single_conn_graph = [[] for _ in ' '*(end+1)]
        while deq:
            cur = deq.popleft()
            if not min(len(nodes), left_edge_count): continue
            connect_nodes = random.randint(1, min(len(nodes), left_edge_count))
            left_edge_count -= connect_nodes
            for _ in range(connect_nodes):
                nxt = nodes.pop()
                conn_graph[cur].add(nxt)
                conn_graph[nxt].add(cur)
                single_conn_graph[cur].append(nxt)
                deq.append(nxt)
        nodes = [*all_nodes]
        for cur in nodes:
            not_conn = list(all_nodes^{ cur }^conn_graph[cur])
            connect_nodes = random.randint(0, min(len(not_conn), left_edge_count))
            left_edge_count -= connect_nodes
            for _ in range(connect_nodes):
                nxt = not_conn.pop()
                conn_graph[cur].add(nxt)
                conn_graph[nxt].add(cur)
                single_conn_graph[cur].append(nxt)
        graph = []
        for _s in range(start, end+1):
            for _e in single_conn_graph[_s]:
                variables['_s'] = (_s, 'int')
                variables['_e'] = (_e, 'int')
                graph.extend(type_line_data_generator(variables, sequence, config))
        return graph

    if 'node_count' not in config:
        raise ValueError('config에 node_count는 필수입니다.')
    is_zero_start = config.get('is_zero_start', False) # 노드 번호가 0부터인지 여부
    is_perfect = config.get('is_perfect', False) # 완전그래프 여부
    # is_connect = config.get('is_connect', True) # 연결그래프 여부
    is_connect = True # 샘플은 일단 이거 켜두자 너무 복잡해진다
    node_count = safe_eval(config.get('node_count').replace("$", ""), variables) # 노드 개수
    is_cycle = config.get('is_cycle', True) # 사이클 여부
    is_tree = is_connect and not is_cycle
    # is_self_cycle = config.get('is_self_cycle', False) 이건 일반적으로 문제에 없으니까 나중에 생각하자

    edge_count = get_edge_count(is_perfect, is_tree, is_connect, config) # 간선 개수
    # 검증
    if is_perfect:
        if not is_connect:
            raise ValueError(f"완전그래프가 연결그래프가 아닐 수 없습니다.")
        expected_edge_count = node_count * (node_count - 1) // 2
        if edge_count != expected_edge_count:
            raise ValueError(f"완전그래프는 선의 개수가 {expected_edge_count}여야합니다.")
    if is_connect and not node_count-1 <= edge_count <= node_count*(node_count-1)//2:
        raise ValueError(f"연결그래프는 {node_count-1}개부터 {node_count*(node_count-1)//2}개까지의 간선만을 가질 수 있습니다.")
    if is_tree and edge_count != node_count-1:
        raise ValueError(f"트리 간선의 개수는 {node_count-1}여야합니다.")

    if is_perfect:
        graph = create_perfect_graph()
    elif is_tree:
        start, end = 1, node_count
        if is_zero_start:
            start, end = 0, node_count-1
        nodes = [*range(start, end+1)]
        random.shuffle(nodes)
        graph = create_tree(nodes.pop(), nodes)
    else:
        graph = create_general_graph(edge_count)
    return graph

LINE_TYPE_FUNCTION = {
    'line': type_line_data_generator,
    'undirected_graph': type_undirected_graph_data_generator,
}

def process(variable_format, lines):
    result = []
    variables = create_variables(variable_format)
    for i in lines:
        line_repeat = safe_eval(i.get('line_repeat', '1').replace("$", ""), variables)
        config = i.get('config', {})
        for _ in range(line_repeat):
            formats = i.get('format', {})
            line_type = i.get('type', 'line')
            sequence = formats.get('sequence', [])  # formats에서 sequence는 variable에 지정한 변수를 사용 가능하다 하자
            separator = formats.get('separator', ' ')  # 그리고 세퍼레이터. 기본값은 스페이스
            type_function = LINE_TYPE_FUNCTION[line_type]
            variable_format = i.get('variable', {})

            repeat_count = safe_eval(i.get('repeat', '1').replace("$", ""), variables)
            current_line_data = []
            for _ in range(repeat_count):
                variables |= create_variables(variable_format)
                current_line_data.extend(type_function(variables, sequence, config))
            for line_data in current_line_data:
                result.append(separator.join(map(str, line_data)))
    return result

# print(process([
#     { "name": "T", "type": "int", "range": [3, 3] }
# ], [
#   {
#     "variable": [{ "name": "n", "type": "int", "range": [1, 1] }],
#     "format": { "sequence": ["$n"] }
#   },
#   {
#     "variable": [{ "name": "a", "type": "char", "range": [97, 122] }],
#     "repeat": "1",
#     "line_repeat": "$T",
#     "format": { "sequence": ["$a"], "separator": "" }
#   }
# ]
# ))

print(process([], [
    {
        'variable': [
            { 'name': 'n', 'type': 'int', 'range': [3, 3] },
        ],
        'format': { 'sequence': ['$n'] }
    },
    {
        'type': 'undirected_graph',
        'config': {
            'node_count': '$n',
            'is_perfect': True
        },
        'format': { 'sequence': ['$_s', '$_e'] }
    }
]))

print(process([], [
    {
        'variable': [
            { 'name': 'n', 'type': 'int', 'range': [5, 10] },
            # { 'name': 'm', 'type': 'int', 'range': ['$n-1', '$n*$n-n'] } # 이거 repeat에 수식 가능하게 수정 필요
            { 'name': 'm', 'type': 'int', 'range': [4, 10] }
        ],
        'format': { 'sequence': ['$n', '$m'] }
    },
    {
        'type': 'undirected_graph',
        'config': {
            'node_count': '$n'
        },
        'format': { 'sequence': ['$_s', '$_e'] }
    }
]))