import { test, expect } from '@playwright/test';

test.describe('Autenticación', () => {
  test('login exitoso con credenciales válidas', async ({ page }) => {
    await page.goto('/login');

    await page.fill('input[type="text"]', 'admin');
    await page.fill('input[type="password"]', 'secret');
    await page.click('button');

    await expect(page).toHaveURL('http://localhost:5173/', { timeout: 10000 });
    await expect(page.locator('text=Logout')).toBeVisible({ timeout: 5000 });
  });

  test('login rechazado con credenciales inválidas', async ({ page }) => {
    await page.goto('/login');

    await page.fill('input[type="text"]', 'admin');
    await page.fill('input[type="password"]', 'wrongpassword');
    await page.click('button');

    await expect(page.locator('text=401')).toBeVisible({ timeout: 5000 });
  });

  test('redirección a login sin autenticación', async ({ page }) => {
    await page.goto('/empleados');
    await expect(page).toHaveURL(/\/login/);
  });
});
