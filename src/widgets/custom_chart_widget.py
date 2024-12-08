from typing import Optional, Dict, List, Any
from PySide6.QtCharts import QChart, QChartView, QBarSet, QBarSeries
from PySide6.QtCharts import QBarCategoryAxis, QValueAxis
from PySide6.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QToolTip
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QPainter, QImage
from utils.utils_db import EnumEjes
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import numpy as np

class CustomChartWidget(QScrollArea):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        # Configurar el scroll
        self.setWidgetResizable(True)
        self._chart_container = QWidget()
        self._layout = QVBoxLayout(self._chart_container)
        self.setWidget(self._chart_container)

        # Crear el gráfico y añadirlo al contenedor
        self._chart = QChart()
        self._chart_view = QChartView(self._chart)
        self._chart_view.setRenderHint(QPainter.Antialiasing)
        self._layout.addWidget(self._chart_view)

        # Configuración inicial
        self._set_empty_chart()

    def _clean_data(self, data: Dict[str, List[Any]]) -> Dict[str, List[int]]:
        """
        Limpia los datos eliminando valores no finitos y convirtiéndolos a enteros.
        """
        cleaned_data = {}
        for key, values in data.items():
            values_array = np.array(values, dtype=np.float64)
            valid_values = np.where(np.isfinite(values_array), values_array, 0)
            cleaned_data[key] = valid_values.astype(int).tolist()
        return cleaned_data

    def _set_data(self, data: Dict[str, Any]) -> None:
        """
        Configura el gráfico con los datos proporcionados.
        """
        eje_x: List[str] = data.get(EnumEjes.EJE_X.value, [])
        barritas_datos: Dict[str, List[Any]] = data.get(EnumEjes.EJE_Y.value, {})

        self._set_empty_chart()
        self._chart.removeAllSeries()
        self._chart.setTitle("Gráfico de ventas por Videojuego")

        if not eje_x or not any(barritas_datos.values()):
            self._set_empty_chart()
            return

        bar_series = QBarSeries()
        for name, values in barritas_datos.items():
            cleaned_values = [
                value if value is not None and np.isfinite(value) else 0
                for value in values
            ]

            if len(cleaned_values) != len(eje_x):
                print(f"Advertencia: El tamaño de los datos de '{name}' no coincide con las categorías del eje X.")
                continue

            bar_set = QBarSet(name)
            bar_set.append(cleaned_values)
            bar_set.hovered.connect(lambda status, index, bar_set=bar_set: self._show_tooltip(status, index, bar_set))
            bar_series.append(bar_set)

        if not bar_series.barSets():
            self._set_empty_chart()
            return

        self._chart.addSeries(bar_series)
        self._configure_axes(eje_x, bar_series)

    def _configure_axes(self, eje_x: List[str], bar_series: QBarSeries) -> None:
        """
        Configura los ejes del gráfico.
        """
        axis_x = QBarCategoryAxis()
        axis_x.append(eje_x)
        axis_x.setLabelsAngle(-90)
        self._chart.setAxisX(axis_x, bar_series)

        all_values = [
            bar_set.at(i)
            for bar_set in bar_series.barSets()
            for i in range(bar_set.count())
        ]
        finite_values = [v for v in all_values if np.isfinite(v)]

        if finite_values:
            min_y = min(finite_values)
            max_y = max(finite_values)
        else:
            print("Advertencia: No hay valores válidos para el eje Y. Configurando rango predeterminado.")
            min_y, max_y = 0, 1

        axis_y = QValueAxis()
        axis_y.setRange(min_y, max_y)
        axis_y.setTitleText("Valores")
        self._chart.setAxisY(axis_y, bar_series)

        self._chart_view.setMinimumWidth(len(eje_x) * 100)

    def _set_empty_chart(self) -> None:
        """
        Configura el gráfico como vacío.
        """
        self._chart.removeAllSeries()
        self._chart.setTitle("Sin datos disponibles")

        axis_x = QBarCategoryAxis()
        axis_x.append(["Sin datos"])
        self._chart.setAxisX(axis_x)

        axis_y = QValueAxis()
        axis_y.setTitleText("Valores")
        self._chart.setAxisY(axis_y)

    def clear_chart(self) -> None:
        """
        Limpia el gráfico actual.
        """
        self._set_empty_chart()

    def _show_tooltip(self, status: bool, index: int, bar_set: QBarSet) -> None:
        """
        Muestra un tooltip cuando se pasa el ratón sobre un elemento del gráfico.
        """
        if status:
            try:
                value = bar_set.at(index)
                categories = self._chart.axisX().categories()
                if index < len(categories):
                    category = categories[index]
                    QToolTip.showText(
                        self.mapToGlobal(self._chart_view.pos() + QPoint(10, 10)),
                        f"{category}: {value}"
                    )
            except (IndexError, ValueError):
                print(f"Invalid index {index} for tooltip.")

    def export_to_pdf(self, file_path: str) -> None:
        """
        Exporta el gráfico a un archivo PDF.
        """
        if not file_path.lower().endswith(".pdf"):
            raise ValueError("The file path must end with .pdf")

        chart_image = QImage(self._chart_view.size(), QImage.Format_ARGB32)
        chart_image.fill(Qt.transparent)

        painter = QPainter(chart_image)
        self._chart_view.render(painter)
        painter.end()

        temp_image_path = file_path.replace(".pdf", ".png")
        chart_image.save(temp_image_path)

        pdf_canvas = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter

        pdf_canvas.setFont("Helvetica-Bold", 16)
        pdf_canvas.drawString(30, height - 50, "Chart Export")
        pdf_canvas.drawImage(temp_image_path, 30, 100, width - 60, height - 200)
        pdf_canvas.save()

        os.remove(temp_image_path)

    def get_chart_image_path(self) -> str:
        """
        Obtiene la ruta de la imagen del gráfico en el sistema de archivos.
        """
        temp_image_path = "chart_export.png"
        chart_image = QImage(self._chart_view.size(), QImage.Format_ARGB32)
        chart_image.fill(Qt.transparent)

        painter = QPainter(chart_image)
        self._chart_view.render(painter)
        painter.end()

        chart_image.save(temp_image_path)
        return temp_image_path
