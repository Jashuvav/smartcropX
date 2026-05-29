import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import newsData from '../data/newsData.json';

const TAG_COLORS = {
  Technology: 'bg-blue-500',
  Policy: 'bg-purple-500',
  Sustainability: 'bg-green-500',
  Research: 'bg-amber-500',
  Market: 'bg-red-500',
};

const AgriNewsSection = () => {
  const [isVisible, setIsVisible] = useState(false);
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

  // Only show first 3 on the homepage section
  const displayed = filtered.slice(0, 3);

  useEffect(() => {
    const handleScroll = () => {
      const element = document.getElementById('news');
      if (element) {
        const position = element.getBoundingClientRect();
        if (position.top < window.innerHeight * 0.75) {
          setIsVisible(true);
        }
      }
    };
    handleScroll();
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div id="news" className="relative py-16 bg-smart-green">
      <div className="max-w-6xl mx-auto px-4">
        {/* Header */}
        <div
          className={`text-center mb-8 transition-all duration-1000 ${
            isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
          }`}
        >
          <h3 className="text-smart-yellow font-semibold mb-2 tracking-wider uppercase">
            FROM THE BLOG
          </h3>
          <h2 className="text-4xl font-bold text-white mb-4 relative inline-block">
            News & Articles
            <span className="absolute -bottom-2 left-0 h-1 w-full bg-smart-yellow"></span>
          </h2>
        </div>

        {/* Tag pills + Search */}
        <div
          className={`flex flex-col sm:flex-row items-center justify-between gap-4 mb-8 transition-all duration-700 ${
            isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-6'
          }`}
          style={{ transitionDelay: '200ms' }}
        >
          <div className="flex flex-wrap gap-2 justify-center">
            {allTags.map((tag) => (
              <button
                key={tag}
                onClick={() => setActiveTag(tag)}
                className={`px-3 py-1 rounded-full text-sm font-medium transition-all duration-300 ${
                  activeTag === tag
                    ? 'bg-smart-yellow text-smart-green'
                    : 'bg-white/10 text-white hover:bg-white/20'
                }`}
              >
                {tag}
              </button>
            ))}
          </div>
          <div className="relative w-full sm:w-64">
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search articles…"
              className="w-full bg-white/10 text-white placeholder-gray-400 rounded-full px-4 py-2 text-sm outline-none focus:ring-2 focus:ring-smart-yellow transition"
            />
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-4 w-4 absolute right-3 top-1/2 -translate-y-1/2 text-gray-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
          </div>
        </div>

        {/* Cards */}
        {displayed.length === 0 ? (
          <p className="text-center text-gray-300 py-12">No articles match your criteria.</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {displayed.map((article, index) => (
              <div
                key={article.id}
                className={`bg-white rounded-lg overflow-hidden shadow-lg transition-all duration-700 transform ${
                  isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
                }`}
                style={{ transitionDelay: `${index * 200 + 400}ms` }}
              >
                <div className="relative overflow-hidden h-56 bg-gradient-to-br from-green-100 to-green-200">
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
                  <div className={`${article.imageUrl ? 'hidden' : 'flex'} items-center justify-center h-full text-6xl opacity-30 select-none`}>
                    {article.tag === 'Technology'
                      ? '🤖'
                      : article.tag === 'Policy'
                      ? '🏛️'
                      : article.tag === 'Sustainability'
                      ? '🌿'
                      : article.tag === 'Research'
                      ? '🔬'
                      : '📈'}
                  </div>
                  <div className="absolute top-4 left-4">
                    <span
                      className={`${
                        TAG_COLORS[article.tag] || 'bg-gray-500'
                      } text-white px-3 py-1 text-xs font-semibold rounded-full`}
                    >
                      {article.tag}
                    </span>
                  </div>
                  <div className="absolute bottom-4 left-4">
                    <div className="bg-smart-yellow text-smart-green px-3 py-1 text-sm font-medium rounded">
                      {article.date}
                    </div>
                  </div>
                </div>

                <div className="p-6 bg-white">
                  <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                    <div className="flex items-center space-x-1">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="h-4 w-4 text-smart-yellow"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                        />
                      </svg>
                      <span className="text-gray-400">by {article.author}</span>
                    </div>
                  </div>

                  <h3 className="text-lg font-bold mb-2 text-gray-800 hover:text-smart-yellow transition-colors duration-300 line-clamp-2">
                    {article.url ? (
                      <a href={article.url} target="_blank" rel="noopener noreferrer" className="hover:text-smart-yellow no-underline text-gray-800">{article.title}</a>
                    ) : article.title}
                  </h3>
                  <p className="text-gray-500 text-sm line-clamp-2">{article.description}</p>
                  {article.url && (
                    <a href={article.url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1 mt-3 text-sm font-semibold text-smart-green hover:text-smart-yellow transition-colors duration-300 no-underline">
                      Read more
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor"><path fillRule="evenodd" d="M10.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L12.586 11H5a1 1 0 110-2h7.586l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" /></svg>
                    </a>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* View All link */}
        {filtered.length > 3 && (
          <div className="text-center mt-10">
            <Link
              to="/news"
              className="inline-flex items-center gap-2 bg-smart-yellow text-smart-green px-6 py-3 rounded-full font-semibold hover:brightness-110 transition-all duration-300 hover:scale-105 no-underline"
            >
              View All Articles
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-5 w-5"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fillRule="evenodd"
                  d="M10.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L12.586 11H5a1 1 0 110-2h7.586l-2.293-2.293a1 1 0 010-1.414z"
                  clipRule="evenodd"
                />
              </svg>
            </Link>
          </div>
        )}
      </div>
    </div>
  );
};

export default AgriNewsSection;