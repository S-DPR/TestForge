import random
from collections import deque

from request.config_structs import Output, GraphConfigDataclass, Range, IntRange
from request.expression import safe_eval_helper, safe_eval
from error.exception import ConfigValueError
from input_generator.base_generator import BaseGenerator, BaseConfig
from input_generator.line_generator import line_generator

class GraphConfig(BaseConfig):
    def __init__(self, variables: dict[str, tuple[int, str]], config: GraphConfigDataclass):
        print(config.node_count)
        try:
            self.node_count = safe_eval(config.node_count.replace('$', ''), variables)  # 노드 개수
        except ValueError:
            raise ConfigValueError('node_count', 'node_count는 그래프 config에 반드시 포함되어있어야 합니다.')

        self.is_zero_start = config.is_zero_start # 노드 번호가 0부터인지 여부
        self.start, self.end = [0, self.node_count-1] if self.is_zero_start else [1, self.node_count]

        self.weight_range = [IntRange(1, 10)]
        if config.weight_range:
            self.weight_range = []
            for weight in config.weight_range:
                mn = safe_eval(weight.min.replace('$', ''), variables)
                mx = safe_eval(weight.max.replace('$', ''), variables)
                self.weight_range.append(IntRange(mn, mx))

        self.is_connect = config.is_connect # 연결그래프 여부
        self.is_cycle = config.is_cycle # 사이클 여부
        # is_self_cycle = config.get('is_self_cycle', False) 이건 일반적으로 문제에 없으니까 나중에 생각하자
        self.edge_count = self.get_edge_count(variables, config.edge_count) # 간선 개수
        self.validate()

    @property
    def is_tree(self) -> bool:
        return self.is_connect and not self.is_cycle

    def get_edge_count(self, variables, edge_count) -> int:
        node_count = self.node_count
        if edge_count is not None:
            return safe_eval(edge_count.replace('$', ''), variables)
        if node_count == 1:
            return 0
        if node_count == 2 and self.is_connect:
            return 1
        if self.is_tree:
            return node_count - 1
        if self.is_connect:
            return random.randint(node_count - 1, node_count * (node_count - 1) // 2)
        return random.randint(0, node_count * (node_count - 1) // 2)

    def validate(self) -> None:
        n = self.node_count
        e = self.edge_count
        if not 1 <= n <= 1_000:
            raise ConfigValueError('node_count', f"node_count가 너무 크거나 작습니다. 1 이상 1000 이하의 수만 사용할 수 있습니다. node_count : {n}")
        if not 0 <= e <= 1_000_000:
            raise ConfigValueError('edge_count', f"edge_count가 너무 크거나 작습니다. 0 이상 100만 이하의 수만 사용할 수 있습니다. edge_count : {e}")

        min_edge = n - 1
        max_edge = n * (n - 1) // 2

        if self.is_connect and not min_edge <= e <= max_edge:
            raise ConfigValueError("edge_count", f"연결그래프는 {min_edge}개부터 {max_edge}개까지의 간선만을 가질 수 있습니다. 현재 {e}개입니다.")

        if self.is_tree and e != min_edge:
            raise ConfigValueError("edge_count", f"트리의 간선 개수는 {min_edge}여야 합니다. 현재 {e}개입니다.")

class GraphGenerator(BaseGenerator):
    def generate(self, variables, output: Output, config: GraphConfig):
        # 초기 vis는 cur을 제외한 모든 노드가 한 번씩 들어간 데이터
        def create_tree(cur, vis):
            graph = []
            if len(vis) != config.node_count-1: # 루트가 아니라면
                is_leaf = random.randint(0, 1)
                if is_leaf or not vis: return graph
            while vis:
                nxt = vis.pop()
                self.set_variable(variables, cur, nxt, config.weight_range)
                graph.extend(line_generator.generate(variables, output, config))
                graph.extend(create_tree(nxt, vis))
            return graph

        def create_general_graph():
            start, end = config.start, config.end
            graph = []

            # connect상태인 경우 트리 구성해두기
            using_edges = set()
            if config.is_connect:
                nodes = [*range(start, end+1)]
                random.shuffle(nodes)
                deq = deque([nodes.pop()])
                while nodes:
                    cur = deq.popleft()
                    conn_edge_count = random.randint(1, min(3, len(nodes))) # 유사 성게 생성 방지
                    for _ in range(conn_edge_count):
                        nxt = nodes.pop()
                        using_edges.add((nxt, cur))
                        using_edges.add((cur, nxt))
                        self.set_variable(variables, cur, nxt, config.weight_range)
                        graph.extend(line_generator.generate(variables, output, config))
                        deq.append(nxt)

            # 모든 간선을 만든 뒤 그중에 N개를 뽑자
            edges = [[_s, _e] for _s in range(start, end+1) for _e in range(_s+1, end+1) if (_s, _e) not in using_edges]
            random.shuffle(edges)
            for i in edges:
                random.shuffle(i)

            # 라인 만들기
            for _s, _e in edges[:config.edge_count]:
                self.set_variable(variables, _s, _e, config.weight_range)
                graph.extend(line_generator.generate(variables, output, config))
            return graph

        if config.is_tree:
            nodes = [*range(config.start, config.end+1)]
            random.shuffle(nodes)
            graph = create_tree(nodes.pop(), nodes)
        else:
            graph = create_general_graph()
        return graph

    def set_variable(self, variables, _s, _e, weight_range: list[IntRange]):
        variables['_s'] = (_s, 'int')
        variables['_e'] = (_e, 'int')
        if weight_range is not None:
            select_w = random.choice(weight_range)
            w = random.randint(select_w.min, select_w.max)
            variables['_w'] = (w, 'int')

graph_generator = GraphGenerator()
