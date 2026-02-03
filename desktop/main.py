import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QTableWidget, QTableWidgetItem,
    QFrame, QMessageBox, QTabWidget, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QLineEdit
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
      border:1px solid rgba(52,211,153,0.25);
      padding:10px;
      border-radius:10px;
    }

    QLabel#StatusErr{
      background:rgba(251,113,133,0.12);
      color:#fb7185;
      border:1px solid rgba(251,113,133,0.25);
      padding:10px;
      border-radius:10px;
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
    QHeaderView::section{
      background:#171a2b;
      color:#9aa3b2;
      padding:10px;
      border:none;
      font-weight:800;
      font-size:14px;
    }

    /* optional: even if the corner existed, keep it dark */
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

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(360, 220)

        lay = QVBoxLayout()
        lay.setContentsMargins(18, 18, 18, 18)
        lay.setSpacing(10)

        t = QLabel("Login")
        t.setStyleSheet("font-size:22px; font-weight:800; color:#6366f1;")
        lay.addWidget(t)

        self.user = QLineEdit()
        self.user.setPlaceholderText("Username")
        self.user.setStyleSheet("padding:10px; border-radius:10px; background:#111426; border:1px solid #262a40; color:white;")
        lay.addWidget(self.user)

        self.pwd = QLineEdit()
        self.pwd.setPlaceholderText("Password")
        self.pwd.setEchoMode(QLineEdit.Password)
        self.pwd.setStyleSheet("padding:10px; border-radius:10px; background:#111426; border:1px solid #262a40; color:white;")
        lay.addWidget(self.pwd)

        self.status = QLabel("")
        self.status.setStyleSheet("color:#fb7185;")
        lay.addWidget(self.status)

        btn = QPushButton("Login")
        btn.clicked.connect(self.do_login)
        lay.addWidget(btn)

        self.setLayout(lay)

    def do_login(self):
        u = self.user.text().strip()
        p = self.pwd.text().strip()
        if not u or not p:
            self.status.setText("Enter username & password")
            return
        try:
            login(u, p)
            self.accept()
        except Exception as e:
            self.status.setText(str(e))


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
        self.latest_title.setStyleSheet("font-weight:800; font-size:15px;")

        self.latest_file = QLabel("No uploads yet")
        self.latest_file.setObjectName("Muted")

        top_left = QVBoxLayout()
        top_left.setSpacing(2)
        top_left.addWidget(self.latest_title)
        top_left.addWidget(self.latest_file)
        latest_layout.addLayout(top_left)

        # KPI GRID (2x2), uniform spacing, fills area nicely
        self.kpi_grid = QGridLayout()
        self.kpi_grid.setContentsMargins(16, 16, 16, 16)
        self.kpi_grid.setHorizontalSpacing(28)
        self.kpi_grid.setVerticalSpacing(28)

        self.kpi_total = self.make_kpi("Total equipment", "-", "#6366f1")
        self.kpi_flow = self.make_kpi("Avg flowrate", "-", "#34d399")
        self.kpi_pressure = self.make_kpi("Avg pressure", "-", "#fbbf24")
        self.kpi_temp = self.make_kpi("Avg temperature", "-", "#fb7185")

        self.kpi_grid.addWidget(self.kpi_total, 0, 0)
        self.kpi_grid.addWidget(self.kpi_flow, 0, 1)
        self.kpi_grid.addWidget(self.kpi_pressure, 1, 0)
        self.kpi_grid.addWidget(self.kpi_temp, 1, 1)

        self.kpi_grid.setColumnStretch(0, 1)
        self.kpi_grid.setColumnStretch(1, 1)
        self.kpi_grid.setRowStretch(0, 1)
        self.kpi_grid.setRowStretch(1, 1)

        latest_layout.addLayout(self.kpi_grid, 1)

        # --------- History card (table) ---------
        self.history_card = Card()
        history_layout = QVBoxLayout(self.history_card)
        history_layout.setContentsMargins(16, 16, 16, 16)
        history_layout.setSpacing(12)

        htitle = QLabel("Last 5 Uploads")
        htitle.setStyleSheet("font-weight:800; font-size:15px;")
        history_layout.addWidget(htitle)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Filename", "Uploaded At", "Total", "Avg Flow"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("alternate-background-color: #0f1220;")
        self.table.verticalHeader().setDefaultSectionSize(46)

        # ✅ removes the white box + row header
        self.table.verticalHeader().setVisible(False)
        self.table.setCornerButtonEnabled(False)

        history_layout.addWidget(self.table)

        # --------- Bar chart card ---------
        self.bar_card = Card()
        bar_layout = QVBoxLayout(self.bar_card)
        bar_layout.setContentsMargins(16, 16, 16, 16)
        bar_layout.setSpacing(10)

        bar_title = QLabel("Type Distribution (Latest)")
        bar_title.setStyleSheet("font-weight:800; font-size:15px;")
        bar_layout.addWidget(bar_title)

        self.bar_canvas = MplCanvas()
        bar_layout.addWidget(self.bar_canvas, 1)

        # --------- Line chart card ---------
        self.line_card = Card()
        line_layout = QVBoxLayout(self.line_card)
        line_layout.setContentsMargins(16, 16, 16, 16)
        line_layout.setSpacing(10)

        line_title = QLabel("Averages Trend (Last 5)")
        line_title.setStyleSheet("font-weight:800; font-size:15px;")
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

    # KPI tiles: website colors, square-ish, uniform, not bright blocks
    def make_kpi(self, label, value, color):
      box = QFrame()
      box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
      box.setMinimumHeight(150)

      box.setStyleSheet(f"""
          QFrame {{
            background: {color};
            border-radius: 14px;
          }}
      """)

      lay = QVBoxLayout(box)
      lay.setContentsMargins(16, 14, 16, 14)
      lay.setSpacing(6)
      lay.setAlignment(Qt.AlignCenter)

      title = QLabel(label)
      title.setAlignment(Qt.AlignCenter)
      title.setStyleSheet("font-weight:800; color: rgba(255,255,255,0.95); font-size:15px;")

      value_lbl = QLabel(value)
      value_lbl.setAlignment(Qt.AlignCenter)
      value_lbl.setStyleSheet("font-weight:900; font-size:30px; color:#ffffff;")

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
            self.set_status(f"Selected: {path.split('\\\\')[-1]}", ok=True)

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
                self.bar_canvas.clear("Type Distribution (Latest)")
                self.line_canvas.clear("Averages Trend (Last 5)")
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
                self.table.setItem(r, 0, QTableWidgetItem(str(item.get("filename", ""))))
                self.table.setItem(r, 1, QTableWidgetItem(str(item.get("uploaded_at", ""))))
                self.table.setItem(r, 2, QTableWidgetItem(str(summ.get("total_equipment", "-"))))
                self.table.setItem(r, 3, QTableWidgetItem(str(summ.get("avg_flowrate", "-"))))

            dist = s.get("type_distribution", {}) or {}
            self.bar_canvas.bar(list(dist.keys()), list(dist.values()), title="Type Distribution (Latest)")

            ordered = list(reversed(data))
            xlabels = [f"#{i+1}" for i in range(len(ordered))]
            flow = [it.get("summary", {}).get("avg_flowrate") for it in ordered]
            pressure = [it.get("summary", {}).get("avg_pressure") for it in ordered]
            temp = [it.get("summary", {}).get("avg_temperature") for it in ordered]

            self.line_canvas.lines(
                xlabels,
                {"Flow": flow, "Pressure": pressure, "Temp": temp},
                title="Averages Trend (Last 5)"
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

