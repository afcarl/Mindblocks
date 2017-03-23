import theano.tensor as T

from compilation.graph_compiler import GraphCompiler
from compilation.graph_runner import GraphRunner
from components.component import Component


class SubgraphComponent(Component):
    name = "Subgraph"
    links_out = []
    links_in = []

    def python_init(self, arguments={}):
        # Define the subgraph
        # Or later: Mark for definition
        gc = GraphCompiler()
        for line in gc.yield_code(self.sub_graph, name="subgraph"):
            yield line

        yield "manifest = " + str(self.manifest)
        yield self.get_name() + " = " + self.__class__.__name__ + "(subgraph, manifest=manifest)"
        yield arguments['name'] + ".merge(" + self.get_name() + ".get_graph())"
        if self.attributes != {}:
            yield self.get_name() + ".attributes = " + str(self.attributes)
        for enumerator, in_edge in enumerate(self.edges_in):
            yield in_edge.origin.get_name() + " = " + self.get_name() + ".edges_in[" + str(enumerator) + "].origin"
        for enumerator, out_edge in enumerate(self.edges_out):
            yield out_edge.destination.get_name() + " = " + self.get_name() + ".edges_out[" + str(
                enumerator) + "].destination"

        for in_edge in self.edges_in:
            in_link = in_edge.origin
            for x in in_link.edges_in:
                yield arguments['name'] + ".add_edge(" + x.origin.get_name() + ", " + in_link.get_name() + ")"
        yield ""

    def get_python_import(self):
        yield "from " + self.module + " import " + self.__class__.__name__
        gc = GraphCompiler()
        for line in gc.yield_headers(self.sub_graph):
            yield line

    def compile_theano(self):
        pass

    def compile_python(self):
        gr= GraphRunner()

        #TODO: Get type
        for vertex in self.sub_graph.vertices:
            vertex.parse_attributes()

        compiled_graph = self.sub_graph.compile_theano()
        print("doner")
        args = tuple([self.pull_by_index(i) for i in range(len(self.links_in))])

        print(args)
        results = compiled_graph(*args)

        for i,r in enumerate(results):
            self.push_by_index(i,r)


    def __init__(self, graph, manifest=None, identifier=None, create_graph=True):
        self.sub_graph = graph

        inputs = self.sub_graph.get_inputs()
        outputs = self.sub_graph.get_outputs()

        available_space = 80

        self.links_in = []
        self.links_out = []

        if len(inputs) > 0:
            input_spacing = available_space/(len(inputs))
            for i,inp in enumerate(inputs):
                self.links_in.append({'position': [-40 + int((i+0.5) * input_spacing), 20],
                                      'name': 'Input_'+str(i)})

        if len(outputs) > 0:
            output_spacing = available_space/(len(outputs))
            for i,oup in enumerate(outputs):
                self.links_out.append({'position': [-40 + int((i+0.5) * output_spacing), -20],
                                      'name': 'Output_'+str(i)})


        Component.__init__(self, manifest=manifest, identifier=identifier, create_graph=create_graph)


    def copy(self, identifier=None):
        return self.__class__(self.graph, identifier=identifier)