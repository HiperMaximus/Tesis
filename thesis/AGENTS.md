# Thesis Instructions

This is the active Tesis II document.

- Reuse plan material when it remains accurate, but revise proposal/future tense
  to describe the work actually performed.
- Results and claims must be traceable to accepted outputs in
  `../../equivariant-vae`.
- Describe patch experiments as WSI segmentation at patch-grid resolution and
  explicitly state that evaluation is non-exhaustive because dense labels were
  unavailable.
- Describe the equivariant model as continuous `SO(2)`.
- Preserve mixed findings and limitations; do not turn favorable point estimates
  into significance or general superiority claims.
- Put final experiment figures in `figures/experiments/` and record provenance
  in `figures/manifest.yml`.
- Edit chapter prose in `chapters/`. Use the ignored `includeonly.local.tex`
  only for focused builds and remove it before final validation.
- Run `../scripts/document.sh check thesis` and render the PDF after substantive
  edits.
