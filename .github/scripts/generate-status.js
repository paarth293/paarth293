#!/usr/bin/env node
'use strict';
/**
 * Regenerates the three "live" SVGs (departure board, service status,
 * commuter line) from real GitHub data, then writes them into ../../assets/.
 *
 * Runs inside GitHub Actions (see .github/workflows/service.yml) with the
 * built-in GITHUB_TOKEN. Requires nothing beyond Node 20+'s native fetch
 * -- no npm install step, no axios, no external font loading (GitHub
 * strips @import'd webfonts from SVGs shown via <img>, so gen-live.js /
 * lib.js only ever use system font stacks).
 *
 * If the GitHub API is unreachable or a query fails, every step falls
 * back to a sane default so the Action never breaks the profile page --
 * it just skips updating that one section until the next run.
 */
const fs = require('fs');
const path = require('path');
const { generateBoard, generateStatus, generateCommuter } = require('./gen-live');

const TOKEN = process.env.GITHUB_TOKEN;
const OWNER = process.env.GITHUB_OWNER || 'paarth293';
const OUT_DIR = path.join(__dirname, '..', '..', 'assets');

// ---- Edit this map when you add/rename/retire a station -------------------
// key = repo name (as it appears in the URL github.com/OWNER/<repo>)
const REPOS = {
  'the-index': { lines: ['web', 'ai', 'd3'], label: 'Index Central' },
  promptforge: { lines: ['web', 'ai'], label: 'PromptForge' },
  drishti: { lines: ['web', 'ai'], label: 'Drishti' },
  truememory: { lines: ['ai'], label: 'TrueMemory' },
  verivolunte: { lines: ['web'], label: 'VeriVolunte' },
  'blur-robustness': { lines: ['ai'], label: 'Blur Robustness' },
};

async function gql(query, variables) {
  if (!TOKEN) throw new Error('GITHUB_TOKEN not set');
  const res = await fetch('https://api.github.com/graphql', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${TOKEN}`,
      'Content-Type': 'application/json',
      'User-Agent': 'transit-profile-bot',
    },
    body: JSON.stringify({ query, variables }),
  });
  const json = await res.json();
  if (json.errors) throw new Error(JSON.stringify(json.errors));
  return json.data;
}

async function fetchRepoData(owner, repo) {
  const query = `
    query($owner: String!, $repo: String!) {
      repository(owner: $owner, name: $repo) {
        defaultBranchRef { target { ... on Commit { committedDate } } }
        releases(first: 3, orderBy: { field: CREATED_AT, direction: DESC }) {
          nodes { name tagName createdAt }
        }
        milestones(states: OPEN, first: 3, orderBy: { field: UPDATED_AT, direction: DESC }) {
          nodes { title }
        }
      }
    }`;
  const data = await gql(query, { owner, repo });
  const r = data.repository;
  if (!r) return null;
  return {
    lastPush: r.defaultBranchRef?.target?.committedDate || null,
    releases: r.releases.nodes || [],
    milestone: r.milestones.nodes[0]?.title || null,
  };
}

async function fetchContributionWeeks(login) {
  const to = new Date();
  const from = new Date(to.getTime() - 52 * 7 * 24 * 60 * 60 * 1000);
  const query = `
    query($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) {
        contributionsCollection(from: $from, to: $to) {
          contributionCalendar {
            weeks { contributionDays { contributionCount } }
          }
        }
      }
    }`;
  const data = await gql(query, { login, from: from.toISOString(), to: to.toISOString() });
  const weeks = data.user.contributionsCollection.contributionCalendar.weeks;
  return weeks.map((w) => ({
    count: w.contributionDays.reduce((sum, d) => sum + d.contributionCount, 0),
  }));
}

function daysAgo(iso) {
  if (!iso) return Infinity;
  return Math.floor((Date.now() - new Date(iso).getTime()) / 86400000);
}

function statusFor(days) {
  if (days <= 3) return 'good';
  if (days <= 14) return 'minor';
  return 'planned';
}

const STATUS_LABEL = { good: 'GOOD SERVICE', minor: 'MINOR DELAYS', planned: 'PLANNED WORKS' };
const DEFAULT_NOTE = {
  web: 'Shipping at Language Metrics',
  ai: 'Agent systems in progress',
  d3: 'First station opening soon',
};

async function buildStatusData() {
  const perRepo = {};
  for (const repo of Object.keys(REPOS)) {
    try {
      perRepo[repo] = await fetchRepoData(OWNER, repo);
    } catch (e) {
      console.warn(`⚠ could not fetch ${repo}: ${e.message}`);
      perRepo[repo] = null;
    }
  }

  const lines = ['web', 'ai', 'd3'].map((key) => {
    const reposOnLine = Object.entries(REPOS).filter(([, v]) => v.lines.includes(key));
    let bestDays = Infinity;
    let milestoneNote = null;
    for (const [repo] of reposOnLine) {
      const d = perRepo[repo];
      if (!d) continue;
      bestDays = Math.min(bestDays, daysAgo(d.lastPush));
      if (!milestoneNote && d.milestone) milestoneNote = `${REPOS[repo].label}: ${d.milestone}`;
    }
    const status = statusFor(bestDays);
    return {
      key,
      label: `${key === 'd3' ? '3D' : key.toUpperCase()} LINE`,
      label2: STATUS_LABEL[status],
      status,
      note: milestoneNote || DEFAULT_NOTE[key],
    };
  });

  // Collect releases across all tracked repos for the commuter line.
  const allReleases = [];
  for (const [repo, meta] of Object.entries(REPOS)) {
    const d = perRepo[repo];
    if (!d) continue;
    for (const rel of d.releases) {
      allReleases.push({ date: rel.createdAt, label: rel.tagName || rel.name, line: meta.lines[0] });
    }
  }

  return { lines, allReleases, perRepo };
}

function releasesToWeekIndices(allReleases, weekCount) {
  const now = Date.now();
  return allReleases
    .map((r) => {
      const ageDays = (now - new Date(r.date).getTime()) / 86400000;
      const weekIndex = Math.round(weekCount - ageDays / 7);
      return { ...r, weekIndex };
    })
    .filter((r) => r.weekIndex >= 0 && r.weekIndex < weekCount)
    .slice(0, 6); // keep the board readable
}

function monthLabels(weekCount) {
  const labels = [];
  const now = new Date();
  for (let i = 0; i <= 4; i++) {
    const weekIndex = Math.round((i * weekCount) / 4);
    const d = new Date(now.getTime() - (weekCount - weekIndex) * 7 * 86400000);
    labels.push({ weekIndex, label: d.toLocaleString('en-US', { month: 'short' }).toUpperCase() });
  }
  return labels;
}

async function main() {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const write = (name, svg) => {
    const p = path.join(OUT_DIR, name);
    fs.writeFileSync(p, svg, 'utf8');
    console.log('wrote', name);
  };

  // ---- Service status (real per-line data, falls back to defaults) ----
  let statusData;
  try {
    statusData = await buildStatusData();
  } catch (e) {
    console.warn('⚠ status build failed, using fallback:', e.message);
    statusData = {
      lines: ['web', 'ai', 'd3'].map((key) => ({
        key,
        label: `${key === 'd3' ? '3D' : key.toUpperCase()} LINE`,
        label2: 'STATUS UNKNOWN',
        status: 'planned',
        note: DEFAULT_NOTE[key],
      })),
      allReleases: [],
    };
  }

  // ---- Commuter line (real contribution weeks, falls back to flat track) ----
  let weeks;
  try {
    weeks = await fetchContributionWeeks(OWNER);
  } catch (e) {
    console.warn('⚠ contribution fetch failed, using flat fallback:', e.message);
    weeks = Array.from({ length: 52 }, () => ({ count: 0 }));
  }
  const releaseMarks = releasesToWeekIndices(statusData.allReleases || [], weeks.length);
  const commuterData = { weeks, releases: releaseMarks, months: monthLabels(weeks.length) };

  // ---- Departure board (static shape + live "updated" timestamp) ----
  const boardData = {
    name: 'PAARTH GUPTA',
    role: 'FULL-STACK ENGINEER · AI & AGENTIC SYSTEMS',
    location: 'GHAZIABAD',
    rows: [
      { time: 'NOW', dest: 'LANGUAGE METRICS — FULL STACK', lines: ['web'], status: 'RUNNING' },
      { time: 'NEXT', dest: 'SDE / FULL-STACK INTERNSHIPS', lines: ['web', 'ai'], status: 'BOARDING' },
      { time: '2028', dest: 'B.TECH CSE · KIET', lines: ['web'], status: 'ON TIME' },
    ],
    updated:
      new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata', dateStyle: 'medium', timeStyle: 'short' }) +
      ' IST',
  };

  for (const theme of ['light', 'dark']) {
    write(`board-${theme}.svg`, generateBoard(theme, boardData));
    write(`status-${theme}.svg`, generateStatus(theme, statusData));
    write(`commuter-${theme}.svg`, generateCommuter(theme, commuterData));
  }

  console.log('✅ done');
}

main().catch((e) => {
  console.error('❌ generate-status.js failed:', e);
  process.exit(1);
});
