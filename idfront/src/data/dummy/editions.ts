// ============================================================
// MERIDIAN Magazine — Editorial Dashboard Dummy Data
// ============================================================

import type { EditorialQueueItem, EditorialActivity, EditorialStats } from '../types';

export const editorialQueue: EditorialQueueItem[] = [
  {
    id: 'eq-01',
    articleId: 'article-new-01',
    title: 'The Race to Build a Quantum Internet',
    authorName: 'Sarah Chen',
    authorSlug: 'sarah-chen',
    category: 'Science & Tech',
    categorySlug: 'science-tech',
    coverImage: '/images/article-quantum.png',
    excerpt: 'Researchers worldwide are competing to create unhackable communication networks using quantum entanglement. A deep dive into the science and geopolitics of quantum networking.',
    status: 'published',
    submittedAt: '2026-07-10T08:30:00Z',
    updatedAt: '2026-07-12T14:00:00Z',
    reviewedBy: 'James Okonkwo',
    wordCount: 2450,
    readingTime: 10,
  },
  {
    id: 'eq-02',
    articleId: 'article-new-02',
    title: 'Inside the UN Digital Rights Treaty',
    authorName: 'James Okonkwo',
    authorSlug: 'james-okonkwo',
    category: 'World News',
    categorySlug: 'world-news',
    coverImage: '/images/article-un-digital-rights.png',
    excerpt: 'After years of negotiations, 193 nations agree on a framework to protect digital privacy. But critics say it lacks enforcement teeth.',
    status: 'in_review',
    submittedAt: '2026-07-14T10:15:00Z',
    updatedAt: '2026-07-14T10:15:00Z',
    wordCount: 1800,
    readingTime: 8,
  },
  {
    id: 'eq-03',
    articleId: 'article-new-03',
    title: 'CRISPR 3.0: Gene Editing Gets Precise',
    authorName: 'Priya Sharma',
    authorSlug: 'priya-sharma',
    category: 'Health',
    categorySlug: 'health',
    coverImage: '/images/article-crispr.png',
    excerpt: 'Third-generation CRISPR tools can edit single DNA letters with 99.7% accuracy. Clinical trials for sickle cell disease show promising early results.',
    status: 'approved',
    submittedAt: '2026-07-12T09:00:00Z',
    updatedAt: '2026-07-13T16:30:00Z',
    reviewedBy: 'Sarah Chen',
    wordCount: 2100,
    readingTime: 9,
  },
  {
    id: 'eq-04',
    articleId: 'article-new-04',
    title: 'The Psychology of Climate Anxiety',
    authorName: 'Priya Sharma',
    authorSlug: 'priya-sharma',
    category: 'Health',
    categorySlug: 'health',
    coverImage: '/images/article-mental-health.png',
    excerpt: 'A growing number of young people report "eco-anxiety" linked to climate change. Researchers are studying effective coping strategies and the role of community action.',
    status: 'draft',
    submittedAt: '2026-07-15T07:45:00Z',
    updatedAt: '2026-07-15T07:45:00Z',
    wordCount: 1200,
    readingTime: 5,
  },
  {
    id: 'eq-05',
    articleId: 'article-new-05',
    title: 'Mars Colony Blueprint: Engineering the Red Planet',
    authorName: 'Dr. Amira Patel',
    authorSlug: 'amira-patel',
    category: 'Science & Tech',
    categorySlug: 'science-tech',
    coverImage: '/images/article-mars.png',
    excerpt: 'NASA and SpaceX unveil a joint plan for a permanent human settlement on Mars. The 30-year roadmap includes in-situ resource utilization and nuclear propulsion.',
    status: 'rejected',
    submittedAt: '2026-07-08T11:00:00Z',
    updatedAt: '2026-07-10T09:00:00Z',
    reviewedBy: 'Sarah Chen',
    rejectionReason: 'Needs more technical detail on life support systems. Current draft reads more like a press release than a technical feature. Consider adding expert interviews from aerospace engineers.',
    wordCount: 1600,
    readingTime: 7,
  },
  {
    id: 'eq-06',
    articleId: 'article-new-06',
    title: 'Global Fusion Breakthrough: Net Energy Confirmed',
    authorName: 'Sarah Chen',
    authorSlug: 'sarah-chen',
    category: 'Science & Tech',
    categorySlug: 'science-tech',
    coverImage: '/images/article-brain.png',
    excerpt: 'A European consortium reports sustained net energy gain from a tokamak reactor for over 24 hours, shattering previous records and reigniting hope for commercial fusion power.',
    status: 'in_review',
    submittedAt: '2026-07-14T14:20:00Z',
    updatedAt: '2026-07-14T14:20:00Z',
    wordCount: 1950,
    readingTime: 8,
  },
  {
    id: 'eq-07',
    articleId: 'article-new-07',
    title: 'African Cinema Renaissance at Cannes',
    authorName: 'Elena Rodriguez',
    authorSlug: 'elena-rodriguez',
    category: 'Culture',
    categorySlug: 'culture',
    coverImage: '/images/article-african-cinema.png',
    excerpt: 'Filmmakers from Nigeria, Senegal, and Kenya dominate this year\'s selection, signaling a seismic shift in global cinema. A look at the movement\'s roots and rising stars.',
    status: 'published',
    submittedAt: '2026-07-06T08:00:00Z',
    updatedAt: '2026-07-09T12:00:00Z',
    reviewedBy: 'Marcus Johnson',
    wordCount: 2200,
    readingTime: 9,
  },
  {
    id: 'eq-08',
    articleId: 'article-new-08',
    title: 'Arctic Ice Melt Accelerates Beyond Models',
    authorName: 'Marcus Johnson',
    authorSlug: 'marcus-johnson',
    category: 'Environment',
    categorySlug: 'environment',
    coverImage: '/images/article-arctic.png',
    excerpt: 'New satellite data shows Arctic sea ice is declining 40% faster than the most pessimistic climate models predicted. Scientists call for emergency policy action.',
    status: 'draft',
    submittedAt: '2026-07-15T12:00:00Z',
    updatedAt: '2026-07-15T12:00:00Z',
    wordCount: 800,
    readingTime: 3,
  },
];

export const editorialActivity: EditorialActivity[] = [
  {
    id: 'ea-01',
    action: 'published',
    articleTitle: 'The Race to Build a Quantum Internet',
    performedBy: 'James Okonkwo',
    timestamp: '2026-07-12T14:00:00Z',
    details: 'Published to Science & Tech category',
  },
  {
    id: 'ea-02',
    action: 'approved',
    articleTitle: 'CRISPR 3.0: Gene Editing Gets Precise',
    performedBy: 'Sarah Chen',
    timestamp: '2026-07-13T16:30:00Z',
    details: 'Approved with minor edits to clinical trial section',
  },
  {
    id: 'ea-03',
    action: 'submitted',
    articleTitle: 'Inside the UN Digital Rights Treaty',
    performedBy: 'James Okonkwo',
    timestamp: '2026-07-14T10:15:00Z',
    details: 'Submitted for editorial review',
  },
  {
    id: 'ea-04',
    action: 'rejected',
    articleTitle: 'Mars Colony Blueprint: Engineering the Red Planet',
    performedBy: 'Sarah Chen',
    timestamp: '2026-07-10T09:00:00Z',
    details: 'Needs more technical depth and expert interviews',
  },
  {
    id: 'ea-05',
    action: 'submitted',
    articleTitle: 'Global Fusion Breakthrough: Net Energy Confirmed',
    performedBy: 'Sarah Chen',
    timestamp: '2026-07-14T14:20:00Z',
    details: 'Submitted for editorial review',
  },
  {
    id: 'ea-06',
    action: 'published',
    articleTitle: 'African Cinema Renaissance at Cannes',
    performedBy: 'Marcus Johnson',
    timestamp: '2026-07-09T12:00:00Z',
    details: 'Published to Culture category',
  },
  {
    id: 'ea-07',
    action: 'edited',
    articleTitle: 'The Race to Build a Quantum Internet',
    performedBy: 'Sarah Chen',
    timestamp: '2026-07-11T11:00:00Z',
    details: 'Revised intro paragraph and added expert quote',
  },
  {
    id: 'ea-08',
    action: 'created',
    articleTitle: 'The Psychology of Climate Anxiety',
    performedBy: 'Priya Sharma',
    timestamp: '2026-07-15T07:45:00Z',
    details: 'Draft created — 1200 words, needs completion',
  },
  {
    id: 'ea-09',
    action: 'created',
    articleTitle: 'Arctic Ice Melt Accelerates Beyond Models',
    performedBy: 'Marcus Johnson',
    timestamp: '2026-07-15T12:00:00Z',
    details: 'Draft created — 800 words, data analysis in progress',
  },
  {
    id: 'ea-10',
    action: 'edited',
    articleTitle: 'CRISPR 3.0: Gene Editing Gets Precise',
    performedBy: 'Priya Sharma',
    timestamp: '2026-07-12T08:30:00Z',
    details: 'Updated clinical trial data and added safety section',
  },
];

/** Get all editorial queue items. */
export function getEditorialQueue(): EditorialQueueItem[] {
  return editorialQueue;
}

/** Get editorial stats computed from queue data. */
export function getEditorialStats(): EditorialStats {
  const totalArticles = editorialQueue.length;
  const totalDrafts = editorialQueue.filter(q => q.status === 'draft').length;
  const inReview = editorialQueue.filter(q => q.status === 'in_review').length;
  const approved = editorialQueue.filter(q => q.status === 'approved').length;
  const rejected = editorialQueue.filter(q => q.status === 'rejected').length;
  const publishedThisWeek = editorialQueue.filter(q => q.status === 'published').length;
  const avgReadingTime = Math.round(
    editorialQueue.reduce((sum, q) => sum + q.readingTime, 0) / totalArticles
  );

  return {
    totalDrafts,
    inReview,
    approved,
    rejected,
    publishedThisWeek,
    totalArticles,
    avgReadingTime,
  };
}

/** Get recent editorial activity log (sorted newest first). */
export function getRecentActivity(limit: number = 10): EditorialActivity[] {
  return editorialActivity
    .sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())
    .slice(0, limit);
}
