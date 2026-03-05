/**
 * CommunityFeed – /community
 * Lists posts with search, tag filter, sort. "Create Post" button for logged-in users.
 */
import React, { useState, useEffect, useCallback } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Heart, MessageCircle, Search, Plus, Filter, Clock, TrendingUp, Tag, User } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { API_URL } from '../config/api';
import axios from 'axios';

const CommunityFeed = () => {
  const { user, token } = useAuth();
  const navigate = useNavigate();

  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [tagFilter, setTagFilter] = useState('');
  const [sort, setSort] = useState('latest');
  const [error, setError] = useState('');

  const fetchPosts = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const params = new URLSearchParams();
      if (search) params.set('search', search);
      if (tagFilter) params.set('tag', tagFilter);
      params.set('sort', sort);

      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      const res = await axios.get(`${API_URL}/api/community/posts?${params}`, { headers });
      setPosts(res.data);
    } catch (err) {
      setError('Failed to load posts');
    } finally {
      setLoading(false);
    }
  }, [search, tagFilter, sort, token]);

  useEffect(() => { fetchPosts(); }, [fetchPosts]);

  const handleLike = async (postId) => {
    if (!user) { navigate('/LoginPage'); return; }
    try {
      const res = await axios.post(`${API_URL}/api/community/posts/${postId}/like`, {}, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setPosts(prev => prev.map(p =>
        p.id === postId ? { ...p, like_count: res.data.like_count, liked_by_me: res.data.liked_by_me } : p
      ));
    } catch { /* ignore */ }
  };

  // Gather unique tags from posts
  const allTags = [...new Set(posts.flatMap(p => (p.tags || '').split(',').map(t => t.trim()).filter(Boolean)))];

  // Skeleton loader
  const Skeleton = () => (
    <div className="animate-pulse bg-white rounded-xl p-6 shadow">
      <div className="h-4 bg-gray-200 rounded w-3/4 mb-3"></div>
      <div className="h-3 bg-gray-200 rounded w-full mb-2"></div>
      <div className="h-3 bg-gray-200 rounded w-5/6 mb-4"></div>
      <div className="flex space-x-4">
        <div className="h-3 bg-gray-200 rounded w-16"></div>
        <div className="h-3 bg-gray-200 rounded w-16"></div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50 pt-4 pb-12">
      <div className="max-w-4xl mx-auto px-4">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-800">Community</h1>
            <p className="text-gray-500 text-sm mt-1">Share knowledge, ask questions, connect with fellow farmers</p>
          </div>
          {user ? (
            <Link
              to="/community/new"
              className="flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white px-5 py-2.5 rounded-lg font-medium transition-all shadow-md hover:shadow-lg"
            >
              <Plus size={18} /> New Post
            </Link>
          ) : (
            <Link
              to="/LoginPage"
              className="flex items-center gap-2 bg-gray-600 hover:bg-gray-700 text-white px-5 py-2.5 rounded-lg font-medium transition-all"
            >
              Login to Post
            </Link>
          )}
        </div>

        {/* Search + Filters */}
        <div className="bg-white rounded-xl shadow-sm p-4 mb-6 flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              placeholder="Search posts…"
              value={search}
              onChange={e => setSearch(e.target.value)}
              className="w-full pl-9 pr-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
            />
          </div>
          <div className="relative">
            <Filter size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <select
              value={tagFilter}
              onChange={e => setTagFilter(e.target.value)}
              className="pl-9 pr-8 py-2 border border-gray-200 rounded-lg text-sm appearance-none focus:outline-none focus:ring-2 focus:ring-green-500"
            >
              <option value="">All Tags</option>
              {allTags.map(t => <option key={t} value={t}>{t}</option>)}
            </select>
          </div>
          <div className="flex gap-1">
            <button
              onClick={() => setSort('latest')}
              className={`flex items-center gap-1 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${sort === 'latest' ? 'bg-green-100 text-green-700' : 'text-gray-500 hover:bg-gray-100'}`}
            >
              <Clock size={14} /> Latest
            </button>
            <button
              onClick={() => setSort('top')}
              className={`flex items-center gap-1 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${sort === 'top' ? 'bg-green-100 text-green-700' : 'text-gray-500 hover:bg-gray-100'}`}
            >
              <TrendingUp size={14} /> Top
            </button>
          </div>
        </div>

        {/* Error */}
        {error && <div className="text-red-600 text-sm mb-4">{error}</div>}

        {/* Posts List */}
        <div className="space-y-4">
          {loading ? (
            <>
              <Skeleton /><Skeleton /><Skeleton />
            </>
          ) : posts.length === 0 ? (
            <div className="text-center py-16 text-gray-400">
              <MessageCircle size={48} className="mx-auto mb-3 opacity-40" />
              <p className="text-lg">No posts yet. Be the first to share!</p>
            </div>
          ) : (
            posts.map(post => (
              <div
                key={post.id}
                className="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow p-5 cursor-pointer border border-gray-100"
                onClick={() => navigate(`/community/post/${post.id}`)}
              >
                <div className="flex items-center gap-2 mb-2 text-xs text-gray-500">
                  <User size={14} />
                  <span className="font-medium text-gray-700">{post.author?.full_name}</span>
                  <span>·</span>
                  <span>{new Date(post.created_at).toLocaleDateString()}</span>
                  {post.author?.role && (
                    <span className={`ml-1 px-2 py-0.5 rounded-full text-[10px] font-semibold uppercase ${
                      post.author.role === 'ADMIN' ? 'bg-purple-100 text-purple-700'
                      : post.author.role === 'AGRONOMIST' ? 'bg-blue-100 text-blue-700'
                      : 'bg-green-100 text-green-700'
                    }`}>{post.author.role}</span>
                  )}
                </div>
                <h2 className="text-lg font-semibold text-gray-800 mb-1">{post.title}</h2>
                <p className="text-gray-600 text-sm line-clamp-2 mb-3">{post.body}</p>

                {/* Tags */}
                {post.tags && (
                  <div className="flex flex-wrap gap-1.5 mb-3">
                    {post.tags.split(',').filter(Boolean).map(t => (
                      <span key={t} className="flex items-center gap-0.5 bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full text-xs">
                        <Tag size={10} />{t.trim()}
                      </span>
                    ))}
                  </div>
                )}

                {/* Actions */}
                <div className="flex items-center gap-5 text-sm text-gray-500">
                  <button
                    onClick={e => { e.stopPropagation(); handleLike(post.id); }}
                    className={`flex items-center gap-1 transition-colors ${post.liked_by_me ? 'text-red-500' : 'hover:text-red-400'}`}
                  >
                    <Heart size={16} fill={post.liked_by_me ? 'currentColor' : 'none'} /> {post.like_count}
                  </button>
                  <span className="flex items-center gap-1">
                    <MessageCircle size={16} /> {post.comment_count}
                  </span>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default CommunityFeed;
