/**
 * AuthContext – stores JWT + user info in localStorage; provides login/register/logout.
 */
import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { API_URL } from '../config/api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);

  // Hydrate from localStorage on mount
  useEffect(() => {
    const stored = localStorage.getItem('smartcropx_auth');
    if (stored) {
      try {
        const parsed = JSON.parse(stored);
        setToken(parsed.token);
        setUser(parsed.user);
      } catch {
        localStorage.removeItem('smartcropx_auth');
      }
    }
    setLoading(false);
  }, []);

  const persist = (tok, usr) => {
    localStorage.setItem('smartcropx_auth', JSON.stringify({ token: tok, user: usr }));
    setToken(tok);
    setUser(usr);
  };

  const register = async (full_name, email, password, role = 'FARMER') => {
    const res = await axios.post(`${API_URL}/api/auth/register`, { full_name, email, password, role });
    persist(res.data.access_token, res.data.user);
    return res.data;
  };

  const login = async (email, password) => {
    const res = await axios.post(`${API_URL}/api/auth/login`, { email, password });
    persist(res.data.access_token, res.data.user);
    return res.data;
  };

  const logout = useCallback(() => {
    localStorage.removeItem('smartcropx_auth');
    setToken(null);
    setUser(null);
  }, []);

  // Role helpers
  const role = user?.role || null;
  const isAdmin = role === 'ADMIN';
  const isFarmer = role === 'FARMER';
  const isBuyer = role === 'BUYER';
  const hasRole = (...roles) => roles.map(r => r.toUpperCase()).includes((role || '').toUpperCase());

  // Axios instance with auto Bearer header
  const authAxios = useCallback(() => {
    const instance = axios.create({ baseURL: API_URL });
    if (token) {
      instance.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    }
    return instance;
  }, [token]);

  return (
    <AuthContext.Provider value={{ user, token, loading, register, login, logout, authAxios, role, isAdmin, isFarmer, isBuyer, hasRole }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used inside AuthProvider');
  return ctx;
}

export default AuthContext;
