/**
 * ScrollExpansionHero – A scroll-driven hero section built with framer-motion.
 * Adapted from a Next.js "Scroll Expansion Hero" pattern to React/CRA.
 *
 * Title : "SmartCropX — AI-powered Crop Insights"
 * Subtitle: "2026 Edition"
 * Background: Unsplash agriculture image
 * Buttons : "Discover More" scrolls to Dashboard, "Learn More" scrolls to About (Agriinfo)
 */
import React, { useRef } from 'react';
import { motion, useScroll, useTransform } from 'framer-motion';

const HERO_IMAGE =
  'https://images.unsplash.com/photo-1625246333195-78d9c38ad449?auto=format&fit=crop&w=1920&q=80';

const ScrollExpansionHero = () => {
  const containerRef = useRef(null);

  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ['start start', 'end start'],
  });

  // Clip-path expands from a rounded rectangle to full viewport as user scrolls
  const clipProgress = useTransform(scrollYProgress, [0, 0.5], [20, 0]);   // border-radius %
  const scaleImg     = useTransform(scrollYProgress, [0, 0.6], [1.15, 1]); // subtle zoom-out
  const titleY       = useTransform(scrollYProgress, [0, 0.4], [0, -80]);
  const titleOpacity = useTransform(scrollYProgress, [0.25, 0.5], [1, 0]);
  const overlayOp    = useTransform(scrollYProgress, [0, 0.4], [0.55, 0.35]);

  const scrollTo = (id) => {
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  return (
    <section
      ref={containerRef}
      className="relative w-full"
      style={{ height: '140vh' }} /* extra height so scroll animation has room */
    >
      {/* Sticky wrapper — stays in view while user scrolls the extra height */}
      <div className="sticky top-0 h-screen w-full overflow-hidden">
        {/* Expanding image container */}
        <motion.div
          className="absolute inset-0"
          style={{
            borderRadius: useTransform(clipProgress, (v) => `${v}px`),
            overflow: 'hidden',
          }}
        >
          <motion.img
            src={HERO_IMAGE}
            alt="Lush green agriculture field"
            className="w-full h-full object-cover"
            style={{ scale: scaleImg }}
            loading="eager"
          />

          {/* Dark overlay */}
          <motion.div
            className="absolute inset-0 bg-black"
            style={{ opacity: overlayOp }}
          />
        </motion.div>

        {/* ── Content ─────────────────────────────────────────── */}
        <motion.div
          className="relative z-10 flex flex-col items-center justify-center h-full text-center px-4"
          style={{ y: titleY, opacity: titleOpacity }}
        >
          {/* Badge */}
          <motion.span
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.6 }}
            className="inline-block mb-4 px-4 py-1.5 rounded-full bg-white/10 backdrop-blur-md text-sm font-medium text-[#f7c35f] tracking-wider uppercase border border-white/20"
          >
            2026 Edition
          </motion.span>

          {/* Main title */}
          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5, duration: 0.7, ease: 'easeOut' }}
            className="text-4xl sm:text-5xl md:text-7xl font-extrabold text-white leading-tight max-w-4xl"
          >
            SmartCropX
            <span className="block text-[#f7c35f] mt-1">AI-powered Crop Insights</span>
          </motion.h1>

          {/* Subtitle */}
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.7, duration: 0.6 }}
            className="mt-6 text-lg md:text-xl text-gray-200 max-w-2xl leading-relaxed"
          >
            Harness satellite imagery, ML disease detection, and real-time weather
            intelligence to grow smarter — from soil to harvest.
          </motion.p>

          {/* CTA Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.9, duration: 0.5 }}
            className="flex flex-wrap gap-4 mt-10 justify-center"
          >
            <button
              onClick={() => scrollTo('dashboard')}
              className="group relative bg-[#f7c35f] text-gray-900 font-bold py-3 px-8 rounded-xl text-sm uppercase tracking-wide overflow-hidden transition-transform duration-300 hover:scale-105 hover:shadow-xl focus:outline-none"
            >
              <span className="relative z-10">Discover More</span>
              <span className="absolute inset-0 w-0 bg-white/30 transition-all duration-300 group-hover:w-full" />
            </button>

            <button
              onClick={() => scrollTo('agriinfo')}
              className="border-2 border-white text-white font-bold py-3 px-8 rounded-xl text-sm uppercase tracking-wide transition-all duration-300 hover:bg-white hover:text-gray-900 hover:scale-105 focus:outline-none"
            >
              Learn More
            </button>
          </motion.div>

          {/* Scroll indicator */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 0.7 }}
            transition={{ delay: 1.3, duration: 0.8 }}
            className="absolute bottom-10 flex flex-col items-center"
          >
            <span className="text-xs text-white/70 uppercase tracking-widest mb-2">
              Scroll Down
            </span>
            <div className="w-6 h-10 border-2 border-white/50 rounded-full flex justify-center p-1">
              <motion.div
                className="w-1.5 h-1.5 bg-white rounded-full"
                animate={{ y: [0, 16, 0] }}
                transition={{ repeat: Infinity, duration: 1.6, ease: 'easeInOut' }}
              />
            </div>
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
};

export default ScrollExpansionHero;