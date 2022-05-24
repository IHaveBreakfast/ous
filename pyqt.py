from PyQt6.QtWidgets import QWidget, QTabWidget, QLabel, QPushButton, QMenuBar, QMenu, QGroupBox, QComboBox, \
    QMainWindow, QHBoxLayout, QLineEdit, QTableWidget, QTableWidgetItem, QCheckBox, QSpinBox, QDoubleSpinBox, \
    QRadioButton, QVBoxLayout, QPlainTextEdit
from PyQt6.QtCore import QRect, QCoreApplication, QMetaObject

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from networkx import draw, draw_networkx_labels, drawing

class pyqt(QMainWindow):
    def __init__(self, presenter):
        super().__init__()

        self.presenter = presenter

        self.setFixedSize(1280, 720)

        self.mainWidget = QWidget()
        self.mainWidget.setObjectName("mainWidget")

        self.tabWidget = QTabWidget(self.mainWidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 1280, 720))
        self.regulation = QWidget()
        self.regulation.setObjectName("regulation")
        self.results = QWidget()
        self.results.setObjectName("results")

        self.GraphGroup = QGroupBox(self.regulation)
        self.GraphGroup.setObjectName("graphGroupBox")
        self.GraphGroup.setGeometry(QRect(610, 0, 670, 700))

        self.fig = Figure(dpi = 100)
        self.fig.subplots_adjust(left=0.1, bottom=0.2, right=0.95, top=0.95)
        self.axes_fig = self.fig.add_subplot(111)
        self.axes_fig.axis('off')
        self.graph_plot = FigureCanvasQTAgg(self.fig)
        self.vbox = QHBoxLayout()
        self.vbox.addWidget(self.graph_plot)
        self.GraphGroup.setLayout(self.vbox)

        self.GraphSettingsGroup = QGroupBox(self.regulation)
        self.GraphSettingsGroup.setObjectName("GraphSettingsGroup")
        self.GraphSettingsGroup.setGeometry(QRect(0, 0, 610, 700))

        self.TopologyLabel = QLabel(self.GraphSettingsGroup)
        self.TopologyLabel.setObjectName("TopologyLabel")
        self.TopologyLabel.setGeometry(QRect(20, 20, 94, 16))

        self.TopologycomboBox = QComboBox(self.GraphSettingsGroup)
        self.TopologycomboBox.setObjectName("TopologycomboBox")
        self.TopologycomboBox.setGeometry(QRect(120, 18, 120, 22))

        self.TopologyButton = QPushButton(self.GraphSettingsGroup)
        self.TopologyButton.setObjectName("TopologyButton")
        self.TopologyButton.setGeometry(QRect(250, 18, 75, 22))
        self.TopologyButton.clicked.connect(self.CreateGraphClick)

        self.FirstNodelabel = QLabel(self.GraphSettingsGroup)
        self.FirstNodelabel.setObjectName("FirstNodelabel")
        self.FirstNodelabel.setGeometry(QRect(20, 84, 100, 16))

        self.FirstNodelineEdit = QLineEdit(self.GraphSettingsGroup)
        self.FirstNodelineEdit.setObjectName("FirstNodelineEdit")
        self.FirstNodelineEdit.setGeometry(QRect(70, 82, 130, 22))

        self.LastNodelabel = QLabel(self.GraphSettingsGroup)
        self.LastNodelabel.setObjectName("LastNodelabel")
        self.LastNodelabel.setGeometry(QRect(220, 84, 100, 16))

        self.LastNodelineEdit = QLineEdit(self.GraphSettingsGroup)
        self.LastNodelineEdit.setObjectName("LastNodelineEdit")
        self.LastNodelineEdit.setGeometry(QRect(270, 82, 130, 22))

        self.label_failure_node = QLabel(self.GraphSettingsGroup)
        self.label_failure_node.setObjectName("label_failure_node")
        self.label_failure_node.setGeometry(QRect(10, 144, 124, 16))

        self.failure_node_table = QTableWidget(self.GraphSettingsGroup)
        self.failure_node_table.setObjectName("failure_node_table")
        self.failure_node_table.setGeometry(QRect(0, 0, 0, 0))
        self.failure_node_table.setColumnCount(2)
        self.failure_node_table.setHorizontalHeaderLabels(["Узел", "Интенсивность отказа"])
        self.failure_node_table.setColumnWidth(0, 20)
        self.failure_node_table.setColumnWidth(1, 180)
        self.failure_node_table.resizeRowsToContents()

        self.label_length_connection = QLabel(self.GraphSettingsGroup)
        self.label_length_connection.setObjectName("label_length_connection")
        self.label_length_connection.setGeometry(QRect(10, 335, 130, 16))


        self.length_connection_table = QTableWidget(self.GraphSettingsGroup)
        self.length_connection_table.setObjectName("length_connection_table")
        self.length_connection_table.setGeometry(QRect(0, 0, 0, 0))
        self.length_connection_table.setColumnCount(2)
        self.length_connection_table.setHorizontalHeaderLabels(["Линия", "Длина"])
        self.length_connection_table.setColumnWidth(0, 50)
        self.length_connection_table.setColumnWidth(1, 180)
        self.length_connection_table.resizeRowsToContents()

        self.SpecificIntensitylabel = QLabel(self.GraphSettingsGroup)
        self.SpecificIntensitylabel.setObjectName("SpecificIntensitylabel")
        self.SpecificIntensitylabel.setGeometry(QRect(20, 50, 210, 16))

        self.SpecificIntensitylineEdit = QLineEdit(self.GraphSettingsGroup)
        self.SpecificIntensitylineEdit.setObjectName("SpecificIntensitylineEdit")
        self.SpecificIntensitylineEdit.setGeometry(QRect(250, 50, 80, 22))

        self.RecoverycheckBox = QCheckBox(self.GraphSettingsGroup)
        self.RecoverycheckBox.setObjectName("RecoverycheckBox")
        self.RecoverycheckBox.setGeometry(QRect(350, 50, 160, 20))

        self.CalculationButton = QPushButton(self.GraphSettingsGroup)
        self.CalculationButton.setObjectName("CalculationButton")
        self.CalculationButton.setGeometry(QRect(20, 390, 140, 20))
        self.CalculationButton.clicked.connect(self.CalculationClick)

        self.CountFailureslabel = QLabel(self.regulation)
        self.CountFailureslabel.setObjectName("CountFailureslabel")
        self.CountFailureslabel.setGeometry(QRect(20, 120, 170, 20))

        self.CountFailuresspinBox = QSpinBox(self.regulation)
        self.CountFailuresspinBox.setObjectName("CountFailuresspinBox")
        self.CountFailuresspinBox.setGeometry(QRect(140, 120, 100, 20))
        self.CountFailuresspinBox.setMaximum(999999)
        self.CountFailuresspinBox.setDisplayIntegerBase(10)

        self.RestoreTeamslabel = QLabel(self.regulation)
        self.RestoreTeamslabel.setObjectName("RestoreTeamslabel")
        self.RestoreTeamslabel.setGeometry(QRect(20, 160, 190, 20))

        self.RestoreTeamsspinBox = QSpinBox(self.regulation)
        self.RestoreTeamsspinBox.setObjectName("RestoreTeamsspinBox")
        self.RestoreTeamsspinBox.setGeometry(QRect(200, 160, 100, 20))

        self.IntensityRestorelabel = QLabel(self.regulation)
        self.IntensityRestorelabel.setObjectName("IntensityRestorelabel")
        self.IntensityRestorelabel.setGeometry(QRect(20, 200, 190, 20))

        self.IntensityRestorespinBox = QDoubleSpinBox(self.regulation)
        self.IntensityRestorespinBox.setObjectName("IntensityRestorespinBox")
        self.IntensityRestorespinBox.setGeometry(QRect(200, 200, 100, 20))
        #self.IntensityRestorespinBox.setMinimum(0.0001)
        self.IntensityRestorespinBox.setSingleStep(0.01)


        self.PoliticRestoreGroupBox = QGroupBox(self.regulation)
        self.PoliticRestoreGroupBox.setObjectName("PoliticRestoreGroupBox")
        self.PoliticRestoreGroupBox.setGeometry(QRect(20, 230, 140, 120))

        self.SaveChangesButton = QPushButton(self.regulation)
        self.SaveChangesButton.setObjectName("SaveChangesButton")
        self.SaveChangesButton.setGeometry(QRect(20, 360, 230, 20))
        self.SaveChangesButton.clicked.connect(self.SaveModeClick)

        self.PathsGroupBox = QGroupBox(self.regulation)
        self.PathsGroupBox.setObjectName("PathsGroupBox")
        self.PathsGroupBox.setGeometry(QRect(330, 540, 280, 150))

        self.MinTimelabel = QLabel(self.regulation)
        self.MinTimelabel.setObjectName("MinTimelabel")
        self.MinTimelabel.setGeometry(QRect(20, 540, 180, 20))

        self.SredTimelabel = QLabel(self.regulation)
        self.SredTimelabel.setObjectName("SredTimelabel")
        self.SredTimelabel.setGeometry(QRect(20, 570, 180, 20))

        self.MaxTimelabel = QLabel(self.regulation)
        self.MaxTimelabel.setObjectName("MaxTimelabel")
        self.MaxTimelabel.setGeometry(QRect(20, 600, 180, 20))

        self.SredTimeRestorelabel = QLabel(self.regulation)
        self.SredTimeRestorelabel.setObjectName("SredTimeRestorelabel")
        self.SredTimeRestorelabel.setGeometry(QRect(20, 630, 180, 20))

        self.CoefReadylabel = QLabel(self.regulation)
        self.CoefReadylabel.setObjectName("CoefReadylabel")
        self.CoefReadylabel.setGeometry(QRect(20, 660, 150, 20))

        self.MinTimelineEdit = QLineEdit(self.regulation)
        self.MinTimelineEdit.setObjectName("MinTimelineEdit")
        self.MinTimelineEdit.setGeometry(QRect(175, 540, 150, 20))
        self.MinTimelineEdit.setReadOnly(True)

        self.SredTimelineEdit = QLineEdit(self.regulation)
        self.SredTimelineEdit.setObjectName("SredTimelineEdit")
        self.SredTimelineEdit.setGeometry(QRect(175, 570, 150, 20))
        self.SredTimelineEdit.setReadOnly(True)

        self.MaxTimelineEdit = QLineEdit(self.regulation)
        self.MaxTimelineEdit.setObjectName("MaxTimelineEdit")
        self.MaxTimelineEdit.setGeometry(QRect(175, 600, 150, 20))
        self.MaxTimelineEdit.setReadOnly(True)

        self.SredTimeRestorelineEdit = QLineEdit(self.regulation)
        self.SredTimeRestorelineEdit.setObjectName("SredTimeRestorelineEdit")
        self.SredTimeRestorelineEdit.setGeometry(QRect(175, 630, 150, 20))
        self.SredTimeRestorelineEdit.setReadOnly(True)

        self.CoefReadylineEdit = QLineEdit(self.regulation)
        self.CoefReadylineEdit.setObjectName("CoefReadylineEdit")
        self.CoefReadylineEdit.setGeometry(QRect(175, 660, 150, 20))
        self.CoefReadylineEdit.setReadOnly(True)

        self.politics = QWidget(self.PoliticRestoreGroupBox)
        self.politics.setObjectName("politics")
        self.politics.setGeometry(QRect(20, 20, 90, 90))

        self.PoliticLayout = QVBoxLayout(self.politics)
        self.PoliticLayout.setSpacing(5)
        self.PoliticLayout.setObjectName("PoliticLayout")
        self.PoliticLayout.setContentsMargins(0, 0, 0, 0)

        self.FASTradioButton = QRadioButton(self.politics)
        self.FASTradioButton.setObjectName("FASTradioButton")
        self.PoliticLayout.addWidget(self.FASTradioButton)

        self.LONGradioButton = QRadioButton(self.politics)
        self.LONGradioButton.setObjectName("LONGradioButton")
        self.PoliticLayout.addWidget(self.LONGradioButton)

        self.FIFOradioButton = QRadioButton(self.politics)
        self.FIFOradioButton.setObjectName("FIFOradioButton")
        self.PoliticLayout.addWidget(self.FIFOradioButton)

        self.LIFOradioButton = QRadioButton(self.politics)
        self.LIFOradioButton.setObjectName("LIFOradioButton")
        self.PoliticLayout.addWidget(self.LIFOradioButton)

        self.PathsTextEdit = QPlainTextEdit(self.PathsGroupBox)
        self.PathsTextEdit.setObjectName("PathsTextEdit")
        self.PathsTextEdit.setGeometry(QRect(5, 20, 270, 124))
        self.PathsTextEdit.setReadOnly(True)
##################################################################ПИВО#####################################################
        self.ProbCalcGroupBox = QGroupBox(self.results)
        self.ProbCalcGroupBox.setObjectName("ProbCalcGroupBox")
        self.ProbCalcGroupBox.setGeometry(QRect(20, 20, 330, 200))

        self.ProbCalcplainTextEdit = QPlainTextEdit(self.ProbCalcGroupBox)
        self.ProbCalcplainTextEdit.setObjectName("ProbCalcplainTextEdit")
        self.ProbCalcplainTextEdit.setGeometry(QRect(0, 0, 330, 300))
        self.ProbCalcplainTextEdit.setReadOnly(True)

        self.ChartProbGroupBox = QGroupBox(self.results)
        self.ChartProbGroupBox.setObjectName("ChartProbGroupBox")
        self.ChartProbGroupBox.setGeometry(QRect(0, 0, 0, 0))

        self.FigureChartProb = Figure(dpi = 100)
        self.FigureChartProb.subplots_adjust(left=0.1, bottom=0.2, right=0.95, top=0.95)
        self.ChartProbAxes = self.FigureChartProb.add_subplot(111)
        self.ChartProbAxes.set_xlabel('t, ч')
        self.ChartProbAxes.set_ylabel('P(t)')
        self.ChartProbplot = FigureCanvasQTAgg(self.FigureChartProb)
        self.vbox_ChartProb = QHBoxLayout()
        self.vbox_ChartProb.addWidget(self.ChartProbplot)
        self.ChartProbGroupBox.setLayout(self.vbox_ChartProb)

        self.RecoveryChartGroupBox = QGroupBox(self.results)
        self.RecoveryChartGroupBox.setObjectName("RecoveryChartGroupBox")
        self.RecoveryChartGroupBox.setGeometry(QRect(700, 370, 550, 350))

        self.FigureRecoveryChart = Figure(dpi = 100)
        self.FigureRecoveryChart.subplots_adjust(left=0.1, bottom=0.2, right=0.95, top=0.95)
        self.RecoveryChartAxes = self.FigureRecoveryChart.add_subplot(111)
        self.RecoveryChartplot = FigureCanvasQTAgg(self.FigureRecoveryChart)
        self.RecoveryChartAxes.set_xlabel('t, ч')
        self.vbox_RecoveryChart = QHBoxLayout()
        self.vbox_RecoveryChart.addWidget(self.RecoveryChartplot)
        self.RecoveryChartGroupBox.setLayout(self.vbox_RecoveryChart)

        self.FailureGroupBox = QGroupBox(self.results)
        self.FailureGroupBox.setObjectName("FailureGroupBox")
        self.FailureGroupBox.setGeometry(QRect(700, 20, 550, 350))

        self.FigureFailure = Figure(dpi=100)
        self.FigureFailure.subplots_adjust(left=0.1, bottom=0.2, right=0.95, top=0.95)
        self.FigureAxes = self.FigureFailure.add_subplot(111)
        self.FigureAxes.set_xlabel('t, ч')
        self.FigureAxes.set_ylabel('P(t)')
        self.Failureplot = FigureCanvasQTAgg(self.FigureFailure)
        self.vbox_Failure = QHBoxLayout()
        self.vbox_Failure.addWidget(self.Failureplot)
        self.FailureGroupBox.setLayout(self.vbox_Failure)

        self.tabWidget.addTab(self.regulation, "")
        self.tabWidget.addTab(self.results, "")
        self.setCentralWidget(self.mainWidget)

        self.Interface()
        self.tabWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(self)

    def Interface(self):
        self.setWindowTitle(QCoreApplication.translate("pyqt", "Отказ.уст.сист.", None))
        self.TopologyLabel.setText(QCoreApplication.translate("pyqt", "Тип топологии: ", None))
        self.TopologyButton.setText(QCoreApplication.translate("pyqt", "Построить", None))
        self.FirstNodelabel.setText(QCoreApplication.translate("pyqt", "От узла: ", None))
        self.LastNodelabel.setText(QCoreApplication.translate("pyqt", "До узла: ", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.regulation), QCoreApplication.translate("pyqt", "Настройка", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.results), QCoreApplication.translate("pyqt", "Графики", None))
        self.SpecificIntensitylabel.setText(QCoreApplication.translate("pyqt", "Удельная интенсивность отказа связи:"))
        self.RecoverycheckBox.setText(QCoreApplication.translate("pyqt", "Восстановление"))
        self.CalculationButton.setText(QCoreApplication.translate("pyqt", "Рассчёт"))
        self.CountFailureslabel.setText(QCoreApplication.translate("pyqt", "Количество отказов:", None))
        self.RestoreTeamslabel.setText(QCoreApplication.translate("pyqt", "Количество ремонтных бригад:", None))
        self.IntensityRestorelabel.setText(QCoreApplication.translate("pyqt", "Интенсивность восстановления:", None))
        self.FASTradioButton.setText(QCoreApplication.translate("pyqt", "FAST_FIRST", None))
        self.LONGradioButton.setText(QCoreApplication.translate("pyqt", "LONG_FIRST", None))
        self.FIFOradioButton.setText(QCoreApplication.translate("pyqt", "FIFO", None))
        self.LIFOradioButton.setText(QCoreApplication.translate("pyqt", "LIFO", None))
        self.SaveChangesButton.setText(QCoreApplication.translate("pyqt", "Сохранить изменения восстановления", None))
        self.MinTimelabel.setText(QCoreApplication.translate("pyqt", "Мин. время до отказа:", None))
        self.SredTimelabel.setText(QCoreApplication.translate("pyqt", "Ср. время до отказа:", None))
        self.MaxTimelabel.setText(QCoreApplication.translate("pyqt", "Макс. время до отказа:", None))
        self.SredTimeRestorelabel.setText(QCoreApplication.translate("pyqt", "Ср. время восстановления:", None))
        self.CoefReadylabel.setText(QCoreApplication.translate("pyqt", "Коэффициент готовности:", None))
        self.PathsGroupBox.setTitle(QCoreApplication.translate("pyqt", "Доступные пути", None))
        self.FailureGroupBox.setTitle(QCoreApplication.translate("pyqt", "Гистограмма времён отказов", None))
        self.ChartProbGroupBox.setTitle(QCoreApplication.translate("pyqt", "Зависимость вероятности безотказной работы системы от времени", None))
        self.RecoveryChartGroupBox.setTitle(QCoreApplication.translate("pyqt", "Диаграмма восстановления", None))

    def CreateGraphClick(self):
        choice = self.TopologycomboBox.currentText()
        self.presenter.building_graph_topology(choice)

    def SaveModeClick(self):
        mode = None
        if self.FASTradioButton.isChecked():
            mode = 'FAST_FIRST'
        elif self.LONGradioButton.isChecked():
            mode = 'LONG_FIRST'
        elif self.FIFOradioButton.isChecked():
            mode = 'FIFO'
        elif self.LIFOradioButton.isChecked():
            mode = 'FIFO'
        self.presenter.save_settings(self.CountFailuresspinBox.value(),
                                     self.RestoreTeamsspinBox.value(),
                                     self.IntensityRestorespinBox.value(),
                                     mode)

    def CalculationClick(self):
        node_list = dict()
        bind_list = dict()
        for i in range(self.failure_node_table.rowCount()):
            try:
                node_list[self.failure_node_table.item(i,0).text()] = self.failure_node_table.item(i, 1).text()
            except:
                node_list = None
        for i in range(self.length_connection_table.rowCount()):
            try:
                bind_list[self.length_connection_table.item(i,0).text()] = self.length_connection_table.item(i, 1).text()
            except:
                bind_list = None
        if not self.FirstNodelineEdit.text() or not self.LastNodelineEdit.text() or not node_list \
                or not bind_list or not self.SpecificIntensitylineEdit.text():
            pass
        else:
            self.presenter.start_modeling(self.FirstNodelineEdit.text(), self.LastNodelineEdit.text(),
                                          node_list, bind_list, self.SpecificIntensitylineEdit.text(),
                                          self.RecoverycheckBox.isChecked())

    def GraphsList(self, graphs):
        self.TopologycomboBox.addItems(graphs)

    def DrawGraph(self, graph, labels):
        self.axes_fig.cla()
        pos = drawing.spring_layout(graph)
        draw(graph, pos, self.axes_fig)
        draw_networkx_labels(graph, pos, labels=labels, ax=self.axes_fig)
        self.graph_plot.draw()

    def NodesTable(self, failure_nodes):
        for index, node in enumerate(failure_nodes):
            self.failure_node_table.insertRow(index)
            self.failure_node_table.setItem(index, 0, QTableWidgetItem(node.bind))
            self.failure_node_table.setItem(index, 1, QTableWidgetItem(str(node.intensity)))

    def BindsTable(self, binds):
        for index, bind in enumerate(binds):
            self.length_connection_table.insertRow(index)
            self.length_connection_table.setItem(index, 0, QTableWidgetItem(bind.bind))
            self.length_connection_table.setItem(index, 1, QTableWidgetItem(str(bind.length)))

    def set_settings(self, settings):
        self.CountFailuresspinBox.setValue(settings[0])
        self.RestoreTeamsspinBox.setValue(settings[1])
        self.IntensityRestorespinBox.setValue(settings[2])
        if settings[3] == 'FAST_FIRST':
            self.FASTradioButton.setChecked(True)
        elif settings[3] == 'LONG_FIRST':
            self.LONGradioButton.setChecked(True)
        elif settings[3] == 'FIFO':
            self.FIFOradioButton.setChecked(True)
        elif settings[3] == 'LIFO':
            self.LIFOradioButton.setChecked(True)

    def Result(self, result):
        self.MinTimelineEdit.setText(str(result[0]))
        self.MaxTimelineEdit.setText(str(result[1]))
        self.SredTimelineEdit.setText(str(result[2]))
        if result[3] is not None and result[4] is not None:
            self.SredTimeRestorelineEdit.setText(str(result[3]))
            self.CoefReadylineEdit.setText(str(result[4]))

    def Histogram(self, histogram_failure, restore):
        width = 0.7 * (histogram_failure[1][1] - histogram_failure[1][0])
        if not restore:
            self.FigureAxes.cla()
            self.FigureAxes.bar((histogram_failure[1][:-1] + histogram_failure[1][1:]) / 2, histogram_failure[0],
                                width=width)
            self.Failureplot.draw()
        else:
            self.RecoveryChartAxes.cla()
            self.RecoveryChartAxes.bar((histogram_failure[1][:-1] + histogram_failure[1][1:]) / 2, histogram_failure[0],
                                       width=width)
            self.RecoveryChartplot.draw()

    def Paths(self, path, labels):
        self.PathsTextEdit.clear()
        for item in path:
            string = ''
            length = len(item) - 1
            for num in item:
                if item.index(num) == length:
                    string = string + labels[num]
                else:
                    string = string + f"{labels[num]}-"
            self.PathsTextEdit.appendPlainText(string)

    def ProbChart(self, data):
        self.ChartProbAxes.cla()
        self.ChartProbAxes.plot(data[1], data[0], 'r')

    def ProbFormula(self, data):
        self.ProbCalcplainTextEdit.clear()
        common_formula_string = "P(t) = 1 - "
        for item in data:
            formula_string = f"P{data.index(item)}(t) = e^-("
            local_formula_string = "(1 - e^-("
            object_string = ""
            for obj in item:
                index_obg = item.index(obj)
                if index_obg is not item.index(item[-1]):
                    object_string += u"\u03BB" + obj[0] + "+"
                else:
                    object_string += u"\u03BB" + obj[0] + ") * t"
            formula_string += object_string
            local_formula_string += object_string
            if data.index(item) is data.index(data[-1]):
                local_formula_string += ") "
            else:
                local_formula_string += ") * "
            common_formula_string += local_formula_string
            self.ProbCalcplainTextEdit.appendPlainText(formula_string)
        self.ProbCalcplainTextEdit.appendPlainText(common_formula_string)