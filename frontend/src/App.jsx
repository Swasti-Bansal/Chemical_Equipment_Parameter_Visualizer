import { useEffect, useState } from "react";
import { getHistory, uploadCSV, login, logout } from "./api";
import "./App.css";
import {downloadReport } from "./api";
import { Bar, Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale, LinearScale, BarElement, PointElement, LineElement,
  Tooltip, Legend
} from "chart.js";

ChartJS.register(
  CategoryScale, LinearScale, BarElement, PointElement, LineElement, Tooltip, Legend
);

function numOrDash(x) {
  if (x === null || x === undefined) return "-";
  if (Number.isFinite(x)) return Math.round(x * 100) / 100;
  return x;
}

function isLoggedIn() {
  return !!localStorage.getItem("access_token");
}

export default function App() {

  /* AUTH STATE */
  const [authed, setAuthed] = useState(isLoggedIn());
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  /* DASHBOARD STATE */
  const [history, setHistory] = useState([]);
  const [err, setErr] = useState("");
  const [msg, setMsg] = useState("");
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  /* LOAD DATA */
  async function loadHistory() {
    try {
      setErr("");
      const data = await getHistory();
      setHistory(data);
    } catch (e) {
      if (e.response?.status === 401) {
        setErr("Session expired. Logging out...");
        setTimeout(handleLogout, 1500);
        return;
      }
      setErr("Unauthorized or failed to load history");
    }
  }

  async function handleDownloadReport() {
    try {
      setErr("");
      const blob = await downloadReport();
      const url = window.URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = "report.pdf";
      a.click();

      window.URL.revokeObjectURL(url);
    } catch (e) {
      setErr(e?.response?.data?.error || "Report download failed");
    }
  }


  useEffect(() => {
    if (authed) loadHistory();
  }, [authed]);

  /* ---------------- LOGIN ---------------- */
  async function handleLogin() {
    if (!username || !password) {
      setErr("Enter username & password");
      return;
    }

    try {
      setErr("");
      await login(username, password);
      setAuthed(true);
      setMsg("Logged in ✓");
    } catch {
      setErr("Login failed");
    }
  }

  function handleLogout() {
    logout();
    setAuthed(false);
    setHistory([]);
    setMsg("");
    setErr("");
    setUsername("");
    setPassword("");
    window.location.reload();
  }

  /* UPLOAD */
  async function handleUpload() {
    if (!file) {
      setErr("Please select a CSV file");
      return;
    }

    try {
      setUploading(true);
      setErr("");
      setMsg("");

      await uploadCSV(file);

      setMsg("File uploaded successfully ✓");
      setFile(null);
      document.getElementById("fileInput").value = "";

      await loadHistory();
    } catch {
      setErr("Upload failed");
    } finally {
      setUploading(false);
    }
  }

  const latest = history[0];

  /* ---------------- LOGIN PAGE ---------------- */
  if (!authed) {
    return (
      <div className="loginContainer">
        <div className="loginCard">
          <div className="loginHeader">
            <div className="logoIcon">📊</div>
            <h1 className="loginTitle">CSV Dashboard</h1>
            <p className="loginSubtitle">Sign in to access your analytics</p>
          </div>

          {err && <div className="alert error">{err}</div>}
          {msg && <div className="alert success">{msg}</div>}

          <div className="loginForm">
            <div className="inputGroup">
              <label className="inputLabel">Username</label>
              <input
                className="loginInput"
                placeholder="Enter your username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleLogin()}
              />
            </div>

            <div className="inputGroup">
              <label className="inputLabel">Password</label>
              <input
                className="loginInput"
                type="password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleLogin()}
              />
            </div>

            <button className="loginBtn" onClick={handleLogin}>
              Sign In
            </button>
          </div>

          <div className="loginFooter">
            <p>Don't have an account? Contact your administrator</p>
          </div>
        </div>
      </div>
    );
  }

  /* ---------------- DASHBOARD PAGE ---------------- */
  return (
    <div className="container">

      <div className="header">
        <h1 className="title">CSV Dashboard</h1>

        <div className="actions">
          <button
            onClick={handleLogout}
            style={{
              backgroundColor: "#ef4444",
              // background: "transparent",
              border: "1px solid #262a40",
              color: "#fff",
              padding: "8px 12px",
              borderRadius: 10
            }}
          >
            Logout
          </button>

          <input
            id="fileInput"
            className="inputFile"
            type="file"
            accept=".csv"
            onChange={(e) => setFile(e.target.files[0])}
          />

          <button
            className="btn"
            onClick={handleUpload}
            disabled={uploading}
          >
            {uploading ? "Uploading..." : "Upload CSV"}
          </button>

          <button className="btn" onClick={handleDownloadReport} disabled={uploading}>
            Download Report
          </button>

        </div>
      </div>

      {err && <div className="alert error">{err}</div>}
      {msg && <div className="alert success">{msg}</div>}

      {/* ---------- CARDS ---------- */}
      <div className="grid" style={{ marginTop: 14 }}>

        <div className="card">
          <div className="sectionTitle">Latest Summary</div>

          <div className="kpis">
            <div className="kpi">
              <div className="kpiLabel">Total</div>
              <div className="kpiValue">{numOrDash(latest?.summary?.total_equipment)}</div>
            </div>
            <div className="kpi">
              <div className="kpiLabel">Flow</div>
              <div className="kpiValue">{numOrDash(latest?.summary?.avg_flowrate)}</div>
            </div>
            <div className="kpi">
              <div className="kpiLabel">Pressure</div>
              <div className="kpiValue">{numOrDash(latest?.summary?.avg_pressure)}</div>
            </div>
            <div className="kpi">
              <div className="kpiLabel">Temp</div>
              <div className="kpiValue">{numOrDash(latest?.summary?.avg_temperature)}</div>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="sectionTitle">Last 5 Uploads</div>
          <div className="list">
            {history.map((item) => (
              <div className="item" key={item.id}>
                <b>{item.filename}</b> — {item.uploaded_at}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* ---------- CHARTS ---------- */}
      <div className="grid" style={{ marginTop: 14 }}>

        <div className="card">
          <div className="sectionTitle">Equipment Distribution</div>
          <Bar
            data={{
              labels: Object.keys(latest?.summary?.type_distribution || {}),
              datasets: [{
                data: Object.values(latest?.summary?.type_distribution || {}),
                backgroundColor: ["#6366f1","#34d399","#fbbf24","#fb7185","#60a5fa"]
              }]
            }}
            options={{
              responsive: true,
              plugins: { legend: { display: false } }
            }}
          />
        </div>

        <div className="card">
          <div className="sectionTitle">Metrics Over Time</div>
          <Line
            data={{
              labels: history.map((_, i) => `#${i + 1}`).reverse(),
              datasets: [
                {
                  label: "Flow",
                  data: history.map(h => h.summary?.avg_flowrate).reverse(),
                  borderColor: "#34d399",
                  backgroundColor: "rgba(52, 211, 153, 0.1)",
                  tension: 0.4
                },
                {
                  label: "Pressure",
                  data: history.map(h => h.summary?.avg_pressure).reverse(),
                  borderColor: "#fbbf24",
                  backgroundColor: "rgba(251, 191, 36, 0.1)",
                  tension: 0.4
                },
                {
                  label: "Temperature",
                  data: history.map(h => h.summary?.avg_temperature).reverse(),
                  borderColor: "#fb7185",
                  backgroundColor: "rgba(251, 113, 133, 0.1)",
                  tension: 0.4
                }
              ]
            }}
            options={{
              responsive: true,
              plugins: {
                legend: {
                  display: true,
                  position: 'top'
                }
              },
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            }}
          />
        </div>
      </div>
    </div>
  );
}
