// ============================================================
// MERIDIAN Magazine — RSS Feed Endpoint
// ============================================================
// Generates a valid RSS 2.0 XML feed with the latest 20 public
// (non-premium) articles. Excludes premium content behind paywall.
// ============================================================

import rss from '@astrojs/rss';
import { getLatestArticles, getAllCategories } from '@data/service';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const allArticles = await getLatestArticles(50);
  const premiumCategories = (await getAllCategories())
    .filter(c => c.access === 'premium')
    .map(c => c.id);

  // Only include public articles in RSS feed
  const publicArticles = allArticles.filter(
    article => !premiumCategories.includes(article.categoryId)
  ).slice(0, 20);

  return rss({
    title: 'MERIDIAN — Your World, Synthesized',
    description: 'A daily synthesized knowledge magazine for the curious mind. Covering world news, science, technology, environment, culture, sports, and health.',
    site: context.site!,
    items: publicArticles.map(article => ({
      title: article.title,
      pubDate: new Date(article.publishedAt),
      description: article.excerpt,
      link: `/articles/${article.slug}`,
      categories: [article.category?.name || 'General'].filter(Boolean),
      author: article.author?.name || 'MERIDIAN Staff',
      // Use cover image as enclosure if available
      ...(article.coverImage ? {
        enclosure: {
          url: article.coverImage.startsWith('http')
            ? article.coverImage
            : new URL(article.coverImage, context.site!).toString(),
          length: 0, // Unknown size
          type: 'image/jpeg',
        },
      } : {}),
    })),
    customData: `<language>en-us</language>
<copyright>© ${new Date().getFullYear()} MERIDIAN Magazine. All rights reserved.</copyright>
<managingEditor>editorial@meridian-mag.com (MERIDIAN Editorial)</managingEditor>
<webMaster>tech@meridian-mag.com (MERIDIAN Tech)</webMaster>
<ttl>60</ttl>`,
  });
}
