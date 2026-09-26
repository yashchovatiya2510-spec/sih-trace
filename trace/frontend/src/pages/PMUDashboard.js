import React from 'react';
import { useNavigate } from 'react-router-dom';

const PMUDashboard = () => {
  const navigate = useNavigate();
  return (
    <div>
      <nav className="bg-blue-800 text-white p-4 flex justify-between items-center">
        <div className="font-bold text-xl">T.R.A.C.E. | PMU Inspector App</div>
        <button onClick={() => navigate('/login')} className="bg-blue-700 px-4 py-2 rounded hover:bg-blue-600">Logout</button>
      </nav>
      <div className="p-8">
        <h1 className="text-2xl font-bold mb-6">My Assignments</h1>
        
        <div className="bg-white rounded-lg shadow p-6 border-t-4 border-blue-500">
          <div className="flex justify-between items-start mb-4">
            <div>
              <h2 className="text-xl font-bold text-gray-800">Surprise Inspection: SkillBridge Foundation</h2>
              <p className="text-gray-600">Scheme: PM-DAKSH | District: South Delhi</p>
            </div>
            <span className="bg-yellow-100 text-yellow-800 text-xs font-semibold px-2.5 py-0.5 rounded">Pending</span>
          </div>
          
          <div className="bg-gray-50 p-4 rounded mb-4">
            <h3 className="font-medium text-sm text-gray-700 mb-2">Required Actions:</h3>
            <ul className="list-disc pl-5 text-sm text-gray-600 space-y-1">
              <li>Verify attendance via head-count</li>
              <li>Inspect training material quality</li>
              <li>Upload geo-tagged photos of classroom</li>
            </ul>
          </div>
          
          <button className="w-full bg-blue-600 text-white py-2 rounded font-medium hover:bg-blue-700">
            Start Inspection (Capture Geo-Tagged Evidence)
          </button>
        </div>
      </div>
    </div>
  );
};

export default PMUDashboard;
