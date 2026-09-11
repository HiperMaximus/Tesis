# Current Status

Last updated: 2026-09-11

## Complete

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

Verification:

- `./scripts/document.sh check-all` passes for both documents;
- `artifacts/plan.pdf`: 30 pages;
- `artifacts/thesis.pdf`: 98 pages;
- unchanged thesis builds complete in about 0.12 seconds on this host;
- the draft PDF keeps the same page layout while shrinking from about 20.8 MB to
  about 238 kB by omitting image payloads;
- focused Results-chapter builds produce a 13-page working PDF, return to the
  complete PDF without clearing caches, and never overwrite the final
  artifact;
- LTeX+ CLI was smoke-tested in Spanish with the shared scientific dictionary;
- the final 98-page PDF was rendered as a complete contact sheet; the MIL flow,
  local-attention computation, paired WSI comparison, training curves,
  confusion matrices and tissue plots were also inspected page by page at 190
  dpi. Their labels, arrows and continued captions are readable and no diagram
  element overlaps another;
- the final thesis log has no overfull boxes, unresolved references or
  `amsmath` warnings; two inherited float-placement notices and underfull boxes
  remain non-fatal;
- `shellcheck`, Python byte-compilation and `git diff --check` pass.

ChkTeX and LTeX+ intentionally report findings in the reused proposal prose;
they are revision tools, not clean gates until that prose is rewritten.

The Git index still contains the earlier repository restructuring, while the
latest thesis prose, figures and PDF are unstaged. Do not commit the current
partial index; when a commit is requested, stage the complete tree and review
the resulting diff first.

## Current frontier

The thesis has an institutionally grounded structure, an executed methodology
and a first evidence-backed Results chapter. This pass completed structural
and visual review of the full PDF, not line-by-line editorial revision of all
inherited prose. The summary, abstract, introduction and older parts of the
reference framework still come from the approved plan and must be revised for
tense, current literature and consistency with the final experiments.

Next work:

1. finish the functional latent-space analysis and integrate its accepted
   methods, figures and results;
2. write the discussion and conclusions against the completed evidence;
3. rewrite the introduction and the remaining inherited reference-framework
   prose for accuracy and currency;
4. replace the summary and abstract, then complete the administrative annexes.

## Overleaf

Pending creation/configuration of two projects and their Git remotes. No remote
sync has been attempted.
