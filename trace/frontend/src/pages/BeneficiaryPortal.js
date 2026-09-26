import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const BeneficiaryPortal = () => {
  const navigate = useNavigate();
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitted(true);
  };

  return (
    <div>
      <nav className="bg-orange-600 text-white p-4 flex justify-between items-center">
        <div className="font-bold text-xl">T.R.A.C.E. | Jan Portal</div>
        <button onClick={() => navigate('/login')} className="bg-orange-500 px-4 py-2 rounded hover:bg-orange-400">Exit</button>
      </nav>
      
      <div className="p-4 max-w-lg mx-auto mt-8">
        {!submitted ? (
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-bold mb-2">Raise Grievance / SOS</h2>
            <p className="text-gray-600 mb-6 text-sm">Your report will be anonymous. Help us stop fraud.</p>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Issue Type</label>
                <select className="w-full border border-gray-300 rounded p-2 focus:ring-orange-500 focus:border-orange-500">
                  <option>Food Quality is bad</option>
                  <option>Missing Services / Kits not given</option>
                  <option>Staff Misconduct</option>
                  <option>Fake Attendance being marked</option>
                  <option>Other</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                <textarea 
                  className="w-full border border-gray-300 rounded p-2 focus:ring-orange-500 focus:border-orange-500 h-24"
                  placeholder="Explain what is happening..."
                  required
                ></textarea>
              </div>
              
              <button type="submit" className="w-full bg-orange-600 text-white font-bold py-3 rounded hover:bg-orange-700">
                Submit Report Anonymously
              </button>
            </form>
          </div>
        ) : (
          <div className="bg-green-50 border-l-4 border-green-500 p-6 rounded shadow text-center">
            <div className="text-green-500 text-5xl mb-4">✓</div>
            <h2 className="text-xl font-bold text-green-800 mb-2">Grievance Submitted!</h2>
            <p className="text-green-700 mb-4">Tracking code: <strong>TRC-X9M2KL</strong></p>
            <button onClick={() => navigate('/login')} className="bg-white border border-green-500 text-green-700 px-4 py-2 rounded hover:bg-green-50">
              Return Home
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default BeneficiaryPortal;
