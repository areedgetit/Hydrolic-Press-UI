from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QPushButton
from PyQt6.QtGui import QColor, QPainter, QPen, QFont, QPolygon
from PyQt6.QtCore import Qt, QPoint, QRect
from math import cos, sin, radians
import sys

class CircularGauge(QWidget):
    def __init__(self, max_value=5000):
        super().__init__()
        self.max_value = max_value
        self.current_value = 0
        self.setMinimumSize(300, 300)

    def set_value(self, value):
        self.current_value = max(0, min(value, self.max_value))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()
        radius = min(width, height) // 2 - 20
        center = QPoint(width // 2, height // 2)

        # Save the current state of the painter
        painter.save()

        # Draw everything except the needle
        self.draw_gauge(painter, center, radius)
        self.draw_ticks_and_labels(painter, center, radius)

        # Restore the painter state
        painter.restore()

        # Now draw the needle on top of everything
        self.draw_needle(painter, center, radius)

    def draw_gauge(self, painter, center, radius):
        # Draw the gauge circle
        painter.setPen(QPen(QColor(0, 0, 0), 5))
        painter.drawEllipse(center, radius, radius)

        # Draw the gauge arc
        start_angle = 230 * 16  # Start from 0 at 230 degrees
        span_angle = -int(self.current_value / self.max_value * 270 * 16)
        painter.setPen(QPen(QColor(0, 255, 0), 8))
        painter.drawArc(center.x() - radius, center.y() - radius, radius * 2, radius * 2, start_angle, span_angle)

    def draw_ticks_and_labels(self, painter, center, radius):
        for i in range(51):
            tick_value = i * 100
            tick_angle = 230 - (tick_value / self.max_value * 270)

            if i % 10 == 0:
                tick_length = 20
                painter.setPen(QPen(QColor(0, 0, 0), 2))
                label_radius = radius * 0.65  
                label_pos = QPoint(int(center.x() + label_radius * cos(radians(tick_angle))),
                                   int(center.y() - label_radius * sin(radians(tick_angle))))

                painter.setFont(QFont('Arial', 10, QFont.Weight.Bold))
                text = f"{tick_value}"
                text_width = painter.fontMetrics().horizontalAdvance(text)
                text_height = painter.fontMetrics().height()
                text_rect = QRect(label_pos.x() - text_width // 2,
                                  label_pos.y() - text_height // 2,
                                  text_width,
                                  text_height)
                painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, text)
            else:
                tick_length = 10
                painter.setPen(QPen(QColor(0, 0, 0), 1))

            tick_start = QPoint(int(center.x() + (radius - tick_length - 10) * cos(radians(tick_angle))),
                                int(center.y() - (radius - tick_length - 10) * sin(radians(tick_angle))))
            tick_end = QPoint(int(center.x() + (radius - 10) * cos(radians(tick_angle))),
                              int(center.y() - (radius - 10) * sin(radians(tick_angle))))
            painter.drawLine(tick_start, tick_end)

    def draw_needle(self, painter, center, radius):
        needle_length = radius - 25  # Shortened needle length
        needle_angle = 230 - (self.current_value / self.max_value * 270)
        needle_end = QPoint(int(center.x() + needle_length * cos(radians(needle_angle))),
                            int(center.y() - needle_length * sin(radians(needle_angle))))

        # Draw the arrow shaft with increased thickness
        painter.setPen(QPen(QColor(255, 0, 0), 4))  # Thickness is 4
        painter.drawLine(center, needle_end)

        # Draw the arrowhead at the end (near the edge)
        arrowhead_size = 12
        arrowhead_angle = 20  # degrees
        left_point = QPoint(
            int(needle_end.x() - arrowhead_size * cos(radians(needle_angle - arrowhead_angle))),
            int(needle_end.y() + arrowhead_size * sin(radians(needle_angle - arrowhead_angle)))
        )
        right_point = QPoint(
            int(needle_end.x() - arrowhead_size * cos(radians(needle_angle + arrowhead_angle))),
            int(needle_end.y() + arrowhead_size * sin(radians(needle_angle + arrowhead_angle)))
        )

        arrow_polygon = QPolygon([needle_end, left_point, right_point])
        painter.setBrush(QColor(255, 0, 0))
        painter.drawPolygon(arrow_polygon)

        # Draw a small circle at the center to cover the base of the arrow
        painter.setBrush(QColor(255, 0, 0))
        painter.drawEllipse(center, 4, 4)
class PressureUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: limegreen;")
        main_layout = QHBoxLayout()

        label_style = "border: none; font-weight: bold; font-size: 14px;"

        # Create a vertical layout for gauges
        gauges_layout = QVBoxLayout()

        # Frame for the first gauge
        frame1 = QFrame()
        frame1.setStyleSheet("border: 5px solid grey; border-radius: 10px;")
        layout1 = QVBoxLayout(frame1)

        # Pressure gauge 1
        self.gauge1 = CircularGauge()
        self.label1 = QLabel("Current Pressure 1: 0 PSI")
        self.label1.setStyleSheet(label_style)

        title_label1 = QLabel("Pressure 1:")
        title_label1.setStyleSheet(label_style)

        # Centering title and gauge
        layout1.addWidget(title_label1, alignment=Qt.AlignmentFlag.AlignCenter)
        layout1.addWidget(self.gauge1, alignment=Qt.AlignmentFlag.AlignCenter)
        layout1.addWidget(self.label1, alignment=Qt.AlignmentFlag.AlignCenter)
        
        gauges_layout.addWidget(frame1)

        # Frame for the second gauge
        frame2 = QFrame()
        frame2.setStyleSheet("border: 5px solid grey; border-radius: 10px;")
        layout2 = QVBoxLayout(frame2)

        # Pressure gauge 2 
        self.gauge2 = CircularGauge()
        self.label2 = QLabel("Current Pressure 2: 0 PSI")
        self.label2.setStyleSheet(label_style)

        title_label2 = QLabel("Pressure 2:")
        title_label2.setStyleSheet(label_style)

        # Centering title and gauge
        layout2.addWidget(title_label2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout2.addWidget(self.gauge2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout2.addWidget(self.label2, alignment=Qt.AlignmentFlag.AlignCenter)

        gauges_layout.addWidget(frame2)

        # Frame for buttons with a border
        button_frame = QFrame()
        button_frame.setStyleSheet("border: 5px solid grey; border-radius: 10px;") 
        button_layout = QVBoxLayout(button_frame)

        buttons_texts = ["Push Test", "Pull Test", "Lifecycle Test 100", "Lifecycle Test 500"]
        for button_text in buttons_texts:
            button = QPushButton(button_text)
            button.setStyleSheet("""
                background-color: grey; 
                color: white; 
                border: 2px solid darkgrey; 
                border-radius: 5px; 
                font-size: 16px; 
                font-weight: bold; 
                padding: 15px;  
            """)  
            button_layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.addLayout(gauges_layout)
        main_layout.addWidget(button_frame)

        self.setLayout(main_layout)
        self.setWindowTitle('Hydraulic Press Monitor')
        self.resize(600, 800)  
        self.show()

    def update_pressures(self, pressure1, pressure2):
        self.gauge1.set_value(pressure1)
        self.gauge2.set_value(pressure2)
        self.label1.setText(f"Current Pressure 1: {pressure1} PSI")
        self.label2.setText(f"Current Pressure 2: {pressure2} PSI")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PressureUI()

    # Example: Update pressures
    ex.update_pressures(2500, 3500)

    sys.exit(app.exec())
