from controller.description_panel_controller.description_panel_listener import DescriptionPanelListener
from controller.description_panel_controller.description_panel_presenter import DescriptionPanelPresenter
from controller.mediator.canvas_to_graph_mediator import CanvasToGraphMediator
from controller.mediator.graph_to_graph_prototype_mediator import GraphToGraphPrototypeMediator
from controller.menubar_controller.menubar_listener import MenubarListener
from controller.selection_controller.selection_presenter import SelectionPresenter
from controller.toolbox_controller.toolbox_listener import ToolboxListener
from controller.toolbox_controller.toolbox_presenter import ToolboxPresenter
from controller.viewscreen_controller.viewscreen_listener import ViewscreenListener
from controller.viewscreen_controller.viewscreen_presenter import ViewscreenPresenter
from model.canvas.canvas_repository import CanvasRepository
from model.component.component_repository import ComponentRepository
from model.component.component_specification import ComponentSpecification
from model.component.socket.socket_repository import SocketRepository
from model.computation_unit.computation_unit_repository import ComputationUnitRepository
from model.graph.graph_repository import GraphRepository
from model.graph.graph_runners.python_graph_runner import GraphRunner
from model.identifiables.identifier_factory import IdentifierFactory
from model.module.graph_prototype.graph_prototype_repository import GraphPrototypeRepository
from model.module.module_specification import ModuleSpecification
from model.module.toolbox_item.toolbox_item_repository import ToolboxItemRepository

from helpers.xml.xml_helper import XmlHelper
from model.module.module_repository import ModuleRepository


class MindblocksController:

    canvas_repository = None
    view = None

    def __init__(self, view):
        self.identifier_factory = IdentifierFactory()
        self.xml_helper = XmlHelper()

        self.prototype_repository = ToolboxItemRepository()
        self.graph_prototype_repository = GraphPrototypeRepository()
        self.module_repository = ModuleRepository(self.prototype_repository, self.graph_prototype_repository)
        self.module_repository.load_basic_modules()

        self.computation_unit_repository = ComputationUnitRepository(self.identifier_factory)

        self.socket_repository = SocketRepository(self.identifier_factory)
        self.component_repository = ComponentRepository(self.identifier_factory, self.socket_repository, self.module_repository, self.xml_helper)

        self.graph_repository = GraphRepository(self.identifier_factory, self.component_repository, self.xml_helper)
        self.canvas_repository = CanvasRepository(self.identifier_factory, self.graph_repository, self.xml_helper)

        self.selection_presenter = SelectionPresenter(self.canvas_repository)
        self.view = view

        self.viewscreen_listener = ViewscreenListener(self.view,
                                                      self.canvas_repository,
                                                      self.component_repository,
                                                      self.graph_repository,
                                                      self.selection_presenter,
                                                      self.computation_unit_repository)
        self.viewscreen_presenter = ViewscreenPresenter(self.view, self.canvas_repository, self.selection_presenter)

        self.menubar_listener = MenubarListener(self.view.menubar, self.canvas_repository, self.selection_presenter)

        self.toolbox_listener = ToolboxListener(self.view.toolbox, self.selection_presenter)

        self.description_panel_presenter = DescriptionPanelPresenter(self.view.description_panel, self.selection_presenter)
        self.description_panel_listener = DescriptionPanelListener(self.view.description_panel, self.component_repository, self.socket_repository, self.selection_presenter)

        self.toolbox_presenter = ToolboxPresenter(self.view.toolbox, self.module_repository, self.canvas_repository)

        self.graph_to_prototype_mediator = GraphToGraphPrototypeMediator(self.graph_repository, self.graph_prototype_repository)
        self.canvas_to_graph_mediator = CanvasToGraphMediator(self.canvas_repository, self.graph_repository)

    def execute_graph(self, graph):
        runner = GraphRunner()
        return runner.run(graph, {})

    def create_new_canvas(self):
        canvas = self.canvas_repository.create_canvas()
        return canvas

    def update_toolbox(self):
        self.toolbox_presenter.update_toolbox(None)
