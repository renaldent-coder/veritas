import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import './SubmitCase.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

function SubmitCase() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [caseNumber, setCaseNumber] = useState('');
  const [formData, setFormData] = useState({
    lossAmount: '',
    currency: 'USD',
    firstTransaction: '',
    lastTransaction: '',
    transactionMethod: 'CRYPTO',
    // Crypto fields
    senderWallet: '',
    recipientWallet: '',
    txid: '',
    // Bank fields
    bankName: '',
    beneficiaryName: '',
    beneficiaryAccount: '',
    swiftCode: '',
    exchangePlatform: '',
    scamCategory: 'FAKE_INVESTMENT',
    narrative: '',
    // Agreements
    agreedNda: false,
    agreedFee: false,
  });
  const [files, setFiles] = useState([]);

  // Live fee calculation
  const fee = parseFloat(formData.lossAmount) * 0.10 || 0;
  const clientKeeps = parseFloat(formData.lossAmount) - fee || 0;

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const { getRootProps, getInputProps } = useDropzone({
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.gif'],
      'application/pdf': ['.pdf'],
      'text/plain': ['.txt', '.log'],
    },
    maxSize: 50 * 1024 * 1024,
    onDrop: (accepted) => setFiles(accepted),
  });

  const nextStep = () => setStep(step + 1);
  const prevStep = () => setStep(step - 1);

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const payload = {
        loss_amount: parseFloat(formData.lossAmount),
        currency: formData.currency,
        first_transaction_date: formData.firstTransaction,
        last_transaction_date: formData.lastTransaction,
        transaction_method: formData.transactionMethod,
        transaction_data: {
          sender_wallet: formData.senderWallet,
          recipient_wallet: formData.recipientWallet,
          txid: formData.txid,
          bank_name: formData.bankName,
          beneficiary_name: formData.beneficiaryName,
          beneficiary_account: formData.beneficiaryAccount,
          swift_code: formData.swiftCode,
          exchange_platform: formData.exchangePlatform,
        },
        scam_category: formData.scamCategory,
        narrative: formData.narrative,
        agreed_nda: formData.agreedNda,
        agreed_fee: formData.agreedFee,
      };
      
      // Submit the case via API
      const response = await axios.post(`${API_URL}/cases/`, payload, {
        headers: { Authorization: `Token ${token}` },
      });
      
      // If files exist, upload them
      if (files.length > 0 && response.data.id) {
        const formDataUpload = new FormData();
        files.forEach(file => {
          formDataUpload.append('documents', file);
        });
        await axios.post(`${API_URL}/cases/${response.data.id}/upload/`, formDataUpload, {
          headers: { 
            Authorization: `Token ${token}`,
            'Content-Type': 'multipart/form-data',
          },
        });
      }
      
      setCaseNumber(response.data.case_number);
      setSubmitted(true);
    } catch (error) {
      console.error('Submission error:', error);
      alert('Submission failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (submitted) {
    return (
      <div className="success-page">
        <div className="success-card">
          <div className="success-icon">✅</div>
          <h1>{t('wizard.success')}</h1>
          <p>{t('wizard.success_message')}</p>
          <p className="case-number-display">
            <strong>{caseNumber}</strong>
          </p>
          <button onClick={() => navigate('/dashboard')} className="btn-dashboard">
            {t('dashboard.title')}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="submit-case">
      <div className="wizard-container">
        <div className="wizard-header">
          <div className="step-indicators">
            {[1, 2, 3, 4].map((s) => (
              <div key={s} className={`step-dot ${s === step ? 'active' : ''} ${s < step ? 'completed' : ''}`}>
                {s}
              </div>
            ))}
          </div>
          <h2>{t(`wizard.step${step}`)}</h2>
          <p>{t(`wizard.step${step}_title`)}</p>
        </div>

        <div className="wizard-body">
          {step === 1 && (
            <div className="step-content">
              <div className="form-group">
                <label>{t('wizard.loss_amount')}</label>
                <input
                  type="number"
                  name="lossAmount"
                  value={formData.lossAmount}
                  onChange={handleChange}
                  placeholder="e.g., 50000"
                  className="form-control"
                  required
                />
              </div>
              <div className="form-group">
                <label>{t('wizard.first_transaction')}</label>
                <input
                  type="date"
                  name="firstTransaction"
                  value={formData.firstTransaction}
                  onChange={handleChange}
                  className="form-control"
                  required
                />
              </div>
              <div className="form-group">
                <label>{t('wizard.last_transaction')}</label>
                <input
                  type="date"
                  name="lastTransaction"
                  value={formData.lastTransaction}
                  onChange={handleChange}
                  className="form-control"
                  required
                />
              </div>
            </div>
          )}

          {step === 2 && (
            <div className="step-content">
              <div className="form-group">
                <label>{t('wizard.transaction_method')}</label>
                <select
                  name="transactionMethod"
                  value={formData.transactionMethod}
                  onChange={handleChange}
                  className="form-control"
                >
                  <option value="CRYPTO">{t('wizard.crypto')}</option>
                  <option value="BANK_WIRE">{t('wizard.bank_wire')}</option>
                  <option value="CREDIT_CARD">{t('wizard.credit_card')}</option>
                  <option value="GIFT_CARD">{t('wizard.gift_card')}</option>
                  <option value="OTHER">{t('wizard.other')}</option>
                </select>
              </div>

              {formData.transactionMethod === 'CRYPTO' && (
                <>
                  <div className="form-group">
                    <label>{t('wizard.wallet_address')}</label>
                    <input
                      type="text"
                      name="senderWallet"
                      value={formData.senderWallet}
                      onChange={handleChange}
                      className="form-control"
                    />
                  </div>
                  <div className="form-group">
                    <label>{t('wizard.recipient_address')}</label>
                    <input
                      type="text"
                      name="recipientWallet"
                      value={formData.recipientWallet}
                      onChange={handleChange}
                      className="form-control"
                    />
                  </div>
                  <div className="form-group">
                    <label>{t('wizard.txid')}</label>
                    <input
                      type="text"
                      name="txid"
                      value={formData.txid}
                      onChange={handleChange}
                      className="form-control"
                    />
                  </div>
                </>
              )}

              {formData.transactionMethod === 'BANK_WIRE' && (
                <>
                  <div className="form-group">
                    <label>{t('wizard.bank_name')}</label>
                    <input
                      type="text"
                      name="bankName"
                      value={formData.bankName}
                      onChange={handleChange}
                      className="form-control"
                    />
                  </div>
                  <div className="form-group">
                    <label>{t('wizard.beneficiary_name')}</label>
                    <input
                      type="text"
                      name="beneficiaryName"
                      value={formData.beneficiaryName}
                      onChange={handleChange}
                      className="form-control"
                    />
                  </div>
                  <div className="form-group">
                    <label>{t('wizard.beneficiary_account')}</label>
                    <input
                      type="text"
                      name="beneficiaryAccount"
                      value={formData.beneficiaryAccount}
                      onChange={handleChange}
                      className="form-control"
                    />
                  </div>
                  <div className="form-group">
                    <label>{t('wizard.swift_code')}</label>
                    <input
                      type="text"
                      name="swiftCode"
                      value={formData.swiftCode}
                      onChange={handleChange}
                      className="form-control"
                    />
                  </div>
                </>
              )}

              <div className="form-group">
                <label>{t('wizard.exchange_platform')}</label>
                <input
                  type="text"
                  name="exchangePlatform"
                  value={formData.exchangePlatform}
                  onChange={handleChange}
                  className="form-control"
                />
              </div>
            </div>
          )}

          {step === 3 && (
            <div className="step-content">
              <div className="form-group">
                <label>{t('wizard.scam_category')}</label>
                <select
                  name="scamCategory"
                  value={formData.scamCategory}
                  onChange={handleChange}
                  className="form-control"
                >
                  <option value="FAKE_INVESTMENT">{t('wizard.fake_investment')}</option>
                  <option value="ROMANCE">{t('wizard.romance')}</option>
                  <option value="IMPERSONATION">{t('wizard.impersonation')}</option>
                  <option value="PHISHING">{t('wizard.phishing')}</option>
                  <option value="FAKE_JOB">{t('wizard.fake_job')}</option>
                  <option value="CRYPTO_RUGPULL">{t('wizard.crypto_rugpull')}</option>
                  <option value="BANK_WIRE_FRAUD">{t('wizard.bank_wire_fraud')}</option>
                  <option value="OTHER">{t('wizard.other_scam')}</option>
                </select>
              </div>
              <div className="form-group">
                <label>{t('wizard.narrative')}</label>
                <textarea
                  name="narrative"
                  value={formData.narrative}
                  onChange={handleChange}
                  rows="5"
                  className="form-control"
                  placeholder={t('wizard.narrative')}
                />
              </div>
              <div className="form-group">
                <label>{t('wizard.upload_evidence')}</label>
                <div {...getRootProps()} className="dropzone">
                  <input {...getInputProps()} />
                  <p>{t('wizard.upload_hint')}</p>
                  {files.length > 0 && (
                    <ul className="file-list">
                      {files.map((f, i) => <li key={i}>{f.name} ({(f.size/1024).toFixed(0)} KB)</li>)}
                    </ul>
                  )}
                </div>
              </div>
            </div>
          )}

          {step === 4 && (
            <div className="step-content review-step">
              <h3>{t('wizard.fee_calculation')}</h3>
              <div className="fee-breakdown">
                <div className="fee-row">
                  <span>{t('wizard.loss')}</span>
                  <span className="amount">${parseFloat(formData.lossAmount || 0).toLocaleString()}</span>
                </div>
                <div className="fee-row">
                  <span>{t('wizard.fee_amount')}</span>
                  <span className="amount-gold">${fee.toLocaleString()}</span>
                </div>
                <div className="fee-row total">
                  <span>{t('wizard.you_receive')}</span>
                  <span className="amount-green">${clientKeeps.toLocaleString()}</span>
                </div>
              </div>

              <div className="agreement-checkboxes">
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    name="agreedNda"
                    checked={formData.agreedNda}
                    onChange={handleChange}
                  />
                  {t('wizard.agree_terms')}
                </label>
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    name="agreedFee"
                    checked={formData.agreedFee}
                    onChange={handleChange}
                  />
                  {t('wizard.agree_fee')}
                </label>
              </div>
            </div>
          )}
        </div>

        <div className="wizard-footer">
          {step > 1 && (
            <button onClick={prevStep} className="btn-secondary">
              {t('common.back')}
            </button>
          )}
          {step < 4 ? (
            <button onClick={nextStep} className="btn-primary">
              {t('common.next')}
            </button>
          ) : (
            <button
              onClick={handleSubmit}
              disabled={loading || !formData.agreedNda || !formData.agreedFee || !formData.lossAmount}
              className="btn-submit"
            >
              {loading ? t('common.loading') : t('wizard.submit')}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

export default SubmitCase;