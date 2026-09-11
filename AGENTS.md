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
- Preserve the plan's continuous expository form: use substantial connected
  paragraphs, keep heading depth normally at section or subsection, and avoid
  fragmenting one argument into microsections or presentation-style bullets.
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
