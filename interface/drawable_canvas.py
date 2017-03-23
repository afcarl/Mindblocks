import tkinter as tk

from interface.selection import Selection


class DrawableCanvas(tk.Canvas):

    components = None
    parent = None
    selected_graph = None
    graphs = []
    view_name = None
    available_modules = None
    
    def __init__(self, parent, module_manager):
        self.x = self.y = 0
        tk.Canvas.__init__(self, parent, cursor="cross", borderwidth=4, relief='sunken')
        self.bind("<ButtonPress-1>", self.on_button_press)
        self.components = []

        self.parent = parent
        self.selected_graph = Selection(None)
        self.module_manager = module_manager


    def get_available_modules(self):
        modules = self.module_manager.fetch_basis_modules(view=self.view_name)
        modules.extend(self.module_manager.fetch_graph_modules(view=self.view_name))
        return modules

    def on_button_press(self, event):
        x = event.x
        y = event.y

        clicked_component = self.component_at(x,y)
        
        if clicked_component is None and self.selected_component.properties['is_toolbox']:
            new_component = self.selected_component.get().instantiate(identifier=len(self.components))
            self.components.append(new_component)
            self.components.extend(new_component.get_sub_components())

            graph = new_component.get_graph()

            self.graphs.append(graph)
            self.module_manager.register_graph(self.view_name, graph)

            new_component.set_position(x,y)
            new_component.draw(self)
                                  
            self.selected_component.change(new_component, properties={'is_toolbox':False})
            self.selected_graph.change(new_component.get_graph())
        elif clicked_component is None:
            self.selected_component.change(None, properties={'is_toolbox':False})
            self.selected_graph.change(None)
        else:
            if self.should_make_link(self.selected_component.get(), clicked_component):
                self.make_link(self.selected_component.get(), clicked_component)
            elif self.should_make_link(clicked_component, self.selected_component.get()):
                self.make_link(clicked_component, self.selected_component.get())
            else:
                self.selected_component.change(clicked_component, properties={'is_toolbox':False})
                self.selected_graph.change(clicked_component.get_graph())

    def should_make_link(self, c1, c2):
        return c1.__class__.__name__ == 'OutLink' and c2.__class__.__name__ == 'InLink'

    def get_selected_graph(self):
        return self.selected_graph.get()

    def make_link(self, c1, c2):
        self.module_manager.delete_graph(self.view_name, c2.get_graph())
        link = c1.link_to(c2)
        self.components.append(link)
        link.graphic.draw(self, None)
    
    def component_at(self, x, y):
        for component in self.components:
            if component.graphic.contains_position((x,y)):
                return component

        return None
        
