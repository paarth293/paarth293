// Shared theme tokens + helpers for the transit-design SVG generator.
'use strict';

const THEMES = {
  light: {
    paper: '#F3F1EA',
    ink: '#161614',
    web: '#2438E8',
    ai: '#E0283F',
    d3: '#F5A300',
    muted: '#8A877E',
    mutedFill: '#E5E2D8',
    green: '#1F8A4C',
    amberText: '#9C6500', // darker amber for AA text contrast on paper
  },
  dark: {
    paper: '#0F0F0D',
    ink: '#EDEBE4',
    web: '#5B6CFF',
    ai: '#FF4D63',
    d3: '#FFB627',
    muted: '#8A8680',
    mutedFill: '#232320',
    green: '#35C173',
    amberText: '#FFB627',
  },
};

// Font stacks that resolve locally in any renderer (GitHub blocks external
// font loading inside <img>-embedded SVGs, so we never @import webfonts).
const FONT_DISPLAY =
  "'Bricolage Grotesque','Segoe UI',system-ui,-apple-system,sans-serif";
const FONT_MONO =
  "ui-monospace,'Cascadia Mono','Segoe UI Mono','SF Mono',Consolas,'DejaVu Sans Mono',monospace";

// Rough monospace advance width per character at a given px size.
// (Monospace glyphs are ~0.6em wide in most system mono faces.)
function monoWidth(str, size) {
  return Math.round(String(str).length * size * 0.6);
}

function esc(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

// Wraps a finished set of <defs>+body elements into a full SVG document.
function svgDoc(width, height, body, extraDefs = '') {
  return `<svg viewBox="0 0 ${width} ${height}" width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg" role="img">
<defs>
<style>
  text { font-family: ${FONT_MONO}; }
  .disp { font-family: ${FONT_DISPLAY}; }
  @media (prefers-reduced-motion: reduce) {
    .anim { animation: none !important; }
  }
</style>
${extraDefs}
</defs>
${body}
</svg>`;
}

module.exports = { THEMES, FONT_DISPLAY, FONT_MONO, monoWidth, esc, svgDoc };
