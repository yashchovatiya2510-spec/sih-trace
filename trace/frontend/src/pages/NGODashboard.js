import React from 'react';
import { useNavigate } from 'react-router-dom';

const NGODashboard = () => {
  const navigate = useNavigate();
  return (
    <div>
      <nav className="bg-teal-800 text-white p-4 flex justify-between items-center">
        <div className="font-bold text-xl">T.R.A.C.E. | NGO Portal</div>
        <button onClick={() => navigate('/login')} className="bg-teal-700 px-4 py-2 rounded hover:bg-teal-600">Logout</button>
      </nav>
      <div className="p-8">
        <div className="flex justify-between items-end mb-6">
          <h1 className="text-2xl font-bold">Jan Shiksha Sansthan</h1>
          <p className="text-gray-600">Compliance Score: <span className="text-green-600 font-bold">88.5%</span></p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-lg font-bold mb-4">Active Claims</h2>
            <div className="border border-gray-200 rounded p-4 flex justify-between items-center">
              <div>
                <p className="font-medium">Q2 FY2025-26 - SHRESTA</p>
                <p className="text-sm text-gray-500">₹18,50,000 claimed</p>
              </div>
              <span className="bg-green-100 text-green-800 text-xs font-semibold px-2.5 py-0.5 rounded">Inspection Done</span>
            </div>
          </div>
          
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-lg font-bold mb-4">Quick Actions</h2>
            <div className="space-y-3">
              <button className="w-full text-left px-4 py-3 border border-gray-200 rounded hover:bg-gray-50 font-medium text-gray-700">
                + Submit New Claim
              </button>
              <button className="w-full text-left px-4 py-3 border border-gray-200 rounded hover:bg-gray-50 font-medium text-gray-700">
                ↑ Upload Beneficiary List
              </button>
              <button className="w-full text-left px-4 py-3 border border-gray-200 rounded hover:bg-gray-50 font-medium text-gray-700">
                📄 Upload Invoices for OCR
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NGODashboard;
