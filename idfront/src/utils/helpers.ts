// ============================================================
// MERIDIAN Magazine — Utility Functions
// ============================================================
// Pure helper functions used across the project for formatting,
// slug generation, reading time, and SEO.
// ============================================================

/**
 * Generate a URL-safe slug from a string.
 * Strips special chars, lowercases, replaces spaces with hyphens.
 */
export function slugify(text: string): string {
  return text
    .toString()
    .toLowerCase()
    .trim()
    .replace(/\s+/g, '-')
    .replace(/&/g, '-and-')
    .replace(/[^\w\-]+/g, '')
    .replace(/\-\-+/g, '-')
    .replace(/^-+/, '')
    .replace(/-+$/, '');
}

/**
 * Estimate reading time in minutes from plain text or HTML content.
 * Assumes average adult reading speed of 238 words per minute.
 */
export function calculateReadingTime(content: string): number {
  // Strip HTML tags if present
  const plainText = content.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim();
  const wordCount = plainText.split(/\s+/).filter(Boolean).length;
  const minutes = Math.max(1, Math.ceil(wordCount / 238));
  return minutes;
}

/**
 * Count words in text (strips HTML tags).
 */
export function countWords(content: string): number {
  const plainText = content.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim();
  return plainText.split(/\s+/).filter(Boolean).length;
}

/**
 * Format a date string into human-readable format.
 * Supports multiple output styles.
 */
export function formatDate(
  dateStr: string,
  style: 'full' | 'long' | 'medium' | 'short' | 'relative' | 'iso' = 'medium'
): string {
  const date = new Date(dateStr);

  if (style === 'iso') {
    return date.toISOString().split('T')[0];
  }

  if (style === 'relative') {
    return getRelativeTime(date);
  }

  const formatOptionsMap: Record<string, Intl.DateTimeFormatOptions> = {
    full: { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' as const },
    long: { year: 'numeric', month: 'long', day: 'numeric' },
    medium: { year: 'numeric', month: 'short', day: 'numeric' },
    short: { month: 'short', day: 'numeric' },
  };
  const options = formatOptionsMap[style];

  return date.toLocaleDateString('en-US', options);
}

/**
 * Get relative time string (e.g. "2 hours ago", "3 days ago").
 */
function getRelativeTime(date: Date): string {
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffSec = Math.floor(diffMs / 1000);
  const diffMin = Math.floor(diffSec / 60);
  const diffHr = Math.floor(diffMin / 60);
  const diffDay = Math.floor(diffHr / 24);
  const diffWeek = Math.floor(diffDay / 7);
  const diffMonth = Math.floor(diffDay / 30);

  if (diffSec < 60) return 'just now';
  if (diffMin < 60) return `${diffMin} minute${diffMin > 1 ? 's' : ''} ago`;
  if (diffHr < 24) return `${diffHr} hour${diffHr > 1 ? 's' : ''} ago`;
  if (diffDay < 7) return `${diffDay} day${diffDay > 1 ? 's' : ''} ago`;
  if (diffWeek < 4) return `${diffWeek} week${diffWeek > 1 ? 's' : ''} ago`;
  return `${diffMonth} month${diffMonth > 1 ? 's' : ''} ago`;
}

/**
 * Generate edition slug from edition number and date range.
 * e.g. "edition-42-week-of-june-22"
 */
export function generateEditionSlug(number: number, weekStart: string): string {
  const date = new Date(weekStart);
  const month = date.toLocaleString('en-US', { month: 'long' }).toLowerCase();
  const day = date.getDate();
  return `edition-${number}-week-of-${month}-${day}`;
}

/**
 * Generate a display date range for an edition.
 * e.g. "June 22 – 28, 2026"
 */
export function formatEditionDateRange(weekStart: string, weekEnd: string): string {
  const start = new Date(weekStart);
  const end = new Date(weekEnd);
  const startMonth = start.toLocaleString('en-US', { month: 'short' });
  const endMonth = end.toLocaleString('en-US', { month: 'short' });
  const endYear = end.getFullYear();

  if (startMonth === endMonth) {
    return `${startMonth} ${start.getDate()} – ${end.getDate()}, ${endYear}`;
  }
  return `${startMonth} ${start.getDate()} – ${endMonth} ${end.getDate()}, ${endYear}`;
}

/**
 * Truncate text to a specific character length, adding ellipsis if needed.
 */
export function truncate(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength).replace(/\s+\S*$/, '') + '...';
}

/**
 * Generate initials from a name (for avatar fallback).
 * e.g. "Sarah Chen" → "SC"
 */
export function getInitials(name: string): string {
  return name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);
}

/**
 * Get category color classes (Tailwind background + text).
 */
export function getCategoryColorClasses(color: string): { bg: string; text: string; gradient: string } {
  const colorMap: Record<string, { bg: string; text: string; gradient: string }> = {
    blue:     { bg: 'bg-blue-600',     text: 'text-blue-600',     gradient: 'from-blue-900 to-blue-500' },
    purple:   { bg: 'bg-purple-600',   text: 'text-purple-600',   gradient: 'from-purple-900 to-purple-500' },
    green:    { bg: 'bg-green-600',    text: 'text-green-600',    gradient: 'from-emerald-900 to-teal-500' },
    rose:     { bg: 'bg-rose-600',     text: 'text-rose-600',     gradient: 'from-red-900 to-rose-500' },
    amber:    { bg: 'bg-amber-600',    text: 'text-amber-600',    gradient: 'from-amber-900 to-orange-500' },
    teal:     { bg: 'bg-teal-600',     text: 'text-teal-600',     gradient: 'from-teal-900 to-cyan-500' },
    indigo:   { bg: 'bg-indigo-600',   text: 'text-indigo-600',   gradient: 'from-indigo-900 to-violet-500' },
    orange:   { bg: 'bg-orange-600',   text: 'text-orange-600',   gradient: 'from-orange-900 to-yellow-500' },
    cyan:     { bg: 'bg-cyan-600',     text: 'text-cyan-600',     gradient: 'from-cyan-900 to-sky-500' },
    pink:     { bg: 'bg-pink-600',     text: 'text-pink-600',     gradient: 'from-pink-900 to-pink-500' },
    emerald:  { bg: 'bg-emerald-600',  text: 'text-emerald-600',  gradient: 'from-emerald-900 to-green-500' },
  };

  return colorMap[color] || colorMap.blue;
}

/**
 * Build SEO meta tags object for use in Astro frontmatter.
 */
export function buildSEOMeta(seo: {
  title: string;
  description: string;
  ogImage?: string;
  canonicalUrl?: string;
  publishedTime?: string;
  modifiedTime?: string;
  author?: string;
  type?: string;
}) {
  const siteUrl = 'https://meridian-mag.com';
  return {
    title: seo.title,
    description: seo.description,
    ogImage: seo.ogImage ? `${siteUrl}${seo.ogImage}` : `${siteUrl}/og-default.png`,
    canonicalUrl: seo.canonicalUrl ? `${siteUrl}${seo.canonicalUrl}` : undefined,
    contentType: seo.type || 'website',
    publishedTime: seo.publishedTime,
    modifiedTime: seo.modifiedTime,
    author: seo.author,
  };
}

/**
 * Build JSON-LD for a NewsArticle.
 */
export function buildArticleJsonLd(article: {
  title: string;
  excerpt: string;
  coverImage: string;
  publishedAt: string;
  updatedAt?: string;
  authorName: string;
  authorUrl?: string;
  slug?: string;
  category?: string;
  keywords?: string[];
  wordCount?: number;
}) {
  const siteUrl = 'https://meridian-mag.com';
  const articleUrl = article.slug ? `${siteUrl}/articles/${article.slug}` : undefined;
  return {
    '@context': 'https://schema.org',
    '@type': 'NewsArticle',
    headline: article.title,
    description: article.excerpt,
    image: article.coverImage.startsWith('http') ? article.coverImage : `${siteUrl}${article.coverImage}`,
    datePublished: article.publishedAt,
    dateModified: article.updatedAt || article.publishedAt,
    ...(articleUrl ? { mainEntityOfPage: { '@type': 'WebPage', '@id': articleUrl } } : {}),
    ...(article.wordCount ? { wordCount: article.wordCount } : {}),
    ...(article.keywords?.length ? { keywords: article.keywords.join(', ') } : {}),
    ...(article.category ? { articleSection: article.category } : {}),
    author: {
      '@type': 'Person',
      name: article.authorName,
      ...(article.authorUrl ? { url: `${siteUrl}${article.authorUrl}` } : {}),
    },
    publisher: {
      '@type': 'Organization',
      name: 'MERIDIAN',
      logo: {
        '@type': 'ImageObject',
        url: `${siteUrl}/logo.svg`,
      },
    },
  };
}

/**
 * Build JSON-LD for a CollectionPage (category/edition listing).
 */
export function buildCollectionJsonLd(collection: {
  name: string;
  description: string;
  url: string;
  image?: string;
  datePublished?: string;
}) {
  const siteUrl = 'https://meridian-mag.com';
  return {
    '@context': 'https://schema.org',
    '@type': 'CollectionPage',
    name: collection.name,
    description: collection.description,
    url: collection.url.startsWith('http') ? collection.url : `${siteUrl}${collection.url}`,
    ...(collection.image ? { image: collection.image.startsWith('http') ? collection.image : `${siteUrl}${collection.image}` } : {}),
    ...(collection.datePublished ? { datePublished: collection.datePublished } : {}),
    publisher: {
      '@type': 'Organization',
      name: 'MERIDIAN',
      logo: {
        '@type': 'ImageObject',
        url: `${siteUrl}/logo.svg`,
      },
    },
  };
}

/**
 * Paginate an array.
 */
export function paginate<T>(
  items: T[],
  page: number = 1,
  perPage: number = 12
): { items: T[]; totalPages: number; total: number; currentPage: number } {
  const total = items.length;
  const totalPages = Math.max(1, Math.ceil(total / perPage));
  const currentPage = Math.max(1, Math.min(page, totalPages));
  const start = (currentPage - 1) * perPage;
  const itemsOnPage = items.slice(start, start + perPage);

  return {
    items: itemsOnPage,
    totalPages,
    total,
    currentPage,
  };
}

/**
 * Shuffle an array (Fisher-Yates). Returns a new array.
 */
export function shuffleArray<T>(array: T[]): T[] {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}

/**
 * Deduplicate an array by a key function.
 */
export function uniqueBy<T>(array: T[], keyFn: (item: T) => string): T[] {
  const seen = new Set<string>();
  return array.filter(item => {
    const key = keyFn(item);
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}
