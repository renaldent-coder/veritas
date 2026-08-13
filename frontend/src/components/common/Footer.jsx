import React from 'react';
import { useTranslation } from 'react-i18next';
import './Footer.css';

function Footer() {
  const { t } = useTranslation();
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-section">
          <h3 className="footer-logo">Veritas Asset Recovery</h3>
          <p className="footer-tagline">{t('header.tagline')}</p>
          <div className="footer-social">
            <a href="https://t.me/Renaldeti" target="_blank" rel="noopener noreferrer" className="social-link">
              Telegram
            </a>
          </div>
        </div>
        <div className="footer-section">
          <h4>Quick Links</h4>
          <ul className="footer-links">
            <li><a href="/">{t('header.home')}</a></li>
            <li><a href="/submit">{t('header.submit')}</a></li>
            <li><a href="/contact">{t('header.contact')}</a></li>
          </ul>
        </div>
        <div className="footer-section">
          <h4>Legal</h4>
          <ul className="footer-links">
            <li><a href="/privacy">Privacy Policy</a></li>
            <li><a href="/terms">Terms of Service</a></li>
            <li><a href="/disclaimer">Disclaimer</a></li>
          </ul>
        </div>
        <div className="footer-bottom">
          <p>&copy; {currentYear} Veritas Asset Recovery. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}

export default Footer;