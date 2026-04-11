// ============================================================
// MERIDIAN Magazine — API Client
// ============================================================
// Raw HTTP client for the Django Ninja backend.
// All functions return snake_case JSON from the API.
// Transformers in service.ts convert these to frontend types.
// ============================================================

const API_BASE = import.meta.env.PUBLIC_API_URL || 'http://localhost:8085/api/v1';

// ---- Fetch wrapper ----

interface FetchOptions {
  token?: string;
  params?: Record<string, string | number | boolean | undefined>;
}

async function apiFetch<T>(endpoint: string, options: FetchOptions = {}): Promise<T> {
  const url = new URL(`${API_BASE}${endpoint}`);

  if (options.params) {
    for (const [key, value] of Object.entries(options.params)) {
      if (value !== undefined && value !== '') {
        url.searchParams.set(key, String(value));
      }
    }
  }

  const headers: Record<string, string> = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
  };

  if (options.token) {
    headers['Authorization'] = `Token ${options.token}`;
  }

  const response = await fetch(url.toString(), {
    headers,
    method: 'GET',
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.status} ${response.statusText} — ${endpoint}`);
  }

  return response.json() as Promise<T>;
}

// ---- Raw API Response Types (snake_case) ----

export interface ApiArticleBrief {
  id: string;
  title: string;
  slug: string;
  excerpt: string;
  cover_image: string;
  author_name: string;
  author_slug: string;
  category_name: string;
  category_slug: string;
  published_at: string | null;
  reading_time: number;
  content_type: string;
  access: string;
  featured: boolean;
  trending: boolean;
  pinned: boolean;
}

export interface ApiAuthorBrief {
  id: string;
  name: string;
  slug: string;
  avatar: string;
  role: string;
}

export interface ApiCategoryBrief {
  id: string;
  name: string;
  slug: string;
  color: string;
  access: string;
}

export interface ApiArticleOut extends ApiArticleBrief {
  subtitle: string;
  content: string;
  cover_caption: string;
  author: ApiAuthorBrief;
  category: ApiCategoryBrief;
  status: string;
  seo_title: string;
  seo_description: string;
  seo_keywords: string[];
  updated_at: string | null;
  created_at: string | null;
  word_count: number;
  reviewed_by_name: string | null;
  rejection_reason: string;
}

export interface ApiCategoryOut extends ApiCategoryBrief {
  description: string;
  icon: string;
  featured: boolean;
  article_count: number;
  created_at: string | null;
  updated_at: string | null;
}

export interface ApiAuthorOut {
  id: string;
  name: string;
  slug: string;
  bio: string;
  avatar: string;
  role: string;
  twitter: string;
  linkedin: string;
  instagram: string;
  website: string;
  article_count: number;
  created_at: string | null;
  updated_at: string | null;
}

export interface ApiEditionBrief {
  id: string;
  number: number;
  title: string;
  slug: string;
  cover_image: string;
  status: string;
  published_at: string | null;
  week_start: string | null;
  week_end: string | null;
  article_count: number;
  print_ready: boolean;
}

export interface ApiEditionOut extends ApiEditionBrief {
  subtitle: string;
  featured_article: ApiArticleBrief | null;
  print_ready: boolean;
  print_pdf_url: string;
  articles: ApiArticleBrief[];
  created_at: string | null;
  updated_at: string | null;
}

export interface ApiSubscriptionPlanOut {
  id: string;
  name: string;
  plan_type: string;
  price: number;
  currency: string;
  interval: string;
  features: string[];
  highlighted: boolean;
  print_included: boolean;
  is_active: boolean;
}

export interface ApiHomepageData {
  featured_articles: ApiArticleBrief[];
  trending_articles: ApiArticleBrief[];
  pinned_articles: ApiArticleBrief[];
  latest_edition: ApiEditionBrief | null;
  categories: ApiCategoryBrief[];
}

export interface ApiPaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// ---- Public API Functions ----

export async function fetchHomepage(): Promise<ApiHomepageData> {
  return apiFetch<ApiHomepageData>('/homepage/');
}

export async function fetchArticles(params?: {
  page?: number;
  page_size?: number;
  category?: string;
  access?: string;
  featured?: boolean;
  trending?: boolean;
  author?: string;
}): Promise<ApiPaginatedResponse<ApiArticleBrief>> {
  return apiFetch<ApiPaginatedResponse<ApiArticleBrief>>('/articles/', { params });
}

export async function fetchArticle(slug: string): Promise<ApiArticleOut> {
  return apiFetch<ApiArticleOut>(`/articles/${slug}`);
}

export async function fetchCategories(): Promise<ApiCategoryOut[]> {
  return apiFetch<ApiCategoryOut[]>('/categories/');
}

export async function fetchCategory(slug: string): Promise<ApiCategoryOut> {
  return apiFetch<ApiCategoryOut>(`/categories/${slug}`);
}

export async function fetchAuthors(): Promise<ApiAuthorOut[]> {
  return apiFetch<ApiAuthorOut[]>('/authors/');
}

export async function fetchAuthor(slug: string): Promise<ApiAuthorOut> {
  return apiFetch<ApiAuthorOut>(`/authors/${slug}`);
}

export async function fetchEditions(params?: {
  page?: number;
  page_size?: number;
}): Promise<ApiPaginatedResponse<ApiEditionBrief>> {
  return apiFetch<ApiPaginatedResponse<ApiEditionBrief>>('/editions/', { params });
}

export async function fetchEdition(slug: string): Promise<ApiEditionOut> {
  return apiFetch<ApiEditionOut>(`/editions/${slug}`);
}

export async function fetchLatestEdition(): Promise<ApiEditionOut> {
  return apiFetch<ApiEditionOut>('/editions/latest/');
}

export async function fetchSearchResults(query: string, params?: {
  page?: number;
  page_size?: number;
  category?: string;
}): Promise<ApiPaginatedResponse<ApiArticleBrief>> {
  return apiFetch<ApiPaginatedResponse<ApiArticleBrief>>('/search/', {
    params: { q: query, ...params },
  });
}

export async function fetchPlans(): Promise<ApiSubscriptionPlanOut[]> {
  return apiFetch<ApiSubscriptionPlanOut[]>('/plans/');
}

export async function fetchPrintPricing() {
  return apiFetch<{
    unit_price_us: number;
    shipping_us: number;
    unit_price_international: number;
    shipping_international: number;
    bulk_discount_threshold: number;
    bulk_discount_percent: number;
    currency: string;
  }>('/print/pricing/');
}

// ---- Site Config API ----

export interface ApiNavLink {
  label: string;
  href: string;
  access?: string;
}

export interface ApiSocialLink {
  platform: string;
  url: string;
  label: string;
}

export interface ApiPaymentGateway {
  id: string;
  name: string;
  description: string;
  icon: string;
  payment_link: string;
  enabled: boolean;
}

export interface ApiSiteConfigOut {
  name: string;
  tagline: string;
  description: string;
  url: string;
  terms_of_service_url: string;
  nav_links: ApiNavLink[];
  footer_links: ApiNavLink[];
  social_links: ApiSocialLink[];
  payment_gateways: ApiPaymentGateway[];
  subscription_plans: ApiSubscriptionPlanOut[];
  print_pricing: {
    unit_price_us: number;
    shipping_us: number;
    unit_price_international: number;
    shipping_international: number;
    bulk_discount_threshold: number;
    bulk_discount_percent: number;
    currency: string;
  } | null;
}

export async function fetchSiteConfig(): Promise<ApiSiteConfigOut> {
  return apiFetch<ApiSiteConfigOut>('/site-config/');
}

// ---- Auth API Functions ----

export interface ApiTokenOut {
  token: string;
  user_id: string;
  username: string;
  role: string;
}

export interface ApiUserOut {
  id: number;
  username: string;
  email: string;
  role: string;
  first_name: string;
  last_name: string;
  is_active: boolean;
  date_joined: string | null;
}

export async function apiLogin(username: string, password: string): Promise<ApiTokenOut> {
  const response = await fetch(`${API_BASE}/auth/login/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || `Login failed: ${response.status}`);
  }
  return response.json() as Promise<ApiTokenOut>;
}

export async function apiRegister(username: string, email: string, password: string): Promise<ApiTokenOut> {
  const response = await fetch(`${API_BASE}/auth/register/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, email, password }),
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || `Registration failed: ${response.status}`);
  }
  return response.json() as Promise<ApiTokenOut>;
}

export async function apiGetCurrentUser(token: string): Promise<ApiUserOut> {
  return apiFetch<ApiUserOut>('/auth/me/', { token });
}

export async function apiLogout(token: string): Promise<void> {
  await fetch(`${API_BASE}/auth/logout/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Token ${token}`,
    },
  });
}

// ---- Newsletter API Functions ----

export async function apiNewsletterSubscribe(email: string): Promise<{ message: string }> {
  const response = await fetch(`${API_BASE}/newsletter/subscribe/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email }),
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || `Newsletter subscription failed: ${response.status}`);
  }
  return response.json() as Promise<{ message: string }>;
}

// ---- Helper: Check if API is reachable ----

export async function isApiAvailable(): Promise<boolean> {
  try {
    await fetch(`${API_BASE}/homepage/`, { method: 'HEAD', signal: AbortSignal.timeout(5000) });
    return true;
  } catch {
    return false;
  }
}
