/**
 * ProtectedRoute — wraps pages that require a specific role.
 *
 * Usage:
 *   <Route path="/disease-detection"
 *     element={<ProtectedRoute roles={['FARMER','ADMIN']}><PlantDiseaseDetection /></ProtectedRoute>} />
 */
import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { ShieldAlert, LogIn } from 'lucide-react';

const ProtectedRoute = ({ children, roles = [] }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-green-600" />
      </div>
    );
  }

  // Not logged in
  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 to-emerald-50 px-4">
        <div className="bg-white rounded-2xl shadow-xl p-8 max-w-md w-full text-center">
          <LogIn className="w-12 h-12 text-green-600 mx-auto mb-4" />
          <h2 className="text-xl font-bold text-gray-800 mb-2">Login Required</h2>
          <p className="text-gray-500 mb-6">
            You need to be logged in to access this feature.
          </p>
          <Link
            to="/LoginPage"
            className="inline-block px-6 py-3 bg-green-600 text-white rounded-xl font-semibold hover:bg-green-700 transition-colors"
          >
            Go to Login
          </Link>
        </div>
      </div>
    );
  }

  // Logged in but wrong role
  const userRole = (user.role || '').toUpperCase();
  if (roles.length > 0 && !roles.map(r => r.toUpperCase()).includes(userRole)) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-red-50 to-orange-50 px-4">
        <div className="bg-white rounded-2xl shadow-xl p-8 max-w-md w-full text-center">
          <ShieldAlert className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-bold text-gray-800 mb-2">Access Denied</h2>
          <p className="text-gray-500 mb-2">
            Your role <span className="font-semibold text-gray-700">{user.role}</span> does not have
            permission to access this page.
          </p>
          <p className="text-sm text-gray-400 mb-6">
            Required role: {roles.join(' or ')}
          </p>
          <Link
            to="/"
            className="inline-block px-6 py-3 bg-gray-700 text-white rounded-xl font-semibold hover:bg-gray-800 transition-colors"
          >
            Back to Home
          </Link>
        </div>
      </div>
    );
  }

  return children;
};

export default ProtectedRoute;
