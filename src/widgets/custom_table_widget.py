"""
* WEBGRAFÍA *

- QTableView Class. (s. f.). Doc.qt.io. de https://doc.qt.io/qtforpython-6.7/PySide6/QtWidgets/QTableView.html#PySide6.QtWidgets.QTableView

- QStandardItemModel Class. (s. f.). Doc.qt.io. de https://doc.qt.io/qtforpython-6.7/PySide6/QtGui/QStandardItemModel.html#PySide6.QtGui.QStandardItemModel

- QStandardItem Class. (s. f.). Doc.qt.io. de https://doc.qt.io/qtforpython-6.7/PySide6/QtGui/QStandardItem.html#PySide6.QtGui.QStandardItem

"""

# Archivo: src\widgets\custom_table_widget.py

from PySide6.QtWidgets import QTableView
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class CustomTableWidget(QTableView):
    """
    Widget personalizado para mostrar tablas utilizando QTableView.
    Recibe datos en forma de diccionario y los renderiza automáticamente.
    """

    def _init_(self, data=None, parent=None):
        """
        Inicializa el widget de tabla y, opcionalmente, configura los datos iniciales.

        Parámetros:
        - data (dict | None): Diccionario que contiene los datos iniciales para la tabla.
          - "columns" (list[str]): Lista de nombres de las columnas.
          - "data" (list[dict]): Lista de filas, donde cada fila es un diccionario con clave/valor.
        - parent (QWidget | None): Widget padre opcional.
        """
        super()._init_(parent)

        # Inicializamos el modelo interno
        self._model = QStandardItemModel()
        self.setModel(self._model)

        # Si se proporcionan datos, configuramos la tabla
        if data:
            self._set_data(data)
    # _init_ (fin)

    def _set_data(self, data):
        """
        Configura los datos en la tabla.

        Parámetros:
        - data (dict): Diccionario que contiene:
          - "columns" (list[str]): Lista de nombres de las columnas.
          - "data" (list[dict]): Lista de filas, donde cada fila es un diccionario con clave/valor.

        Si los datos no son válidos o no contienen las claves requeridas, el método no realiza cambios.
        """
        if not data or not isinstance(data, dict):
            print("[ERROR] Los datos proporcionados no son válidos. Se esperaba un diccionario con 'columns' y 'data'.")
            return

        # Configurar columnas
        columns = data.get("columns", [])
        if not columns:
            print("[ERROR] No se encontraron columnas en los datos proporcionados.")
            return
        self._model.setHorizontalHeaderLabels(columns)

        # Limpiar filas actuales y agregar nuevas
        self._model.clear()
        for row in data.get("data", []):
            items = [QStandardItem(str(row.get(col, ""))) for col in columns]
            self._model.appendRow(items)

        # Ajustar el tamaño de las columnas automáticamente
        self.resizeColumnsToContents()
    # _set_data (fin)
    def export_table_to_pdf(self, file_path: str) -> None:
        """
        Exports the table data to a PDF file.

        Parameters:
        - file_path (str): Path where the PDF file will be saved.

        Raises:
        - ValueError: If the provided file_path is not a valid PDF file.
        """
        if not file_path.lower().endswith(".pdf"):
            raise ValueError("The file path must end with .pdf")

        # Get data from the model
        column_count = self._model.columnCount()
        row_count = self._model.rowCount()

        if column_count == 0 or row_count == 0:
            raise ValueError("The table has no data to export.")

        # Fetch column headers
        headers = [self._model.headerData(col, Qt.Horizontal) for col in range(column_count)]

        # Fetch row data
        data = [
            [self._model.item(row, col).text() if self._model.item(row, col) else "" for col in range(column_count)]
            for row in range(row_count)
        ]

        # Create a PDF and write the table data
        pdf_canvas = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter

        pdf_canvas.setFont("Helvetica-Bold", 14)
        pdf_canvas.drawString(30, height - 30, "Exported Table Data")

        pdf_canvas.setFont("Helvetica", 10)
        x_start = 30
        y_start = height - 60
        line_height = 20

        # Write the headers
        y = y_start
        pdf_canvas.drawString(x_start, y, " | ".join(headers))
        y -= line_height
        pdf_canvas.drawString(x_start, y, "-" * 100)

        # Write the rows
        for row in data:
            y -= line_height
            if y < 40:  # Start a new page if the content goes below the margin
                pdf_canvas.showPage()
                y = height - 40
            pdf_canvas.drawString(x_start, y, " | ".join(row))

        pdf_canvas.save()
# CustomTableWidget (fin)