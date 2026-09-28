'use strict';
// Generators for the three "live" SVGs the GitHub Action regenerates daily.
// Shared between the one-off local build and .github/scripts/generate-status.js
// so what gets visually verified here is exactly what ships.
const { THEMES, esc, svgDoc, monoWidth } = require('./lib');

const STATUS_SYMBOL = { good: '●', minor: '◐', planned: '○' };

function generateBoard(theme, data) {
  const c = THEMES[theme];
  const W = 1200, H = 300;
  const lineColor = { web: c.web, ai: c.ai, d3: c.d3 };
  let body = `<rect width="${W}" height="${H}" fill="${c.paper}"/>`;
  body += `<rect x="20" y="20" width="${W - 40}" height="${H - 40}" fill="none" stroke="${c.ink}" stroke-width="2"/>`;

  body += `<text x="40" y="52" class="disp" font-size="26" font-weight="800" fill="${c.ink}">${esc(data.name)}</text>`;
  body += `<text x="${W - 40}" y="48" text-anchor="end" font-size="13" fill="${c.muted}">◎ INDEX CTRL</text>`;
  body += `<text x="40" y="72" font-size="12" fill="${c.muted}">${esc(data.role)}</text>`;
  body += `<text x="${W - 40}" y="68" text-anchor="end" font-size="12" fill="${c.muted}">${esc(data.location)}</text>`;
  body += `<line x1="40" y1="86" x2="${W - 40}" y2="86" stroke="${c.ink}" stroke-width="1.5"/>`;

  body += `<text x="50" y="110" font-size="13" font-weight="700" fill="${c.ink}">TIME</text>`;
  body += `<text x="120" y="110" font-size="13" font-weight="700" fill="${c.ink}">DESTINATION</text>`;
  body += `<text x="800" y="110" font-size="13" font-weight="700" fill="${c.ink}">LINE</text>`;
  body += `<text x="950" y="110" font-size="13" font-weight="700" fill="${c.ink}">STATUS</text>`;
  body += `<line x1="50" y1="120" x2="${W - 50}" y2="120" stroke="${c.muted}" stroke-width="1" stroke-dasharray="2,3"/>`;

  const rows = data.rows; // [{time,dest,lines,status}]
  rows.forEach((r, i) => {
    const y = 148 + i * 35;
    body += `<text x="50" y="${y}" font-size="13" font-weight="700" fill="${c.ink}">${esc(r.time)}</text>`;
    body += `<text x="120" y="${y}" font-size="13" fill="${c.ink}">${esc(r.dest)}</text>`;
    let lx = 800;
    r.lines.forEach((ln) => {
      body += `<rect x="${lx}" y="${y - 10}" width="14" height="14" fill="${lineColor[ln]}"/>`;
      lx += 14 + 6 + 26;
    });
    body += `<text x="950" y="${y}" font-size="13" font-weight="600" fill="${c.ink}">${esc(r.status)}</text>`;
  });

  body += `<text x="40" y="${H - 28}" font-size="11" fill="${c.muted}">Updated ${esc(data.updated)}</text>`;
  return svgDoc(W, H, body);
}

function generateStatus(theme, data) {
  const c = THEMES[theme];
  const W = 1200, H = 180;
  const lineColor = { web: c.web, ai: c.ai, d3: c.d3 };
  const statusColor = { good: c.green, minor: c.amberText, planned: c.muted };
  let body = `<rect width="${W}" height="${H}" fill="${c.paper}"/>`;

  data.lines.forEach((line, i) => {
    const y = 44 + i * 42;
    body += `<rect x="20" y="${y - 15}" width="14" height="14" fill="${lineColor[line.key]}"/>`;
    body += `<text x="44" y="${y - 3}" font-size="15" font-weight="700" fill="${c.ink}">${esc(line.label)}</text>`;
    body += `<text x="200" y="${y - 2}" font-size="18" fill="${statusColor[line.status]}">${STATUS_SYMBOL[line.status]}</text>`;
    body += `<text x="222" y="${y - 3}" font-size="13" font-weight="600" fill="${c.ink}">${esc(line.label2)}</text>`;
    body += `<text x="420" y="${y - 3}" font-size="12" fill="${c.muted}">${esc(line.note)}</text>`;
  });

  return svgDoc(W, H, body);
}

function generateCommuter(theme, data) {
  const c = THEMES[theme];
  const W = 1200, H = 200;
  const lineColor = { web: c.web, ai: c.ai, d3: c.d3 };
  let body = `<rect width="${W}" height="${H}" fill="${c.paper}"/>`;

  const left = 50, right = W - 50, trackY = 100;
  body += `<line x1="${left}" y1="${trackY - 3}" x2="${right}" y2="${trackY - 3}" stroke="${c.ink}" stroke-width="2"/>`;
  body += `<line x1="${left}" y1="${trackY + 3}" x2="${right}" y2="${trackY + 3}" stroke="${c.ink}" stroke-width="2"/>`;

  const weeks = data.weeks; // array of {count} length 52, count 0..4 relative intensity
  const n = weeks.length;
  const span = right - left;
  const step = span / n;
  const maxCount = Math.max(1, ...weeks.map((w) => w.count));
  weeks.forEach((w, i) => {
    const x = left + i * step + step / 2;
    const intensity = w.count / maxCount; // 0..1
    const hgt = 5 + intensity * 9;
    const op = 0.35 + intensity * 0.65;
    body += `<rect x="${x - 1.5}" y="${trackY - hgt / 2}" width="3" height="${hgt.toFixed(1)}" fill="${c.ink}" opacity="${op.toFixed(2)}"/>`;
  });

  // Release markers (stations)
  (data.releases || []).forEach((rel) => {
    const x = left + rel.weekIndex * step + step / 2;
    const color = lineColor[rel.line] || c.ink;
    body += `<circle cx="${x}" cy="${trackY}" r="7" fill="${color}" stroke="${c.paper}" stroke-width="2"/>`;
    body += `<text x="${x}" y="${trackY - 20}" text-anchor="middle" font-size="10" font-weight="700" fill="${c.ink}">${esc(rel.label)}</text>`;
  });

  // Train parked at "today"
  const trainX = right - 6;
  body += `<g>
<rect x="${trainX - 42}" y="${trackY - 12}" width="12" height="18" fill="${c.web}" stroke="${c.ink}" stroke-width="1" rx="2"/>
<rect x="${trainX - 28}" y="${trackY - 12}" width="12" height="18" fill="${c.ai}" stroke="${c.ink}" stroke-width="1" rx="2"/>
<rect x="${trainX - 14}" y="${trackY - 12}" width="12" height="18" fill="${c.d3}" stroke="${c.ink}" stroke-width="1" rx="2"/>
</g>`;
  body += `<circle cx="${right}" cy="${trackY}" r="6" fill="${c.ink}"/>`;
  body += `<text x="${right}" y="${trackY - 22}" text-anchor="end" font-size="11" font-weight="700" fill="${c.ink}">TODAY</text>`;

  // Month labels
  (data.months || []).forEach((m) => {
    const x = left + m.weekIndex * step;
    body += `<text x="${x}" y="${H - 24}" font-size="11" fill="${c.muted}">${esc(m.label)}</text>`;
  });

  return svgDoc(W, H, body);
}

module.exports = { generateBoard, generateStatus, generateCommuter };
