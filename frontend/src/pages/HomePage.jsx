import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import './HomePage.css';

function HomePage() {
  const { t } = useTranslation();
  const [lossAmount, setLossAmount] = useState('');
  
  const calculateFee = (amount) => {
    const num = parseFloat(amount);
    if (isNaN(num) || num <= 0) return null;
    return {
      fee: num * 0.10,
      clientKeeps: num * 0.90,
    };
  };
  
  const result = calculateFee(lossAmount);

  return (
    <div className="homepage">
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-container">
          <div className="hero-content">
            <h1 className="hero-title">{t('home.hero.title')}</h1>
            <p className="hero-subtitle">{t('home.hero.subtitle')}</p>
            <div className="hero-stats">
              <span className="stat-badge">⭐ {t('home.hero.stats')}</span>
            </div>
            <Link to="/register" className="hero-cta">
              {t('home.hero.cta')}
            </Link>
          </div>
        </div>
      </section>

      {/* Fee Estimator */}
      <section className="fee-estimator">
        <div className="container">
          <h2 className="section-title">{t('home.fee_estimator.title')}</h2>
          <div className="estimator-box">
            <div className="estimator-input-group">
              <label>{t('home.fee_estimator.label')}</label>
              <input
                type="number"
                min="0"
                step="100"
                value={lossAmount}
                onChange={(e) => setLossAmount(e.target.value)}
                placeholder="e.g., 50000"
                className="estimator-input"
              />
            </div>
            {result && (
              <div className="estimator-results">
                <div className="result-row">
                  <span>{t('home.fee_estimator.you_keep')}</span>
                  <span className="amount-green">${result.clientKeeps.toLocaleString()}</span>
                </div>
                <div className="result-row">
                  <span>{t('home.fee_estimator.our_fee')}</span>
                  <span className="amount-gold">${result.fee.toLocaleString()}</span>
                </div>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="how-it-works">
        <div className="container">
          <h2 className="section-title">{t('home.how_it_works.title')}</h2>
          <div className="steps-grid">
            <div className="step-card">
              <div className="step-number">1</div>
              <h3>{t('home.how_it_works.step1')}</h3>
              <p>{t('home.how_it_works.step1_desc')}</p>
            </div>
            <div className="step-card">
              <div className="step-number">2</div>
              <h3>{t('home.how_it_works.step2')}</h3>
              <p>{t('home.how_it_works.step2_desc')}</p>
            </div>
            <div className="step-card">
              <div className="step-number">3</div>
              <h3>{t('home.how_it_works.step3')}</h3>
              <p>{t('home.how_it_works.step3_desc')}</p>
            </div>
            <div className="step-card">
              <div className="step-number">4</div>
              <h3>{t('home.how_it_works.step4')}</h3>
              <p>{t('home.how_it_works.step4_desc')}</p>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="testimonials">
        <div className="container">
          <h2 className="section-title">{t('home.testimonials.title')}</h2>
          <div className="testimonial-grid">
            <div className="testimonial-card">
              <p>"{t('home.testimonials.client1')}"</p>
              <span>— A.R., Germany</span>
            </div>
            <div className="testimonial-card">
              <p>"{t('home.testimonials.client2')}"</p>
              <span>— M.S., UK</span>
            </div>
            <div className="testimonial-card">
              <p>"{t('home.testimonials.client3')}"</p>
              <span>— J.L., USA</span>
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="cta-section">
        <div className="container">
          <h2>{t('home.cta_section.title')}</h2>
          <p>{t('home.cta_section.subtitle')}</p>
          <Link to="/register" className="cta-button">
            {t('home.cta_section.button')}
          </Link>
        </div>
      </section>
    </div>
  );
}

export default HomePage;