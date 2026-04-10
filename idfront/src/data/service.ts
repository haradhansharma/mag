// ============================================================
// MERIDIAN Magazine — Service Layer (API-Backed)
// ============================================================
// Single data abstraction layer.
// Fetches from Django Ninja API when PUBLIC_API_URL is set,
// falls back to dummy data when API is unavailable.
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
  SubscriptionPlan,
  AccessLevel,
  EditorialQueueItem,
  EditorialActivity,
  EditorialStats,
} from './types';
import {
  isApiAvailable,
  fetchHomepage,
  fetchArticles,
  fetchArticle,
  fetchCategories,
  fetchCategory,
  fetchAuthors,
  fetchAuthor,
  fetchEditions,
  fetchEdition,
  fetchLatestEdition,
  fetchSearchResults,
  fetchPlans,
  fetchPrintPricing,
  type ApiArticleBrief,
  type ApiArticleOut,
  type ApiCategoryOut,
  type ApiAuthorOut,
  type ApiEditionBrief,
  type ApiEditionOut,
  type ApiSubscriptionPlanOut,
  type ApiHomepageData,
  type ApiPaginatedResponse,
} from '../lib/api';

import { authors as dummyAuthors } from './dummy/authors';
import { categories as dummyCategories } from './dummy/categories';
import { articles as dummyArticles } from './dummy/articles';
import { editions as dummyEditions } from './dummy/editions';
import { siteConfig as dummySiteConfig } from './dummy/site-config';
import { paginate } from '../utils/helpers';

// ========================
// API Availability Check
// ========================

let _apiAvailable: boolean | null = null;

async function checkApi(): Promise<boolean> {
  if (_apiAvailable !== null) return _apiAvailable;
  _apiAvailable = await isApiAvailable();
  return _apiAvailable;
}

// ========================
// Transformers: API → Frontend Types
// ========================

function transformArticleBrief(b: ApiArticleBrief): Article {
  return {
    id: b.id,
    title: b.title,
    slug: b.slug,
    subtitle: '',
    content: '',
    excerpt: b.excerpt,
    coverImage: b.cover_image,
    coverCaption: '',
    authorId: '',
    author: {
      id: '',
      name: b.author_name,
      slug: b.author_slug,
      bio: '',
      avatar: '',
      role: '',
      socials: {},
      articleCount: 0,
    },
    categoryId: '',
    category: {
      id: '',
      name: b.category_name,
      slug: b.category_slug,
      description: '',
      color: (b.category_name ? guessCategoryColor(b.category_name) : 'blue') as Article['category'] extends undefined ? never : NonNullable<Article['category']>['color'],
      access: (b.access || 'public') as AccessLevel,
      articleCount: 0,
    },
    contentType: b.content_type as Article['contentType'],
    access: b.access as AccessLevel,
    seo: {
      title: b.title,
      description: b.excerpt,
      keywords: [],
    },
    publishedAt: b.published_at || new Date().toISOString(),
    updatedAt: undefined,
    readingTime: b.reading_time,
    wordCount: 0,
    featured: b.featured,
    trending: b.trending,
    pinned: b.pinned,
  };
}

function transformArticleOut(a: ApiArticleOut): Article {
  return {
    id: a.id,
    title: a.title,
    slug: a.slug,
    subtitle: a.subtitle,
    content: a.content,
    excerpt: a.excerpt,
    coverImage: a.cover_image,
    coverCaption: a.cover_caption,
    authorId: a.author.id,
    author: {
      id: a.author.id,
      name: a.author.name,
      slug: a.author.slug,
      bio: '',
      avatar: a.author.avatar,
      role: a.author.role,
      socials: {},
      articleCount: 0,
    },
    categoryId: a.category.id,
    category: {
      id: a.category.id,
      name: a.category.name,
      slug: a.category.slug,
      description: '',
      color: a.category.color as Category['color'],
      access: a.category.access as AccessLevel,
      articleCount: 0,
    },
    contentType: a.content_type as Article['contentType'],
    access: a.access as AccessLevel,
    seo: {
      title: a.seo_title || a.title,
      description: a.seo_description || a.excerpt,
      keywords: a.seo_keywords,
    },
    publishedAt: a.published_at || new Date().toISOString(),
    updatedAt: a.updated_at || undefined,
    readingTime: a.reading_time,
    wordCount: a.word_count,
    featured: a.featured,
    trending: a.trending,
    pinned: a.pinned,
  };
}

function transformCategoryOut(c: ApiCategoryOut): Category {
  return {
    id: String(c.id),
    name: c.name,
    slug: c.slug,
    description: c.description,
    color: c.color as Category['color'],
    icon: c.icon || undefined,
    access: c.access as AccessLevel,
    articleCount: c.article_count,
    featured: c.featured,
  };
}

function transformAuthorOut(a: ApiAuthorOut): Author {
  return {
    id: a.id,
    name: a.name,
    slug: a.slug,
    bio: a.bio,
    avatar: a.avatar,
    role: a.role,
    socials: {
      ...(a.twitter ? { twitter: a.twitter } : {}),
      ...(a.linkedin ? { linkedin: a.linkedin } : {}),
      ...(a.instagram ? { instagram: a.instagram } : {}),
      ...(a.website ? { website: a.website } : {}),
    },
    articleCount: a.article_count,
  };
}

function transformEditionBrief(e: ApiEditionBrief): Edition {
  return {
    id: e.id,
    number: e.number,
    title: e.title,
    subtitle: '',
    slug: e.slug,
    coverImage: e.cover_image,
    articleIds: [],
    articles: [],
    status: e.status as Edition['status'],
    publishedAt: e.published_at || new Date().toISOString(),
    weekStart: e.week_start || '',
    weekEnd: e.week_end || '',
    articleCount: e.article_count,
    featuredArticleId: undefined,
    featuredArticle: undefined,
    printReady: false,
  };
}

function transformEditionOut(e: ApiEditionOut): Edition {
  const articles = (e.articles || []).map(transformArticleBrief);
  const featured = e.featured_article ? transformArticleBrief(e.featured_article) : undefined;

  return {
    id: e.id,
    number: e.number,
    title: e.title,
    subtitle: e.subtitle,
    slug: e.slug,
    coverImage: e.cover_image,
    articleIds: articles.map(a => a.id),
    articles,
    status: e.status as Edition['status'],
    publishedAt: e.published_at || new Date().toISOString(),
    weekStart: e.week_start || '',
    weekEnd: e.week_end || '',
    articleCount: e.article_count,
    featuredArticleId: featured?.id,
    featuredArticle: featured,
    printReady: e.print_ready,
    printPdfUrl: e.print_pdf_url || undefined,
  };
}

function transformPlan(p: ApiSubscriptionPlanOut): SubscriptionPlan {
  return {
    id: p.id,
    name: p.name,
    type: p.plan_type as SubscriptionPlan['type'],
    price: p.price,
    currency: p.currency,
    interval: p.interval as SubscriptionPlan['interval'],
    features: p.features,
    highlighted: p.highlighted,
    printIncluded: p.print_included,
  };
}

/** Guess a category color token from the category name (for API responses that lack color) */
function guessCategoryColor(name: string): string {
  const lower = name.toLowerCase();
  if (lower.includes('science') || lower.includes('tech')) return 'blue';
  if (lower.includes('world') || lower.includes('news')) return 'rose';
  if (lower.includes('environ') || lower.includes('climate')) return 'green';
  if (lower.includes('culture') || lower.includes('art')) return 'purple';
  if (lower.includes('health') || lower.includes('well')) return 'teal';
  if (lower.includes('sport') || lower.includes('olymp')) return 'orange';
  if (lower.includes('business') || lower.includes('economy') || lower.includes('market')) return 'amber';
  if (lower.includes('opinion') || lower.includes('analysis')) return 'indigo';
  if (lower.includes('deep') || lower.includes('investig')) return 'cyan';
  if (lower.includes('future') || lower.includes('innov')) return 'pink';
  if (lower.includes('life') || lower.includes('travel')) return 'emerald';
  return 'blue';
}

// ========================
// Dummy-data helpers (fallback)
// ========================

function withAuthor(article: Article): Article {
  return { ...article, author: dummyAuthors.find(a => a.id === article.authorId) };
}
function withCategory(article: Article): Article {
  return { ...article, category: dummyCategories.find(c => c.id === article.categoryId) };
}
function withRelations(article: Article): Article {
  return withCategory(withAuthor(article));
}
function withArticles(edition: Edition): Edition {
  const editionArticles = dummyArticles.filter(a => edition.articleIds.includes(a.id)).map(withRelations);
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

export function getSiteConfig(): SiteConfig {
  return dummySiteConfig;
}

// ========================
// Authors
// ========================

export async function getAllAuthors(): Promise<Author[]> {
  if (await checkApi()) {
    try {
      const apiAuthors = await fetchAuthors();
      return apiAuthors.map(transformAuthorOut);
    } catch { /* fall through */ }
  }
  return dummyAuthors;
}

export async function getAuthorBySlug(slug: string): Promise<Author | undefined> {
  if (await checkApi()) {
    try {
      const apiAuthor = await fetchAuthor(slug);
      return transformAuthorOut(apiAuthor);
    } catch { /* fall through */ }
  }
  return dummyAuthors.find(a => a.slug === slug);
}

export async function getArticlesByAuthorId(authorId: string): Promise<Article[]> {
  if (await checkApi()) {
    try {
      const author = dummyAuthors.find(a => a.id === authorId);
      const authorSlug = author?.slug;
      if (!authorSlug) return [];
      const response = await fetchArticles({ author: authorSlug, page_size: 50 });
      return response.results.map(transformArticleBrief);
    } catch { /* fall through */ }
  }
  return dummyArticles.filter(a => a.authorId === authorId).map(withRelations);
}

// ========================
// Categories
// ========================

export async function getAllCategories(): Promise<Category[]> {
  if (await checkApi()) {
    try {
      const apiCategories = await fetchCategories();
      return apiCategories.map(transformCategoryOut);
    } catch { /* fall through */ }
  }
  return dummyCategories;
}

export async function getCategoryBySlug(slug: string): Promise<Category | undefined> {
  if (await checkApi()) {
    try {
      const apiCategory = await fetchCategory(slug);
      return transformCategoryOut(apiCategory);
    } catch { /* fall through */ }
  }
  return dummyCategories.find(c => c.slug === slug);
}

export async function getFeaturedCategories(): Promise<Category[]> {
  const all = await getAllCategories();
  return all.filter(c => c.featured);
}

export async function getPublicCategories(): Promise<Category[]> {
  const all = await getAllCategories();
  return all.filter(c => c.access === 'public');
}

export async function getPremiumCategories(): Promise<Category[]> {
  const all = await getAllCategories();
  return all.filter(c => c.access === 'premium');
}

export async function getAuthorById(id: string): Promise<Author | undefined> {
  if (await checkApi()) {
    try {
      const authors = await fetchAuthors();
      const found = authors.find(a => a.id === id);
      return found ? transformAuthorOut(found) : undefined;
    } catch { /* fall through */ }
  }
  return dummyAuthors.find(a => a.id === id);
}

export async function getEditionById(id: string): Promise<Edition | undefined> {
  if (await checkApi()) {
    try {
      const response = await fetchEditions({ page_size: 100 });
      const edition = response.results.find(e => e.id === id);
      return edition ? transformEditionBrief(edition) : undefined;
    } catch { /* fall through */ }
  }
  const edition = dummyEditions.find(e => e.id === id);
  return edition ? withArticles(edition) : undefined;
}

// ========================
// Articles
// ========================

export async function getAllArticles(): Promise<Article[]> {
  if (await checkApi()) {
    try {
      const response = await fetchArticles({ page_size: 100 });
      return response.results.map(transformArticleBrief);
    } catch { /* fall through */ }
  }
  return dummyArticles.map(withRelations);
}

export async function getArticleBySlug(slug: string): Promise<Article | undefined> {
  if (await checkApi()) {
    try {
      const apiArticle = await fetchArticle(slug);
      return transformArticleOut(apiArticle);
    } catch { /* fall through */ }
  }
  const article = dummyArticles.find(a => a.slug === slug);
  return article ? withRelations(article) : undefined;
}

export async function getArticlesByCategory(categorySlug: string): Promise<Article[]> {
  if (await checkApi()) {
    try {
      const response = await fetchArticles({ category: categorySlug, page_size: 50 });
      return response.results.map(transformArticleBrief);
    } catch { /* fall through */ }
  }
  const category = dummyCategories.find(c => c.slug === categorySlug);
  if (!category) return [];
  return dummyArticles.filter(a => a.categoryId === category.id).map(withRelations);
}

export async function getFeaturedArticles(): Promise<Article[]> {
  if (await checkApi()) {
    try {
      const response = await fetchArticles({ featured: true, page_size: 10 });
      return response.results.map(transformArticleBrief);
    } catch { /* fall through */ }
  }
  return dummyArticles.filter(a => a.featured).map(withRelations);
}

export async function getTrendingArticles(): Promise<Article[]> {
  if (await checkApi()) {
    try {
      const response = await fetchArticles({ trending: true, page_size: 10 });
      return response.results.map(transformArticleBrief);
    } catch { /* fall through */ }
  }
  return dummyArticles.filter(a => a.trending).map(withRelations);
}

export async function getPinnedArticles(): Promise<Article[]> {
  if (await checkApi()) {
    try {
      const response = await fetchArticles({ featured: true, page_size: 5 });
      // API doesn't have a pinned filter in public listing, use featured as proxy
      return response.results.map(transformArticleBrief);
    } catch { /* fall through */ }
  }
  return dummyArticles.filter(a => a.pinned).map(withRelations);
}

export async function getLatestArticles(limit: number = 10): Promise<Article[]> {
  if (await checkApi()) {
    try {
      const response = await fetchArticles({ page_size: limit });
      return response.results.map(transformArticleBrief);
    } catch { /* fall through */ }
  }
  return dummyArticles
    .sort((a, b) => new Date(b.publishedAt).getTime() - new Date(a.publishedAt).getTime())
    .slice(0, limit)
    .map(withRelations);
}

// ========================
// Search
// ========================

export async function searchArticles(
  query: string,
  options: PaginationOptions = {}
): Promise<SearchResult> {
  if (await checkApi()) {
    try {
      const response = await fetchSearchResults(query, {
        page: options.page || 1,
        page_size: options.perPage || 12,
      });
      return {
        articles: response.results.map(transformArticleBrief),
        totalResults: response.count,
        page: options.page || 1,
        perPage: options.perPage || 12,
        totalPages: Math.ceil(response.count / (options.perPage || 12)),
      };
    } catch { /* fall through */ }
  }

  // Fallback: local search
  const normalizedQuery = query.toLowerCase().trim();
  if (!normalizedQuery) {
    const paginated = paginate(dummyArticles.map(withRelations), options.page, options.perPage);
    return {
      articles: paginated.items,
      totalResults: paginated.total,
      page: paginated.currentPage,
      perPage: options.perPage || 12,
      totalPages: paginated.totalPages,
    };
  }
  const results = dummyArticles.filter(a => {
    const haystack = [
      a.title, a.subtitle || '', a.excerpt,
      dummyAuthors.find(au => au.id === a.authorId)?.name || '',
      dummyCategories.find(c => c.id === a.categoryId)?.name || '',
    ].join(' ').toLowerCase();
    return haystack.includes(normalizedQuery);
  });
  results.sort((a, b) => {
    const aMatch = a.title.toLowerCase().includes(normalizedQuery) ? 0 : 1;
    const bMatch = b.title.toLowerCase().includes(normalizedQuery) ? 0 : 1;
    if (aMatch !== bMatch) return aMatch - bMatch;
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

export async function getAllEditions(): Promise<Edition[]> {
  if (await checkApi()) {
    try {
      const response = await fetchEditions({ page_size: 100 });
      return response.results.map(transformEditionBrief);
    } catch { /* fall through */ }
  }
  return dummyEditions.filter(e => e.status === 'published').sort((a, b) => b.number - a.number).map(withArticles);
}

export async function getEditionBySlug(slug: string): Promise<Edition | undefined> {
  if (await checkApi()) {
    try {
      const apiEdition = await fetchEdition(slug);
      return transformEditionOut(apiEdition);
    } catch { /* fall through */ }
  }
  const edition = dummyEditions.find(e => e.slug === slug);
  return edition ? withArticles(edition) : undefined;
}

export async function getLatestEdition(): Promise<Edition | undefined> {
  if (await checkApi()) {
    try {
      const apiEdition = await fetchLatestEdition();
      return transformEditionOut(apiEdition);
    } catch { /* fall through */ }
  }
  const latest = dummyEditions.filter(e => e.status === 'published').sort((a, b) => b.number - a.number)[0];
  return latest ? withArticles(latest) : undefined;
}

// ========================
// Aggregation helpers (homepage)
// ========================

export async function getHomepageData() {
  if (await checkApi()) {
    try {
      const homepage = await fetchHomepage();

      // Fetch category-specific articles in parallel
      const [scienceRes, worldRes, envRes] = await Promise.allSettled([
        fetchArticles({ category: 'science-tech', page_size: 3 }),
        fetchArticles({ category: 'world-news', page_size: 3 }),
        fetchArticles({ category: 'environment', page_size: 3 }),
      ]);

      const latestScience = scienceRes.status === 'fulfilled' ? scienceRes.value.results.map(transformArticleBrief) : [];
      const latestWorld = worldRes.status === 'fulfilled' ? worldRes.value.results.map(transformArticleBrief) : [];
      const latestEnvironment = envRes.status === 'fulfilled' ? envRes.value.results.map(transformArticleBrief) : [];

      const featured = homepage.featured_articles.map(transformArticleBrief);
      const trending = homepage.trending_articles.map(transformArticleBrief);
      const latestEdition = homepage.latest_edition ? transformEditionBrief(homepage.latest_edition) : undefined;

      // Hero = first featured article (or first trending as fallback)
      const heroArticle = featured[0] || trending[0];

      return {
        latestEdition,
        heroArticle,
        trending,
        featured,
        latestScience,
        latestWorld,
        latestEnvironment,
        editionCount: latestEdition?.number || 0,
      };
    } catch { /* fall through */ }
  }

  // Fallback to dummy data
  const latestEdition = getLatestEditionDummy();
  const heroArticle = latestEdition?.featuredArticle || dummyArticles.filter(a => a.featured).map(withRelations)[0];
  const trending = dummyArticles.filter(a => a.trending).map(withRelations);
  const featured = dummyArticles.filter(a => a.featured).map(withRelations);
  const latestScience = getArticlesByCategoryDummy('science-tech').slice(0, 3);
  const latestWorld = getArticlesByCategoryDummy('world-news').slice(0, 3);
  const latestEnvironment = getArticlesByCategoryDummy('environment').slice(0, 3);
  const editionCount = dummyEditions.filter(e => e.status === 'published').length;

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

function getLatestEditionDummy(): Edition | undefined {
  const latest = dummyEditions.filter(e => e.status === 'published').sort((a, b) => b.number - a.number)[0];
  return latest ? withArticles(latest) : undefined;
}

function getArticlesByCategoryDummy(slug: string): Article[] {
  const category = dummyCategories.find(c => c.slug === slug);
  if (!category) return [];
  return dummyArticles
    .filter(a => a.categoryId === category.id)
    .map(withRelations)
    .sort((a, b) => new Date(b.publishedAt).getTime() - new Date(a.publishedAt).getTime());
}

export async function getCategoryPageData(slug: string, options: PaginationOptions = {}) {
  const category = await getCategoryBySlug(slug);
  if (!category) return null;

  const allArticles = await getArticlesByCategory(slug);
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

export async function getArticlePageData(slug: string) {
  const article = await getArticleBySlug(slug);
  if (!article) return null;

  const related = (await getArticlesByCategory(article.category?.slug || ''))
    .filter(a => a.id !== article.id)
    .slice(0, 4);

  return {
    article,
    related,
  };
}

// ========================
// Subscription Plans
// ========================

export async function getSubscriptionPlans(): Promise<SubscriptionPlan[]> {
  if (await checkApi()) {
    try {
      const apiPlans = await fetchPlans();
      return apiPlans.map(transformPlan);
    } catch { /* fall through */ }
  }
  return dummySiteConfig.subscriptionPlans;
}

// ========================
// Print-on-Demand
// ========================

export function getPrintPricing() {
  return {
    single: 12.99,
    multiCopy: 10.99,
    bulk: 9.49,
    shippingUS: 4.99,
    shippingInternational: 9.99,
    freeShippingThreshold: 50,
    currency: 'USD',
  };
}

export function calculatePrintOrderTotal(quantity: number, region: 'us' | 'international') {
  const pricing = getPrintPricing();
  const unitPrice = quantity >= 5 ? pricing.bulk : quantity >= 2 ? pricing.multiCopy : pricing.single;
  const subtotal = unitPrice * quantity;
  const shipping = subtotal >= pricing.freeShippingThreshold
    ? 0
    : region === 'us' ? pricing.shippingUS : pricing.shippingInternational;
  const discount = Math.max(0, pricing.single * quantity - subtotal);
  return { unitPrice, subtotal, shipping, discount, total: subtotal + shipping - discount };
}
