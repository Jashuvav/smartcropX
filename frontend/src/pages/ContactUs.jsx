import React, { useState } from 'react';

const ContactUs = () => {
  const [form, setForm] = useState({ name: '', email: '', message: '' });
  const [submitted, setSubmitted] = useState(false);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitted(true);
    setTimeout(() => setSubmitted(false), 4000);
    setForm({ name: '', email: '', message: '' });
  };

  return (
    <div id="contactus" className="bg-gradient-to-b from-green-900 to-[#1a2e1c] text-white">
      {/* Contact Form + Info */}
      <div className="max-w-6xl mx-auto px-6 py-20">
        <div className="text-center mb-14">
          <p className="text-green-400 uppercase tracking-widest text-sm font-semibold mb-2">Get In Touch</p>
          <h2 className="text-4xl md:text-5xl font-bold">Contact Us</h2>
          <div className="w-20 h-1 bg-green-400 mx-auto mt-4 rounded-full" />
        </div>

        <div className="grid md:grid-cols-2 gap-12">
          {/* Info cards */}
          <div className="space-y-6">
            {[
              { icon: '📍', title: 'Address', text: 'SmartCropX HQ, Hyderabad, Telangana, India' },
              { icon: '📧', title: 'Email', text: 'support@smartcropx.com' },
              { icon: '📞', title: 'Phone', text: '+91 98765 43210' },
              { icon: '🕐', title: 'Working Hours', text: 'Mon – Sat, 9 AM – 6 PM IST' },
            ].map((item, i) => (
              <div key={i} className="flex items-start gap-4 bg-white/5 backdrop-blur-sm rounded-xl p-5 hover:bg-white/10 transition-all duration-300">
                <span className="text-3xl">{item.icon}</span>
                <div>
                  <h4 className="font-semibold text-green-300">{item.title}</h4>
                  <p className="text-gray-300 text-sm">{item.text}</p>
                </div>
              </div>
            ))}
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="bg-white/5 backdrop-blur-sm rounded-2xl p-8 space-y-5 border border-white/10">
            <div>
              <label className="block text-sm text-green-300 mb-1">Name</label>
              <input
                name="name" value={form.name} onChange={handleChange} required
                className="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-400 transition"
                placeholder="Your name"
              />
            </div>
            <div>
              <label className="block text-sm text-green-300 mb-1">Email</label>
              <input
                name="email" type="email" value={form.email} onChange={handleChange} required
                className="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-400 transition"
                placeholder="you@example.com"
              />
            </div>
            <div>
              <label className="block text-sm text-green-300 mb-1">Message</label>
              <textarea
                name="message" value={form.message} onChange={handleChange} required rows={4}
                className="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-400 transition resize-none"
                placeholder="How can we help?"
              />
            </div>
            <button
              type="submit"
              className="w-full bg-green-600 hover:bg-green-500 py-3 rounded-lg font-semibold transition-all duration-300 hover:scale-[1.02] hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-green-400"
            >
              {submitted ? '✅ Message Sent!' : 'Send Message'}
            </button>
          </form>
        </div>
      </div>

      {/* Footer */}
      <div className="border-t border-white/10">
        <div className="max-w-6xl mx-auto px-6 py-8 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2 text-lg font-bold">
            <span className="text-green-300">🌿</span>
            <span>SmartCropX</span>
          </div>
          <p className="text-gray-400 text-sm text-center">
            © {new Date().getFullYear()} SmartCropX. All rights reserved. Built with 💚 for farmers.
          </p>
          <div className="flex gap-4 text-gray-400">
            <a href="https://github.com/bunnysunny24/AgriSync" target="_blank" rel="noopener noreferrer" className="hover:text-green-300 transition">GitHub</a>
            <span>•</span>
            <span className="hover:text-green-300 cursor-pointer transition">Privacy</span>
            <span>•</span>
            <span className="hover:text-green-300 cursor-pointer transition">Terms</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ContactUs;
