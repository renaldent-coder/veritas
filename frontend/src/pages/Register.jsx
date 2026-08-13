import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate, Link } from 'react-router-dom';
import { authService } from '../services/api';
import './Auth.css';

function Register() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    confirm_password: '',
    phone: '',
    country: '',
    telegram: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (formData.password !== formData.confirm_password) {
      setError('Passwords do not match');
      return;
    }

    setLoading(true);

    try {
      const payload = {
        first_name: formData.first_name,
        last_name: formData.last_name,
        email: formData.email,
        password: formData.password,
        phone_number: formData.phone,
        country: formData.country,
        telegram_handle: formData.telegram,
      };
      const response = await authService.register(payload);
      // Auto-login after registration
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h2 className="auth-title">{t('auth.register_title')}</h2>
        <p className="auth-subtitle">{t('auth.register_subtitle')}</p>

        {error && <div className="auth-error">{error}</div>}

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-row">
            <div className="form-group half">
              <label>{t('auth.first_name')}</label>
              <input
                type="text"
                name="first_name"
                value={formData.first_name}
                onChange={handleChange}
                className="form-control"
                required
              />
            </div>
            <div className="form-group half">
              <label>{t('auth.last_name')}</label>
              <input
                type="text"
                name="last_name"
                value={formData.last_name}
                onChange={handleChange}
                className="form-control"
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label>{t('auth.email')}</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className="form-control"
              required
            />
          </div>

          <div className="form-row">
            <div className="form-group half">
              <label>{t('auth.password')}</label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className="form-control"
                required
              />
            </div>
            <div className="form-group half">
              <label>{t('auth.confirm_password')}</label>
              <input
                type="password"
                name="confirm_password"
                value={formData.confirm_password}
                onChange={handleChange}
                className="form-control"
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label>{t('auth.phone')}</label>
            <input
              type="text"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              className="form-control"
            />
          </div>

          <div className="form-group">
            <label>{t('auth.country')}</label>
            <input
              type="text"
              name="country"
              value={formData.country}
              onChange={handleChange}
              className="form-control"
              placeholder="e.g., USA, UK, Germany"
            />
          </div>

          <div className="form-group">
            <label>{t('auth.telegram')}</label>
            <input
              type="text"
              name="telegram"
              value={formData.telegram}
              onChange={handleChange}
              className="form-control"
              placeholder="@username"
            />
          </div>

          <button type="submit" className="btn-primary auth-btn" disabled={loading}>
            {loading ? t('common.loading') : t('auth.register_button')}
          </button>
        </form>

        <p className="auth-switch">
          {t('auth.already_have_account')}{' '}
          <Link to="/login">{t('auth.login_title')}</Link>
        </p>
      </div>
    </div>
  );
}

export default Register;