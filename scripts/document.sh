#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
texmf_var="$repo_dir/.cache/texmf-var"

usage() {
    cat >&2 <<'EOF'
usage: ./scripts/document.sh COMMAND DOCUMENT

COMMAND:
  build     incremental final build; refreshes artifacts/<document>.pdf
  watch     keep rebuilding after saved changes; stop with Ctrl-C
  draft     incremental build with images replaced by layout-preserving boxes
  check     validate assets, final PDF, citations and references
  lint      run ChkTeX over every TeX source
  grammar   run offline LTeX+ over the document tree
  render    render all final PDF pages as PNGs for visual review
  clean     remove document build state; use only for cache-related problems

DOCUMENT: plan | thesis

The special command check-all validates both documents.
EOF
    exit 2
}

require_document() {
    case "$1" in
        plan|thesis) ;;
        *) usage ;;
    esac
}

read_focus_pretex() {
    sed \
        -e 's/%.*$//' \
        -e '/^[[:space:]]*$/d' \
        "$1" \
        | tr -d '\n'
}

run_latexmk() {
    local document="$1"
    local build_dir="$2"
    local mode="${3:-final}"
    local source_dir="$repo_dir/$document"
    local pretex=""
    local latexmk_mode_args=()
    local build_state="$mode-full"
    local state_file="$build_dir/.document-mode"
    local focus_file="$repo_dir/thesis/includeonly.local.tex"

    if [[ "$mode" == "draft" ]]; then
        pretex='\def\ThesisDraft{1}'
    fi
    if [[ "$document" == "thesis" && -e "$focus_file" ]]; then
        pretex+="$(read_focus_pretex "$focus_file")"
        build_state="$mode-focused-$(sha256sum "$focus_file" | cut -d' ' -f1)"
    fi
    if [[ -n "$pretex" ]]; then
        latexmk_mode_args+=("-usepretex=$pretex")
    fi
    if [[ ! -e "$state_file" || "$(<"$state_file")" != "$build_state" ]]; then
        latexmk_mode_args+=(-g)
    fi

    mkdir -p "$build_dir/chapters" "$texmf_var"
    (
        cd "$source_dir"
        TEXMFVAR="$texmf_var" latexmk \
            -pdf \
            -interaction=nonstopmode \
            -halt-on-error \
            -file-line-error \
            -outdir="$build_dir" \
            "${latexmk_mode_args[@]}" \
            main.tex
    )
    printf '%s\n' "$build_state" > "$state_file"
}

build_document() {
    local document="$1"
    local build_dir="$repo_dir/build/$document"
    local artifact="$repo_dir/artifacts/$document.pdf"
    local focused_build=false

    if [[ "$document" == "thesis" && -e "$repo_dir/thesis/includeonly.local.tex" ]]; then
        focused_build=true
    fi

    mkdir -p "$repo_dir/artifacts"
    run_latexmk "$document" "$build_dir" final
    if [[ "$focused_build" == true ]]; then
        echo "focused build: $build_dir/main.pdf"
        echo "artifact preserved: $artifact"
        return
    fi
    if [[ ! -e "$artifact" || "$build_dir/main.pdf" -nt "$artifact" ]]; then
        cp "$build_dir/main.pdf" "$artifact"
        echo "updated: $artifact"
    else
        echo "current: $artifact"
    fi
}

watch_document() {
    local document="$1"
    local source_dir="$repo_dir/$document"
    local build_dir="$repo_dir/build/$document"
    local pretex=""
    local latexmk_mode_args=()
    local focus_file="$repo_dir/thesis/includeonly.local.tex"

    if [[ "$document" == "thesis" && -e "$focus_file" ]]; then
        pretex="$(read_focus_pretex "$focus_file")"
        latexmk_mode_args+=("-usepretex=$pretex")
    fi

    mkdir -p "$build_dir/chapters" "$texmf_var"
    echo "watching: $source_dir (stop with Ctrl-C)"
    (
        cd "$source_dir"
        TEXMFVAR="$texmf_var" latexmk \
            -pdf \
            -pvc \
            -g \
            -view=none \
            -interaction=nonstopmode \
            -file-line-error \
            -outdir="$build_dir" \
            "${latexmk_mode_args[@]}" \
            main.tex
    )
}

draft_document() {
    local document="$1"
    local build_dir="$repo_dir/build/$document-draft"

    run_latexmk "$document" "$build_dir" draft
    echo "draft: $build_dir/main.pdf"
}

check_document() {
    local document="$1"
    local build_dir="$repo_dir/build/$document"
    local artifact="$repo_dir/artifacts/$document.pdf"
    local log_file="$build_dir/main.log"

    if [[ "$document" == "thesis" && -e "$repo_dir/thesis/includeonly.local.tex" ]]; then
        echo "Remove thesis/includeonly.local.tex before a final check." >&2
        return 1
    fi

    python3 "$repo_dir/scripts/check_tex_assets.py" "$repo_dir/$document"
    build_document "$document"
    qpdf --check "$artifact"

    if rg -n \
        'LaTeX Warning: (Citation|Reference).*undefined|There were undefined (citations|references)' \
        "$log_file"; then
        echo "undefined citations or references found in $log_file" >&2
        return 1
    fi
    echo "check passed: $document"
}

render_document() {
    local document="$1"
    local render_dir="$repo_dir/build/$document/render"

    build_document "$document"
    mkdir -p "$render_dir"
    find "$render_dir" -maxdepth 1 -type f -name 'page-*.png' -delete
    pdftoppm -png -r 120 \
        "$repo_dir/artifacts/$document.pdf" \
        "$render_dir/page"
    echo "rendered: $render_dir"
}

lint_document() {
    local document="$1"

    find "$repo_dir/$document" -type f -name '*.tex' -print0 \
        | xargs -0 -r chktex -q
}

grammar_document() {
    local document="$1"
    local ltex_cli=""

    if command -v ltex-cli-plus >/dev/null 2>&1; then
        ltex_cli="$(command -v ltex-cli-plus)"
    elif [[ -x "$repo_dir/.tools/ltex-ls-plus/bin/ltex-cli-plus" ]]; then
        ltex_cli="$repo_dir/.tools/ltex-ls-plus/bin/ltex-cli-plus"
    else
        echo "LTeX+ CLI is not installed. Run ./scripts/setup_ltex.sh first." >&2
        return 1
    fi

    "$ltex_cli" \
        --client-configuration="$repo_dir/.ltex-config.json" \
        "$repo_dir/$document"
}

clean_document() {
    local document="$1"
    local source_dir="$repo_dir/$document"
    local build_dir="$repo_dir/build/$document"
    local draft_dir="$repo_dir/build/$document-draft"

    (
        cd "$source_dir"
        latexmk -C -outdir="$build_dir" main.tex
        latexmk -C -outdir="$draft_dir" main.tex
    )
    echo "cleaned document build state; preserved .cache/texmf-var and artifacts"
}

command="${1:-}"
case "$command" in
    build|watch|draft|check|lint|grammar|render|clean)
        document="${2:-}"
        require_document "$document"
        ;;
    check-all)
        [[ $# -eq 1 ]] || usage
        check_document plan
        check_document thesis
        exit 0
        ;;
    *) usage ;;
esac

[[ $# -eq 2 ]] || usage
case "$command" in
    build) build_document "$document" ;;
    watch) watch_document "$document" ;;
    draft) draft_document "$document" ;;
    check) check_document "$document" ;;
    lint) lint_document "$document" ;;
    grammar) grammar_document "$document" ;;
    render) render_document "$document" ;;
    clean) clean_document "$document" ;;
esac
