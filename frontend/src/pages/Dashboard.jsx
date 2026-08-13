import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate, Link } from 'react-router-dom';
import { caseService } from '../services/api';
import './Dashboard.css';

function Dashboard() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [cases, setCases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    // Check if user is authenticated
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
      return;
    }

    const fetchCases = async () => {
      try {
        const response = await caseService.getMyCases();
        setCases(response.data);
      } catch (err) {
        console.error('Error fetching cases:', err);
        setError('Failed to load your cases. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchCases();
  }, [navigate]);

  const getStatusColor = (status) => {
    const colors = {
      'PENDING_REVIEW': '#FFA500',
      'UNDER_INVESTIGATION': '#1E90FF',
      'EXCHANGE_CONTACTED': '#9370DB',
      'RECOVERY_IN_PROGRESS': '#FF6B6B',
      'RECOVERED': '#2ECC71',
      'CLOSED': '#95A5A6',
      'UNRECOVERABLE': '#E74C3C',
    };
    return colors[status] || '#CCD6F6';
  };

  const getStatusText = (status) => {
    const map = {
      'PENDING_REVIEW': 'pending',
      'UNDER_INVESTIGATION': 'investigation',
      'EXCHANGE_CONTACTED': 'exchange_contacted',
      'RECOVERY_IN_PROGRESS': 'recovery_progress',
      'RECOVERED': 'recovered',
      'CLOSED': 'closed',
      'UNRECOVERABLE': 'unrecoverable',
    };
    return t(`dashboard.${map[status]}`) || status;
  };

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="spinner"></div>
        <p>{t('common.loading')}</p>
      </div>
    );
  }

  return (
    <div className="dashboard-page">
      <div className="dashboard-header">
        <h1 className="dashboard-title">{t('dashboard.title')}</h1>
        <Link to="/submit" className="btn-new-case">
          + {t('dashboard.submit_case')}
        </Link>
      </div>

      {error && <div className="dashboard-error">{error}</div>}

      {cases.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📂</div>
          <h2>{t('dashboard.no_cases')}</h2>
          <Link to="/submit" className="btn-submit-first">
            {t('dashboard.submit_case')}
          </Link>
        </div>
      ) : (
        <div className="cases-table-container">
          <table className="cases-table">
            <thead>
              <tr>
                <th>{t('dashboard.case_number')}</th>
                <th>{t('dashboard.loss')}</th>
                <th>{t('dashboard.status')}</th>
                <th>{t('dashboard.submitted')}</th>
                <th>{t('dashboard.recovery')}</th>
              </tr>
            </thead>
            <tbody>
              {cases.map((caseItem) => (
                <tr key={caseItem.id} className="case-row">
                  <td className="case-number-cell">
                    <Link to={`/cases/${caseItem.id}`} className="case-link">
                      {caseItem.case_number}
                    </Link>
                  </td>
                  <td className="loss-amount">
                    ${parseFloat(caseItem.loss_amount).toLocaleString()}
                  </td>
                  <td>
                    <span
                      className="status-badge"
                      style={{ backgroundColor: getStatusColor(caseItem.status) }}
                    >
                      {getStatusText(caseItem.status)}
                    </span>
                  </td>
                  <td>{new Date(caseItem.submitted_at).toLocaleDateString()}</td>
                  <td>
                    {caseItem.recovery_amount ? (
                      <span className="recovered-amount">
                        ${parseFloat(caseItem.recovery_amount).toLocaleString()}
                      </span>
                    ) : (
                      <span className="not-recovered">—</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Dashboard;