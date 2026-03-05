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
    try {
      const res = await axios.post(`${API_URL}/api/auth/register`, {
        full_name: full_name.trim(),
        email: email.trim().toLowerCase(),
        password,
        role: role.toUpperCase(),
      });
      persist(res.data.access_token, res.data.user);
      return res.data;
    } catch (err) {
      // Re-throw with a clear message the UI can display
      const status = err.response?.status;
      const detail = err.response?.data?.detail;
      if (status === 409) {
        const err409 = new Error(detail || 'This email is already registered. Please login.');
        err409.status = 409;
        throw err409;
      }
      if (status === 422) throw new Error('Invalid input – please check all fields');
      throw new Error(detail || 'Registration failed');
    }
  };

  const login = async (email, password) => {
    try {
      const res = await axios.post(`${API_URL}/api/auth/login`, {
        email: email.trim().toLowerCase(),
        password,
      });
      persist(res.data.access_token, res.data.user);
      return res.data;
    } catch (err) {
      const detail = err.response?.data?.detail;
      throw new Error(detail || 'Invalid email or password');
    }
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
  const isAgronomist = role === 'AGRONOMIST';
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
    <AuthContext.Provider value={{ user, token, loading, register, login, logout, authAxios, role, isAdmin, isFarmer, isAgronomist, hasRole }}>
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
