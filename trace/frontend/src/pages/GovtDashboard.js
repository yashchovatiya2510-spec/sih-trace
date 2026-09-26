import React from 'react';
import { useNavigate } from 'react-router-dom';

const GovtDashboard = () => {
  const navigate = useNavigate();
  return (
    <div>
      <nav className="bg-slate-800 text-white p-4 flex justify-between items-center">
        <div className="font-bold text-xl">T.R.A.C.E. | DoSJE Dashboard</div>
        <button onClick={() => navigate('/login')} className="bg-slate-700 px-4 py-2 rounded hover:bg-slate-600">Logout</button>
      </nav>
      <div className="p-8">
        <h1 className="text-2xl font-bold mb-6">Government Oversight Overview</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow border-l-4 border-blue-500">
            <h3 className="text-gray-500 text-sm font-medium">Active Schemes</h3>
            <p className="text-3xl font-bold mt-2">4</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow border-l-4 border-green-500">
            <h3 className="text-gray-500 text-sm font-medium">NGOs Monitored</h3>
            <p className="text-3xl font-bold mt-2">4</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow border-l-4 border-red-500">
            <h3 className="text-gray-500 text-sm font-medium">Critical Alerts</h3>
            <p className="text-3xl font-bold mt-2 text-red-600">2</p>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Recent Fraud Alerts</h2>
          <div className="space-y-4">
            <div className="border-l-4 border-red-500 pl-4 py-2">
              <p className="font-bold text-red-700">Geo-Spoofing Detected in Evidence Submission</p>
              <p className="text-sm text-gray-600">Swachh India Trust (NAMASTE) - EXIF GPS coordinates do not match network IP location.</p>
            </div>
            <div className="border-l-4 border-orange-500 pl-4 py-2">
              <p className="font-bold text-orange-700">Invoice Price 45% Above GeM Rate</p>
              <p className="text-sm text-gray-600">SkillBridge Foundation (PM-DAKSH) - Training materials overpriced vs GeM benchmark.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GovtDashboard;
