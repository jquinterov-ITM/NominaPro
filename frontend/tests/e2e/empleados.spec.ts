import { test, expect } from '@playwright/test';

test.describe('Empleados', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[type="text"]', 'admin');
    await page.fill('input[type="password"]', 'secret');
    await page.click('button');
    await page.waitForURL('http://localhost:5173/');
  });

  test('crear empleado con datos válidos', async ({ page }) => {
    await page.click('text=Empleados');
    await page.click('text=Agregar Empleado');

    const doc = `TEST-${Date.now()}`;
    await page.fill('input[placeholder="Nombre"]', 'Test Employee');
    await page.fill('input[placeholder="Documento"]', doc);
    await page.fill('input[placeholder="Salario"]', '2000000');
    await page.click('button:has-text("Guardar")');

    await expect(page.locator(`text=${doc}`)).toBeVisible({ timeout: 5000 });
  });

  test('crear empleado con salario inferior al SMMLV', async ({ page }) => {
    await page.click('text=Empleados');
    await page.click('text=Agregar Empleado');

    const doc = `TEST-${Date.now()}`;
    await page.fill('input[placeholder="Nombre"]', 'Test Employee');
    await page.fill('input[placeholder="Documento"]', doc);
    await page.fill('input[placeholder="Salario"]', '1000000');
    await page.click('button:has-text("Guardar")');

    await expect(page.locator('text=SMMLV')).toBeVisible({ timeout: 5000 });
  });

  test('listar empleados', async ({ page }) => {
    await page.click('text=Empleados');
    await expect(page.locator('text=Lista de Empleados')).toBeVisible();
  });
});
