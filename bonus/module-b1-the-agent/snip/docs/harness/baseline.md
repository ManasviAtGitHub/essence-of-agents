# Current Baseline (snip)

> Numbers at a glance, so you can tell if something regressed. Update after a material run.
> No commentary -- the why lives in decisions.md / lessons.md.

| Metric | Value |
|--------|-------|
| Code length | 7 chars |
| Alphabet | 57 (base62 minus `0 O 1 l I`) |
| Code space | `57**7 ~ 1.9e12` |
| Collision prob / create @ 1M links | ~`1e-6` |
| Tests | 9 (5 codec + 4 store), ~2s |
| Pipeline | create / resolve / stats via `python -m snip` |
| Store | one JSON file, `runtime/snip.json` |

Last verified: 2026-07-12.
