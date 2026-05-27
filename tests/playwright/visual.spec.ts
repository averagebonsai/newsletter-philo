import { test, expect } from '@playwright/test';

test.describe('Visual Layout', () => {
  test('homepage looks good on all devices', async ({ page }, testInfo) => {
    await page.goto('/');
    await page.screenshot({ 
      path: `homepage-${testInfo.project.name}.png`,
      fullPage: true 
    });
    await expect(page.locator('h1')).toContainText('Drawing from the Past');
  });

  test('about page looks good on all devices', async ({ page }, testInfo) => {
    await page.goto('/about');
    await page.screenshot({ 
      path: `about-${testInfo.project.name}.png`,
      fullPage: true 
    });
    await expect(page.locator('h1')).toContainText('Why do this?');
  });

  test('archive page looks good on all devices', async ({ page }, testInfo) => {
    await page.goto('/archive');
    await page.screenshot({ 
      path: `archive-${testInfo.project.name}.png`,
      fullPage: true 
    });
    await expect(page.locator('h1')).toContainText('Article Repository');
  });
});
