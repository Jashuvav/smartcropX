/**
 * CreatePost – /community/new
 * Form: title, body, tags, optional image upload. Redirects to post detail on submit.
 */
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Send, Image as ImageIcon, X } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { API_URL } from '../config/api';
import axios from 'axios';

const CreatePost = () => {
  const { user, token } = useAuth();
  const navigate = useNavigate();

  const [title, setTitle] = useState('');
  const [body, setBody] = useState('');
  const [tags, setTags] = useState('');
  const [imageFile, setImageFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  if (!user) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600 mb-4">You need to be logged in to create a post.</p>
          <button onClick={() => navigate('/LoginPage')} className="bg-green-600 text-white px-6 py-2 rounded-lg">
            Login
          </button>
        </div>
      </div>
    );
  }

  const handleImage = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImageFile(file);
      setImagePreview(URL.createObjectURL(file));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');
    try {
      let image_url = null;

      // Upload image first if provided
      if (imageFile) {
        const form = new FormData();
        form.append('file', imageFile);
        const upRes = await axios.post(`${API_URL}/api/community/upload`, form, {
          headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'multipart/form-data' },
        });
        image_url = upRes.data.image_url;
      }

      const res = await axios.post(`${API_URL}/api/community/posts`, {
        title,
        body,
        tags,
        image_url,
      }, {
        headers: { Authorization: `Bearer ${token}` },
      });

      navigate(`/community/post/${res.data.id}`);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create post');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 pt-4 pb-12">
      <div className="max-w-2xl mx-auto px-4">
        <h1 className="text-2xl font-bold text-gray-800 mb-6">Create a new post</h1>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm mb-4">{error}</div>
        )}

        <form onSubmit={handleSubmit} className="bg-white rounded-xl shadow-sm p-6 space-y-5">
          {/* Title */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Title *</label>
            <input
              type="text"
              value={title}
              onChange={e => setTitle(e.target.value)}
              required
              maxLength={300}
              placeholder="What's on your mind?"
              className="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            />
          </div>

          {/* Body */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Body *</label>
            <textarea
              value={body}
              onChange={e => setBody(e.target.value)}
              required
              rows={6}
              placeholder="Share your knowledge, ask a question…"
              className="w-full px-4 py-2.5 border border-gray-200 rounded-lg resize-y focus:outline-none focus:ring-2 focus:ring-green-500"
            />
          </div>

          {/* Tags */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Tags (comma-separated)</label>
            <input
              type="text"
              value={tags}
              onChange={e => setTags(e.target.value)}
              placeholder="e.g. organic, tomato, tips"
              className="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            />
          </div>

          {/* Image */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Image (optional)</label>
            {imagePreview ? (
              <div className="relative inline-block">
                <img src={imagePreview} alt="preview" className="max-h-48 rounded-lg border" />
                <button
                  type="button"
                  onClick={() => { setImageFile(null); setImagePreview(null); }}
                  className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1"
                >
                  <X size={14} />
                </button>
              </div>
            ) : (
              <label className="flex items-center gap-2 cursor-pointer text-green-600 hover:text-green-700 text-sm">
                <ImageIcon size={18} /> Upload an image
                <input type="file" accept="image/*" onChange={handleImage} className="hidden" />
              </label>
            )}
          </div>

          {/* Submit */}
          <button
            type="submit"
            disabled={submitting}
            className="flex items-center gap-2 bg-green-600 hover:bg-green-700 disabled:bg-green-400 text-white px-6 py-2.5 rounded-lg font-medium transition-all"
          >
            {submitting ? (
              <>
                <svg className="animate-spin h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                </svg>
                Publishing…
              </>
            ) : (
              <>
                <Send size={16} /> Publish Post
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  );
};

export default CreatePost;
