# Current Status

Last updated: 2026-10-01

## Temporal-coherence audit and approved edits: completed

Read all thesis chapters, frontmatter and architecture figure sources, with
two independent subagents and comparison to inherited plan passages. No
completed work remains described as pending. Applied four user-approved tense
harmonizations after reading their full contexts: the executed comparison now
uses "incluyó", while three generic explanations use the present. Preserved
"este trabajo compara" and "este trabajo estudia" at the user's request.
Genuine future extensions, objective infinitives and theoretical conditionals
remain valid. Final PDF: 109 pages; build, document check and whitespace check
pass, with no unresolved references or overfull boxes. Reviewed all four
affected PDF pages. Proposals, logs and renders are under
`build/thesis/temporal-audit/`. The user authorized committing and pushing this
approved revision to `origin/main`.

## Bibliography corrections: completed

Applied the user's approved bibliography proposals: corrected NCI years and
author names, normalized journal and proceedings metadata, completed three
conference entries, protected proper names, and explicitly identified five
arXiv preprints. All 33 publication DOI links are present in the final PDF;
all 70 entries have source URLs. Software references retain consultation dates
without presenting them as publication years. Corrected the Elesedy/Zaidi
comparison and Graham's similar parameter budgets in the two cited passages.

Final PDF remains 109 pages. `document.sh check thesis` and `git diff --check`
pass; no missing, unused or duplicate references, unresolved citations or
overfull boxes. Reviewed all eight bibliography pages and four changed or
adjacent body pages. Audit, source evidence, link checks and rendered QA are
under `build/thesis/bibliography-audit/`. The user authorized commit and push
to `origin/main`; no Overleaf synchronization was requested.

## PDF annotation and approved editorial passes: completed

Applied the approved 37-comment pass and the subsequent 35-group style audit.
Removed project-history framing, discarded-candidate narratives and repeated
warnings; consolidated statistical and PCA scope while preserving accepted
metrics, sample sizes, sparse-mask eligibility and the baseline-favorable
continuous end-to-end rotation result. Added the Spanish vector denoising-VAE
pipeline from the accepted INCISCOS revision, completed the architecture table
with supports/normalization/gates/kernel constraints, and added the approved
Introduction result paragraph. Professor comments and research files are intact.

Final PDF: 109 pages. `document.sh check thesis` and `git diff --check` pass.
All 70 bibliography entries are cited in the active document, with none missing
or unused; no overfull boxes or unresolved references remain. Manifest entries
are unique and output hashes pass. The earlier SSIM pseudocode verification
and archived-data figure checks remain valid. Reviewed the final pipeline and
table plus 18 changed or adjacent pages in this pass; QA is under
`build/thesis/annotation-review/style2-pages/`.

Incorporated the approved thesis-length Resumen and equivalent English Abstract,
including the recovered digital-pathology/cancer context, annotation effort,
parameter-sharing motivation and all five wording adjustments. Both cover
methods, downstream tasks, mixed results and the thesis-specific latent analysis.
Each occupies two pages. Academic metadata and keywords are preserved. English
hyphenation and decimal notation are scoped to the Abstract; reviewed all four
summary pages and the updated contents. QA is in
`build/thesis/annotation-review/summary-pages/`; final check and diff checks pass.
The user requested committing and pushing this approved revision to
`origin/main`. No Overleaf synchronization was requested.

Applied the seven residual style groups after user approval: removed the extra
activation/ablation warning, consolidated architecture-comparison scope in
Limitations, stated MIL patch identity and the RGB probe positively, simplified
the dispersion description, made the full-label conclusion concrete, and
rephrased the future pathology review. Nine targeted replacements affected
four chapters. All inline mathematical values and expressions are retained.
`document.sh check thesis` and `git diff --check` pass; no overfull boxes or
unresolved references remain. Reviewed nine affected pages, including the
synthesis table. Final PDF remains 109 pages; QA is under
`build/thesis/annotation-review/residual-pages/`.

## Complete

- Adapted the INCISCOS review improvements to the thesis without changing the approved objectives or chapter sequence: direct microscopic-rotation motivation, prior equivariant-autoencoder work, a 7-by-7 versus 5-by-5 kernel rationale with verified Weiler/Cesa and Worrall precedents, the representative 30.0% learned-coefficient comparison, and an explicit parameter/cost-matching limitation. The statistical-methods chapter now explains that an interval containing zero neither supports a 5% significant difference nor establishes equivalence. Results retain the complete fixed-25 reconstruction mosaic and add a larger first-nine view immediately before it. Thesis-native Spanish figures now show 23-WSI reconstruction distributions, clearer tissue and WSI comparisons, and a training-validation reconstruction-loss view with the logged one-SD band. The band describes within-evaluation dispersion for one run per VAE. All new figure sources and output hashes are recorded in `thesis/figures/manifest.yml` and generated by `scripts/render_selected_paper_views.py`.
- Recovered the complete approved plan from `Plan_Maximiliano_2023.zip`.
- Created independent, self-contained `plan/` and `thesis/` document roots.
- Seeded the thesis with the reusable plan text, references and figures.
- Removed the plan-only schedule and budget from the thesis draft.
- Added thesis chapters for experimental results, latent-space analysis,
  discussion, and conclusions.
- Split the active thesis into nine body files under `thesis/chapters/` (an
  unnumbered introduction plus eight numbered chapters) so
  agents and editors can work on one chapter without loading the monolith.
- Removed generated LaTeX files, notebooks, model code and obsolete duplicate
  assets from the live tree; they remain recoverable from Git history.
- Added one command interface for build, asset checks, PDF validation, linting
  and page rendering.
- Made cached incremental compilation the default in both CLI and VS Code.
  Added `watch`, image-free `draft`, safe local chapter focus, explicit-only
  `clean`, ChkTeX and offline LTeX+ commands.
- Added a pinned, checksum-verified LTeX+ 18.7.0 installer. It is installed in
  the ignored `.tools/` directory on this host; Quarto 1.10.18 is also
  available.
- Reviewed the July 2026 UIS autoarchive instructions, the current EISI
  committee guidance and a 2025 EISI research thesis. Recorded the rationale
  and reuse matrix in `docs/thesis_structure.md`.
- Reorganized the thesis around UIS/EISI practice: separate cover and title
  page, contents, figure/table lists, summary, abstract, unnumbered
  introduction, problem, objectives, reference framework, executed
  methodology, results, discussion, conclusions, future work, bibliography and
  optional appendices.
- Located ethics inside methodology and latent-space analysis inside results so
  methods, evidence and interpretation remain separated.
- Adopted a plan-first writing policy: preserve accurate approved prose and
  make new sections stylistically continuous with it, while correcting tense,
  grammar, technical scope and unsupported claims.
- Rewrote the methodology as executed work against the accepted experiment
  contracts and implementation in `equivariant-vae`: data populations,
  preprocessing, VAE objective and training, sealed evaluations, statistical
  analysis, reproducibility, and ethical scope are now explicit.
- Defined the patch experiment as WSI segmentation at patch-grid resolution.
  It is deliberately non-exhaustive because the masks are sparse and
  unannotated regions cannot be treated as negative labels.
- Added thesis-native TikZ diagrams for atlas construction, derivation of task
  populations, the residual block, `F0`/`F1` fields, the implemented
  steerable convolution, both VAE architectures and the tissue/WSI downstream
  heads. Figure provenance remains internal to `thesis/figures/manifest.yml`.
- Added primary citations for UBC-OCEAN, variational autoencoders, ResNet,
  MAE/SSIM image losses, attention-based MIL, WSI MIL, graph/window/
  convolutional attention, and calibrated sigmoid attention.
- Corrected the architecture lineage: the exploratory prototype was based on
  ResNet-18, while the final model is a custom 16-block residual VAE rather
  than a standard "ResNet-16".
- Defined the matched VAE nonlinearities from the final implementation. Both
  models place 34 learned sigmoid gates at the same sites and initialize them
  as SiLU-like scalar gates; `F1` copies use the necessary shared radial gate,
  whose `SO(2)` equivariance is shown algebraically. The text fixes dimensions,
  initialization, FP32 gate evaluation and the limits of the comparison.
- Documented the implemented continuous-`SO(2)` convolution: the kernel
  constraint, fixed analytic `F0`/`F1` pair bases, learned expansion
  coefficients, supported field types, 9x9/7x7 supports, pseudocode, parameter
  reduction and the countervailing increase in estimated convolutional cost.
- Made the steerable-layer description implementable from linear algebra and
  PyTorch: it now fixes the sampled grid, Gaussian profiles, generators,
  reduced QR convention, bank and coefficient dimensions, physical-channel
  indexing, Kronecker form, four-block direct sum, batched contraction,
  `reshape`/`permute` order and coefficient initialization.
- Documented initialization separately for the ordinary and steerable
  parametrizations, including the zero-initialized RGB decoder head and the
  limited relationship of that choice to Karras et al.; no claim is made that
  the normalization-free diffusion architecture was reproduced.
- Added publication-style detail diagrams for the residual block and
  equivariant kernel mechanism, an accepted learned `F1` stem kernel, and made
  the MIL diagram expose its spatial radius-two neighborhood. The equivariant
  convolution diagram now separates kernel construction from application:
  fixed bases and trainable coefficients build `K`, while the feature map
  enters only the subsequent `K*x` operation.
- Documented both data-access paths: a pre-shuffled CHW `uint8` binary shard
  read through read-only `mmap`, and strip-wise sequential WSI access that
  writes paired FP32 posterior means without an intermediate RGB cohort.
- Added readable thesis-native figures for strip-wise patch extraction,
  parameter sharing inside a steerable kernel and the exact local-global MIL
  tensor flow. Replaced the earlier didactic segmentation view with the real
  UBC-OCEAN WSI 11557 thumbnail, its supplemental sparse mask and the derived
  256x256 patch-grid labels; source URLs, checksums and derivation are recorded
  in the figure manifest.
- Added `scripts/render_wsi_mask_example.py`, which row-streams the full-size
  mask, reduces it without loading the complete RGB image into memory and
  reproduces the tissue-task coverage and purity thresholds for the overlay.
- Set the Figure 4.14 export width to 640 pixels. Its three lossless PNG panels
  now enter the PDF at 331 ppi instead of 621 ppi; together they occupy about
  1.0 MB rather than 3.4 MB, with the thumbnail, sparse mask and patch grid
  still legible at their printed size.
- Expanded the Transformer derivation into a self-contained definition of
  stable row-wise softmax, sigmoid, SiLU, LayerNorm, multi-head attention,
  SwiGLU and pre-normalized residual blocks, with all principal tensor shapes.
  Window attention now has an explicit block mask, complexity argument and
  dense-versus-window attention-map figure.
- Made the complete MIL path implementable from matrix/tensor operations: the
  radius-two `ell_infty` graph, gathered local key/value tensors, radial and
  null biases, `einsum` contractions, the `N x 192` local output, one-way
  cardinality-corrected sigmoid aggregation by CLS plus 16 REG queries, and the
  final CLS-only softmax readout to five logits are defined sequentially. The
  text also explains why independent sigmoid gates avoid competition among
  diagnostically useful patches.
- Added two PyTorch-style listings that connect those equations to an
  implementable local-attention block and to the sigmoid summary, CLS-only
  readout and five-class forward path. The surrounding prose follows one patch
  through its neighbors, the `N x 192` contextualized sequence, the 17 global
  summaries and the final logits.
- Replaced the Results placeholders with the accepted reconstruction, sealed
  WSI diagnosis, sparse patch-grid segmentation and available latent-geometry
  results. Dense dashboards were split into readable views and supplemented by
  single-patch reconstruction and rotation-action enlargements; accepted
  evidence covers training, reconstructions, sealed metrics, confusion
  matrices, label efficiency, transformed-latent reconstructions and
  rotation/PCA diagnostics.
- Removed run-audit incidents and internal validation vocabulary that do not
  affect the scientific exposition or reported results. The manuscript now
  states only reproducible methods, limitations and evidence that a reader can
  understand without access to project conversations.
- Reworked the dense Results graphics for print: Figure 5.4 spans two pages,
  Figure 5.6 gives each training curve a page, each confusion matrix is shown
  separately, and the tissue curves use full-width continued figures. The
  paired WSI reconstruction plot is regenerated in Spanish from the accepted
  per-WSI CSV with thesis-scale typography.
- Applied an independent methodology audit: the final prose now distinguishes
  beta and learning-rate warmups, the two global MIL attention stages, sparse
  tissue sampling, relative edge RMS, and the still-unexecuted functional
  analysis.
- Completed an adversarial citation pass over the introduction, problem,
  reference framework, methodology and results. High-risk numerical and causal
  claims were either tied to a source that supports their exact scope or
  rewritten as bounded descriptive statements.
- Reduced `thesis/references.bib` from the imported Zotero library to the 62
  works actually cited. Entries now use BibTeX-compatible publication fields,
  published versions where available, intact URLs and no workstation-local
  Zotero paths; BibTeX reports no warnings. The generated bibliography was
  checked for duplicate, missing and uncited entries and for repeated-author
  dashes; none were found.
- Rewrote the introduction and problem statement around traceable sources for
  cancer, Colombian mortality, diagnostic variability, WSI scale and sparse
  annotation. The reference framework now distinguishes translation,
  rotation, reflection, invariance and equivariance without attributing those
  properties to an ordinary CNN indiscriminately.
- Specified the experimental statistics at reproducible resolution: seeds,
  WSI-level cluster resampling, stratification, percentile intervals and the
  simultaneous centered band are explicit. Traceability is explained through
  fixed whole-WSI partitions, paired ordered manifests, validation-only model
  selection and sealed test inference, without repository hashes or internal
  conversation-dependent vocabulary.
- Defined the current latent-space probes mathematically, including the RGB
  affine probe, RMS action/canonicalization/end-to-end ratios and normalized
  cyclic local-linearity measure. The manuscript states explicitly which wider
  functional analyses remain pending.
- Standardized the sparse mask and patch-grid task terminology throughout the
  thesis as `tumor`, `estroma` and `necrosis`.
- Replaced the Discussion, Conclusions and Future Work outlines with a first
  evidence-backed draft. It states that the downstream superiority hypothesis
  is not statistically established, records the suggestive low-label pattern,
  and identifies the much smaller rotation-action error as the clearest current
  finding without claiming global latent factorization or perfect continuous
  end-to-end equivariance.
- Used Sutton's *Bitter Lesson* as a bounded interpretive lens rather than as a
  result tested by the experiments. Related the latent analysis to Elphick et
  al.'s pathology study while keeping rotation invariance distinct from the
  prescribed equivariant action evaluated here.
- Reviewed those three chapters against the approved plan's expository style.
  They now use the same impersonal voice, connected substantial paragraphs,
  chapter-opening orientation and transitions such as `En este sentido`, `Por
  otra parte` and `En síntesis`. Modern shorthand such as `embedding`,
  `regularidad operacional` and `ablación causal` was replaced by explicit
  Spanish explanations, and the Conclusions now answer the three approved
  specific objectives in order.

Verification:

- `./scripts/document.sh check thesis` passes;
- `artifacts/plan.pdf`: 30 pages;
- `artifacts/thesis.pdf`: 103 pages and 31,169,094 bytes;
- the optimized Figure 4.14 reduced `artifacts/thesis.pdf` by about 2.56 MB
  (8.5 percent) without sacrificing its printed legibility;
- unchanged thesis builds complete in about 0.12 seconds on this host;
- the draft PDF keeps the same page layout while shrinking from about 20.8 MB to
  about 238 kB by omitting image payloads;
- focused Results-chapter builds produce a 13-page working PDF, return to the
  complete PDF without clearing caches, and never overwrite the final
  artifact;
- LTeX+ CLI was smoke-tested in Spanish with the shared scientific dictionary;
- a focused LTeX+ pass over Discussion, Conclusions and Future Work found only
  dictionary notices for scientific terms, acronyms and author names, with no
  remaining grammatical finding;
- the thesis PDF was rendered as a complete contact sheet; the MIL flow,
  local-attention computation, paired WSI comparison, training curves,
  confusion matrices and tissue plots were also inspected page by page at 190
  dpi. Their labels, arrows and continued captions are readable and no diagram
  element overlaps another. The new Discussion, Conclusions and Future Work
  pages were inspected after compilation and again after the style pass; their
  paragraphs remain readable, and Discussion and Conclusions were condensed to
  avoid isolated continuation pages;
- the final thesis log and bibliography have no overfull boxes, unresolved
  citations, BibTeX warnings or `amsmath` warnings; inherited float-placement
  notices and two underfull table cells remain non-fatal;
- `shellcheck`, Python byte-compilation and `git diff --check` pass.

ChkTeX and LTeX+ intentionally report findings in the reused proposal prose;
they are revision tools, not clean gates until that prose is rewritten.

The reviewed thesis prose, bibliography, figures and PDF are included in the
GitHub publication authorized by the user on 2026-09-30. The destination is
`main` at `origin` (`HiperMaximus/Tesis`); Overleaf remains untouched.

## Current frontier

The thesis has an institutionally grounded structure, a revised introduction
and reference framework, an executed methodology, an evidence-backed Results
chapter and first full drafts of Discussion, Conclusions and Future Work. The
citation audit covered every active citation and the current bibliography is
clean. The final interpretation remains provisional where the functional
latent-space analysis is incomplete. The summary and abstract still come from
the approved plan.

## Selective INCISCOS corrections: completed

Adapted the accepted paper revision
`b85d7f2c23aa1620dbabcc902aee2d10a7062caa` from
`../equivariant-vae/paper/inciscos2026/` on 2026-09-30. Reviewed the existing
unstaged adaptations first and preserved the approved plan, objectives,
chapter order, Spanish expository voice, results and frozen experiments.
The adaptation did not access Overleaf or modify the research repository.
The user subsequently authorized committing and pushing the reviewed thesis
tree to GitHub.

- Introduction now distinguishes low-magnification tissue architecture from
  cellular patterns without a fixed image orientation at high magnification,
  motivating rotational inductive bias without claiming exact encoder
  equivariance.
- Reference framework connects unsupervised reconstruction to downstream use
  of frozen features and expands the existing TARGET-VAE/O2-VAE discussion.
  Translation already preceded rotation. A Spanish vector-field rotation
  schematic replaces the small generic commutative diagram (Figure 3.10).
- Methods explicitly separate the 513 source WSIs into 361 VAE-development,
  129 supervised-development and 23 shared sealed-test WSIs. The new Spanish
  Figure 4.1 branches test directly from the source and feeds all three final
  evaluations; the existing task-population diagram remains complementary.
- Kernel prose now separates sampled support, learned coefficients and dense
  convolution cost. Retained the representative 7,680/25,600 (30.0%) comparison
  and the full-model 29.8% ratio. Architecture/residual-block captions point to
  the existing detailed justification without merging their diagrams.
- Identified the scalar gate as a parameterized SiLU variant and added Elfwing
  et al. (2018), preserving equations and initialization. Full UBC-OCEAN naming
  was already correct. MIL scope now explicitly names Otsu-selected patches.
- Both new TikZ assets are self-contained and have paper source commit/path
  provenance in `thesis/figures/manifest.yml`. The general paper MIL schematic
  was not added because the existing thesis diagrams already explain that flow.
- Kept fixed-25 and enlarged fixed-nine mosaics and the training/validation
  spread interpretation (within-evaluation mean +/- SD, one VAE run). Summary
  and abstract remain pending; no kernel rationale was moved there.

Validation: final `./scripts/document.sh check thesis` and `git diff --check`
pass. The generated bibliography contains 62 entries, all cited, with no
missing or duplicate keys, unused entries, workstation-local paths or BibTeX
warnings. No unresolved references or overfull boxes. Changed prose,
architecture captions, both new diagrams and all generated bibliography pages
were rendered and visually reviewed; the partition diagram was corrected for
inherited line spacing before the final build. Final PDF: 103 pages. Existing
float-placement notices remain non-fatal. Review PNGs and logs are under
`build/thesis/inciscos-review/` and `build/inciscos-selective-*.log`.

Editorial pass after the adaptation: removed repeated superiority disclaimers,
metatext about previous architecture names, generic closing phrases and the
informal expression about a "free" fidelity improvement. Revised the Methods
opening, related-work closing, conceptual caption and final conclusion into
direct expository prose; retained the scientific limitations and all results.
User preference: English technical terms may remain, but introduce them first
with their Spanish name. Added first-use introductions for WSI/VAE/CNN,
Transformer, softmax, token, SwiGLU/SiLU, BatchNorm/ReLU/GroupNorm, batched,
logits, antialiasing, ridge, bootstrap and metric/precision/PCA abbreviations.
Preserve proper model names, published titles and executable identifiers.
Final document check and diff whitespace check pass; 62 references remain
cited. Reviewed 28 rendered pages affected by the edits and reflow; final PDF
is 103 pages. Style-review PNGs are in `build/thesis/style-review/`.
The whole-tree LTeX+ scan was interrupted after reviewing its output; it
reported inherited findings and false positives in formulas, identifiers and
English references. It is not a clean language gate for this pass.

Approved neutral-language pass: renamed the section to "Limitaciones del
estudio" and replaced admonitory or repeated warnings in Methods, Results,
Discussion, Conclusions and Future Work with concrete descriptions of scope.
Retained the sample sizes, uncertainty, one initialization, architecture
differences, partial masks and numerical thresholds. The continuous end-to-end
comparison was already performed and favored the baseline; Results, Discussion
and Conclusions state this separately from the lower latent-action error.
Saved the user's tone, terminology and before/after review preferences in
`AGENTS.md`. Final check and `git diff --check` pass, with no unresolved
references or overfull boxes. Visually reviewed 20 affected/adjacent pages;
final PDF: 103 pages, 31,169,094 bytes. Logs and PNGs:
`build/neutral-style-check.log`, `build/thesis/neutral-style-review/`.

Other pending work:

1. expand the functional latent-space analysis and revise any affected results,
   discussion and conclusions;
2. replace the summary and abstract;
3. complete the administrative annexes and final institutional review.

## Overleaf

Pending creation/configuration of two projects and their Git remotes. No remote
sync has been attempted.
