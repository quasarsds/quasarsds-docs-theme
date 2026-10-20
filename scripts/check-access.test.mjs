import {test} from 'node:test';
import assert from 'node:assert/strict';
import {checkUrl} from './check-access.mjs';

const fake = (status, headers = {}) => async () => new Response(status >= 300 && status < 400 ? null : 'x', {status, headers});

test('redirección al login de Cloudflare Access → protegida', async () => {
  const r = await checkUrl('https://p.example/', {
    fetchImpl: fake(302, {location: 'https://quasarsds.cloudflareaccess.com/cdn-cgi/access/login/p.example'}),
  });
  assert.equal(r.ok, true);
});

test('401/403 → protegida', async () => {
  assert.equal((await checkUrl('https://p.example/', {fetchImpl: fake(403)})).ok, true);
  assert.equal((await checkUrl('https://p.example/', {fetchImpl: fake(401)})).ok, true);
});

test('200 → fallo (contenido expuesto)', async () => {
  assert.equal((await checkUrl('https://p.example/', {fetchImpl: fake(200)})).ok, false);
});

test('redirección a otro sitio → fallo', async () => {
  const r = await checkUrl('https://p.example/', {fetchImpl: fake(302, {location: 'https://evil.cloudflareaccess.com.attacker.io/'})});
  assert.equal(r.ok, false);
  const r2 = await checkUrl('https://p.example/', {fetchImpl: fake(301, {location: '/docs'})});
  assert.equal(r2.ok, false);
});

test('404 o error de red → fallo (no se puede demostrar que está protegida)', async () => {
  assert.equal((await checkUrl('https://p.example/', {fetchImpl: fake(404)})).ok, false);
  const boom = async () => { throw new TypeError('fetch failed', {cause: {code: 'ENOTFOUND'}}); };
  const r = await checkUrl('https://p.example/', {fetchImpl: boom});
  assert.equal(r.ok, false);
  assert.match(r.detail, /ENOTFOUND/);
});
