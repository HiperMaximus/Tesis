#!/usr/bin/env python3
"""Render the approved WSI 10246 example from frozen scored predictions."""

import argparse
import csv
import gzip
import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PatchCollection
from matplotlib.patches import Patch, Rectangle
from matplotlib.ticker import FuncFormatter, MultipleLocator


ROOT = Path(__file__).resolve().parents[1]
RELATIVE_BUNDLE = Path("runs/local/tissue_test_scored_v1")
WSI_ID = "10246"
CELL_SIZE = 256
COLORS = ("#d53b3b", "#2f9856", "#3269c6")
CLASS_NAMES = ("Tumor", "Estroma", "Necrosis")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_branch(bundle, branch, status):
    relative = f"branches/{branch}/budget_5671_per_class/scored_predictions.csv.gz"
    path = bundle / relative
    checksum = digest(path)
    if checksum != status["artifacts"][relative]["sha256"]:
        raise ValueError(f"Archived checksum mismatch: {relative}")
    with gzip.open(path, "rt", newline="") as stream:
        rows = list(csv.DictReader(stream))
    keys = [
        tuple(row[key] for key in
              ("dataset_row", "atlas_row_index", "wsi_id", "x", "y", "truth"))
        for row in rows
    ]
    coordinates = [(row["wsi_id"], int(row["x"]), int(row["y"])) for row in rows]
    if len(rows) != 31572 or len(set(coordinates)) != len(rows):
        raise ValueError("Unexpected total count or duplicate coordinates")
    for row in rows:
        truth, prediction = int(row["truth"]), int(row["prediction"])
        logits = [float(row[f"logit_{name}"]) for name in ("tumor", "stroma", "necrosis")]
        if truth not in range(3) or prediction not in range(3):
            raise ValueError("Unexpected class code")
        if not np.isfinite(logits).all() or prediction != int(np.argmax(logits)):
            raise ValueError("Prediction disagrees with stored logits")
        if int(row["x"]) % CELL_SIZE or int(row["y"]) % CELL_SIZE:
            raise ValueError("Coordinates do not align with the native patch grid")
    return rows, keys, {str(RELATIVE_BUNDLE / relative): checksum}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--research-root", type=Path, default=ROOT.parent / "equivariant-vae")
    args = parser.parse_args()
    bundle = args.research_root / RELATIVE_BUNDLE
    status = json.loads((bundle / "overall_status.json").read_text())
    if status["status"] != "complete":
        raise ValueError("Scoring bundle is incomplete")
    base, base_keys, hashes = read_branch(bundle, "normal_vae", status)
    so2, so2_keys, so2_hashes = read_branch(bundle, "so2_vae", status)
    hashes.update(so2_hashes)
    if base_keys != so2_keys:
        raise ValueError("The two branches have different ordered identities or truth")
    slide_classes = {}
    for row in base:
        slide_classes.setdefault(row["wsi_id"], set()).add(int(row["truth"]))
    eligible = sorted((key for key, values in slide_classes.items() if values == {0, 1, 2}), key=int)
    if eligible[0] != WSI_ID:
        raise ValueError("The approved class-coverage/identifier selection rule changed")
    selected_base = [row for row in base if row["wsi_id"] == WSI_ID]
    selected_so2 = [row for row in so2 if row["wsi_id"] == WSI_ID]
    if len(selected_base) != 1407:
        raise ValueError("Unexpected selected WSI count")
    x = np.array([int(row["x"]) for row in selected_base])
    y = np.array([int(row["y"]) for row in selected_base])
    labels = [
        np.array([int(row["truth"]) for row in selected_base]),
        np.array([int(row["prediction"]) for row in selected_base]),
        np.array([int(row["prediction"]) for row in selected_so2]),
    ]
    bounds = [int(x.min()), int(x.max()) + CELL_SIZE,
              int(y.min()), int(y.max()) + CELL_SIZE]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})
    fig = plt.figure(figsize=(8.4, 7.9), facecolor="white")
    placements = ((0.335, 0.59, 0.34, 0.33),
                  (0.10, 0.13, 0.34, 0.33), (0.57, 0.13, 0.34, 0.33))
    titles = ("(a) Clases de referencia", "(b) Predicción: VAE base",
              r"(c) Predicción: VAE-SO(2)")
    for placement, title, classes in zip(placements, titles, labels):
        ax = fig.add_axes(placement)
        rectangles = [Rectangle((px, py), CELL_SIZE, CELL_SIZE) for px, py in zip(x, y)]
        ax.add_collection(PatchCollection(
            rectangles, facecolors=[COLORS[value] for value in classes],
            edgecolors="none", linewidths=0, antialiased=False))
        ax.set_xlim(bounds[:2])
        ax.set_ylim(bounds[3], bounds[2])
        ax.set_aspect("equal")
        ax.set_title(title, fontsize=12, pad=12)
        ax.set_xlabel("x (miles de píxeles)")
        ax.set_ylabel("y (miles de píxeles)")
        for axis in (ax.xaxis, ax.yaxis):
            axis.set_major_locator(MultipleLocator(10000))
            axis.set_major_formatter(FuncFormatter(lambda value, _: f"{value / 1000:g}"))
        ax.tick_params(labelsize=10)
        for spine in ax.spines.values():
            spine.set_color("#888888")
    handles = [Patch(facecolor=color, label=name) for color, name in zip(COLORS, CLASS_NAMES)]
    handles.append(Patch(facecolor="white", edgecolor="#888888", label="Sin evaluación"))
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, 0.015),
               ncol=4, frameon=False, fontsize=11)
    output = ROOT / "thesis/figures/experiments/tissue_prediction_maps_wsi_10246.png"
    fig.savefig(output, dpi=450, facecolor="white", bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)
    audit = {
        "wsi_id": WSI_ID, "budget_per_class": 5671, "cells": len(x),
        "cell_size_native_pixels": CELL_SIZE, "bounds_native_pixels": bounds,
        "true_class_counts": dict(zip(CLASS_NAMES, np.bincount(labels[0], minlength=3).tolist())),
        "selection_rule": "lowest numeric WSI ID with all three true classes",
        "all_branch_rows": len(base), "ordered_pairing_verified": True,
        "all_predictions_match_stored_logit_argmax": True,
        "source_sha256": hashes, "output_sha256": digest(output),
    }
    qa_dir = ROOT / "build/thesis/revision-punto-08"
    qa_dir.mkdir(parents=True, exist_ok=True)
    (qa_dir / "figure_audit.json").write_text(json.dumps(audit, indent=2) + "\n")
    print(json.dumps(audit, indent=2))


if __name__ == "__main__":
    main()
