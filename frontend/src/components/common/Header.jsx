import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import './Header.css';

function Header() {
  const { t, i18n } = useTranslation();
  const navigate = useNavigate();
  const isAuthenticated = localStorage.getItem('token'); // Simple auth check

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
    document.documentElement.dir = lng === 'ar' ? 'rtl' : 'ltr';
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/');
  };

  return (
    <header className="header">
      <div className="header-container">
        <div className="header-left">
          <Link to="/" className="logo">
            <span className="logo-icon">⚖️</span>
            <span className="logo-text">Veritas</span>
            <span className="logo-sub">Asset Recovery</span>
          </Link>
        </div>

        <nav className="header-nav">
          <Link to="/" className="nav-link">{t('header.home')}</Link>
          <Link to="/submit" className="nav-link nav-link-gold">{t('header.submit')}</Link>
          {isAuthenticated && (
            <Link to="/dashboard" className="nav-link">{t('header.dashboard')}</Link>
          )}
          <Link to="/contact" className="nav-link">
            <span className="telegram-icon">📱</span> {t('header.contact')}
          </Link>
        </nav>

        <div className="header-right">
          <div className="language-switcher">
            <button 
              onClick={() => changeLanguage('en')} 
              className={`lang-btn ${i18n.language === 'en' ? 'active' : ''}`}
            >
              EN
            </button>
            <button 
              onClick={() => changeLanguage('es')} 
              className={`lang-btn ${i18n.language === 'es' ? 'active' : ''}`}
            >
              ES
            </button>
            <button 
              onClick={() => changeLanguage('fr')} 
              className={`lang-btn ${i18n.language === 'fr' ? 'active' : ''}`}
            >
              FR
            </button>
            <button 
              onClick={() => changeLanguage('ar')} 
              className={`lang-btn ${i18n.language === 'ar' ? 'active' : ''}`}
            >
              ع
            </button>
          </div>

          <div className="auth-buttons">
            {isAuthenticated ? (
              <button onClick={handleLogout} className="btn-logout">
                {t('header.logout')}
              </button>
            ) : (
              <>
                <Link to="/login" className="btn-login">{t('header.login')}</Link>
                <Link to="/register" className="btn-register">{t('header.register')}</Link>
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;