// ============================================================
// MERIDIAN Magazine — Site Configuration
// ============================================================

import type { SiteConfig } from '../types';

export const siteConfig: SiteConfig = {
  // ==================== Payment Gateways ====================
  paymentGateways: [
    {
      id: 'stripe',
      name: 'Stripe',
      description: 'Pay securely with credit/debit card via Stripe',
      icon: 'stripe',
      paymentLink: 'https://buy.stripe.com/placeholder_subscription',
      enabled: true,
    },
    {
      id: 'paypal',
      name: 'PayPal',
      description: 'Pay with your PayPal account or debit card',
      icon: 'paypal',
      paymentLink: 'https://www.paypal.com/ncp/payment/placeholder_subscription',
      enabled: true,
    },
  ],
  termsOfServiceUrl: '/terms',
  name: 'MERIDIAN',
  tagline: 'Your World, Synthesized',
  description:
    'A daily synthesized knowledge magazine for the curious mind. Covering world news, science, technology, environment, culture, sports, and health — delivering clarity in a world of noise.',
  url: 'https://meridian-mag.com',
  logo: '/logo.svg',
  ogDefaultImage: '/og-default.svg',
  favicon: '/favicon.svg',
  language: 'en',

  // ==================== Navigation ====================
  navLinks: [
    { label: 'World', href: '/categories/world-news' },
    { label: 'Science', href: '/categories/science-tech' },
    { label: 'Environment', href: '/categories/environment' },
    { label: 'Culture', href: '/categories/culture' },
    { label: 'Sports', href: '/categories/sports' },
    { label: 'Health', href: '/categories/health' },
    { label: 'Business', href: '/categories/business-economy', access: 'premium' },
    { label: 'Opinion', href: '/categories/opinion-analysis', access: 'premium' },
  ],

  footerLinks: [
    { label: 'Home', href: '/' },
    { label: 'All Editions', href: '/editions/archive' },
    { label: 'Subscribe', href: '/subscribe' },
    { label: 'Premium Plan', href: '/subscribe/pricing' },
    { label: 'Print Edition', href: '/print/order' },
    { label: 'RSS Feed', href: '/rss.xml' },
    { label: 'About', href: '/about' },
    { label: 'Contact', href: '/contact' },
  ],

  // ==================== Social Links ====================
  socialLinks: [
    {
      platform: 'twitter',
      url: 'https://twitter.com/meridianmag',
      label: 'Follow us on X (Twitter)',
    },
    {
      platform: 'instagram',
      url: 'https://instagram.com/meridianmag',
      label: 'Follow us on Instagram',
    },
    {
      platform: 'youtube',
      url: 'https://youtube.com/@meridianmag',
      label: 'Subscribe on YouTube',
    },
    {
      platform: 'rss',
      url: '/rss.xml',
      label: 'RSS Feed',
    },
    {
      platform: 'linkedin',
      url: 'https://linkedin.com/company/meridianmag',
      label: 'Follow us on LinkedIn',
    },
  ],

  // ==================== Subscription Plans ====================
  subscriptionPlans: [
    {
      id: 'plan-free',
      name: 'Free',
      type: 'free',
      price: 0,
      currency: 'USD',
      interval: 'monthly',
      features: [
        'Access to all public category articles',
        'Daily edition summaries',
        'Search across all articles',
        'Newsletter with top stories',
        'Basic reading experience',
      ],
      highlighted: false,
      printIncluded: false,
    },
    {
      id: 'plan-premium',
      name: 'Premium',
      type: 'premium',
      price: 9.99,
      currency: 'USD',
      interval: 'monthly',
      features: [
        'Everything in Free, plus:',
        'Full access to premium categories',
        'Deep Dives and long-form journalism',
        'Expert opinion & analysis columns',
        'Ad-free reading experience',
        'Early access to exclusive features',
        'Bookmark & save articles',
      ],
      highlighted: true,
      printIncluded: false,
    },
    {
      id: 'plan-print',
      name: 'Premium + Print',
      type: 'premium_print',
      price: 19.99,
      currency: 'USD',
      interval: 'monthly',
      features: [
        'Everything in Premium, plus:',
        'Weekly print-on-demand magazine',
        'High-quality printed edition delivered',
        'PDF downloads of every edition',
        'Collectible cover art',
        'Gift subscription option',
      ],
      highlighted: false,
      printIncluded: true,
    },
    {
      id: 'plan-premium-annual',
      name: 'Premium Annual',
      type: 'premium',
      price: 99.99,
      currency: 'USD',
      interval: 'yearly',
      features: [
        'Everything in Premium, plus:',
        'Save 17% with annual billing',
        'Exclusive annual digest book',
        'Priority support',
        'Founder badge on comments',
      ],
      highlighted: false,
      printIncluded: false,
    },
  ],
};
