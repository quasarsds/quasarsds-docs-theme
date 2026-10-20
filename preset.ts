// Tema y configuración común de los sitios de documentación de QuasarSDS.
//
// Lo usan los tres sitios (quasarsds-docs, -partners, -internal), que incluyen
// este repo como submódulo Git en theme/. Este repo es PÚBLICO (Cloudflare Pages
// solo puede clonar submódulos públicos): aquí solo puede haber estilos, marca y
// herramientas — nunca contenido de documentación.
//
// Las dependencias (prism-react-renderer, @docusaurus/theme-mermaid…) se
// resuelven desde el node_modules del sitio que importa este fichero.

import path from 'node:path';
import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const themeDir = __dirname;

/** Directorio estático con logo, favicons e imagen social (se sirve en /img/...). */
export const brandStaticDir = path.join(themeDir, 'brand');

/** Hoja de estilos del tema (paleta, tipografía, navbar, tablas…). */
export const customCss = path.join(themeDir, 'css', 'custom.css');

/** Opciones comunes del sitio. */
export const sharedSiteConfig = {
  favicon: 'img/favicon.svg',
  headTags: [
    {tagName: 'link', attributes: {rel: 'icon', type: 'image/png', sizes: '32x32', href: '/img/favicon-32.png'}},
    {tagName: 'link', attributes: {rel: 'apple-touch-icon', href: '/img/apple-touch-icon.png'}},
  ],
  future: {
    v4: true,
    faster: true,
  },
  trailingSlash: false,
  onBrokenLinks: 'throw',
  markdown: {
    mermaid: true,
    hooks: {
      onBrokenMarkdownLinks: 'throw',
    },
  },
  themes: ['@docusaurus/theme-mermaid'],
} satisfies Partial<Config>;

/** Logo de la barra de navegación. */
export const navbarLogo = {
  alt: 'QuasarSDS',
  src: 'img/logo.svg',
};

/** themeConfig común (cada sitio añade su navbar y footer). */
export const sharedThemeConfig = {
  image: 'img/quasarsds-social-card.jpg',
  colorMode: {
    defaultMode: 'dark',
    respectPrefersColorScheme: true,
  },
  docs: {
    sidebar: {
      hideable: true,
      autoCollapseCategories: true,
    },
  },
  prism: {
    theme: prismThemes.github,
    darkTheme: prismThemes.dracula,
    additionalLanguages: ['bash', 'yaml', 'json'],
  },
  mermaid: {
    theme: {light: 'neutral', dark: 'dark'},
  },
} satisfies Preset.ThemeConfig;
