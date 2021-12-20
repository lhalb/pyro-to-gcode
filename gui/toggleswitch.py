from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtGui import QPen, QBrush, QColor, QPaintEvent, QPainter, QFont
from PyQt5.QtCore import *


class ToggleSwitch(QCheckBox):
    _transparent_pen = QPen(Qt.transparent)
    _light_grey_pen = QPen(Qt.lightGray)
    _black_pen = QPen(Qt.black)
    _white_pen = QPen(Qt.white)

    def __init__(self,
                 parent=None,
                 bar_color=Qt.gray,
                 checked_color=Qt.gray,  # '"#00B0FF",
                 handle_color=Qt.white,
                 h_scale=1.0,
                 v_scale=1.0,
                 fontSize=8):

        super().__init__(parent)

        # Save our properties on the object via self, so we can access them later
        # in the paintEvent.
        self._bar_brush = QBrush(bar_color)
        self._bar_checked_brush = QBrush(QColor(checked_color).lighter())

        self._handle_brush = QBrush(handle_color)
        self._handle_checked_brush = QBrush(QColor(checked_color))

        # Setup the rest of the widget.

        self.setContentsMargins(2, 0, 2, 0)
        self._handle_position = 0
        self._h_scale = h_scale
        self._v_scale = v_scale
        self._fontSize = fontSize

        self.stateChanged.connect(self.handle_state_change)

    def sizeHint(self):
        return QSize(80, 45)

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    def paintEvent(self, e: QPaintEvent):

        contRect = self.contentsRect()
        width = contRect.width() * self._h_scale
        height = contRect.height() * self._v_scale
        handleRadius = round(0.24 * height)

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        p.setPen(self._transparent_pen)
        barRect = QRectF(0, 0, width - handleRadius, 0.40 * height)
        barRect.moveCenter(contRect.center())
        rounding = barRect.height() / 2

        # the handle will move along this line
        trailLength = contRect.width() * self._h_scale - 2 * handleRadius
        xLeft = contRect.center().x() - (trailLength + handleRadius) / 2
        xRight = xLeft + handleRadius * 1.6
        xPos = xLeft + handleRadius * 0.5 + trailLength * self._handle_position

        if self.isChecked():
            p.setBrush(self._bar_checked_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setBrush(self._handle_checked_brush)

            p.setPen(self._black_pen)
            p.setFont(QFont('Helvetica', self._fontSize, 75))
            p.drawText(xLeft + handleRadius / 2, contRect.center().y() +
                       handleRadius / 2, "NP-2")

        else:
            p.setBrush(self._bar_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setPen(self._white_pen)
            p.setFont(QFont('Helvetica', self._fontSize, 75))
            p.drawText(xRight + handleRadius / 2, contRect.center().y() +
                       handleRadius / 2, "NP-1")
            p.setBrush(self._handle_brush)

        p.setPen(self._light_grey_pen)
        p.drawEllipse(
            QPointF(xPos, barRect.center().y()),
            handleRadius, handleRadius)

        p.end()

    @Slot(int)
    def handle_state_change(self, value):
        self._handle_position = 1 if value else 0

    @Property(float)
    def handle_position(self):
        return self._handle_position

    @handle_position.setter
    def handle_position(self, pos):
        """change the property
           we need to trigger QWidget.update() method, either by:
           1- calling it here [ what we're doing ].
           2- connecting the QPropertyAnimation.valueChanged() signal to it.
        """
        self._handle_position = pos
        self.update()

    def setH_scale(self, value):
        self._h_scale = value
        self.update()

    def setV_scale(self, value):
        self._v_scale = value
        self.update()

    def setFontSize(self, value):
        self._fontSize = value
        self.update()