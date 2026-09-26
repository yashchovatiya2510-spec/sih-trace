import React from 'react';
import { useNavigate } from 'react-router-dom';

const AdminDashboard = () => {
  const navigate = useNavigate();
  return (
    <div>
      <nav className="bg-purple-900 text-white p-4 flex justify-between items-center shadow-md">
        <div className="font-bold text-xl flex items-center gap-2">
          <span>⚙️</span> T.R.A.C.E. | Global Admin Control Panel
        </div>
        <button onClick={() => navigate('/login')} className="bg-purple-700 px-4 py-2 rounded hover:bg-purple-600 transition-colors">
          Secure Logout
        </button>
      </nav>
      <div className="p-8">
        <div className="mb-6 flex justify-between items-end">
          <div>
            <h1 className="text-3xl font-bold text-slate-800">Master Administration</h1>
            <p className="text-gray-600 mt-1">Full access to manage users, NGOs, schemes, and system data.</p>
          </div>
          <span className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm font-bold border border-purple-200">
            Role: SUPER ADMIN
          </span>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
            <h3 className="text-gray-500 text-sm font-medium">Total Users</h3>
            <p className="text-3xl font-bold mt-2 text-slate-700">128</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
            <h3 className="text-gray-500 text-sm font-medium">Registered NGOs</h3>
            <p className="text-3xl font-bold mt-2 text-slate-700">42</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
            <h3 className="text-gray-500 text-sm font-medium">Active Schemes</h3>
            <p className="text-3xl font-bold mt-2 text-slate-700">8</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
            <h3 className="text-gray-500 text-sm font-medium">Total Funds Monitored</h3>
            <p className="text-3xl font-bold mt-2 text-green-600">₹12.4 Cr</p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
            <div className="bg-slate-50 px-6 py-4 border-b border-gray-200 flex justify-between items-center">
              <h2 className="text-lg font-semibold text-slate-800">Entity Management</h2>
            </div>
            <div className="p-2">
              <div className="flex flex-col">
                <button className="text-left px-6 py-4 hover:bg-purple-50 transition-colors border-b border-gray-100 flex justify-between items-center group">
                  <span className="font-medium text-slate-700 group-hover:text-purple-700">Manage Users & Roles</span>
                  <span className="text-gray-400 group-hover:text-purple-500">→</span>
                </button>
                <button className="text-left px-6 py-4 hover:bg-purple-50 transition-colors border-b border-gray-100 flex justify-between items-center group">
                  <span className="font-medium text-slate-700 group-hover:text-purple-700">NGO Approvals & Suspensions</span>
                  <span className="text-gray-400 group-hover:text-purple-500">→</span>
                </button>
                <button className="text-left px-6 py-4 hover:bg-purple-50 transition-colors border-b border-gray-100 flex justify-between items-center group">
                  <span className="font-medium text-slate-700 group-hover:text-purple-700">Configure Government Schemes</span>
                  <span className="text-gray-400 group-hover:text-purple-500">→</span>
                </button>
                <button className="text-left px-6 py-4 hover:bg-purple-50 transition-colors flex justify-between items-center group">
                  <span className="font-medium text-red-600 group-hover:text-red-700">Database Wipe / Reset (Danger)</span>
                  <span className="text-red-400 group-hover:text-red-600">→</span>
                </button>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
            <div className="bg-slate-50 px-6 py-4 border-b border-gray-200 flex justify-between items-center">
              <h2 className="text-lg font-semibold text-slate-800">System Logs & AI Health</h2>
            </div>
            <div className="p-6">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-gray-600">API Status</span>
                  <span className="flex items-center gap-2 text-sm text-green-600"><span className="w-2 h-2 rounded-full bg-green-500"></span> Online</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-gray-600">Database Connection</span>
                  <span className="flex items-center gap-2 text-sm text-green-600"><span className="w-2 h-2 rounded-full bg-green-500"></span> Stable</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-gray-600">YOLO AI Module (Headcount)</span>
                  <span className="flex items-center gap-2 text-sm text-yellow-600"><span className="w-2 h-2 rounded-full bg-yellow-500"></span> Running (Stub Mode)</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-gray-600">OCR Module (Tesseract)</span>
                  <span className="flex items-center gap-2 text-sm text-green-600"><span className="w-2 h-2 rounded-full bg-green-500"></span> Active</span>
                </div>
              </div>
              <button className="mt-6 w-full bg-slate-800 text-white py-2 rounded hover:bg-slate-700 transition-colors">
                View Detailed Audit Logs
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
