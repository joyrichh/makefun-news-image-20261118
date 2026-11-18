// 18 November 2026 — World News in One Image (Node 22, standard library only).
// The infographic is baked into the repository as base64 text (entry.png.b64:
// a 1024x1024 PNG rendered at authoring time from the verified 18 Nov 2026
// news in news.json — see build_image.py). This program decodes it and writes
// it to /output/entry.png. No network, no randomness, no timestamps: every
// run writes identical bytes. (Base64 keeps the whole entry plain UTF-8 text.)
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const png = Buffer.from(
  readFileSync(new URL('./entry.png.b64', import.meta.url), 'utf8').trim(),
  'base64',
);
if (png.subarray(0, 8).toString('hex') !== '89504e470d0a1a0a') {
  throw new Error('entry.png.b64 did not decode to a PNG');
}
writeFileSync(join(outDir, 'entry.png'), png);
