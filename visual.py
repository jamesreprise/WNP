import sys
import os
from plot import Plot
from bound import Bound
from fspl import fspl_min
from search.random_search import RandomSearch
from search.simulated_annealing import SimulatedAnnealing
from search.genetic_search import GeneticSearch
from search.bayesian_search import BayesianSearch
from PySide6 import QtCore, QtWidgets, QtGui

FUNCTION = fspl_min

class OptimiseGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.method = "None"
        self.bound = None
        self.bayes_radio = QtWidgets.QRadioButton("Bayesian Optimisation")
        self.sa_radio = QtWidgets.QRadioButton("Simulated Annealing")
        self.ga_radio = QtWidgets.QRadioButton("Genetic Search")
        self.random_radio = QtWidgets.QRadioButton("Random Search")

        self.start_button = QtWidgets.QPushButton("Optimise")
        self.file_button = QtWidgets.QPushButton("Choose File...")

        self.bayes_radio.toggled.connect(self.set_method)
        self.sa_radio.toggled.connect(self.set_method)
        self.ga_radio.toggled.connect(self.set_method)
        self.random_radio.toggled.connect(self.set_method)

        self.start_button.clicked.connect(self.optimise)
        self.file_button.clicked.connect(self.choose_file)

        self.layout = QtWidgets.QVBoxLayout(self)

        self.buttons = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.LeftToRight, None)
        self.buttons.addWidget(self.bayes_radio)
        self.buttons.addWidget(self.sa_radio)
        self.buttons.addWidget(self.ga_radio)
        self.buttons.addWidget(self.random_radio)

        
        self.image = QtWidgets.QLabel(self)
        self.image.setAlignment(QtCore.Qt.AlignCenter)
        self.image.resize(500, 500)
        self.image.setFrameStyle(QtWidgets.QFrame.Panel)
        # self.image.setFrameShadow(QtWidgets.QFrame.Raised)
        self.image.setLineWidth(1)

        self.layout.addWidget(self.image)
        
        self.layout.addWidget(self.file_button)
        self.layout.addWidget(self.start_button)
        self.layout.addLayout(self.buttons)
        
        self.setWindowTitle("Wireless Node Placement Optimisation")

    @QtCore.Slot()
    def set_method(self):
        button = self.sender()
        self.method = button.text()

    @QtCore.Slot()
    def optimise(self):
        if self.method == "None":
            error_msg = QtWidgets.QMessageBox.warning(self, "Error", "You haven't picked an optimisation method! Please pick one and try again.")
        elif self.bound == None:
            error_msg = QtWidgets.QMessageBox.warning(self, "Error", "You haven't picked a bounds file! Please pick one and try again.")
        else:
            optimisers = {
              "Random Search": RandomSearch(FUNCTION, self.bound), 
              "Simulated Annealing": SimulatedAnnealing(FUNCTION, self.bound),
              "Genetic Search": GeneticSearch(FUNCTION, self.bound),
              "Bayesian Optimisation": BayesianSearch(FUNCTION, self.bound)}

            opt = optimisers[self.method]
            result = opt.search()
            nodes = result[0]
            self.display_image(nodes)
            node_output = QtWidgets.QMessageBox()
            node_output.setWindowTitle(f"Result of {opt.name}")
            node_output.setText(f"Average FSPL is {result[1]}")
            node_output.setDetailedText(f"Nodes: \n {str(nodes)}")
            node_output.exec()

    @QtCore.Slot()
    def choose_file(self):
        button = self.sender()
        filename = QtWidgets.QFileDialog.getOpenFileName(self,
        "Open Bounds", os.path.expanduser("~"), "Bounds Files (*.bounds)")[0]
        if filename != "":
            try:
                self.bound = Bound.from_file(filename)
            except:
                error_msg = QtWidgets.QMessageBox.Critical(self, "Error", "Bounds file isn't valid, or we don't have permission to access this file.")
            if self.bound.node_count >= len(self.bound.points):
                error_msg = QtWidgets.QMessageBox.warning(self, "Warning", f"You're trying to place {self.bound.node_count} nodes to cover {len(self.bound.points)} sensors. Are you sure you want to do this?")
            button.setText(f"{self.bound.name} imported.")
            self.display_image([])

    def display_image(self, nodes):
        plot = Plot(nodes, self.bound)
        fig = plot.plot_space()
        if os.path.exists("temp.png"):
            os.remove("temp.png")
        fig.savefig("temp.png")
        picture = QtGui.QPixmap("temp.png")
        self.image.setPixmap(picture)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = OptimiseGUI()
    palette = widget.palette()
    palette.setColor(widget.backgroundRole(), QtCore.Qt.white)
    widget.setPalette(palette)
    widget.resize(700, 600)
    widget.show()

    sys.exit(app.exec_())