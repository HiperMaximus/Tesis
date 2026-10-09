# Repository Instructions

Read `GOAL.md` and `CURRENT.md` before editing.
Read `docs/thesis_structure.md` before changing chapter order or scope.

## Documents

- `plan/` is the approved Tesis I plan. Do not change its academic content.
- `thesis/` is the active Tesis II document and may reuse material from the
  plan.
- Reuse as much approved plan prose as remains accurate. New writing must
  preserve its Spanish expository voice and terminology, while correcting
  grammar, technical imprecision, obsolete proposal tense and unsupported
  claims. Prefer revising an existing passage over replacing it from scratch.
- Introduce each technical term at its first Spanish-language mention with
  its Spanish name followed by the English name in parentheses. Thereafter,
  choose one name, Spanish or English according to established usage in the
  relevant literature, and use it consistently in prose, captions, tables,
  and diagrams. Do not alternate translations for the same concept or repeat
  the bilingual introduction throughout the document. Preserve original titles
  in bibliographic entries. For this review, introduce "convoluciones
  direccionables (steerable convolutions)" and then use "convoluciones
  steerable", applying the same naming choice to kernels, filters, and CNNs.
  The Spanish Resumen counts as the first mention: VAE and steerable
  convolutions are already introduced there; do not redefine them in
  Introduction. Use "kernel"/"kernels" in the subsequent prose, introducing
  "núcleo (kernel)" at its first mention when the deferred terminology review
  is performed. Say "equivariante al grupo ..." when naming the group.
- Preserve the plan's continuous expository form: use substantial connected
  paragraphs, keep heading depth normally at section or subsection, and avoid
  fragmenting one argument into microsections or presentation-style bullets.
- Use neutral, direct wording for experimental scope and limitations. Prefer
  "Limitaciones del estudio" to "Amenazas a la validez" and explain concrete
  constraints without alarmist language or repeated admonitions. Preserve
  scientific qualifications and technical terms. Common English technical
  terms may remain after their first introduction with the Spanish name.
- Before a new editorial pass, show representative before/after examples and
  wait for the user's approval of that scope. Continue approved changes without
  requesting the same approval again.
- Both document roots must compile independently; never reference files through
  `../` from LaTeX.
- Keep generated files under `build/`. Only final PDFs under `artifacts/` are
  tracked.

## Scientific sources

- Experiment truth lives in the sibling `equivariant-vae` repository. Copy only
  accepted figures, tables and claims, and record their source commit/path.
- The equivariant target is continuous `SO(2)`, not a discrete rotation group.
- Patch experiments represent WSI segmentation at patch-grid resolution. The
  evaluation is not exhaustive because dense WSI labels were unavailable.
- Do not claim general superiority when the accepted evidence supports only a
  mixed or descriptive result.

## Workflow

- Use incremental `./scripts/document.sh build thesis` while editing and
  `./scripts/document.sh check thesis` before handoff.
- Use `draft` for image-heavy prose work and `includeonly.local.tex` for a
  focused chapter build. Never update a final artifact from a focused build.
- Preserve LaTeX build state. Run `clean` only to recover from a confirmed
  cache-related problem.
- Use `./scripts/document.sh grammar thesis` for offline language review when
  the repo-local LTeX+ CLI is installed.
- Inspect rendered pages after material layout changes.
- Keep `CURRENT.md` compact and current before handing work off.
- Do not push, create tags, or synchronize Overleaf without explicit user
  permission. Overleaf must receive only the intended document subtree.
