// ============================================================
// MERIDIAN Magazine — Dummy Editions
// ============================================================

import type { Edition } from '../types';

export const editions: Edition[] = [
  {
    id: 'edition-05',
    number: 46,
    title: 'The Ocean Awakening',
    subtitle: 'New species, new shipping routes, and the deep blue unknown',
    slug: 'edition-46-week-of-july-6',
    coverImage: '/images/edition-cover-ocean.png',
    articleIds: [
      'article-09',  // Deep Ocean Expedition
      'article-20',  // Arctic Ice Melt
      'article-23',  // Pacific Island Climate Migration
      'article-22',  // Wearable Biosensors
      'article-19',  // Democracy in the Digital Age
    ],
    status: 'published',
    publishedAt: '2026-07-06T08:00:00Z',
    weekStart: '2026-07-06',
    weekEnd: '2026-07-12',
    articleCount: 5,
    featuredArticleId: 'article-09',
    printReady: false,
  },
  {
    id: 'edition-04',
    number: 45,
    title: 'The Quantum Leap',
    subtitle: 'Computing\'s new frontier and the race to fusion energy',
    slug: 'edition-45-week-of-june-29',
    coverImage: '/images/edition-cover-quantum.png',
    articleIds: [
      'article-01',  // Quantum Computing Breakthrough
      'article-10',  // Fusion Energy Milestone
      'article-04',  // AI Regulation Debate
      'article-14',  // Digital Art Revolution
      'article-15',  // Global Markets Rally
      'article-17',  // Central Banks Cryptocurrency
    ],
    status: 'published',
    publishedAt: '2026-06-29T08:00:00Z',
    weekStart: '2026-06-29',
    weekEnd: '2026-07-05',
    articleCount: 6,
    featuredArticleId: 'article-01',
    printReady: true,
  },
  {
    id: 'edition-03',
    number: 44,
    title: 'The Climate Crossroads',
    subtitle: 'Historic summits, Arctic shifts, and the future of our planet',
    slug: 'edition-44-week-of-june-22',
    coverImage: '/images/edition-cover-climate.png',
    articleIds: [
      'article-02',  // Global Climate Summit
      'article-05',  // UN Digital Rights Treaty
      'article-06',  // ASEAN Digital Currency
      'article-12',  // Olympic Games 2028
      'article-07',  // WHO Mental Health Framework
      'article-18',  // Universal Basic Income
    ],
    status: 'published',
    publishedAt: '2026-06-22T08:00:00Z',
    weekStart: '2026-06-22',
    weekEnd: '2026-06-28',
    articleCount: 6,
    featuredArticleId: 'article-02',
    printReady: true,
  },
  {
    id: 'edition-02',
    number: 43,
    title: 'The Red Planet Returns',
    subtitle: 'Mars samples, CRISPR breakthroughs, and the business of tomorrow',
    slug: 'edition-43-week-of-june-15',
    coverImage: '/images/edition-cover-mars.png',
    articleIds: [
      'article-03',  // Mars Mission Update
      'article-08',  // CRISPR Gene Therapy
      'article-11',  // Soccer League Reform
      'article-13',  // African Cinema Rise
      'article-16',  // Startup Ecosystem Report
    ],
    status: 'published',
    publishedAt: '2026-06-15T08:00:00Z',
    weekStart: '2026-06-15',
    weekEnd: '2026-06-21',
    articleCount: 5,
    featuredArticleId: 'article-03',
    printReady: true,
  },
  {
    id: 'edition-01',
    number: 42,
    title: 'Inside the Human Brain',
    subtitle: 'The race to map consciousness and the AI creativity debate',
    slug: 'edition-42-week-of-june-8',
    coverImage: '/images/edition-cover-brain.png',
    articleIds: [
      'article-21',  // Inside the Race to Map the Human Brain
      'article-24',  // East Africa Tech Hub
      'article-14',  // Digital Art Revolution (cross-edition)
      'article-04',  // AI Regulation (cross-edition)
    ],
    status: 'published',
    publishedAt: '2026-06-08T08:00:00Z',
    weekStart: '2026-06-08',
    weekEnd: '2026-06-14',
    articleCount: 4,
    featuredArticleId: 'article-21',
    printReady: true,
  },
];

/**
 * Get an edition by ID.
 */
export function getEditionById(id: string): Edition | undefined {
  return editions.find(e => e.id === id);
}

/**
 * Get an edition by slug.
 */
export function getEditionBySlug(slug: string): Edition | undefined {
  return editions.find(e => e.slug === slug);
}

/**
 * Get the latest published edition.
 */
export function getLatestEdition(): Edition | undefined {
  return editions
    .filter(e => e.status === 'published')
    .sort((a, b) => b.number - a.number)[0];
}
