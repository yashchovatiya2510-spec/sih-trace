import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import GovtDashboard from './pages/GovtDashboard';
import PMUDashboard from './pages/PMUDashboard';
import NGODashboard from './pages/NGODashboard';
import BeneficiaryPortal from './pages/BeneficiaryPortal';
import AdminDashboard from './pages/AdminDashboard';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/admin/*" element={<AdminDashboard />} />
          <Route path="/govt/*" element={<GovtDashboard />} />
          <Route path="/pmu/*" element={<PMUDashboard />} />
          <Route path="/ngo/*" element={<NGODashboard />} />
          <Route path="/beneficiary/*" element={<BeneficiaryPortal />} />
          <Route path="/" element={<Navigate to="/login" replace />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
