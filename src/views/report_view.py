from PySide6.QtWidgets import (
    QGridLayout, QWidget, QTableView, QLineEdit, QComboBox,
    QLabel, QSizePolicy, QPushButton, QFileDialog
)
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QIcon
from widgets.custom_chart_widget import CustomChartWidget
from utils import utils_sizes, utils_path, utils_estilos
from fpdf import FPDF  # Biblioteca para la creación de PDF

class ReportView(QWidget):
    """
    Clase encargada de gestionar la interfaz de usuario para la visualización de informes.
    """
    apply_filters_signal = Signal(str, str)  # Señal para emitir texto de búsqueda y categoría

    def __init__(self):
        """
        Inicializa la vista de informes, configurando filtros, tabla de datos y gráficos.
        """
        super().__init__()

        # Configuración de la ventana
        self.setMinimumSize(
            utils_sizes.SIZE_MINIMUM_WIDTH_WIDGET,
            utils_sizes.SIZE_MINIMUM_HEIGHT_WIDGET
        )

        # Inicialización de componentes principales
        self._init_filters()
        self._init_table()
        self._init_summary()
        self._init_pdf_buttons()  # Nuevos botones PDF

        # Inicializar gráfico
        self.chart_widget = CustomChartWidget()
        self.chart_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Configuración del diseño principal
        main_layout = QGridLayout()
        main_layout.addLayout(self.filters_layout, 0, 0, 1, 2)
        main_layout.addWidget(self.table_view, 1, 0, 1, 2)
        main_layout.addWidget(self.summary_label, 2, 0, 1, 1)
        main_layout.addWidget(self.chart_widget, 3, 0, 1, 2)  # Añadir gráfico al diseño
        main_layout.addWidget(self.pdf_table_button, 4, 0)  # Botón PDF Tabla
        main_layout.addWidget(self.pdf_chart_button, 4, 1)  # Botón PDF Gráfico

        # Ajustes de márgenes y espaciado
        main_layout.setContentsMargins(
            utils_sizes.MARGIN_10, utils_sizes.MARGIN_10,
            utils_sizes.MARGIN_10, utils_sizes.MARGIN_10
        )
        main_layout.setHorizontalSpacing(utils_sizes.MARGIN_10)
        main_layout.setVerticalSpacing(utils_sizes.MARGIN_10)

        # Establecemos el diseño en la ventana
        self.setLayout(main_layout)

    def _init_filters(self):
        """
        Inicializa los filtros de búsqueda y selección de categorías.
        """
        self.filters_layout = QGridLayout()

        # Barra de búsqueda
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar videojuegos...")
        self.search_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.filters_layout.addWidget(QLabel("Buscar:"), 0, 0)
        self.filters_layout.addWidget(self.search_input, 0, 1)

        # Conectar búsqueda en tiempo real
        self.search_input.textChanged.connect(self._emit_apply_filters_signal)

        # Selector de categoría
        self.category_select = QComboBox()
        self.category_select.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.filters_layout.addWidget(QLabel("Categoría:"), 1, 0)
        self.filters_layout.addWidget(self.category_select, 1, 1)

        # Botón para aplicar filtros
        self.apply_filter_button = QPushButton("Aplicar Filtros")
        self.apply_filter_button.setIcon(QIcon(utils_path.SEARCH_ICON_PATH))
        self.apply_filter_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.filters_layout.addWidget(self.apply_filter_button, 2, 1)

        # Conectar botón a la señal de filtros
        self.apply_filter_button.clicked.connect(self._emit_apply_filters_signal)

    def _init_table(self):
        """
        Configura la tabla de datos para mostrar los resultados.
        """
        self.table_view = QTableView()
        self.table_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

    def _init_summary(self):
        """
        Configura el resumen de datos, incluyendo el total de elementos y la suma total.
        """
        self.summary_label = QLabel("Total de elementos: 0, Suma total: 0")
        self.summary_label.setAlignment(Qt.AlignLeft)

    def _init_pdf_buttons(self):
        """
        Inicializa los botones de PDF con estilos personalizados.
        """
        # Botón de exportar tabla a PDF
        self.pdf_table_button = QPushButton("PDF Tabla")
        self.pdf_table_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.pdf_table_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; /* Color base */
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049; /* Color al pasar el mouse */
            }
            QPushButton:pressed {
                background-color: #367a3b; /* Color al presionar */
            }
        """)
        self.pdf_table_button.clicked.connect(self._export_table_to_pdf)

        # Botón de exportar gráfico a PDF
        self.pdf_chart_button = QPushButton("PDF Gráfico")
        self.pdf_chart_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.pdf_chart_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; /* Color base */
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049; /* Color al pasar el mouse */
            }
            QPushButton:pressed {
                background-color: #367a3b; /* Color al presionar */
            }
        """)
        self.pdf_chart_button.clicked.connect(self._export_chart_to_pdf)

    @Slot()
    def _export_table_to_pdf(self):
        """
        Exporta la tabla de datos a un archivo PDF.
        """
        file_dialog = QFileDialog(self, "Guardar archivo PDF", "", "PDF Files (*.pdf)")
        if file_dialog.exec_():
            pdf_path = file_dialog.selectedFiles()[0]

            # Agregar extensión .pdf si no está presente
            if not pdf_path.lower().endswith('.pdf'):
                pdf_path += '.pdf'

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            # Obtener el modelo de la tabla
            model = self.table_view.model()
            for row in range(model.rowCount()):
                for column in range(model.columnCount()):
                    item = model.item(row, column)
                    pdf.cell(40, 10, str(item.text()), border=1)
                pdf.ln()

            pdf.output(pdf_path)
            print(f"Archivo PDF guardado en: {pdf_path}")

    @Slot()
    def _export_chart_to_pdf(self):
        """
        Exporta el gráfico a un archivo PDF.
        """
        file_dialog = QFileDialog(self, "Guardar archivo PDF", "", "PDF Files (*.pdf)")
        if file_dialog.exec_():
            pdf_path = file_dialog.selectedFiles()[0]

            # Agregar extensión .pdf si no está presente
            if not pdf_path.lower().endswith('.pdf'):
                pdf_path += '.pdf'

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            # Aquí asumiendo que get_chart_image_path es un método que retorna la imagen del gráfico
            chart_image_path = self.chart_widget.get_chart_image_path()
            if chart_image_path:
                pdf.image(chart_image_path, x=10, y=20, w=180, h=100)  # Ajustar coordenadas y tamaño de la imagen

            pdf.output(pdf_path)
            print(f"Archivo PDF guardado en: {pdf_path}")

    @Slot()
    def _emit_apply_filters_signal(self):
        """
        Emite la señal de aplicar filtros con los valores actuales de búsqueda y categoría.
        """
        search_text = self.search_input.text()
        category = self.category_select.currentText()
        self.apply_filters_signal.emit(search_text, category)

    def _set_model(self, model):
        """
        Establece el modelo de datos en el QTableView y ajusta las columnas.

        Parámetros:
        - model (QStandardItemModel): Modelo de datos compatible con QTableView.
        """
        self.table_view.setModel(model)
        self.table_view.resizeColumnsToContents()

    def _set_genres(self, categories):
        """
        Llena el combo box de categorías con los valores recibidos.

        Parámetros:
        - categories (list[str]): Lista de categorías obtenidas desde el controlador.
        """
        self.category_select.clear()
        #self.category_select.addItem("Todas")  # Añadir opción predeterminada
        self.category_select.addItems(categories)

    def _set_chart(self, data):
        """
        Configura el gráfico utilizando el widget CustomChartWidget.

        Parámetros:
        - data (dict): Datos para el gráfico en el formato esperado por CustomChartWidget.
        """
        self.chart_widget._set_data(data)

    def _update_summary(self, total_products: int, total_price: float):
        """
        Actualiza la etiqueta del resumen con la cantidad total de productos y la suma total de precios.

        Parámetros:
        - total_products (int): Número total de productos.
        - total_price (float): Suma total de los precios de los productos.
        """
        self.summary_label.setText(f"Total de elementos: {total_products}, Suma total: {total_price:.2f}")
