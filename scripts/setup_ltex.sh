#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
version="18.7.0"
platform="linux-x64"
archive="ltex-ls-plus-$version-$platform.tar.gz"
expected_sha256="1e16df6c578dc76ff97d644445d126ba6fba5c2e8e174178ab86372652fd7612"
download_url="https://github.com/ltex-plus/ltex-ls-plus/releases/download/$version/$archive"
tools_dir="$repo_dir/.tools"
install_dir="$tools_dir/ltex-ls-plus-$version"
active_link="$tools_dir/ltex-ls-plus"

if [[ "$(uname -s)" != "Linux" || "$(uname -m)" != "x86_64" ]]; then
    echo "This installer is pinned for Linux x86_64." >&2
    echo "Install LTeX+ manually from https://github.com/ltex-plus/ltex-ls-plus/releases" >&2
    exit 1
fi

if [[ -x "$active_link/bin/ltex-cli-plus" ]]; then
    "$active_link/bin/ltex-cli-plus" --help >/dev/null
    echo "installed: $active_link"
    exit 0
fi

download_dir="$(mktemp -d)"
trap 'rm -rf "$download_dir"' EXIT

curl -fL "$download_url" -o "$download_dir/$archive"
printf '%s  %s\n' "$expected_sha256" "$download_dir/$archive" \
    | sha256sum --check --strict

mkdir -p "$tools_dir"
tar -xzf "$download_dir/$archive" -C "$tools_dir"

if [[ ! -x "$install_dir/bin/ltex-cli-plus" ]]; then
    echo "Unexpected LTeX+ archive layout." >&2
    exit 1
fi

ln -sfn "$(basename "$install_dir")" "$active_link"
"$active_link/bin/ltex-cli-plus" --help >/dev/null
echo "installed: $active_link"
