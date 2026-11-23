# METHOD — Monday 23 November 2026 world news front page

## Research

Researched on 23 Nov 2026 (Chicago, ~16:35–17:00 CST) from web search
across several independent sources per story: Just Security's Early
Edition (AP, Reuters, BBC, NYT, WSJ), Algenom's daily briefing
(Al Jazeera, Reuters, Euronews/AFP), ESA (BepiColombo), CNN, Reuters
Trading Day, MarketWatch, Investopedia, and Formula 1 / AP for sport.
Every figure on the page was checked against at least two independent
sources unless marked SINGLE in `v1-plan.md` (the build notes in the
parent directory). Where sources conflicted, the conservative figure
was printed: Nvidia +31% (CNN +31.48% / +$952bn; Investopedia +31%);
S&P +4.7% close (CNN +4.73%; intraday prints of +5% not used).

## Date discipline

The contest covers events that happened, or were first reported, on
23 November 2026. Weekend events are included only with their real
day, in the DATE CHECK box and in the decks ("closed Sun", "burn Sat
18:24 UTC", "strikes overnight Sat", "attack Sat", "GP Sat"). Nothing
from the Nov 20, Nov 21 or Nov 22 entries was reused — no image, no
art asset, no figure: every number was re-checked for 23 Nov.

Key date traps handled:
- COP31 ended Sunday 22 Nov (two days late), reported Monday.
- BepiColombo's burn was Sat 21 Nov 18:24 UTC; the burn was cut
  short by a software glitch (77% of planned velocity change) and
  ESA's confirmation came Sun/Mon — printed as such, not as a
  clean arrival.
- The Las Vegas GP was raced Saturday; the Friday market rout
  (S&P −3.7%) is Friday's news, Monday is the +4.7% rebound.
- El Chapo Isidro (captured Fri night, announced Sat) was already
  covered in the Nov 21 entry and is not repeated here.

## Layout

1024×1024 newspaper front page, same proven geometry as the Nov 21
entry: masthead, 6-stat strip, 3 lead cards, 10 feature tiles, navy
map panel with 13 numbered dots, ALSO list of 22 one-liners, DATE
CHECK box, sources footer. All 35 stories (13 main + 22 ALSO) across
6 regions: Europe 8, Americas 15, Asia 5, Africa 3, Middle East 3,
Space 1.

## Illustrations

The 13 card illustrations are fresh editorial images generated for
23 Nov only (see the parent directory's `art_raw/`); none carries
any text. Every word and number on the page is drawn in code with
Liberation / Noto Serif Condensed fonts, so the text stays
pixel-exact. The page was rendered with Pillow and visually checked:
0 layout warnings (no headline, deck, stat label, ALSO item or
DATE CHECK block overflows its box).

## Verification

- `python3 compose_v1.py` → `entry.png`, 1024×1024, 473,104 bytes
  (< 1 MiB), 0 warnings.
- `python3 main.py` run twice → byte-identical `/output/entry.png`
  (determinism check).
- Kit check: `node cli/makefun.mjs check --kit . --repo <repo>`
  (see STATUS.md in the parent directory for the full output).
