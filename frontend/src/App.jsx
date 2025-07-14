import { useState, useEffect } from 'react';
import './App.css';

const API = 'http://localhost:8000';  // Make sure this matches your backend server address

export default function App() {
  const [expr, setExpr] = useState('');
  const [batchExpr, setBatchExpr] = useState('');
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  // Fetch calculation history
  const fetchHistory = async () => {
    try {
      const response = await fetch(`${API}/history`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setHistory(data);
      setError(null);
    } catch (err) {
      setError('Unable to connect to server. Please ensure the backend service is running on the correct port');
    }
  };

  useEffect(() => { fetchHistory(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    
    try {
      if (!expr.trim()) {
        throw new Error('Please enter an expression');
      }

      const resp = await fetch(`${API}/calculate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ expression: expr })
      });
      
      if (!resp.ok) {
        const errorText = await resp.text();
        throw new Error(errorText || 'Calculation failed. Please check the expression format');
      }

      const json = await resp.json();
      setResult(json.result);
      setExpr('');
      fetchHistory();
    } catch (err) {
      setError(err.message || 'Calculation failed. Please check the expression format');
    } finally {
      setLoading(false);
    }
  };

  const handleBatchSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    
    try {
      if (!batchExpr.trim()) {
        throw new Error('Please enter expressions');
      }

      const expressions = batchExpr
        .split('\n')
        .map(line => line.trim())
        .filter(line => line.length > 0);

      if (expressions.length === 0) {
        throw new Error('No valid expressions found');
      }

      const resp = await fetch(`${API}/calculate_batch`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ expressions })
      });
      
      if (!resp.ok) {
        const errorText = await resp.text();
        throw new Error(errorText || 'Batch calculation failed');
      }

      await fetchHistory();
      setBatchExpr('');
      setResult(null);
    } catch (err) {
      setError(err.message || 'Batch calculation failed');
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async () => {
    try {
      const response = await fetch(`${API}/export_csv`);
      if (!response.ok) {
        throw new Error('Export failed');
      }
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'calculator-history.csv';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError('Failed to export CSV. Please try again later');
    }
  };

  return (
    <div className="container">
      <div className="calculator-card">
        <h1>RPN Calculator</h1>
        
        <div className="calculator-tabs">
          <div className="single-calc">
            <h3>Single Expression</h3>
            <form onSubmit={handleSubmit} className="calculator-form">
              <div className="input-group">
                <input
                  value={expr}
                  onChange={e => setExpr(e.target.value)}
                  placeholder="Enter RPN expression (e.g. 2 3 4 + *)"
                  className="calculator-input"
                  disabled={loading}
                />
                <button type="submit" className="calculate-button" disabled={loading}>
                  {loading ? 'Calculating...' : 'Calculate'}
                </button>
              </div>
              
              {result !== null && (
                <div className="result">
                  Result: <strong>{result}</strong>
                </div>
              )}
            </form>
          </div>

          <div className="batch-calc">
            <h3>Batch Calculation</h3>
            <form onSubmit={handleBatchSubmit} className="calculator-form">
              <div className="input-group">
                <textarea
                  value={batchExpr}
                  onChange={e => setBatchExpr(e.target.value)}
                  placeholder="Enter multiple RPN expressions (one per line)&#10;Example:&#10;2 3 +&#10;5 3 2 + *&#10;3 4 5 * +"
                  className="calculator-textarea"
                  disabled={loading}
                  rows={5}
                />
                <button type="submit" className="calculate-button" disabled={loading}>
                  {loading ? 'Processing...' : 'Calculate All'}
                </button>
              </div>
            </form>
          </div>
          
          {error && (
            <div className="error-message">
              {error}
            </div>
          )}
        </div>

        <div className="history-section">
          <div className="history-header">
            <h2>History</h2>
            <button onClick={handleExport} className="export-button">
              Export CSV
            </button>
          </div>
          
          <div className="history-table-container">
            <table className="history-table">
              <thead>
                <tr>
                  <th>Expression</th>
                  <th>Result</th>
                </tr>
              </thead>
              <tbody>
                {history.map(h => (
                  <tr key={h.id}>
                    <td>{h.expression}</td>
                    <td>{h.result}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
