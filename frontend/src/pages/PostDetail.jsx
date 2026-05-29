/**
 * PostDetail – /community/post/:id
 * Full post view with like toggle, comments list, add comment, delete/edit for author/admin.
 */
import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { Heart, MessageCircle, Trash2, Edit3, ArrowLeft, Send, User, Tag, Clock } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { API_URL } from '../config/api';
import axios from 'axios';

const PostDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user, token } = useAuth();

  const [post, setPost] = useState(null);
  const [comments, setComments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [commentBody, setCommentBody] = useState('');
  const [commenting, setCommenting] = useState(false);
  const [error, setError] = useState('');

  // Editing state
  const [editing, setEditing] = useState(false);
  const [editTitle, setEditTitle] = useState('');
  const [editBody, setEditBody] = useState('');
  const [editTags, setEditTags] = useState('');

  const headers = token ? { Authorization: `Bearer ${token}` } : {};

  const fetchPost = useCallback(async () => {
    try {
      const [pRes, cRes] = await Promise.all([
        axios.get(`${API_URL}/api/community/posts/${id}`, { headers }),
        axios.get(`${API_URL}/api/community/posts/${id}/comments`),
      ]);
      setPost(pRes.data);
      setComments(cRes.data);
      setEditTitle(pRes.data.title);
      setEditBody(pRes.data.body);
      setEditTags(pRes.data.tags || '');
    } catch {
      setError('Post not found');
    } finally {
      setLoading(false);
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id, token]);

  useEffect(() => { fetchPost(); }, [fetchPost]);

  const handleLike = async () => {
    if (!user) { navigate('/LoginPage'); return; }
    try {
      const res = await axios.post(`${API_URL}/api/community/posts/${id}/like`, {}, { headers });
      setPost(prev => ({ ...prev, like_count: res.data.like_count, liked_by_me: res.data.liked_by_me }));
    } catch { /* ignore */ }
  };

  const handleComment = async (e) => {
    e.preventDefault();
    if (!user) { navigate('/LoginPage'); return; }
    if (!commentBody.trim()) return;
    setCommenting(true);
    try {
      const res = await axios.post(`${API_URL}/api/community/posts/${id}/comments`, { body: commentBody }, { headers });
      setComments(prev => [...prev, res.data]);
      setCommentBody('');
      setPost(prev => ({ ...prev, comment_count: (prev.comment_count || 0) + 1 }));
    } catch { /* ignore */ }
    setCommenting(false);
  };

  const handleDeleteComment = async (commentId) => {
    if (!window.confirm('Delete this comment?')) return;
    try {
      await axios.delete(`${API_URL}/api/community/comments/${commentId}`, { headers });
      setComments(prev => prev.filter(c => c.id !== commentId));
      setPost(prev => ({ ...prev, comment_count: Math.max(0, (prev.comment_count || 1) - 1) }));
    } catch { /* ignore */ }
  };

  const handleDeletePost = async () => {
    if (!window.confirm('Delete this post? This cannot be undone.')) return;
    try {
      await axios.delete(`${API_URL}/api/community/posts/${id}`, { headers });
      navigate('/community');
    } catch { /* ignore */ }
  };

  const handleSaveEdit = async () => {
    try {
      const res = await axios.patch(`${API_URL}/api/community/posts/${id}`, {
        title: editTitle, body: editBody, tags: editTags,
      }, { headers });
      setPost(res.data);
      setEditing(false);
    } catch { /* ignore */ }
  };

  const canModify = user && post && (post.author?.id === user.id || user.role === 'ADMIN');

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 pt-4 pb-12">
        <div className="max-w-3xl mx-auto px-4 animate-pulse">
          <div className="h-6 bg-gray-200 rounded w-2/3 mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-full mb-2"></div>
          <div className="h-4 bg-gray-200 rounded w-5/6"></div>
        </div>
      </div>
    );
  }

  if (error || !post) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600 mb-4">{error || 'Post not found'}</p>
          <Link to="/community" className="text-green-600 hover:underline">Back to Community</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 pt-4 pb-12">
      <div className="max-w-3xl mx-auto px-4">
        {/* Back */}
        <button onClick={() => navigate('/community')} className="flex items-center gap-1 text-gray-500 hover:text-gray-700 mb-4 text-sm">
          <ArrowLeft size={16} /> Back to Community
        </button>

        {/* Post Card */}
        <div className="bg-white rounded-xl shadow-sm p-6 mb-6 border border-gray-100">
          {/* Author */}
          <div className="flex items-center gap-2 text-xs text-gray-500 mb-3">
            <User size={14} />
            <span className="font-medium text-gray-700">{post.author?.full_name}</span>
            {post.author?.role && (
              <span className={`px-2 py-0.5 rounded-full text-[10px] font-semibold uppercase ${
                post.author.role === 'ADMIN' ? 'bg-purple-100 text-purple-700'
                : post.author.role === 'AGRONOMIST' ? 'bg-blue-100 text-blue-700'
                : 'bg-green-100 text-green-700'
              }`}>{post.author.role}</span>
            )}
            <span>·</span>
            <Clock size={12} />
            <span>{new Date(post.created_at).toLocaleString()}</span>
          </div>

          {/* Title & body */}
          {editing ? (
            <div className="space-y-3 mb-4">
              <input value={editTitle} onChange={e => setEditTitle(e.target.value)} className="w-full px-3 py-2 border rounded-lg text-lg font-semibold" />
              <textarea value={editBody} onChange={e => setEditBody(e.target.value)} rows={5} className="w-full px-3 py-2 border rounded-lg resize-y" />
              <input value={editTags} onChange={e => setEditTags(e.target.value)} placeholder="tags" className="w-full px-3 py-2 border rounded-lg text-sm" />
              <div className="flex gap-2">
                <button onClick={handleSaveEdit} className="bg-green-600 text-white px-4 py-1.5 rounded-lg text-sm">Save</button>
                <button onClick={() => setEditing(false)} className="bg-gray-200 text-gray-700 px-4 py-1.5 rounded-lg text-sm">Cancel</button>
              </div>
            </div>
          ) : (
            <>
              <h1 className="text-2xl font-bold text-gray-800 mb-3">{post.title}</h1>
              <p className="text-gray-700 whitespace-pre-wrap leading-relaxed mb-4">{post.body}</p>
            </>
          )}

          {/* Image */}
          {post.image_url && (
            <img src={post.image_url.startsWith('http') ? post.image_url : `${API_URL}${post.image_url}`} alt="" className="rounded-lg max-h-96 mb-4" />
          )}

          {/* Tags */}
          {post.tags && (
            <div className="flex flex-wrap gap-1.5 mb-4">
              {post.tags.split(',').filter(Boolean).map(t => (
                <span key={t} className="flex items-center gap-0.5 bg-gray-100 text-gray-600 px-2.5 py-0.5 rounded-full text-xs">
                  <Tag size={10} />{t.trim()}
                </span>
              ))}
            </div>
          )}

          {/* Actions bar */}
          <div className="flex items-center gap-5 pt-3 border-t border-gray-100">
            <button
              onClick={handleLike}
              className={`flex items-center gap-1 text-sm transition-colors ${post.liked_by_me ? 'text-red-500 font-medium' : 'text-gray-500 hover:text-red-400'}`}
            >
              <Heart size={18} fill={post.liked_by_me ? 'currentColor' : 'none'} /> {post.like_count} {post.like_count === 1 ? 'Like' : 'Likes'}
            </button>
            <span className="flex items-center gap-1 text-sm text-gray-500">
              <MessageCircle size={18} /> {post.comment_count} Comments
            </span>
            {canModify && !editing && (
              <>
                <button onClick={() => setEditing(true)} className="flex items-center gap-1 text-sm text-blue-500 hover:text-blue-600 ml-auto">
                  <Edit3 size={15} /> Edit
                </button>
                <button onClick={handleDeletePost} className="flex items-center gap-1 text-sm text-red-500 hover:text-red-600">
                  <Trash2 size={15} /> Delete
                </button>
              </>
            )}
          </div>
        </div>

        {/* Comments */}
        <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Comments ({comments.length})</h2>

          {/* Add comment */}
          {user ? (
            <form onSubmit={handleComment} className="flex gap-2 mb-6">
              <input
                type="text"
                value={commentBody}
                onChange={e => setCommentBody(e.target.value)}
                placeholder="Write a comment…"
                className="flex-1 px-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
              />
              <button
                type="submit"
                disabled={commenting || !commentBody.trim()}
                className="flex items-center gap-1 bg-green-600 hover:bg-green-700 disabled:bg-green-400 text-white px-4 py-2 rounded-lg text-sm transition-colors"
              >
                <Send size={14} /> {commenting ? '…' : 'Send'}
              </button>
            </form>
          ) : (
            <p className="text-sm text-gray-400 mb-6">
              <Link to="/LoginPage" className="text-green-600 hover:underline">Login</Link> to comment.
            </p>
          )}

          {/* Comment list */}
          <div className="space-y-4">
            {comments.length === 0 ? (
              <p className="text-gray-400 text-sm">No comments yet. Start the conversation!</p>
            ) : (
              comments.map(c => (
                <div key={c.id} className="flex gap-3 group">
                  <div className="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center text-green-700 text-xs font-bold flex-shrink-0">
                    {c.author?.full_name?.charAt(0)?.toUpperCase() || '?'}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 text-xs text-gray-500">
                      <span className="font-medium text-gray-700">{c.author?.full_name}</span>
                      <span>·</span>
                      <span>{new Date(c.created_at).toLocaleString()}</span>
                      {user && (c.author?.id === user.id || user.role === 'ADMIN') && (
                        <button
                          onClick={() => handleDeleteComment(c.id)}
                          className="opacity-0 group-hover:opacity-100 text-red-400 hover:text-red-600 transition-opacity ml-auto"
                          title="Delete"
                        >
                          <Trash2 size={13} />
                        </button>
                      )}
                    </div>
                    <p className="text-gray-700 text-sm mt-0.5">{c.body}</p>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default PostDetail;
