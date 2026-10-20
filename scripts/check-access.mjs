#!/usr/bin/env node
// Comprueba que un sitio privado NO sirve contenido sin autenticación.
//
// Uso:  node check-access.mjs access-check.json
//
// access-check.json:
//   {
//     "hosts": ["partners.quasarsds.io", "quasarsds-docs-partners.pages.dev", ...],
//     "paths": ["/", "/sitemap.xml", "/404.html"]
//   }
//
// Cada combinación host+ruta se pide sin cookies ni credenciales. Se considera
// protegida si responde:
//   - una redirección al login de Cloudflare Access (*.cloudflareaccess.com), o
//   - 401 / 403.
// Cualquier otra respuesta (200, 404, error de red…) cuenta como fallo: si no
// se puede demostrar que está protegida, no se da por buena.
// Sale con código 1 si alguna URL falla.

import fs from 'node:fs';

const ACCESS_LOGIN_HOST = /(^|\.)cloudflareaccess\.com$/i;
const TIMEOUT_MS = 15000;

export async function checkUrl(url, {fetchImpl = fetch} = {}) {
  let res;
  try {
    res = await fetchImpl(url, {
      redirect: 'manual',
      headers: {'User-Agent': 'quasarsds-access-check'},
      signal: AbortSignal.timeout(TIMEOUT_MS),
    });
  } catch (err) {
    return {url, ok: false, detail: `error de red: ${err.cause?.code ?? err.message}`};
  }
  if (res.status === 401 || res.status === 403) {
    return {url, ok: true, detail: `${res.status}`};
  }
  if (res.status >= 300 && res.status < 400) {
    const location = res.headers.get('location') ?? '';
    let host = '';
    try {
      host = new URL(location, url).hostname;
    } catch {
      // Location inválida → fallo abajo
    }
    if (ACCESS_LOGIN_HOST.test(host)) {
      return {url, ok: true, detail: `${res.status} → login de Cloudflare Access`};
    }
    return {url, ok: false, detail: `${res.status} → ${location || '(sin Location)'} (no es Cloudflare Access)`};
  }
  return {url, ok: false, detail: `${res.status} — ¡sirve contenido sin autenticación!`};
}

export async function checkAll({hosts, paths}, opts) {
  const urls = hosts.flatMap((h) => paths.map((p) => `https://${h}${p}`));
  return Promise.all(urls.map((u) => checkUrl(u, opts)));
}

async function main() {
  const file = process.argv[2];
  if (!file) {
    console.error('Uso: node check-access.mjs access-check.json');
    process.exit(2);
  }
  const config = JSON.parse(fs.readFileSync(file, 'utf8'));
  if (!config.hosts?.length || !config.paths?.length) {
    console.error(`${file}: "hosts" y "paths" no pueden estar vacíos`);
    process.exit(2);
  }
  const results = await checkAll(config);
  for (const r of results) {
    console.log(`${r.ok ? 'OK   ' : 'FALLO'}  ${r.url}  ${r.detail}`);
  }
  const failed = results.filter((r) => !r.ok).length;
  if (failed > 0) {
    console.error(`\n${failed} de ${results.length} URLs NO están protegidas.`);
    process.exit(1);
  }
  console.log(`\nLas ${results.length} URLs están protegidas.`);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  await main();
}
