<div align="center">

<h1 style="font-size: 48px;">📊 CSV Analytics Dashboard</h1>

<p style="font-size: 18px;">
A full-stack analytics dashboard that lets users upload CSV data, automatically compute statistics, visualize insights, and generate PDF reports — available on both <strong>Web</strong> and <strong>Desktop</strong> platforms.
</p>

</div>

---

<h2 style="font-size: 32px;">🎯 Overview</h2>

<p style="font-size: 16px;">
CSV Analytics Dashboard is a comprehensive data analytics solution that combines the power of Django REST Framework, React, and PyQt5 to deliver seamless data analysis across web and desktop platforms. Upload CSV files, visualize trends, generate reports, and track your analytics history—all through an intuitive, secure interface.
</p>

### Why Choose This Dashboard?

- **🚀 Fast & Automated** - No more manual spreadsheet work
- **📊 Visual Insights** - Interactive charts and KPI summaries
- **🔄 Multi-Platform** - Works on web browsers and desktop
- **📄 Professional Reports** - Generate PDF exports instantly
- **🔐 Secure** - JWT-based authentication
- **📈 Historical Tracking** - Monitor trends across uploads

<hr style="border: 0; height: 2px; background: linear-gradient(to right, #4CAF50, #2196F3); margin: 40px 0;">

<h2 style="font-size: 32px;">✨ Features</h2>

### Core Functionality

- 📂 **CSV File Upload** - Drag-and-drop or browse to upload
- 📊 **Auto Statistics** - Automatic calculation of totals, averages, and key metrics
- 📈 **Data Visualization** - Dynamic bar charts and line trend graphs
- 🕒 **Upload History** - Track and review your last 5 uploads
- 📄 **PDF Report Generation** - Export professional analytics reports
- 🔐 **Secure Authentication** - JWT-based login system
- 🌐 **Dual Interface** - Web dashboard + standalone desktop application

<p style="font-size: 16px; font-weight: bold; color: #2196F3;">
All powered by a single Django REST API.
</p>

<hr style="border: 0; height: 2px; background: linear-gradient(to right, #4CAF50, #2196F3); margin: 40px 0;">

<h2 style="font-size: 32px;">💡 Why the Project is Useful</h2>

<p style="font-size: 16px;">
Working with raw CSV files is slow and manual.
</p>

**This project helps by:**

✅ Automating calculations  
✅ Showing instant visual insights  
✅ Tracking historical uploads  
✅ Exporting professional reports  
✅ Supporting both browser & desktop usage  

**Useful for:**

- Equipment monitoring
- Operations analytics
- Lab/industrial data
- CSV-based reporting systems
- Academic projects

<hr style="border: 0; height: 2px; background: linear-gradient(to right, #4CAF50, #2196F3); margin: 40px 0;">

<h2 style="font-size: 32px;">🏗️ Project Structure</h2>

```
FOSSEE/
│
├── backend/                   # Django REST API Backend
│   ├── api/                   # API application
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── backend/               # Django project configuration
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── db.sqlite3            # Database file
│   ├── manage.py             # Django management script
│   └── Requirements.txt      # Python dependencies
│
├── desktop/                  # PyQt5 Desktop Application
│   ├── __pycache__/
│   ├── api_client.py         # API communication module
│   ├── charts.py             # Chart generation logic
│   ├── main.py               # Main application entry
│   └── report.pdf            # Sample generated report
│
├── frontend/                 # React Web Application
│   ├── node_modules/         # npm dependencies
│   ├── public/               # Static public assets
│   │   ├── index.html
│   │   ├── favicon.ico
│   │   └── manifest.json
│   ├── src/                 # React source code
│   │   ├── assets/          # Images, fonts, etc.
│   │   ├── api.js           # API service layer
│   │   ├── App.css          # Main styles
│   │   ├── App.jsx          # Root component
│   │   ├── index.css        # Global styles
│   │   └── main.jsx         # Application entry point
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json         # npm dependencies
│   └── vite.config.js       # Vite bundler config
│
└── README.md                # This file
```

<hr style="border: 0; height: 2px; background: linear-gradient(to right, #4CAF50, #2196F3); margin: 40px 0;">

<h2 style="font-size: 32px;">⚡ How to Get Started</h2>

### Prerequisites

<p style="font-size: 16px;">
Before you begin, ensure you have the following installed:
</p>

- **Python** 3.8 or higher
- **Node.js** 16+ and npm
- **Git**
- **pip** (Python package manager)

---

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/csv-analytics-dashboard.git
cd csv-analytics-dashboard
```

---

### 2️⃣ Backend Setup (Django API)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r Requirements.txt

# Run migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser
# Follow prompts to create username and password

# Start development server
python manage.py runserver
```

<p style="font-size: 16px; font-weight: bold; color: #4CAF50;">
✅ Backend will run at: <code>http://127.0.0.1:8000</code>
</p>

---

### 3️⃣ Frontend Setup (React Web App)

```bash
# Open new terminal and navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

<p style="font-size: 16px; font-weight: bold; color: #4CAF50;">
✅ Frontend will run at: <code>http://localhost:3000</code>
</p>

---

### 4️⃣ Desktop Application Setup (PyQt5)

```bash
# Open new terminal and navigate to desktop
cd desktop

# Install dependencies
pip install PyQt5 requests matplotlib pandas

# Run desktop application
python main.py
```

<hr style="border: 0; height: 2px; background: linear-gradient(to right, #4CAF50, #2196F3); margin: 40px 0;">

<h2 style="font-size: 32px;">🔐 Login</h2>

<p style="font-size: 16px;">
Create a user using:
</p>

```bash
python manage.py createsuperuser
```

<p style="font-size: 16px;">
Use the same credentials for:
</p>

- ✅ Web app
- ✅ Desktop app

<hr style="border: 0; height: 2px; background: linear-gradient(to right, #4CAF50, #2196F3); margin: 40px 0;">

<h2 style="font-size: 32px;">📖 Documentation</h2>

### API Endpoints

#### Authentication
- `POST /api/auth/login/` - User login (returns JWT token)
- `POST /api/auth/register/` - User registration

#### CSV Operations
- `POST /api/upload/` - Upload CSV file
- `GET /api/history/` - Get upload history (last 5)
- `GET /api/analytics/<id>/` - Get specific analytics
- `GET /api/report/<id>/` - Download PDF report

#### Protected Routes
<p style="font-size: 16px; background-color: #FFF3CD; padding: 10px; border-radius: 5px;">
⚠️ All endpoints except login/register require JWT authentication:
<br>
<code>Authorization: Bearer &lt;your_jwt_token&gt;</code>
</p>

---

### CSV Format Requirements

Your CSV file should have:
- ✅ **Headers in first row**
- ✅ **Numeric columns** for statistics
- ✅ **UTF-8 encoding** (recommended)

<hr style="border: 0; height: 2px; background: linear-gradient(to right, #4CAF50, #2196F3); margin: 40px 0;">

### Step-by-Step Workflow

#### 1. 🔐 Login
- Use credentials created with `createsuperuser`
- Works on both web and desktop apps

#### 2. 📤 Upload CSV
- Click "Upload" button
- Select your CSV file
- Wait for processing (typically < 2 seconds)

#### 3. 📊 View Insights
- KPI cards show totals and averages
- Charts display trends and distributions
- Data table shows recent entries

#### 4. 📥 Download Report
- Click "Download Report"
- PDF downloads with all visualizations
- Share with stakeholders

#### 5. 🕒 Review History
- Access previous uploads
- Compare trends over time
- Re-download past reports

<hr style="border: 0; height: 2px; background: linear-gradient(to right, #4CAF50, #2196F3); margin: 40px 0;">

<h2 style="font-size: 32px;">🛠️ Tech Stack</h2>

### Backend
| Technology | Purpose |
|------------|---------|
| Django | Web framework |
| Django REST Framework | API development |
| djangorestframework-simplejwt | JWT authentication |
| SQLite | Database (dev) |
| ReportLab | PDF generation |
| Pandas | Data processing |

### Frontend
| Technology | Purpose |
|------------|---------|
| React | UI framework |
| Vite | Build tool & dev server |
| Axios | HTTP client |
| Chart.js | Data visualization |

### Desktop
| Technology | Purpose |
|------------|---------|
| PyQt5 | GUI framework |
| Matplotlib | Chart rendering |
| Requests | API communication |

<hr style="border: 0; height: 2px; background: linear-gradient(to right, #4CAF50, #2196F3); margin: 40px 0;">

<h2 style="font-size: 32px;">🧩 Troubleshooting</h2>

<p style="font-size: 16px;">
If you face issues, check the following:
</p>

### Common Issues

**❌ Backend server won't start**
```bash
# Check if port 8000 is in use
lsof -i :8000  # On Unix/Mac
netstat -ano | findstr :8000  # On Windows
```

**❌ Frontend build errors**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**❌ CORS errors**
- Ensure Django CORS settings allow your frontend URL
- Check `ALLOWED_HOSTS` in `settings.py`

**✅ Quick Checklist:**
- [ ] Backend server running on port 8000?
- [ ] Frontend server running on port 3000?
- [ ] Superuser created with `createsuperuser`?
- [ ] All dependencies installed?
- [ ] Database migrations applied?

<hr style="border: 0; height: 2px; background: linear-gradient(to right, #4CAF50, #2196F3); margin: 40px 0;">

<h2 style="font-size: 32px;">📊 Use Cases</h2>

<p style="font-size: 16px;">
This dashboard is perfect for:
</p>

- **🏭 Industrial IoT** - Equipment monitoring and analytics
- **🔬 Research Labs** - Experimental data analysis
- **📈 Business Analytics** - Sales, operations, and KPI tracking
- **🎓 Academic Projects** - Data science coursework and research
- **📊 Financial Analysis** - Market data and trends
- **🌾 Agriculture** - Sensor data and yield monitoring
- **🏥 Healthcare** - Patient data analytics (with proper security)

<hr style="border: 0; height: 2px; background: linear-gradient(to right, #4CAF50, #2196F3); margin: 40px 0;">

<h2 style="font-size: 32px;">⭐ Future Improvements</h2>

- [ ] **Role-based authentication** - Admin, Analyst, Viewer roles
- [ ] **Excel export** - Download data in .xlsx format
- [ ] **Cloud deployment** - AWS/Heroku deployment guides
- [ ] **Advanced filtering** - Date ranges, value filters, search
- [ ] **Docker support** - Containerized deployment
- [ ] **Real-time updates** - WebSocket integration
- [ ] **Mobile app** - React Native version
- [ ] **Email reports** - Scheduled automated reports

<hr style="border: 0; height: 2px; background: linear-gradient(to right, #4CAF50, #2196F3); margin: 40px 0;">

<h2 style="font-size: 32px;">📄 License</h2>

<p style="font-size: 16px; background-color: #E3F2FD; padding: 15px; border-radius: 5px; border-left: 4px solid #2196F3;">
📝 This project is created for <strong>educational purposes</strong> as part of a screening task.
</p>

<hr style="border: 0; height: 2px; background: linear-gradient(to right, #4CAF50, #2196F3); margin: 40px 0;">

<h2 style="font-size: 32px;">👏 Acknowledgments</h2>

- **Django** - For the robust backend framework
- **React** - For the dynamic frontend library
- **PyQt** - For native desktop capabilities
- **Chart.js** - For beautiful visualizations
- **ReportLab** - For PDF generation
- **FOSSEE** - For project inspiration and structure

---

<div align="center">

<h3 style="font-size: 28px;">Happy Coding! 🚀</h3>

<p style="font-size: 16px;">
⭐ Star this repo if you find it helpful!
</p>

**Built with ❤️ using Django, React, and PyQt5**

</div>
