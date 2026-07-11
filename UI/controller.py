import flet as ft
from UI.view import View
from model.modello import Model

class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    # PUNTO 1a ----------------------------------------------------------
    def fillDDYear(self):
        years = self._model.getYears()

        yearssDD = list(map(lambda x: ft.dropdown.Option(x), years))
        self._view.ddyear.options = yearssDD

        self._view.update_page()
    # FINE PUNTO 1a ------------------------------------------------------

    # PUNTO 1b ----------------------------------------------------------
    def fillDDShape(self, e):

        year = int(self._view.ddyear.value)
        shapes = self._model.getShapesYear(year)

        shapesDD = list(map(lambda x: ft.dropdown.Option(x), shapes))
        self._view.ddshape.options = shapesDD

        self._view.update_page()
    # FINE PUNTO 1b ------------------------------------------------------

    # PUNTO 1c,d ----------------------------------------------------------
    def handle_graph(self, e):

        if self._view.ddyear.value is None:
            self._view.create_alert("Selezionare un anno!")
            return

        anno = int(self._view.ddyear.value)

        if self._view.ddshape.value is None or self._view.ddshape.value == "":
            self._view.create_alert("Selezionare una shape!")
            return

        forma = self._view.ddshape.value

        self._model.buildGraph(anno, forma)
        n = self._model.getNumNodes()
        m = self._model.getNumEdges()
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(ft.Text(f"Numero di nodi: {n}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {m}"))

        self._view.txt_result1.controls.append(
            ft.Text(f"Il grafo ha: {self._model.get_num_connesse()} componenti connesse"))

        connessa = self._model.getConnectedComponents()
        self._view.txt_result1.controls.append(ft.Text(f"La componente connessa più grande "
                                                       f"è costituita da {len(connessa)} nodi:"))

        for c in connessa:
            self._view.txt_result1.controls.append(ft.Text(c))

        self._view.update_page()
    # FINE PUNTO 1c,d ------------------------------------------------------

    def handle_path(self, e):
        pass
