# The World — Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/laoanbest-coder/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/laoanbest-coder/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A one-page newspaper front page summing up 23 November 2026's world
news in a single 1024×1024 image: 35 stories (13 main + 22 also)
across 6 regions.

## What's on the page

- **Leads:** Nvidia reinstates Jensen Huang and stocks soar
  (shares +31%, +$952bn in a day); Ukraine sinks a Russian warship
  in Benghazi port; COP31 ends with no deal — the first climate
  talks to fail since Copenhagen 2009.
- **Features:** BepiColombo reaches Mercury orbit despite a
  glitched burn (77% of the planned push); Trump on Iran and the
  Bahrain attack; the Kryvyi Rih toll; NATO meets on the Poland
  airspace breach; Russia's reported nuclear-satellite plan; the SEC
  probe of Nvidia; Asian chip stocks sliding; the Democrats'
  biggest House majority in 30 years; Hasina's fate in Bangladesh;
  and Seoul's cabinet shuffle.
- **Also on Monday:** 22 one-liners, from Gaza and the West Bank
  to the Las Vegas Grand Prix and a $450m Mets deal for Skubal.
  A small world map dots the 13 main stories at their locations
  and counts the stories per region: Americas 15, Europe 8,
  Asia 5, Africa 3, Middle East 3, Space 1.
- **Date check:** a box that separates what actually happened
  earlier (COP31 closing Sunday, the BepiColombo burn Saturday,
  Friday's market rout) from what was confirmed on Monday itself,
  so no story is misdated.

## How it was made

The page is drawn by `compose_v1.py` (Pillow) from the story list
in that file and thirteen small illustrations in `art/`, each stored
as base64. Running the script writes `entry.png` and a base64 copy
`entry.png.b64`. The entrypoint `main.py` decodes the bundled
base64 image and writes it to `/output/entry.png`; it uses only the
Python standard library, needs no network, and produces identical
bytes on every run.

All figures were checked against reporting published on 23 November
2026. See `METHOD.md` for the sourcing and verification notes.
