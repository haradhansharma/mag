// ============================================================
// MERIDIAN Magazine — Service Layer
// ============================================================
// Single data abstraction layer.
// Currently reads from dummy data; will be replaced with API calls.
// All components and pages should import from this file ONLY.
// ============================================================

import type {
  Article,
  Author,
  Category,
  Edition,
  SiteConfig,
  SearchResult,
  PaginationOptions,
  AccessLevel,
} from './types';
import { authors } from './dummy/authors';
import { categories } from './dummy/categories';
import { articles } from './dummy/articles';
import { editions } from './dummy/editions';
import { siteConfig } from './dummy/site-config';
import { paginate } from '../utils/helpers';

// ========================
// Helper: Populate relations
// ========================

function withAuthor(article: Article): Article {
  return {
    ...article,
    author: authors.find(a => a.id === article.authorId),
  };
}

function withCategory(article: Article): Article {
  return {
    ...article,
    category: categories.find(c => c.id === article.categoryId),
  };
}

function withRelations(article: Article): Article {
  return withCategory(withAuthor(article));
}

function withArticles(edition: Edition): Edition {
  const editionArticles = articles
    .filter(a => edition.articleIds.includes(a.id))
    .map(withRelations);

  return {
    ...edition,
    articles: editionArticles,
    articleCount: editionArticles.length,
    featuredArticle: editionArticles.find(a => a.id === edition.featuredArticleId),
  };
}

// ========================
// Site Config
// ========================

/** Get the full site configuration. */
export function getSiteConfig(): SiteConfig {
  return siteConfig;
}

// ========================
// Authors
// ========================

/** Get all authors. */
export function getAllAuthors(): Author[] {
  return authors;
}

/** Get a single author by ID. */
export function getAuthorById(id: string): Author | undefined {
  return authors.find(a => a.id === id);
}

/** Get a single author by slug. */
export function getAuthorBySlug(slug: string): Author | undefined {
  return authors.find(a => a.slug === slug);
}

/** Get articles written by a specific author. */
export function getArticlesByAuthorId(authorId: string): Article[] {
  return articles
    .filter(a => a.authorId === authorId)
    .map(withRelations);
}

// ========================
// Categories
// ========================

/** Get all categories. */
export function getAllCategories(): Category[] {
  return categories;
}

/** Get a single category by ID. */
export function getCategoryById(id: string): Category | undefined {
  return categories.find(c => c.id === id);
}

/** Get a single category by slug. */
export function getCategoryBySlug(slug: string): Category | undefined {
  return categories.find(c => c.slug === slug);
}

/** Get all public categories. */
export function getPublicCategories(): Category[] {
  return categories.filter(c => c.access === 'public');
}

/** Get all premium categories. */
export function getPremiumCategories(): Category[] {
  return categories.filter(c => c.access === 'premium');
}

/** Get featured categories (shown in navigation). */
export function getFeaturedCategories(): Category[] {
  return categories.filter(c => c.featured);
}

// ========================
// Articles
// ========================

/** Get all articles (with relations populated). */
export function getAllArticles(): Article[] {
  return articles.map(withRelations);
}

/** Get a single article by ID. */
export function getArticleById(id: string): Article | undefined {
  const article = articles.find(a => a.id === id);
  return article ? withRelations(article) : undefined;
}

/** Get a single article by slug. */
export function getArticleBySlug(slug: string): Article | undefined {
  const article = articles.find(a => a.slug === slug);
  return article ? withRelations(article) : undefined;
}

/** Get articles by category slug. */
export function getArticlesByCategory(categorySlug: string): Article[] {
  const category = categories.find(c => c.slug === categorySlug);
  if (!category) return [];
  return articles
    .filter(a => a.categoryId === category.id)
    .map(withRelations);
}

/** Get articles by category ID. */
export function getArticlesByCategoryId(categoryId: string): Article[] {
  return articles
    .filter(a => a.categoryId === categoryId)
    .map(withRelations);
}

/** Get featured articles (for homepage). */
export function getFeaturedArticles(): Article[] {
  return articles
    .filter(a => a.featured)
    .map(withRelations);
}

/** Get trending articles. */
export function getTrendingArticles(): Article[] {
  return articles
    .filter(a => a.trending)
    .map(withRelations);
}

/** Get pinned articles (top of category pages). */
export function getPinnedArticles(): Article[] {
  return articles
    .filter(a => a.pinned)
    .map(withRelations);
}

/** Get latest articles (sorted by publishedAt desc). */
export function getLatestArticles(limit: number = 10): Article[] {
  return articles
    .sort((a, b) => new Date(b.publishedAt).getTime() - new Date(a.publishedAt).getTime())
    .slice(0, limit)
    .map(withRelations);
}

/** Get articles by access level. */
export function getArticlesByAccess(access: AccessLevel): Article[] {
  return articles
    .filter(a => a.access === access)
    .map(withRelations);
}

/** Get articles for a specific edition (by edition ID). */
export function getArticlesByEditionId(editionId: string): Article[] {
  const edition = editions.find(e => e.id === editionId);
  if (!edition) return [];
  return articles
    .filter(a => edition.articleIds.includes(a.id))
    .map(withRelations);
}

/**
 * Search articles by query string.
 * Matches against title, subtitle, excerpt, and author name.
 */
export function searchArticles(
  query: string,
  options: PaginationOptions = {}
): SearchResult {
  const normalizedQuery = query.toLowerCase().trim();

  if (!normalizedQuery) {
    const paginated = paginate(articles.map(withRelations), options.page, options.perPage);
    return {
      articles: paginated.items,
      totalResults: paginated.total,
      page: paginated.currentPage,
      perPage: options.perPage || 12,
      totalPages: paginated.totalPages,
    };
  }

  const results = articles.filter(a => {
    const haystack = [
      a.title,
      a.subtitle || '',
      a.excerpt,
      authors.find(au => au.id === a.authorId)?.name || '',
      categories.find(c => c.id === a.categoryId)?.name || '',
    ]
      .join(' ')
      .toLowerCase();

    return haystack.includes(normalizedQuery);
  });

  // Sort by relevance (exact title match first)
  results.sort((a, b) => {
    const aTitleMatch = a.title.toLowerCase().includes(normalizedQuery) ? 0 : 1;
    const bTitleMatch = b.title.toLowerCase().includes(normalizedQuery) ? 0 : 1;
    if (aTitleMatch !== bTitleMatch) return aTitleMatch - bTitleMatch;
    return new Date(b.publishedAt).getTime() - new Date(a.publishedAt).getTime();
  });

  const withRels = results.map(withRelations);
  const paginated = paginate(withRels, options.page, options.perPage);

  return {
    articles: paginated.items,
    totalResults: results.length,
    page: paginated.currentPage,
    perPage: options.perPage || 12,
    totalPages: paginated.totalPages,
  };
}

// ========================
// Editions
// ========================

/** Get all editions (with articles populated). */
export function getAllEditions(): Edition[] {
  return editions
    .filter(e => e.status === 'published')
    .sort((a, b) => b.number - a.number)
    .map(withArticles);
}

/** Get a single edition by ID. */
export function getEditionById(id: string): Edition | undefined {
  const edition = editions.find(e => e.id === id);
  return edition ? withArticles(edition) : undefined;
}

/** Get a single edition by slug. */
export function getEditionBySlug(slug: string): Edition | undefined {
  const edition = editions.find(e => e.slug === slug);
  return edition ? withArticles(edition) : undefined;
}

/** Get the latest published edition. */
export function getLatestEdition(): Edition | undefined {
  const latest = editions
    .filter(e => e.status === 'published')
    .sort((a, b) => b.number - a.number)[0];
  return latest ? withArticles(latest) : undefined;
}

/** Get a specific edition by edition number. */
export function getEditionByNumber(number: number): Edition | undefined {
  const edition = editions.find(e => e.number === number);
  return edition ? withArticles(edition) : undefined;
}

// ========================
// Aggregation helpers (for homepage)
// ========================

/** Get the hero/cover story for the latest edition. */
export function getHeroArticle(): Article | undefined {
  const latest = getLatestEdition();
  if (latest?.featuredArticle) return latest.featuredArticle;
  return getFeaturedArticles()[0];
}

/**
 * Get the homepage data bundle.
 * Returns everything needed to render the homepage in one call.
 */
export function getHomepageData() {
  const latestEdition = getLatestEdition();
  const heroArticle = latestEdition?.featuredArticle || getFeaturedArticles()[0];
  const trending = getTrendingArticles();
  const featured = getFeaturedArticles();
  const latestScience = getArticlesByCategory('science-tech')
    .sort((a, b) => new Date(b.publishedAt).getTime() - new Date(a.publishedAt).getTime())
    .slice(0, 3);
  const latestWorld = getArticlesByCategory('world-news')
    .sort((a, b) => new Date(b.publishedAt).getTime() - new Date(a.publishedAt).getTime())
    .slice(0, 3);
  const latestEnvironment = getArticlesByCategory('environment')
    .sort((a, b) => new Date(b.publishedAt).getTime() - new Date(a.publishedAt).getTime())
    .slice(0, 3);
  const editionCount = editions.filter(e => e.status === 'published').length;

  return {
    latestEdition,
    heroArticle,
    trending,
    featured,
    latestScience,
    latestWorld,
    latestEnvironment,
    editionCount,
  };
}

/**
 * Get category page data bundle.
 */
export function getCategoryPageData(slug: string, options: PaginationOptions = {}) {
  const category = getCategoryBySlug(slug);
  if (!category) return null;

  const allArticles = getArticlesByCategory(slug);
  const pinned = allArticles.filter(a => a.pinned);
  const unpinned = allArticles.filter(a => !a.pinned);
  const sorted = [...pinned, ...unpinned]
    .sort((a, b) => new Date(b.publishedAt).getTime() - new Date(a.publishedAt).getTime());
  const paginated = paginate(sorted, options.page, options.perPage);

  return {
    category,
    articles: paginated.items,
    totalPages: paginated.totalPages,
    totalArticles: paginated.total,
    currentPage: paginated.currentPage,
  };
}

// ========================
// Print-on-Demand
// ========================

/** Get all print-ready editions. */
export function getPrintReadyEditions(): Edition[] {
  return editions
    .filter(e => e.status === 'published' && e.printReady)
    .sort((a, b) => b.number - a.number)
    .map(withArticles);
}

/** Get an edition by its week start date. */
export function getEditionByWeek(weekStart: string): Edition | undefined {
  const edition = editions.find(e => e.weekStart === weekStart && e.status === 'published');
  return edition ? withArticles(edition) : undefined;
}

/** Get editions by year. */
export function getEditionsByYear(year: number): Edition[] {
  return editions
    .filter(e => {
      const date = new Date(e.publishedAt);
      return date.getFullYear() === year && e.status === 'published';
    })
    .sort((a, b) => b.number - a.number)
    .map(withArticles);
}

/** Get print pricing tiers. */
export function getPrintPricing() {
  return {
    single: 12.99,
    multiCopy: 10.99,     // 2+ copies
    bulk: 9.49,            // 5+ copies
    shippingUS: 4.99,
    shippingInternational: 9.99,
    freeShippingThreshold: 50,
    currency: 'USD',
  };
}

/** Calculate print order total. */
export function calculatePrintOrderTotal(quantity: number, region: 'us' | 'international') {
  const pricing = getPrintPricing();
  const unitPrice = quantity >= 5 ? pricing.bulk : quantity >= 2 ? pricing.multiCopy : pricing.single;
  const subtotal = unitPrice * quantity;
  const shipping = subtotal >= pricing.freeShippingThreshold
    ? 0
    : region === 'us'
      ? pricing.shippingUS
      : pricing.shippingInternational;
  const discount = Math.max(0, pricing.single * quantity - subtotal);

  return {
    unitPrice,
    subtotal,
    shipping,
    discount,
    total: subtotal + shipping - discount,
  };
}

/**
 * Get article page data with related articles.
 */
export function getArticlePageData(slug: string) {
  const article = getArticleBySlug(slug);
  if (!article) return null;

  // Get related articles: same category, different article
  const related = getArticlesByCategory(article.category?.slug || '')
    .filter(a => a.id !== article.id)
    .slice(0, 4);

  // Get more from same author
  const moreFromAuthor = articles
    .filter(a => a.authorId === article.authorId && a.id !== article.id)
    .map(withRelations)
    .slice(0, 3);

  return {
    article,
    related,
    moreFromAuthor,
  };
}
