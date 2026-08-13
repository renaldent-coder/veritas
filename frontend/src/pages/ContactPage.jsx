import React from 'react';
import { useTranslation } from 'react-i18next';
import './ContactPage.css';

function ContactPage() {
  const { t } = useTranslation();

  return (
    <div className="contact-page">
      <div className="contact-container">
        <div className="contact-card">
          <div className="contact-icon">📱</div>
          <h1 className="contact-title">{t('contact.title')}</h1>
          <p className="contact-subtitle">{t('contact.subtitle')}</p>
          
          <a 
            href="https://t.me/Renaldeti" 
            target="_blank" 
            rel="noopener noreferrer"
            className="contact-telegram-btn"
          >
            <span className="telegram-icon">✈️</span> {t('contact.button')}
          </a>

          <div className="contact-disclaimer">
            <span className="disclaimer-icon">⚠️</span>
            <p>{t('contact.disclaimer')}</p>
          </div>

          <div className="contact-alternate">
            <p>Or email us at:</p>
            <a href="mailto:Renaldent@gmail.com" className="contact-email">
              Renaldent@gmail.com
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ContactPage;