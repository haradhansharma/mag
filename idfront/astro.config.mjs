// @ts-check
import { defineConfig } from 'astro/config';

import node from '@astrojs/node';

import tailwindcss from '@tailwindcss/vite';

import alpinejs from '@astrojs/alpinejs';

import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://meridian-mag.com',
  output: 'static',
  build: {
    assets: '_astro',
  },
  image: {
    domains: [],
  },
  adapter: node({
    mode: 'standalone'
  }),

  vite: {
    plugins: [tailwindcss()],
    resolve: {
      alias: {
        '@': '/src',
        '@components': '/src/components',
        '@layouts': '/src/layouts',
        '@assets': '/src/assets',
        '@utils': '/src/utils',
        '@data': '/src/data',
        '@styles': '/src/styles'
      },
    },
  },

  integrations: [
    alpinejs(), 
    sitemap({
      filter: (page) => {
        // Exclude premium category pages, API routes, and print order page
        const excludedPatterns = [
          '/categories/business-economy',
          '/categories/opinion-analysis',
          '/categories/deep-dives',
          '/categories/future-forward',
          '/categories/lifestyle-travel',
          '/print/order',
          '/print/',
          '/api/',
          '/search',
        ];
        return !excludedPatterns.some(pattern => page.includes(pattern));
      },
      changefreq: 'daily',
      priority: 0.7,
      lastmod: new Date(),
    }),
  ]
});