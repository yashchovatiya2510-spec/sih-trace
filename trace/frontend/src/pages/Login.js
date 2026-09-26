import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    // Dummy login logic based on email prefix for demo
    if (email.includes('admin')) {
      navigate('/admin');
    } else if (email.includes('officer')) {
      navigate('/govt');
    } else if (email.includes('inspector')) {
      navigate('/pmu');
    } else if (email.includes('ngo')) {
      navigate('/ngo');
    } else {
      navigate('/beneficiary');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-900">
      <div className="bg-white p-8 rounded-lg shadow-xl w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-slate-800">T.R.A.C.E.</h1>
          <p className="text-slate-500 mt-2">Transparent Resource & Audit Compliance Ecosystem</p>
        </div>
        
        <form onSubmit={handleLogin} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700">Email Address</label>
            <input 
              type="email" 
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500" 
              placeholder="user@example.com" 
              required 
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Password</label>
            <input 
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500" 
              placeholder="••••••••" 
              required 
            />
          </div>
          <button type="submit" className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500">
            Sign In
          </button>
        </form>
        
        <div className="mt-6 text-sm text-center text-gray-500">
          Demo: Use officer@ / inspector@ / ngo@ / beneficiary@ to route appropriately.
        </div>
      </div>
    </div>
  );
};

export default Login;
