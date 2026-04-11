// ============================================================
// MERIDIAN Magazine — Dummy Editions (3 editions)
// ============================================================

import type { Edition } from '../types';

export const editions: Edition[] = [
  // ==================== EDITION 01 ====================
  {
    id: 'edition-01',
    number: 1,
    title: 'The Quantum Leap',
    subtitle: 'Quantum computing, climate accords, and the future of digital rights',
    slug: 'edition-01-the-quantum-leap',
    coverImage: '/images/edition-01-cover.png',
    articleIds: [
      'article-01', // Breakthrough in Quantum Computing
      'article-02', // Global Climate Summit 2026
      'article-03', // Mars Mission Update
      'article-04', // AI Regulation Debate
      'article-05', // UN Digital Rights Treaty
    ],
    articles: [],
    status: 'published',
    publishedAt: '2026-06-22T09:00:00Z',
    weekStart: '2026-06-16',
    weekEnd: '2026-06-22',
    articleCount: 5,
    featuredArticleId: 'article-01',
    featuredArticle: undefined,
    printReady: true,
    printPdfUrl: '/editions/edition-01.pdf',
  },

  // ==================== EDITION 02 ====================
  {
    id: 'edition-02',
    number: 2,
    title: 'The Global Shift',
    subtitle: 'ASEAN digital currencies, CRISPR approvals, and deep ocean discoveries',
    slug: 'edition-02-the-global-shift',
    coverImage: '/images/edition-02-cover.png',
    articleIds: [
      'article-06', // ASEAN Digital Currency Framework
      'article-07', // WHO Mental Health Framework
      'article-08', // CRISPR Gene Therapy
      'article-09', // Deep Ocean Expedition
    ],
    articles: [],
    status: 'published',
    publishedAt: '2026-06-29T06:00:00Z',
    weekStart: '2026-06-23',
    weekEnd: '2026-06-29',
    articleCount: 4,
    featuredArticleId: 'article-08',
    featuredArticle: undefined,
    printReady: true,
    printPdfUrl: '/editions/edition-02.pdf',
  },

  // ==================== EDITION 03 ====================
  {
    id: 'edition-03',
    number: 3,
    title: 'The Innovation Frontier',
    subtitle: 'Brain-computer interfaces, fusion energy, and the future of space colonization',
    slug: 'edition-03-the-innovation-frontier',
    coverImage: '/images/edition-03-cover.png',
    articleIds: [
      'article-10', // Brain-Computer Interface Breakthrough
      'article-11', // Fusion Energy Milestone
      'article-12', // Space Tourism Era
    ],
    articles: [],
    status: 'published',
    publishedAt: '2026-07-06T08:00:00Z',
    weekStart: '2026-06-30',
    weekEnd: '2026-07-06',
    articleCount: 3,
    featuredArticleId: 'article-10',
    featuredArticle: undefined,
    printReady: false,
  },
];
