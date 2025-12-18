import { test, expect } from '@playwright/test';

test.describe('dom management smoke', () => {
  test('renders home and redirects protected routes', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByRole('heading', { name: 'Dom Management Portal' })).toBeVisible();

    await page.goto('/tenant/dashboard');
    await expect(page).toHaveURL(/login/);
  });

  test('login page shows form', async ({ page }) => {
    await page.goto('/login');
    await expect(page.getByLabel('Email')).toBeVisible();
    await expect(page.getByLabel('Password')).toBeVisible();
  });
});
