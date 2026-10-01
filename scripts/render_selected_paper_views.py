#!/usr/bin/env python3
"""Render thesis-sized views of the accepted VAE and classification results."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch
from matplotlib.ticker import FixedFormatter, FixedLocator, NullLocator

RESEARCH = Path(__file__).resolve().parents[2] / "equivariant-vae"
OUT = Path(__file__).resolve().parents[1] / "thesis/figures/experiments"
BASE = "#216b80"
SO2 = "#b45143"
GRID = "#dfe5e8"
INK = "#26343c"


def style() -> None:
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.edgecolor": "#a9b5bb",
        "axes.labelcolor": INK,
        "text.color": INK,
        "xtick.color": "#4c5c65",
        "ytick.color": "#4c5c65",
        "legend.fontsize": 8,
        "figure.dpi": 160,
    })


def fixed9() -> None:
    original = torch.load(RESEARCH / "docs/data/fixed25/originals.pt",
                          map_location="cpu", weights_only=True)["images_uint8"][:9]
    normal = torch.load(
        RESEARCH / "runs/kaggle/selected_runtime_full_v4_session3/artifacts/fixed25"
        / "boundary_060000/reconstruction_progress.pt",
        map_location="cpu", weights_only=True)["reconstruction"][:9]
    so2 = torch.load(
        RESEARCH / "runs/kaggle/so2_selected_runtime_full_session7_fresh_v1_retry1"
        / "artifacts/fixed25/boundary_060000/reconstruction_progress.pt",
        map_location="cpu", weights_only=True)["reconstruction"][:9]
    fig, axes = plt.subplots(3, 9, figsize=(7.2, 2.95))
    for branch, images in enumerate((original, normal, so2)):
        for index in range(9):
            row, column = divmod(index, 3)
            image = images[index].permute(1, 2, 0).numpy()
            image = image / 255 if branch == 0 else (np.clip(image, -1, 1) + 1) / 2
            axes[row, 3 * branch + column].imshow(image)
            axes[row, 3 * branch + column].axis("off")
    fig.subplots_adjust(left=0.005, right=0.995, top=0.87, bottom=0.005,
                        wspace=0.025, hspace=0.025)
    for x, label in zip((1 / 6, 1 / 2, 5 / 6),
                        ("Original", "VAE base", r"VAE-$\mathrm{SO}(2)$")):
        fig.text(x, 0.94, label, ha="center", va="center", fontsize=11)
    fig.savefig(OUT / "vae_reconstructions_fixed9.png", dpi=300)
    plt.close(fig)


def reconstruction_wsi() -> None:
    path = RESEARCH / "runs/local/vae_test_reconstruction_scored_v1/metrics/per_wsi_metrics.csv"
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    metrics = [
        ("mae_norm", "MAE", "RGB normalizado"),
        ("mse_norm", "MSE", "RGB normalizado"),
        ("psnr_img", "PSNR", "dB"),
        ("ssim_img", "SSIM", "Dominio de imagen"),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 4), constrained_layout=True)
    for ax, (key, title, unit) in zip(axes.flat, metrics, strict=True):
        data = [np.array([float(row[f"{branch}_{key}"]) for row in rows])
                for branch in ("normal", "so2")]
        box = ax.boxplot(data, positions=[1, 2], widths=0.36,
                         patch_artist=True, showfliers=False,
                         medianprops={"color": INK, "linewidth": 1.4},
                         whiskerprops={"color": "#64717b"},
                         capprops={"color": "#64717b"})
        for patch, color in zip(box["boxes"], (BASE, SO2), strict=True):
            patch.set_facecolor(color)
            patch.set_edgecolor(color)
            patch.set_alpha(0.24)
        jitter = np.linspace(-0.12, 0.12, len(rows))
        for position, values, color in zip((1, 2), data, (BASE, SO2), strict=True):
            ax.scatter(position + jitter, values, s=10, color=color,
                       alpha=0.72, linewidths=0, zorder=3)
        ax.set_xticks([1, 2], ["VAE base", r"VAE-$\mathrm{SO}(2)$"])
        ax.set_xlim(0.62, 2.38)
        ax.set_title(title, loc="left")
        ax.set_ylabel(unit)
        ax.grid(axis="y", color=GRID, linewidth=0.6)
        ax.spines["left"].set_visible(False)
        ax.tick_params(length=0)
    fig.savefig(OUT / "vae_test_wsi_distributions.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def classification() -> None:
    path = RESEARCH / "runs/local/tissue_test_scored_v1/label_efficiency_table.json"
    rows = json.loads(path.read_text(encoding="utf-8"))["rows"]
    budgets = np.array([row["labels_per_class"] for row in rows])
    normal = np.array([row["normal_vae"]["metrics"]["macro_f1"] for row in rows])
    so2 = np.array([row["so2_vae"]["metrics"]["macro_f1"] for row in rows])
    fig, ax = plt.subplots(figsize=(7.2, 3.25), constrained_layout=True)
    ax.plot(budgets, normal, "o-", color=BASE, linewidth=2, markersize=5,
            label="VAE base", zorder=3)
    ax.plot(budgets, so2, "s--", color=SO2, linewidth=2, markersize=5,
            label=r"VAE-$\mathrm{SO}(2)$", zorder=3)
    ax.set_xscale("log")
    ax.xaxis.set_major_locator(FixedLocator(budgets))
    ax.xaxis.set_major_formatter(FixedFormatter(["250", "500", "1.000", "2.500", "5.671"]))
    ax.xaxis.set_minor_locator(NullLocator())
    ax.set_ylim(0.46, 0.80)
    ax.set_xlabel("Etiquetas de entrenamiento por clase de tejido")
    ax.set_ylabel("Macro-F1 en prueba sellada")
    ax.grid(axis="y", color=GRID, linewidth=0.65)
    ax.legend(frameon=False, loc="upper left", ncol=2)
    ax.text(500, so2[1] + 0.010, "*", ha="center", va="bottom",
            color=SO2, fontsize=12, fontweight="bold")
    ax.spines["left"].set_visible(False)
    ax.tick_params(length=0)
    fig.savefig(OUT / "tissue_label_efficiency_refined.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    def scores(name: str) -> dict:
        path = RESEARCH / "runs/local/ubc_ocean_mil_test_scored_v1" / name
        return json.loads((path / "scored_predictions_and_metrics.json").read_text())[
            "metrics"
        ]
    base_scores, so2_scores = scores("normal_vae"), scores("so2_vae")
    keys = ["macro_f1", "balanced_accuracy", "accuracy"]
    labels = ["Macro-F1", "Exactitud balanceada", "Exactitud"]
    a = [base_scores[key] for key in keys]
    b = [so2_scores[key] for key in keys]
    y = np.arange(3)[::-1]
    fig, ax = plt.subplots(figsize=(7.2, 2.65), constrained_layout=True)
    for position, left, right in zip(y, a, b, strict=True):
        ax.plot([left, right], [position, position], color="#aab7bd",
                linewidth=1.6, zorder=2)
    ax.scatter(a, y + 0.075, s=57, color=BASE, marker="o", label="VAE base", zorder=3)
    ax.scatter(b, y - 0.075, s=57, color=SO2, marker="s",
               label=r"VAE-$\mathrm{SO}(2)$", zorder=3)
    ax.set_yticks(y, labels)
    ax.set_xlim(0, 0.70)
    ax.set_xticks(np.arange(0, 0.71, 0.1))
    ax.set_ylim(-0.45, 2.45)
    ax.set_xlabel("Puntuación en prueba sellada")
    ax.grid(axis="x", color=GRID, linewidth=0.65)
    ax.legend(frameon=False, loc="upper left", ncol=2)
    ax.spines["left"].set_visible(False)
    ax.tick_params(length=0)
    fig.savefig(OUT / "mil_test_metrics_refined.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def training() -> None:
    segments = [
        ("VAE base", BASE, ["selected_runtime_full_v2",
                            "selected_runtime_full_v3_session2",
                            "selected_runtime_full_v4_session3"]),
        (r"VAE-$\mathrm{SO}(2)$", SO2, [
            "so2_selected_runtime_full_v1_session1",
            "so2_selected_runtime_full_v2_session2",
            "so2_selected_runtime_full_v3_session3",
            "so2_selected_runtime_full_v4_session4",
            "so2_selected_runtime_full_v5_session5",
            "so2_selected_runtime_full_session6_fresh_v1",
            "so2_selected_runtime_full_session7_fresh_v1_retry1",
        ]),
    ]
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.85), sharey=True,
                             constrained_layout=True)
    for ax, (title, color, sessions) in zip(axes, segments, strict=True):
        bins: dict[int, list[float]] = {}
        validation: dict[int, list[tuple[float, float, int]]] = {}
        for session in sessions:
            metrics = RESEARCH / "runs/kaggle" / session / "metrics"
            with (metrics / "train_steps.csv").open(newline="", encoding="utf-8") as stream:
                for row in csv.DictReader(stream):
                    step = int(row["optimizer_step"])
                    boundary = (step - 1) // 3000 * 3000 + 3000
                    bins.setdefault(boundary, []).append(float(row["recon_loss"]))
            with (metrics / "validation_metrics.csv").open(newline="", encoding="utf-8") as stream:
                for row in csv.DictReader(stream):
                    if row["view"] == "deterministic_denoising":
                        validation.setdefault(int(row["optimizer_step"]), []).append((
                            float(row["recon_loss"]), float(row["recon_loss_std"]),
                            int(row["sample_count"])))
        steps = np.array(sorted(validation))
        train = np.array([np.mean(bins[int(step)]) for step in steps])
        means, spreads = [], []
        for step in steps:
            records = validation[int(step)]
            weights = [count for _, _, count in records]
            mean = np.average([value for value, _, _ in records], weights=weights)
            second = np.average([sd**2 + value**2 for value, sd, _ in records],
                                weights=weights)
            means.append(mean)
            spreads.append(np.sqrt(max(0.0, second - mean**2)))
        means, spreads = np.array(means), np.array(spreads)
        ax.fill_between(steps / 1000, means - spreads, means + spreads,
                        color=color, alpha=0.14, linewidth=0,
                        label="Validación ±1 DE registrada")
        ax.plot(steps / 1000, train, ":", color="#64717b", linewidth=1.7,
                label="Entrenamiento, media en 3.000 pasos")
        ax.plot(steps / 1000, means, "o-", color=color, linewidth=1.8,
                markersize=3.3, label="Media de validación")
        ax.set_title(title, loc="left")
        ax.set_xlabel("Actualizaciones del optimizador (miles)")
        ax.set_xlim(0, 61)
        ax.set_xticks([0, 15, 30, 45, 60])
        ax.set_ylim(0.07, 0.15)
        ax.grid(axis="y", color=GRID, linewidth=0.6)
        ax.spines["left"].set_visible(False)
        ax.tick_params(length=0)
    axes[0].set_ylabel("Pérdida de reconstrucción")
    axes[0].legend(frameon=False, fontsize=6.5, loc="upper right")
    fig.savefig(OUT / "vae_training_curves_refined.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    style()
    fixed9()
    reconstruction_wsi()
    classification()
    training()
    for name in ["vae_reconstructions_fixed9.png", "vae_test_wsi_distributions.png",
                 "tissue_label_efficiency_refined.png", "mil_test_metrics_refined.png",
                 "vae_training_curves_refined.png"]:
        path = OUT / name
        print(name, hashlib.sha256(path.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
