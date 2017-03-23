import tkinter as tk
from tkinter import ttk

from compilation.compiler import Compiler
from compilation.graph_compiler import GraphCompiler
from interface.other.description_panel import DescriptionPanel
from interface.other.menubar import Menubar
from interface.other.toolbox import Toolbox
from interface.selection import Selection
from interface.views.agent_view import AgentView
from interface.views.experiment_view import ExperimentView
from interface.views.inference_view import InferenceView
from module_management.module_importer import ModuleImporter
from module_management.module_manager import ModuleManager


class Interface(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        self.title('Mindblocks')
        self.geometry('{}x{}'.format(800, 600))

        self.selected_component = Selection(None)
        
        self.menubar = Menubar(self)
        self.config(menu=self.menubar)
        
        self.make_support_frames()
        self.add_views()
        self.add_interface()

        self.initialize_component_selection()
        self.initialize_canvas_selection()

        return


        self.layout()


        

    def make_support_frames(self):
        self.left_frame = tk.Frame(self, background="blue")
        self.right_frame = tk.Frame(self, background="green")

        self.right_frame.pack(side=tk.RIGHT, expand=False, fill=tk.Y, pady=0, padx=0, anchor="ne")
        self.left_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, pady=0, padx=0, anchor="ne")

    def add_interface(self):
        self.toolbox = Toolbox(self.right_frame)
        self.description_panel = DescriptionPanel(self.right_frame)

        self.description_panel.pack(side=tk.BOTTOM, expand=False, fill=tk.X, pady=0, padx=0, anchor="s")
        self.toolbox.pack(side=tk.BOTTOM, expand=True, fill=tk.Y, pady=0, padx=0, anchor="n")

    def initialize_canvas_selection(self):
        self.selected_canvas = Selection(self.agent_view)
        self.selected_canvas.set_watcher(self.toolbox.canvas_selection_changed) 
        
        def tabChangedEvent(event):
            if event.widget.index("current") == 0:
                self.selected_canvas.change(self.agent_view)
            elif event.widget.index("current") == 1:
                self.selected_canvas.change(self.inference_view)
            elif event.widget.index("current") == 2:
                self.selected_canvas.change(self.experiment_view)
                        
        self.note.bind_all("<<NotebookTabChanged>>", tabChangedEvent)

    def initialize_component_selection(self):
        self.selected_component = Selection(None, properties = {'is_toolbox':False})

        self.agent_view.selected_component = self.selected_component
        self.inference_view.selected_component = self.selected_component
        self.experiment_view.selected_component = self.selected_component

        self.toolbox.selected_component = self.selected_component
        self.description_panel.selected_component = self.selected_component

        self.selected_component.set_watcher(self.description_panel.component_selection_changed) 
        

    def predict_selection(self):
        graph = self.agent_view.get_selected_graph()
        predict_function = graph.compile_theano(mode='predict')
        print(predict_function())

    def compile_selection(self):
        print("Compiling functions...")
        graph = self.experiment_view.get_selected_graph()

        c = Compiler(GraphCompiler())
        c.compile(graph, "out.py")

        print("done")

        
    def add_views(self):
        self.note = ttk.Notebook(self.left_frame)

        module_importer = ModuleImporter()
        module_manager = ModuleManager(module_importer)
        
        self.agent_view = AgentView(self.note, module_manager)
        self.inference_view = InferenceView(self.note, module_manager)
        self.experiment_view = ExperimentView(self.note, module_manager)

        self.note.add(self.agent_view, text="Agents")
        self.note.add(self.inference_view, text="Inference")
        self.note.add(self.experiment_view, text="Experiment")
        
        self.note.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, anchor="nw")


    def layout(self):
        self.description_panel.pack(side=tk.BOTTOM, expand=False, pady=0, padx=0, anchor="se")
        self.toolbox.pack(side=tk.RIGHT, expand=True, fill=tk.Y, pady=0, padx=0, anchor="ne")
        self.note.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, pady=0, padx=0, anchor="ne")
