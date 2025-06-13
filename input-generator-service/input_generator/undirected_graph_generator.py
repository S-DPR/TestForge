import random
from collections import deque

from request.config_structs import Output, UndirectedGraphConfigDataclass, Range
from request.expression import safe_eval_helper, safe_eval
from error.exception import ConfigValueError
from input_generator.base_generator import BaseGenerator, BaseConfig
from input_generator.line_generator import line_generator

class UndirectedGraphConfig(BaseConfig):
    def __init__(self, variables: dict[str, tuple[int, str]], config: UndirectedGraphConfigDataclass):
        try:
            self.node_count = safe_eval(config.node_count, variables)  # 노드 개수
        except ValueError:
            raise ConfigValueError('node_count', 'node_count는 그래프 config에 반드시 포함되어있어야 합니다.')

        self.is_zero_start = config.is_zero_start # 노드 번호가 0부터인지 여부
        self.start, self.end = [0, self.node_count-1] if self.is_zero_start else [1, self.node_count]

        self.weight_range = [Range(1, 10)]
        if config.weight_range:
            w = random.choice(config.weight_range)
            weight_start, weight_end = w.min, w.max
            weight_start = safe_eval_helper(weight_start, config, 'weight_start', '1')
            weight_end = safe_eval_helper(weight_end, config, 'weight_end', '100000')
            self.weight_range = [weight_start, weight_end]

        self.is_perfect = config.is_perfect # 완전그래프 여부
        # is_connect = config.get('is_connect', True) # 연결그래프 여부
        self.is_connect = True # 일단 이거 켜두자 너무 복잡해진다
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
            return safe_eval(edge_count, variables)
        if self.is_perfect:
            return node_count * (node_count - 1) // 2
        if self.is_tree:
            return node_count - 1
        if self.is_connect:
            return random.randint(node_count - 1, node_count * (node_count - 1) // 2)
        return random.randint(0, node_count * (node_count - 1) // 2)

    def validate(self) -> None:
        n = self.node_count
        e = self.edge_count
        if not 1 <= n <= 1_000_000:
            raise ConfigValueError('node_count', f"node_count가 너무 크거나 작습니다. 1 이상 100만 이하의 수만 사용할 수 있습니다. node_count : {n}")
        if not 0 <= e <= 1_000_000:
            raise ConfigValueError('edge_count', f"edge_count가 너무 크거나 작습니다. 0 이상 100만 이하의 수만 사용할 수 있습니다. edge_count : {e}")

        if self.is_perfect:
            if not self.is_connect:
                raise ConfigValueError("edge_count", "완전그래프가 연결그래프가 아닐 수 없습니다.")
            expected = n * (n - 1) // 2
            if e != expected:
                raise ConfigValueError("edge_count", f"완전그래프는 간선 개수가 {expected}여야 합니다. 현재 {e}개입니다.")

        min_edge = n - 1
        max_edge = n * (n - 1) // 2

        if self.is_connect and not min_edge <= e <= max_edge:
            raise ConfigValueError("edge_count", f"연결그래프는 {min_edge}개부터 {max_edge}개까지의 간선만을 가질 수 있습니다. 현재 {e}개입니다.")

        if self.is_tree and e != min_edge:
            raise ConfigValueError("edge_count", f"트리의 간선 개수는 {min_edge}여야 합니다. 현재 {e}개입니다.")

class UndirectedGraphGenerator(BaseGenerator):
    def generate(self, variables, output: Output, config: UndirectedGraphConfig):
        def create_perfect_graph():
            graph = []
            start, end = config.start, config.end
            for _s in range(start, end+1):
                for _e in range(_s+1, end+1):
                    self.set_variable(variables, _s, _e, config.weight_range)
                    # variables['_s'] = (_s, 'int')
                    # variables['_e'] = (_e, 'int')
                    # if config.weight_range is not None:
                    #     w = random.randint(*config.weight_range)
                    #     variables['_w'] = (w, 'int')
                    graph.extend(line_generator.generate(variables, output, config))
            return graph

        # 초기 vis는 cur을 제외한 모든 노드가 한 번씩 들어간 데이터
        def create_tree(cur, vis):
            graph = []
            if len(vis) != config.node_count-1: # 루트가 아니라면
                is_leaf = random.randint(0, 1)
                if is_leaf or not vis: return graph
            while vis:
                nxt = vis.pop()
                self.set_variable(variables, cur, nxt, config.weight_range)
                # variables['_s'] = (cur, 'int')
                # variables['_e'] = (nxt, 'int')
                # if config.weight_range is not None:
                #     w = random.randint(*config.weight_range)
                #     variables['_w'] = (w, 'int')
                graph.extend(line_generator.generate(variables, output, config))
                graph.extend(create_tree(nxt, vis))
            return graph

        def create_general_graph(left_edge_count):
            start, end = config.start, config.end
            nodes = [*range(start, end + 1)]
            all_nodes = set(nodes)
            random.shuffle(nodes)
            deq = deque([nodes.pop()])
            conn_graph = [set() for _ in ' '*(end+1)]
            single_conn_graph = [[] for _ in ' '*(end+1)]

            # bfs를 통해 일단 연결그래프 그리기
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

            # 남은 간선은 이어지지 않은 간선끼리 이어주기
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

            # 라인 만들기
            graph = []
            for _s in range(start, end+1):
                for _e in single_conn_graph[_s]:
                    self.set_variable(variables, _s, _e, config.weight_range)
                    # variables['_s'] = (_s, 'int')
                    # variables['_e'] = (_e, 'int')
                    # if config.weight_range is not None:
                    #     w = random.randint(*config.weight_range)
                    #     variables['_w'] = (w, 'int')
                    graph.extend(line_generator.generate(variables, output, config))
            return graph

        if config.is_perfect:
            graph = create_perfect_graph()
        elif config.is_tree:
            nodes = [*range(config.start, config.end+1)]
            random.shuffle(nodes)
            graph = create_tree(nodes.pop(), nodes)
        else:
            graph = create_general_graph(config.edge_count)
        return graph

    def set_variable(self, variables, _s, _e, weight_range):
        variables['_s'] = (_s, 'int')
        variables['_e'] = (_e, 'int')
        if weight_range is not None:
            w = random.randint(*weight_range)
            variables['_w'] = (w, 'int')

undirected_graph_generator = UndirectedGraphGenerator()
