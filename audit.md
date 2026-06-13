# Audit

Dated log of editorial passes and verification runs. Newest first.

## 2026-06-13 — voice reform

Voice-reform editing pass to remove AI-writing tells (house voice.md).

Lexical density: before — carries/carry 16, load-bearing 4, exactly 1, precisely 1, discipline 1; tricolon proxy 65. After — carries/carry 13, load-bearing 1, exactly 1, precisely 1, discipline 1; tricolon proxy 65.

Changes:
- Thinned "load-bearing" from 4 to 1. Kept the genuine technical use in §3 (knowledge retention is the load-bearing dimension; remove it and the regime collapses). Varied the others: intro "most consistently identifies as decisive"; §4 "the dominant contestation at each kind of interface"; §4 worked-example "the distinction is consequential".
- Fixed inline-contrastive in the abstract ("facts about the model's geometry, not estimates of historical frequency" -> "describe the model's geometry rather than historical frequency").
- Thinned abstract repetitions of "carries" in §8 closing ("carries no judgement / carries the structural fact" -> "passes no judgement / records the structural fact") and §7 ("carries content" -> "is itself a substantive assumption"). Remaining carries/carry uses are literal sheaf-theoretic (stalks carry configurations, edges carry requirements).
- No structure advisory printed; headings already substantive. No numbers, citations, math, or tables touched.

Verify: voice 0 errors (1 remaining warn is the kept technical "load-bearing dimension"); refs 30 in-text keys unchanged, 0 missing, 1 unused (McAnany 2010, pre-existing); claims no-match values pre-existing (percentages and corner constants, untouched); build clean; check => PASS.

## 2026-05-29 — upgrade pass (Group B)

Baseline: voice 0 errors, refs 0 missing, claims clean, 20 pages.

Scope contract:
1. β-robustness: the §3 claim that the basin geometry is robust for β∈[5,20] was
   asserted, not shown. Add a `beta_robustness` computation to the simulation
   (basin volumes at β=5,12,20) and cite the real numbers in §3.
2. State basin-volumes-are-geometry-not-frequency in the abstract (already in §5;
   make the abstract not misreadable as a frequency claim).
3. Label the three propositions as what the model entails, not discoveries
   (one-line lead at §6).
4. Voice tightenings: §2.1 "The decision to model society this way carries
   weight" throat-clear; §5 "is exercised"; §7 opening throat-clear. Keep §7's
   six limits — each is a distinct, load-bearing scope statement that earns its place.

Next-pass candidates (logged): calibrate fitness functions against a corpus of
post-collapse trajectories; continuous-stalk extension.
