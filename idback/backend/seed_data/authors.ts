// ============================================================
// MERIDIAN Magazine — Dummy Authors
// ============================================================

import type { Author } from '../types';

export const authors: Author[] = [
  {
    id: 'author-01',
    name: 'Sarah Chen',
    slug: 'sarah-chen',
    bio: 'Senior Science & Technology Correspondent. Sarah covers breakthroughs in quantum computing, AI research, and emerging technologies. With a PhD in Physics from MIT, she translates complex science into engaging narratives for curious readers worldwide.',
    avatar: '/images/avatars/sarah-chen.jpg',
    role: 'Senior Science Correspondent',
    socials: {
      twitter: 'https://twitter.com/sarahchen',
      linkedin: 'https://linkedin.com/in/sarahchen',
      website: 'https://sarahchen.com',
    },
    articleCount: 24,
  },
  {
    id: 'author-02',
    name: 'Marcus Johnson',
    slug: 'marcus-johnson',
    bio: 'Environment & Climate Editor. Marcus has reported from five continents on climate change, conservation, and sustainability. His investigative work on ocean ecosystems earned him the Global Journalism Award in 2025.',
    avatar: '/images/avatars/marcus-johnson.jpg',
    role: 'Environment & Climate Editor',
    socials: {
      twitter: 'https://twitter.com/marcusjohnson',
      linkedin: 'https://linkedin.com/in/marcusjohnson',
    },
    articleCount: 31,
  },
  {
    id: 'author-03',
    name: 'Dr. Amira Patel',
    slug: 'amira-patel',
    bio: 'Space & Astronomy Writer. A former NASA research scientist, Amira brings insider knowledge to her coverage of space exploration, planetary science, and the growing commercial space industry. She holds degrees from Caltech and Oxford.',
    avatar: '/images/avatars/amira-patel.jpg',
    role: 'Space & Astronomy Correspondent',
    socials: {
      twitter: 'https://twitter.com/dramirapatel',
      website: 'https://amirapatel.space',
    },
    articleCount: 18,
  },
  {
    id: 'author-04',
    name: 'Elena Rodriguez',
    slug: 'elena-rodriguez',
    bio: 'Culture & Society Editor. Elena explores how art, music, film, and digital culture shape our world. Based in Buenos Aires and New York, she brings a global perspective to cultural trends and movements.',
    avatar: '/images/avatars/elena-rodriguez.jpg',
    role: 'Culture & Society Editor',
    socials: {
      twitter: 'https://twitter.com/elenarodriguez',
      instagram: 'https://instagram.com/elenawrites',
    },
    articleCount: 27,
  },
  {
    id: 'author-05',
    name: 'James Okonkwo',
    slug: 'james-okonkwo',
    bio: 'World News & Politics Correspondent. James covers international relations, geopolitics, and global policy. Previously based in Geneva and Nairobi, he now reports from Washington D.C. with a focus on multilateral institutions and diplomacy.',
    avatar: '/images/avatars/james-okonkwo.jpg',
    role: 'World News Correspondent',
    socials: {
      twitter: 'https://twitter.com/jamesokonkwo',
      linkedin: 'https://linkedin.com/in/jamesokonkwo',
    },
    articleCount: 35,
  },
  {
    id: 'author-06',
    name: 'Priya Sharma',
    slug: 'priya-sharma',
    bio: 'Health & Wellness Writer. Priya covers public health, mental wellness, nutrition science, and healthcare policy. With a medical degree from Johns Hopkins and a journalism master\'s from Columbia, she bridges the gap between medical research and public understanding.',
    avatar: '/images/avatars/priya-sharma.jpg',
    role: 'Health & Wellness Correspondent',
    socials: {
      twitter: 'https://twitter.com/priyasharma',
      website: 'https://priyasharma.health',
    },
    articleCount: 22,
  },
  {
    id: 'author-07',
    name: 'Tomás García',
    slug: 'tomas-garcia',
    bio: 'Sports & Competition Reporter. Tomás covers international sports, the Olympic movement, and the intersection of athletics with technology and society. A former semi-professional footballer turned journalist, he brings an insider\'s passion to every story.',
    avatar: '/images/avatars/tomas-garcia.jpg',
    role: 'Sports Correspondent',
    socials: {
      twitter: 'https://twitter.com/tomasgarcia',
      instagram: 'https://instagram.com/tomasgarcia',
    },
    articleCount: 19,
  },
  {
    id: 'author-08',
    name: 'Yuki Tanaka',
    slug: 'yuki-tanaka',
    bio: 'Technology & Innovation Editor. Based in Tokyo and San Francisco, Yuki covers consumer tech, AI applications, cybersecurity, and the societal impact of digital transformation. She has been recognized by the Asian Journalism Awards for her tech reporting.',
    avatar: '/images/avatars/yuki-tanaka.jpg',
    role: 'Technology & Innovation Editor',
    socials: {
      twitter: 'https://twitter.com/yukitanaka',
      website: 'https://yukitanaka.tech',
    },
    articleCount: 26,
  },
];

/**
 * Get an author by ID.
 */
export function getAuthorById(id: string): Author | undefined {
  return authors.find(a => a.id === id);
}

/**
 * Get an author by slug.
 */
export function getAuthorBySlug(slug: string): Author | undefined {
  return authors.find(a => a.slug === slug);
}
