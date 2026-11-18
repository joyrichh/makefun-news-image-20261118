# 18 November 2026 — World News in One Image

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/joyrichh/makefun-news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/joyrichh/makefun-news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

Make.Fun competition entry ([`news-image-20261118`](https://make.fun/bounty/news-image-20261118)) by [@joyrichh](https://github.com/joyrichh).
A program that writes one image summing up the world's news of Wednesday,
18 November 2026, to `/output/entry.png`.

## The image

A 1024×1024 PNG infographic — "18 November 2026: the day's biggest stories,
in one image" — with six main stories and an "Also today" strip:

1. **Middle East** — U.S. strikes Iran; Tehran hits back at Gulf bases
   (U.S. jets hit a missile site on Qeshm Island; Iran fired drones at U.S.
   bases in Kuwait and Bahrain)
2. **Ukraine** — Crimea Bridge partly collapses after a Ukrainian strike
3. **Diplomacy** — Xi and Putin meet in Shenzhen ahead of a Trump summit
4. **U.S. Politics** — Democrats take the Senate in the Alaska upset
   (Mary Peltola beats Sen. Dan Sullivan, 56–44)
5. **Disaster** — Russian military plane crashes in Siberia; 19 dead
6. **Health** — Ebola outbreak in DR Congo more than doubles
   (11,000+ cases, 5,400 deaths)

Also today: the U.S. loses its measles-free status after 26 years;
Category 5 Cyclone Xavier hits the Northern Cook Islands; a magnitude 6.0
earthquake hits Papua New Guinea.

Every story is real 18 November 2026 news, verified on the day against
Reuters/AP reporting via Just Security's Early Edition, One Turn, Horizon,
and the NPR News Now bulletin. No story is invented. Sources are credited
in the image footer.

## How it works

- `main.ts` (Node 22, standard library only) decodes the bundled
  `entry.png.b64` (the 1024×1024 PNG infographic, stored as base64 text so
  the whole entry stays plain UTF-8) and writes it to `/output/entry.png`.
  No network, no randomness, no timestamps — running it twice writes
  byte-identical output.
- `news.json` holds the verified news data in machine-readable form.
- `build_image.py` is the build-time script that rendered the PNG from
  `news.json` (Pillow + DejaVu fonts on the author's machine); the PNG was
  then encoded with `base64 -w0 entry.png > entry.png.b64`. It is
  documentation of how the image was made; the graded program is `main.ts`.
- `.makefun/owner.json` names the entry wallet for this account.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# out/entry.png — 1024x1024 PNG, 132,275 bytes
```

Determinism check:

```sh
mkdir -p out1 out2
MAKEFUN_OUTPUT_DIR=out1 node main.ts
MAKEFUN_OUTPUT_DIR=out2 node main.ts
sha256sum out1/entry.png out2/entry.png   # identical hashes
```

## License

MIT — see `LICENSE`.
