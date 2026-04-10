/**
 * MERIDIAN Magazine — PDF Generation Script
 * ============================================================
 * Converts print template pages to downloadable PDFs using Puppeteer.
 * Run: npx tsx scripts/generate-print-pdf.ts [edition-slug]
 *
 * Without arguments: generates PDFs for all print-ready editions.
 * With an edition slug: generates PDF for that edition only.
 *
 * Output: public/downloads/meridian-edition-{number}.pdf
 *
 * Prerequisites:
 *   npm install puppeteer
 *   (or use existing Playwright installation)
 */

import puppeteer, { type Browser, type Page } from 'puppeteer';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { existsSync, mkdirSync } from 'fs';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = resolve(__dirname, '..');
const OUTPUT_DIR = resolve(PROJECT_ROOT, 'public/downloads');
const BASE_URL = 'http://localhost:4321';

interface EditionMeta {
  slug: string;
  number: number;
  printReady: boolean;
}

// Print-ready editions (mirrors dummy data for offline use)
const PRINT_EDITIONS: EditionMeta[] = [
  { slug: 'edition-45-week-of-june-29', number: 45, printReady: true },
  { slug: 'edition-44-week-of-june-22', number: 44, printReady: true },
  { slug: 'edition-43-week-of-june-15', number: 43, printReady: true },
  { slug: 'edition-42-week-of-june-8', number: 42, printReady: true },
];

/**
 * Ensure output directory exists.
 */
function ensureOutputDir(): void {
  if (!existsSync(OUTPUT_DIR)) {
    mkdirSync(OUTPUT_DIR, { recursive: true });
  }
}

/**
 * Generate a PDF for a single edition.
 */
async function generateEditionPdf(
  browser: Browser,
  slug: string,
  editionNumber: number
): Promise<string> {
  const page = await browser.newPage();
  const printUrl = `${BASE_URL}/print/${slug}`;
  const outputPath = resolve(OUTPUT_DIR, `meridian-edition-${editionNumber}.pdf`);

  console.log(`📄 Generating PDF for ${slug}...`);
  console.log(`   URL: ${printUrl}`);

  try {
    await page.goto(printUrl, {
      waitUntil: 'networkidle0',
      timeout: 30000,
    });

    // Wait for content to render
    await page.waitForSelector('.print-cover', { timeout: 10000 });
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Generate PDF with print-specific settings
    await page.pdf({
      path: outputPath,
      format: 'A4',
      printBackground: true,
      preferCSSPageSize: false,
      margin: {
        top: '0mm',
        right: '0mm',
        bottom: '0mm',
        left: '0mm',
      },
      displayHeaderFooter: false,
      scale: 1,
    });

    console.log(`   ✅ Saved: ${outputPath}`);
    return outputPath;
  } catch (error) {
    console.error(`   ❌ Failed for ${slug}:`, error);
    throw error;
  } finally {
    await page.close();
  }
}

/**
 * Main entry point.
 */
async function main(): Promise<void> {
  const args = process.argv.slice(2);
  const targetSlug = args[0];

  ensureOutputDir();

  if (targetSlug) {
    // Generate for a specific edition
    const edition = PRINT_EDITIONS.find(e => e.slug === targetSlug);
    if (!edition) {
      console.error(`❌ Edition "${targetSlug}" not found in print-ready list.`);
      console.log('Available editions:');
      PRINT_EDITIONS.forEach(e => console.log(`  - ${e.slug}`));
      process.exit(1);
    }

    console.log(`\n🖨️  MERIDIAN PDF Generator — Single Edition Mode\n`);

    const browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox'],
    });

    try {
      await generateEditionPdf(browser, edition.slug, edition.number);
    } finally {
      await browser.close();
    }
  } else {
    // Generate for all print-ready editions
    const readyEditions = PRINT_EDITIONS.filter(e => e.printReady);

    console.log(`\n🖨️  MERIDIAN PDF Generator — Batch Mode`);
    console.log(`   ${readyEditions.length} editions to process\n`);

    const browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox'],
    });

    try {
      for (const edition of readyEditions) {
        await generateEditionPdf(browser, edition.slug, edition.number);
      }

      console.log(`\n✅ All ${readyEditions.length} PDFs generated successfully!`);
      console.log(`   Output directory: ${OUTPUT_DIR}`);
    } finally {
      await browser.close();
    }
  }
}

// Run
main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
