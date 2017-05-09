from module_management.module import Module
from module_management.module_component import GraphModuleComponent


class ModuleManager:

    basic_modules = []

    def __init__(self, importer):
        self.basic_modules = importer.import_modules()
        self.graphs = {'agent':[],
                       'inference':[],
                       'experiment':[]}

    def fetch_basic_modules(self, view=None):
        modules = []
        for module in self.basic_modules:
            filtered_module = module.get_filtered_copy(view)
            if filtered_module.has_components():
                modules.append(filtered_module)
        return modules

    def fetch_graph_modules(self, view=None):
        graph_modules = []
        if view == 'experiment':
            agent_module = self.compile_graph_module('agent')
            if agent_module.has_components():
                graph_modules.append(agent_module)

        return graph_modules

    def compile_graph_module(self, target_view):
        print(self.graphs)
        module_manifest = {'name': target_view}
        module = Module(module_manifest)
        for graph in self.graphs[target_view]:
            manifest = {'file_path': 'components.graph.subgraph_component',
                        'name': 'SubgraphComponent',
                        'languages': ['python']}
            module.add_component(GraphModuleComponent(manifest, graph))

        return module

    def register_graph(self, view, graph):
        print(graph.get_unique_identifier())
        self.graphs[view].append(graph)

    def delete_graph(self, view, graph):
        print(graph.get_unique_identifier())
        new_graphs = []
        for stored_graph in self.graphs[view]:
            if stored_graph.get_unique_identifier() != graph.get_unique_identifier():
                new_graphs.append(stored_graph)
        self.graphs[view] = new_graphs