# quasarsds-docs-theme

Tema común de los sitios de documentación de QuasarSDS. Lo usan como submódulo Git (en `theme/`):

| Sitio | Repo |
|---|---|
| `docs.quasarsds.io` (público) | `quasarsds-docs` |
| `partners.quasarsds.io` (Cloudflare Access) | `quasarsds-docs-partners` |
| `internal.quasarsds.io` (Cloudflare Access) | `quasarsds-docs-internal` |

> **Este repo es público** porque Cloudflare Pages solo puede clonar submódulos públicos. Aquí solo puede haber estilos, marca y herramientas: **nunca contenido de documentación**.

## Contenido

| Qué | Dónde |
|---|---|
| Configuración común de Docusaurus (favicon, Mermaid, colores de código, modo oscuro, logo de la barra) | `preset.ts` |
| Estilos del tema (paleta del logo, tipografía, navbar, tablas) | `css/custom.css` |
| Logo, favicons, imagen social (se sirven en `/img/…`) | `brand/img/` |
| Comprobación de que un sitio privado no sirve contenido sin login | `scripts/check-access.mjs` |
| Scripts que generan el logo y el favicon | `design/logo/` |

## Uso desde un sitio

```ts
// docusaurus.config.ts
import {brandStaticDir, customCss, navbarLogo, sharedSiteConfig, sharedThemeConfig} from './theme/preset';

const config = {
  ...sharedSiteConfig,
  staticDirectories: ['static', brandStaticDir],
  // presets → classic → theme: {customCss}
  themeConfig: {...sharedThemeConfig, navbar: {logo: navbarLogo /* … */}},
};
```

Las dependencias (`prism-react-renderer`, `@docusaurus/theme-mermaid`…) se resuelven desde el `node_modules` del sitio.

Los cambios llegan a cada sitio cuando actualiza su submódulo:

```bash
git submodule update --remote theme
git add theme && git commit -m "Actualizar tema"
```

## Logo

`brand/img/logo.svg` y `favicon.svg` se generan con `python3 design/logo/logo.py salida.svg` y `python3 design/logo/favicon.py salida.svg`. El favicon es una versión simplificada para que se lea a 16 px. La imagen social es `design/logo/social-card.svg` rasterizada a JPG.

## Tests

```bash
npm test
```
