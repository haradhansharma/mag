// ============================================================
// MERIDIAN Magazine — Dummy Categories
// ============================================================

import type { Category } from '../types';

export const categories: Category[] = [
  // ==================== PUBLIC CATEGORIES ====================
  {
    id: 'cat-world',
    name: 'World News',
    slug: 'world-news',
    description: 'Breaking news, geopolitics, and major events shaping our world. Stay informed about international relations, diplomacy, and global developments.',
    color: 'rose',
    access: 'public',
    articleCount: 28,
    featured: true,
  },
  {
    id: 'cat-science',
    name: 'Science & Tech',
    slug: 'science-tech',
    description: 'Cutting-edge discoveries, research breakthroughs, and technological innovations that are redefining what\'s possible in science and engineering.',
    color: 'blue',
    access: 'public',
    articleCount: 35,
    featured: true,
  },
  {
    id: 'cat-environment',
    name: 'Environment',
    slug: 'environment',
    description: 'Climate change, conservation efforts, sustainability solutions, and the urgent stories about our planet\'s ecosystems and natural resources.',
    color: 'green',
    access: 'public',
    articleCount: 22,
    featured: true,
  },
  {
    id: 'cat-sports',
    name: 'Sports',
    slug: 'sports',
    description: 'From the Olympics to local competitions — covering the athletes, events, and stories that inspire millions around the world.',
    color: 'orange',
    access: 'public',
    articleCount: 18,
    featured: false,
  },
  {
    id: 'cat-culture',
    name: 'Culture',
    slug: 'culture',
    description: 'Art, music, film, literature, and the cultural movements that define our era. Exploring creativity and expression across the globe.',
    color: 'purple',
    access: 'public',
    articleCount: 24,
    featured: true,
  },
  {
    id: 'cat-health',
    name: 'Health',
    slug: 'health',
    description: 'Public health news, medical breakthroughs, wellness trends, and healthcare policy updates that affect your daily life.',
    color: 'teal',
    access: 'public',
    articleCount: 20,
    featured: false,
  },

  // ==================== PREMIUM CATEGORIES ====================
  {
    id: 'cat-business',
    name: 'Business & Economy',
    slug: 'business-economy',
    description: 'In-depth analysis of global markets, economic policy, entrepreneurship, and the forces driving the world economy. Premium subscribers get exclusive market insights and expert commentary.',
    color: 'amber',
    access: 'premium',
    articleCount: 16,
    featured: true,
  },
  {
    id: 'cat-opinion',
    name: 'Opinion & Analysis',
    slug: 'opinion-analysis',
    description: 'Expert perspectives, editorial commentary, and deep-dive analysis on the issues that matter most. Thought-provoking takes from leading thinkers and MERIDIAN\'s editorial team.',
    color: 'indigo',
    access: 'premium',
    articleCount: 14,
    featured: false,
  },
  {
    id: 'cat-deep-dive',
    name: 'Deep Dives',
    slug: 'deep-dives',
    description: 'Long-form investigative journalism and comprehensive explainers that go beyond the headlines. Each deep dive is meticulously researched and beautifully presented for a thorough understanding.',
    color: 'cyan',
    access: 'premium',
    articleCount: 10,
    featured: true,
  },
  {
    id: 'cat-future',
    name: 'Future Forward',
    slug: 'future-forward',
    description: 'Speculative features, futurology, and forward-looking reporting on emerging trends that will shape the next decade. From AI ethics to space colonization — what\'s coming next.',
    color: 'pink',
    access: 'premium',
    articleCount: 8,
    featured: false,
  },
  {
    id: 'cat-lifestyle',
    name: 'Lifestyle & Travel',
    slug: 'lifestyle-travel',
    description: 'Travel guides, food culture, sustainable living tips, and lifestyle features designed to enrich your everyday experiences. Premium content for the curious explorer.',
    color: 'emerald',
    access: 'premium',
    articleCount: 12,
    featured: false,
  },
];

/**
 * Get a category by ID.
 */
export function getCategoryById(id: string): Category | undefined {
  return categories.find(c => c.id === id);
}

/**
 * Get a category by slug.
 */
export function getCategoryBySlug(slug: string): Category | undefined {
  return categories.find(c => c.slug === slug);
}

/**
 * Get all public categories.
 */
export function getPublicCategories(): Category[] {
  return categories.filter(c => c.access === 'public');
}

/**
 * Get all premium categories.
 */
export function getPremiumCategories(): Category[] {
  return categories.filter(c => c.access === 'premium');
}

/**
 * Get featured categories (shown in navigation/highlights).
 */
export function getFeaturedCategories(): Category[] {
  return categories.filter(c => c.featured);
}
