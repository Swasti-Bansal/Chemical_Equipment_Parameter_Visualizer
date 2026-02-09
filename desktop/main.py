import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QTableWidget, QTableWidgetItem,
    QFrame, QMessageBox, QTabWidget, QSizePolicy, QGraphicsOpacityEffect
)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtWidgets import QDialog, QLineEdit
from PyQt5.QtGui import QFont
from api_client import login, download_report
import os
import webbrowser
from api_client import upload_csv, get_history
from charts import MplCanvas


def safe(x):
    if x is None:
        return "-"
    if isinstance(x, float):
        return f"{x:.2f}"   
    return str(x)


def qss():
    return """
    QWidget{
      background:#0f1220;
      color:#ffffff;
      font-family:Segoe UI;
      font-size:16px;
    }

    QLabel#Title{
      font-size:28px;
      font-weight:800;
      color:#6366f1;
    }

    QLabel#Muted{
      color:#9aa3b2;
    }

    QPushButton{
      background:#6366f1;
      border:none;
      padding:9px 14px;
      border-radius:10px;
      color:#ffffff;
      font-weight:700;
    }
    QPushButton:hover{
      background:#5558e3;
    }
    QPushButton:disabled{
      background:#3b3f68;
      color:#cbd5e1;
    }

    QPushButton#Secondary{
      background:transparent;
      border:1px solid #262a40;
      color:#cbd5e1;
    }
    QPushButton#Secondary:hover{
      border:1px solid #6366f1;
      color:#ffffff;
    }

    QLabel#StatusOk{
      background:rgba(52,211,153,0.12);
      color:#34d399;
      border-left:4px solid #22c55e;
      padding:12px 16px;
      border-radius:10px;
      font-weight:500;
    }

    QLabel#StatusErr{
      background:rgba(251,113,133,0.12);
      color:#fb7185;
      border-left:4px solid #fb7185;
      padding:12px 16px;
      border-radius:10px;
      font-weight:500;
    }

    QFrame#Card{
      background:#171a2b;
      border:1px solid #262a40;
      border-radius:14px;
    }

    QTableWidget{
      background:#111426;
      border:1px solid #262a40;
      border-radius:12px;
      gridline-color:#262a40;
      font-size:15px;
    }
    QTableWidget::item{
      padding:10px;
    }
    QTableWidget::item:hover{
      background:#1a1f35;
    }
    QHeaderView::section{
      background:#171a2b;
      color:#9aa3b2;
      padding:10px;
      border:none;
      font-weight:800;
      font-size:14px;
    }

    QTableCornerButton::section{
      background:#171a2b;
      border:none;
    }
    """


class Card(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("Card")
        self.setContentsMargins(0, 0, 0, 0)


class AnimatedLabel(QLabel):
    """Label that can animate up and down (floating effect)"""
    def __init__(self, text=""):
        super().__init__(text)
        self._offset = 0
        self.animation = QPropertyAnimation(self, b"offset")
        self.animation.setDuration(3000)
        self.animation.setStartValue(0)
        self.animation.setEndValue(-10)
        self.animation.setEasingCurve(QEasingCurve.InOutSine)
        self.animation.setLoopCount(-1)  # infinite
        
    @pyqtProperty(int)
    def offset(self):
        return self._offset
    
    @offset.setter
    def offset(self, value):
        self._offset = value
        self.setStyleSheet(f"transform: translateY({value}px);")
        

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - CSV Dashboard")
        self.resize(480, 600)
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0f1220, stop:1 #1a1f3a);
            }
        """)

        # Main container
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background: #171a2b;
                border: 1px solid #262a40;
                border-radius: 20px;
            }
        """)
        
        lay = QVBoxLayout(container)
        lay.setContentsMargins(40, 48, 40, 48)
        lay.setSpacing(20)

        # Header section
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignCenter)
        header_layout.setSpacing(8)

        # Animated icon
        self.icon = QLabel("📊")
        self.icon.setAlignment(Qt.AlignCenter)
        self.icon.setStyleSheet("font-size: 64px; background: transparent; border: none;")
        header_layout.addWidget(self.icon)
        
        # Start floating animation
        self.start_float_animation()

        # Title
        title = QLabel("CSV Dashboard")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: 700; color: #6366f1; background: transparent; border: none;")
        header_layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Sign in to access your analytics")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 14px; color: #9aa3b2; background: transparent; border: none;")
        header_layout.addWidget(subtitle)

        lay.addLayout(header_layout)
        lay.addSpacing(12)

        # Username input
        user_label = QLabel("Username")
        user_label.setStyleSheet("color: #ffffff; font-size: 14px; font-weight: 600; background: transparent; border: none; padding-left: 4px;")
        lay.addWidget(user_label)

        self.user = QLineEdit()
        self.user.setPlaceholderText("Enter your username")
        self.user.setStyleSheet("""
            QLineEdit {
                padding: 14px 16px;
                border-radius: 12px;
                background: #0f1220;
                border: 1px solid #262a40;
                color: white;
                font-size: 15px;
            }
            QLineEdit:focus {
                border: 1px solid #6366f1;
            }
        """)
        self.user.returnPressed.connect(self.do_login)
        lay.addWidget(self.user)

        # Password input
        pwd_label = QLabel("Password")
        pwd_label.setStyleSheet("color: #ffffff; font-size: 14px; font-weight: 600; background: transparent; border: none; padding-left: 4px;")
        lay.addWidget(pwd_label)

        self.pwd = QLineEdit()
        self.pwd.setPlaceholderText("Enter your password")
        self.pwd.setEchoMode(QLineEdit.Password)
        self.pwd.setStyleSheet("""
            QLineEdit {
                padding: 14px 16px;
                border-radius: 12px;
                background: #0f1220;
                border: 1px solid #262a40;
                color: white;
                font-size: 15px;
            }
            QLineEdit:focus {
                border: 1px solid #6366f1;
            }
        """)
        self.pwd.returnPressed.connect(self.do_login)
        lay.addWidget(self.pwd)

        # Status message
        self.status = QLabel("")
        self.status.setStyleSheet("color: #fb7185; font-size: 13px; background: transparent; border: none;")
        self.status.setVisible(False)
        lay.addWidget(self.status)

        # Login button
        btn = QPushButton("Sign In")
        btn.setStyleSheet("""
            QPushButton {
                background: #6366f1;
                border: none;
                border-radius: 12px;
                padding: 14px;
                color: white;
                font-size: 16px;
                font-weight: 700;
            }
            QPushButton:hover {
                background: #5558e3;
            }
            QPushButton:pressed {
                background: #4c4fd8;
            }
        """)
        btn.clicked.connect(self.do_login)
        lay.addWidget(btn)

        # Footer
        lay.addSpacing(8)
        footer_line = QFrame()
        footer_line.setFrameShape(QFrame.HLine)
        footer_line.setStyleSheet("background: #262a40; max-height: 1px; border: none;")
        lay.addWidget(footer_line)

        footer = QLabel("Don't have an account? Contact your administrator")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("font-size: 13px; color: #9aa3b2; background: transparent; border: none;")
        lay.addWidget(footer)

        # Wrap container in main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.addWidget(container)
        
        self.setLayout(main_layout)
        self.layout().activate()
        self.adjustSize()


    def start_float_animation(self):
        """Animate the icon floating up and down"""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_float)
        self.timer.start(50)  # Update every 50ms
        self.float_offset = 0
        self.float_direction = 1
        
    def animate_float(self):
        """Update float position"""
        self.float_offset += 0.5 * self.float_direction
        if self.float_offset >= 10:
            self.float_direction = -1
        elif self.float_offset <= 0:
            self.float_direction = 1
            
        # Apply transform
        self.icon.setStyleSheet(f"""
            font-size: 64px;
            background: transparent;
            border: none;
            padding-bottom: {int(self.float_offset)}px;
        """)

    def do_login(self):
        u = self.user.text().strip()
        p = self.pwd.text().strip()
        if not u or not p:
            self.status.setText("Please enter username & password")
            self.status.setVisible(True)
            return
        try:
            login(u, p)
            self.accept()
        except Exception as e:
            self.status.setText(f"Login failed: {str(e)}")
            self.status.setVisible(True)


class Dashboard(QWidget):
  
    def download_report_file(self):
        try:
            self.set_status("Generating report...", ok=True)
            save_path = os.path.join(os.getcwd(), "report.pdf")
            download_report(save_path)
            self.set_status("Report downloaded ✓", ok=True)
            webbrowser.open(save_path)
        except Exception as e:
            self.set_status(f"Report failed: {e}", ok=False)

    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CSV Dashboard (Desktop)")
        self.resize(1280, 760)

        self.file_path = None

        root = QVBoxLayout()
        root.setContentsMargins(28, 24, 28, 24)
        root.setSpacing(14)

        # Header
        header = QHBoxLayout()
        header.setSpacing(12)

        title_wrap = QVBoxLayout()
        title_wrap.setSpacing(2)

        self.title = QLabel("CSV Dashboard")
        self.title.setObjectName("Title")

        self.sub = QLabel("Desktop + Web using same Django API")
        self.sub.setObjectName("Muted")

        title_wrap.addWidget(self.title)
        title_wrap.addWidget(self.sub)
        header.addLayout(title_wrap, 1)

        self.choose_btn = QPushButton("Choose CSV")
        self.choose_btn.setObjectName("Secondary")

        self.upload_btn = QPushButton("Upload CSV")
        
        self.report_btn = QPushButton("Download Report")
        header.addWidget(self.report_btn)
        self.report_btn.clicked.connect(self.download_report_file)

        header.addWidget(self.choose_btn)
        header.addWidget(self.upload_btn)

        root.addLayout(header)

        # Status
        self.status = QLabel("")
        self.status.setVisible(False)
        root.addWidget(self.status)

        # --------- Latest Summary card (KPIs) ---------
        self.latest_card = Card()
        latest_layout = QVBoxLayout(self.latest_card)
        latest_layout.setContentsMargins(16, 16, 16, 16)
        latest_layout.setSpacing(12)

        self.latest_title = QLabel("Latest Summary")
        self.latest_title.setStyleSheet("font-weight:800; font-size:16px; padding-bottom:8px; border-bottom:2px solid #262a40;")

        self.latest_file = QLabel("No uploads yet")
        self.latest_file.setObjectName("Muted")

        top_left = QVBoxLayout()
        top_left.setSpacing(2)
        top_left.addWidget(self.latest_title)
        top_left.addWidget(self.latest_file)
        latest_layout.addLayout(top_left)

        # KPI GRID - Changed to 1x4 to match web version
        self.kpi_grid = QGridLayout()
        self.kpi_grid.setContentsMargins(0, 16, 0, 0)
        self.kpi_grid.setHorizontalSpacing(22)
        self.kpi_grid.setVerticalSpacing(22)

        self.kpi_total = self.make_kpi("Total", "-", "#6366f1")
        self.kpi_flow = self.make_kpi("Flow", "-", "#34d399")
        self.kpi_pressure = self.make_kpi("Pressure", "-", "#fbbf24")
        self.kpi_temp = self.make_kpi("Temp", "-", "#fb7185")

        # 1x4 layout like web version
        self.kpi_grid.addWidget(self.kpi_total, 0, 0)
        self.kpi_grid.addWidget(self.kpi_flow, 0, 1)
        self.kpi_grid.addWidget(self.kpi_pressure, 1, 0)
        self.kpi_grid.addWidget(self.kpi_temp, 1, 1)

        self.kpi_grid.setColumnStretch(0, 1)
        self.kpi_grid.setColumnStretch(1, 1)
        self.kpi_grid.setColumnStretch(0, 1)
        self.kpi_grid.setColumnStretch(1, 1)

        latest_layout.addLayout(self.kpi_grid, 1)

        # --------- History card (table) ---------
        self.history_card = Card()
        history_layout = QVBoxLayout(self.history_card)
        history_layout.setContentsMargins(26, 16, 16, 16)
        history_layout.setSpacing(12)

        htitle = QLabel("Last 5 Uploads")
        htitle.setStyleSheet("font-weight:800; font-size:16px; padding-bottom:8px; border-bottom:2px solid #262a40;")
        history_layout.addWidget(htitle)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["S.No.", "Filename", "Uploaded At", "Total", "Avg Flow"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
        alternate-background-color: #0f1220;
        QTableWidget{
          background:#111426;
          border:1px solid #262a40;
          border-radius:12px;
          gridline-color:#262a40;
          font-size:17px;       
        }
        QTableWidget::item{
          padding:10px;
          padding-left:16px;   
        }
        """)
        self.table.verticalHeader().setDefaultSectionSize(46)

        self.table.verticalHeader().setVisible(False)
        self.table.setCornerButtonEnabled(False)

        history_layout.addWidget(self.table)

        # --------- Bar chart card ---------
        self.bar_card = Card()
        bar_layout = QVBoxLayout(self.bar_card)
        bar_layout.setContentsMargins(16, 16, 16, 16)
        bar_layout.setSpacing(10)

        bar_title = QLabel("Equipment Distribution")
        bar_title.setStyleSheet("font-weight:800; font-size:16px; padding-bottom:8px; border-bottom:2px solid #262a40;")
        bar_layout.addWidget(bar_title)

        self.bar_canvas = MplCanvas()
        bar_layout.addWidget(self.bar_canvas, 1)

        # --------- Line chart card ---------
        self.line_card = Card()
        line_layout = QVBoxLayout(self.line_card)
        line_layout.setContentsMargins(16, 16, 16, 16)
        line_layout.setSpacing(10)

        line_title = QLabel("Metrics Over Time")
        line_title.setStyleSheet("font-weight:800; font-size:16px; padding-bottom:8px; border-bottom:2px solid #262a40;")
        line_layout.addWidget(line_title)

        self.line_canvas = MplCanvas()
        line_layout.addWidget(self.line_canvas, 1)

        # --------- Tabs ---------
        tabs = QTabWidget()
        tabs.setStyleSheet("""
        QTabWidget::pane{ border:0; }
        QTabBar::tab{
          background:#171a2b;
          border:1px solid #262a40;
          padding:14px 28px;
          min-width:120px;
          font-size:16px;  
          border-top-left-radius:10px;
          border-top-right-radius:10px;
          margin-right:8px;
          color:#9aa3b2;
          font-weight:700;
          font-size:16px;
          padding:12px 22px;
        }
        QTabBar::tab:selected{
          background:#111426;
          color:#ffffff;
        }
        QTabBar::tab:hover{
          color:#ffffff;
        }
        """)

        home_tab = QWidget()
        home_layout = QVBoxLayout(home_tab)
        home_layout.setContentsMargins(0, 0, 0, 0)
        home_layout.setSpacing(14)
        home_layout.addWidget(self.latest_card, 1)
        tabs.addTab(home_tab, "Home")

        history_tab = QWidget()
        history_layout2 = QVBoxLayout(history_tab)
        history_layout2.setContentsMargins(0, 0, 0, 0)
        history_layout2.setSpacing(14)
        history_layout2.addWidget(self.history_card, 1)
        tabs.addTab(history_tab, "History")

        graphs_tab = QWidget()
        graphs_layout = QVBoxLayout(graphs_tab)
        graphs_layout.setContentsMargins(0, 0, 0, 0)
        graphs_layout.setSpacing(14)
        graphs_layout.addWidget(self.bar_card, 1)
        graphs_layout.addWidget(self.line_card, 1)
        tabs.addTab(graphs_tab, "Graphs")

        root.addWidget(tabs, 1)
        self.setLayout(root)

        # Hooks
        self.choose_btn.clicked.connect(self.pick_file)
        self.upload_btn.clicked.connect(self.do_upload)

        self.load_data()

    def make_kpi(self, label, value, color):
        """KPI tiles matching web version style"""
        box = QFrame()
        box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        box.setMinimumHeight(100)

        box.setStyleSheet(f"""
            QFrame {{
                background: {color};
                border-radius: 10px;
            }}
        """)

        lay = QVBoxLayout(box)
        lay.setContentsMargins(16, 14, 16, 14)
        lay.setSpacing(6)
        lay.setAlignment(Qt.AlignCenter)

        title = QLabel(label)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-weight:800; color: rgba(255,255,255,0.9); font-size:12px; text-transform: uppercase; letter-spacing: 0.5px;")

        value_lbl = QLabel(value)
        value_lbl.setAlignment(Qt.AlignCenter)
        value_lbl.setStyleSheet("font-weight:800; font-size:28px; color:#ffffff;")

        lay.addWidget(title)
        lay.addWidget(value_lbl)

        box._value_label = value_lbl
        return box

    def set_status(self, text, ok=True):
        self.status.setText(text)
        self.status.setObjectName("StatusOk" if ok else "StatusErr")
        self.status.setVisible(True)
        self.status.style().unpolish(self.status)
        self.status.style().polish(self.status)

    def pick_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select CSV", "", "CSV Files (*.csv)")
        if path:
            self.file_path = path
            self.set_status(f"Selected: {os.path.basename(path)}", ok=True)

    def do_upload(self):
        if not self.file_path:
            QMessageBox.warning(self, "Missing file", "Please choose a CSV file first.")
            return

        try:
            self.choose_btn.setDisabled(True)
            self.upload_btn.setDisabled(True)
            self.upload_btn.setText("Uploading...")
            self.set_status("Uploading...", ok=True)

            upload_csv(self.file_path)
            self.file_path = None

            self.set_status("Uploaded successfully ✓", ok=True)
            self.load_data()

        except Exception as e:
            self.set_status(f"Upload failed: {e}", ok=False)

        finally:
            self.upload_btn.setText("Upload CSV")
            self.choose_btn.setDisabled(False)
            self.upload_btn.setDisabled(False)

    def load_data(self):
        try:
            data = get_history()

            if not data:
                self.latest_file.setText("No uploads yet")
                self.kpi_total._value_label.setText("-")
                self.kpi_flow._value_label.setText("-")
                self.kpi_pressure._value_label.setText("-")
                self.kpi_temp._value_label.setText("-")
                self.table.setRowCount(0)
                self.bar_canvas.clear("Equipment Distribution")
                self.line_canvas.clear("Metrics Over Time")
                return

            latest = data[0]
            s = latest.get("summary", {}) or {}

            self.latest_file.setText(latest.get("filename", ""))
            self.kpi_total._value_label.setText(safe(s.get("total_equipment")))
            self.kpi_flow._value_label.setText(safe(s.get("avg_flowrate")))
            self.kpi_pressure._value_label.setText(safe(s.get("avg_pressure")))
            self.kpi_temp._value_label.setText(safe(s.get("avg_temperature")))

            self.table.setRowCount(len(data))
            for r, item in enumerate(data):
                summ = item.get("summary", {}) or {}
                self.table.setItem(r, 0, QTableWidgetItem(str(r + 1))) 
                self.table.setItem(r, 1, QTableWidgetItem(str(item.get("filename", ""))))
                self.table.setItem(r, 2, QTableWidgetItem(str(item.get("uploaded_at", ""))))
                self.table.setItem(r, 3, QTableWidgetItem(str(summ.get("total_equipment", "-"))))
                self.table.setItem(r, 4, QTableWidgetItem(str(summ.get("avg_flowrate", "-"))))

            dist = s.get("type_distribution", {}) or {}
            self.bar_canvas.bar(list(dist.keys()), list(dist.values()), title="Equipment Distribution")

            ordered = list(reversed(data))
            xlabels = [f"#{i+1}" for i in range(len(ordered))]
            flow = [it.get("summary", {}).get("avg_flowrate") for it in ordered]
            pressure = [it.get("summary", {}).get("avg_pressure") for it in ordered]
            temp = [it.get("summary", {}).get("avg_temperature") for it in ordered]

            self.line_canvas.lines(
                xlabels,
                {"Flow": flow, "Pressure": pressure, "Temp": temp},
                title="Metrics Over Time"
            )

        except Exception as e:
            self.set_status(f"Failed to load history: {e}", ok=False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qss())

    dlg = LoginDialog()
    if dlg.exec_() != QDialog.Accepted:
        sys.exit(0)

    w = Dashboard()
    w.show()
    sys.exit(app.exec_())