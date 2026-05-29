import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import newsData from '../data/newsData.json';

const TAG_COLORS = {
  Technology: 'bg-blue-500',
  Policy: 'bg-purple-500',
  Sustainability: 'bg-green-500',
  Research: 'bg-amber-500',
  Market: 'bg-red-500',
};

const AllNews = () => {
  const [activeTag, setActiveTag] = useState('All');
  const [search, setSearch] = useState('');

  const allTags = ['All', ...Array.from(new Set(newsData.map((a) => a.tag)))];

  const filtered = newsData.filter((a) => {
    const matchesTag = activeTag === 'All' || a.tag === activeTag;
    const matchesSearch =
      !search ||
      a.title.toLowerCase().includes(search.toLowerCase()) ||
      a.description.toLowerCase().includes(search.toLowerCase());
    return matchesTag && matchesSearch;
  });

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-800 to-gray-900 pt-24 pb-16 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <Link to="/" className="text-green-400 hover:text-green-300 text-sm mb-2 inline-flex items-center gap-1 no-underline">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clipRule="evenodd" />
              </svg>
              Back to Home
            </Link>
            <h1 className="text-3xl md:text-4xl font-bold text-white">All News & Articles</h1>
          </div>
        </div>

        {/* Tag pills + Search */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 mb-8">
          <div className="flex flex-wrap gap-2">
            {allTags.map((tag) => (
              <button
                key={tag}
                onClick={() => setActiveTag(tag)}
                className={`px-4 py-1.5 rounded-full text-sm font-medium transition-all duration-300 ${
                  activeTag === tag
                    ? 'bg-green-500 text-white'
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
              >
                {tag}
              </button>
            ))}
          </div>
          <div className="relative w-full sm:w-72">
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search articles…"
              className="w-full bg-gray-800 border border-gray-700 text-white placeholder-gray-500 rounded-full px-4 py-2.5 text-sm outline-none focus:ring-2 focus:ring-green-500 transition"
            />
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 absolute right-4 top-1/2 -translate-y-1/2 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>

        {/* Articles grid */}
        {filtered.length === 0 ? (
          <p className="text-center text-gray-400 py-16 text-lg">No articles match your criteria.</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {filtered.map((article) => (
              <div
                key={article.id}
                className="bg-gray-800/60 border border-gray-700 rounded-2xl overflow-hidden hover:border-green-600/50 transition-all duration-300 hover:-translate-y-1"
              >
                <div className="relative h-48 bg-gradient-to-br from-green-900/40 to-gray-800">
                  {article.imageUrl ? (
                    <img
                      src={article.imageUrl}
                      alt={article.title}
                      className="w-full h-full object-cover"
                      loading="lazy"
                      onError={(e) => {
                        e.target.style.display = 'none';
                        if (e.target.nextSibling) e.target.nextSibling.style.display = 'flex';
                      }}
                    />
                  ) : null}
                  <div className={`${article.imageUrl ? 'hidden' : 'flex'} items-center justify-center h-full text-5xl opacity-20 select-none`}>
                    {article.tag === 'Technology' ? '🤖' : article.tag === 'Policy' ? '🏛️' : article.tag === 'Sustainability' ? '🌿' : article.tag === 'Research' ? '🔬' : '📈'}
                  </div>
                  <div className="absolute top-3 left-3">
                    <span className={`${TAG_COLORS[article.tag] || 'bg-gray-500'} text-white px-3 py-1 text-xs font-semibold rounded-full`}>
                      {article.tag}
                    </span>
                  </div>
                  <div className="absolute bottom-3 left-3 text-xs text-gray-400 bg-black/50 px-2 py-1 rounded">
                    {article.date}
                  </div>
                </div>

                <div className="p-5">
                  <p className="text-xs text-gray-500 mb-2">by {article.author}</p>
                  <h3 className="text-lg font-bold text-white mb-2 line-clamp-2">
                    {article.url ? (
                      <a href={article.url} target="_blank" rel="noopener noreferrer" className="hover:text-green-400 no-underline text-white transition-colors">{article.title}</a>
                    ) : article.title}
                  </h3>
                  <p className="text-gray-400 text-sm leading-relaxed">{article.description}</p>
                  {article.url && (
                    <a href={article.url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1 mt-3 text-sm font-semibold text-green-400 hover:text-green-300 transition-colors no-underline">
                      Read more
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor"><path fillRule="evenodd" d="M10.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L12.586 11H5a1 1 0 110-2h7.586l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" /></svg>
                    </a>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default AllNews;
