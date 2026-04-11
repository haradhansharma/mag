// ============================================================
// MERIDIAN Magazine — Core TypeScript Types
// ============================================================
// All data interfaces, enums, and utility types for the magazine.
// The service layer (service.ts) returns data conforming to these types.
// ============================================================

// ========================
// Enums & Literals
// ========================

/** Content access level — controls what visitors can see */
export type AccessLevel = 'public' | 'premium';

/** The type of editorial content */
export type ContentType = 'article' | 'feature' | 'opinion' | 'brief' | 'explainer' | 'interview';

/** Edition publication status */
export type EditionStatus = 'published' | 'scheduled' | 'draft';

/** Subscription plan type */
export type PlanType = 'free' | 'premium' | 'print' | 'premium_print';

/** Category color tokens — maps to Tailwind classes */
export type CategoryColor =
  | 'blue' | 'purple' | 'green' | 'rose' | 'amber' | 'teal'
  | 'indigo' | 'orange' | 'cyan' | 'pink' | 'emerald';

// ========================
// Author
// ========================

export interface Author {
  id: string;
  name: string;
  slug: string;
  bio: string;
  avatar: string;           // URL or path to avatar image
  role: string;             // e.g. "Senior Science Correspondent"
  socials?: {
    twitter?: string;
    linkedin?: string;
    instagram?: string;
    website?: string;
  };
  articleCount: number;
}

// ========================
// Category
// ========================

export interface Category {
  id: string;
  name: string;
  slug: string;
  description: string;
  color: CategoryColor;
  icon?: string;            // SVG icon name or emoji
  access: AccessLevel;      // Controls visibility of articles in this category
  articleCount: number;
  featured?: boolean;       // Show in hero / highlighted sections
}

// ========================
// SEO
// ========================

export interface SEO {
  title: string;
  description: string;
  ogImage?: string;
  canonicalUrl?: string;
  keywords?: string[];
  publishedTime?: string;    // ISO 8601
  modifiedTime?: string;     // ISO 8601
  author?: string;
  section?: string;          // NewsArticle section
}

// ========================
// Article
// ========================

export interface Article {
  id: string;
  title: string;
  slug: string;
  subtitle?: string;          // Optional deck/sub-headline
  content: string;            // HTML or Markdown body
  excerpt: string;            // Plain text, 150–200 chars
  coverImage: string;         // URL or path
  coverCaption?: string;

  // Relationships
  authorId: string;
  author?: Author;            // Populated by service layer
  categoryId: string;
  category?: Category;        // Populated by service layer
  editionId?: string;         // Which edition this belongs to

  // Metadata
  contentType: ContentType;
  access: AccessLevel;
  seo: SEO;

  // Timestamps
  publishedAt: string;        // ISO 8601
  updatedAt?: string;         // ISO 8601

  // Reading
  readingTime: number;        // Minutes
  wordCount: number;

  // Flags
  featured: boolean;          // Featured on homepage
  trending: boolean;          // In the trending strip
  pinned?: boolean;           // Pinned to top of category
}

// ========================
// Edition
// ========================

export interface Edition {
  id: string;
  number: number;             // Sequential: 1, 2, 3...
  title: string;              // Edition headline (e.g. "The Quantum Leap")
  subtitle?: string;
  slug: string;               // e.g. "edition-42-week-of-june-22"
  coverImage: string;

  // Content
  articleIds: string[];
  articles?: Article[];        // Populated by service layer

  // Metadata
  status: EditionStatus;
  publishedAt: string;        // ISO 8601
  weekStart: string;          // ISO date (Monday)
  weekEnd: string;            // ISO date (Sunday)

  // Stats
  articleCount: number;
  featuredArticleId?: string;
  featuredArticle?: Article;

  // Print
  printReady: boolean;
  printPdfUrl?: string;
}

// ========================
// Site Config
// ========================

export interface NavLink {
  label: string;
  href: string;
  access?: AccessLevel;       // If premium, show lock icon
}

export interface SocialLink {
  platform: 'twitter' | 'instagram' | 'youtube' | 'rss' | 'linkedin';
  url: string;
  label: string;
}

export interface PaymentGateway {
  id: string;
  name: string;
  description: string;
  icon: string;              // SVG path or emoji
  paymentLink: string;       // Hosted payment link URL (e.g. Stripe link)
  enabled: boolean;
}

export interface SiteConfig {
  name: string;
  tagline: string;
  description: string;
  url: string;
  logo: string;
  ogDefaultImage: string;
  favicon: string;
  language: string;
  navLinks: NavLink[];
  footerLinks: NavLink[];
  socialLinks: SocialLink[];
  subscriptionPlans: SubscriptionPlan[];
  paymentGateways?: PaymentGateway[];
  termsOfServiceUrl?: string;
}

export interface SubscriptionPlan {
  id: string;
  name: string;
  type: PlanType;
  price: number;
  currency: string;
  interval: 'monthly' | 'yearly';
  features: string[];
  highlighted?: boolean;      // Recommended plan
  printIncluded?: boolean;
}

// ========================
// Search & Pagination
// ========================

export interface SearchResult {
  articles: Article[];
  totalResults: number;
  page: number;
  perPage: number;
  totalPages: number;
}

export interface PaginationOptions {
  page?: number;
  perPage?: number;
  sortBy?: 'publishedAt' | 'title' | 'readingTime';
  sortOrder?: 'asc' | 'desc';
}

// ========================
// JSON-LD Structured Data
// ========================

export interface JsonLdOrganization {
  '@context': 'https://schema.org';
  '@type': 'Organization';
  name: string;
  url: string;
  logo: string;
  description: string;
  sameAs?: string[];
}

export interface JsonLdArticle {
  '@context': 'https://schema.org';
  '@type': 'NewsArticle';
  headline: string;
  description: string;
  image: string;
  datePublished: string;
  dateModified?: string;
  author: {
    '@type': 'Person';
    name: string;
    url?: string;
  };
  publisher: {
    '@type': 'Organization';
    name: string;
    logo: {
      '@type': 'ImageObject';
      url: string;
    };
  };
}

export interface JsonLdWebSite {
  '@context': 'https://schema.org';
  '@type': 'WebSite';
  name: string;
  url: string;
  description: string;
  potentialAction?: {
    '@type': 'SearchAction';
    target: string;
    'query-input': string;
  };
}

// ========================
// Editorial Dashboard
// ========================

export type EditorialStatus = 'draft' | 'in_review' | 'approved' | 'rejected' | 'published';
export type EditorialAction = 'created' | 'submitted' | 'approved' | 'rejected' | 'edited' | 'published';

export interface EditorialQueueItem {
  id: string;
  articleId: string;
  title: string;
  authorName: string;
  authorSlug: string;
  category: string;
  categorySlug: string;
  coverImage: string;
  excerpt: string;
  status: EditorialStatus;
  submittedAt: string;
  updatedAt: string;
  reviewedBy?: string;
  rejectionReason?: string;
  wordCount: number;
  readingTime: number;
}

export interface EditorialActivity {
  id: string;
  action: EditorialAction;
  articleTitle: string;
  performedBy: string;
  timestamp: string;
  details?: string;
}

export interface EditorialStats {
  totalDrafts: number;
  inReview: number;
  approved: number;
  rejected: number;
  publishedThisWeek: number;
  totalArticles: number;
  avgReadingTime: number;
}
