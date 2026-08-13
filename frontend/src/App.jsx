import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import './App.css';

// Components
import Header from './components/common/Header';
import Footer from './components/common/Footer';
import HomePage from './pages/HomePage';
import SubmitCase from './pages/SubmitCase';
import Dashboard from './pages/Dashboard';
import ContactPage from './pages/ContactPage';
import Login from './pages/Login';
import Register from './pages/Register';

function App() {
  const { i18n } = useTranslation();
  const isRTL = i18n.language === 'ar';

  return (
    <Router>
      <div className={`app ${isRTL ? 'rtl' : 'ltr'}`} dir={isRTL ? 'rtl' : 'ltr'}>
        <Header />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/submit" element={<SubmitCase />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/contact" element={<ContactPage />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;