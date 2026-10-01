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
from matplotlib.ticker import FixedFormatter, FixedLocator, NullLocator, MaxNLocator

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
    fig, ax = plt.subplots(figsize=(7.2, 3.3), constrained_layout=True)
    ax.barh(y + 0.19, a, height=0.32, color=BASE, label="VAE base")
    ax.barh(y - 0.19, b, height=0.32, color=SO2, label=r"VAE-$\mathrm{SO}(2)$")
    for ys, values in ((y + 0.19, a), (y - 0.19, b)):
        for pos, value in zip(ys, values, strict=True):
            ax.text(value + 0.012, pos, f"{value:.3f}".replace(".", ","),
                    va="center", fontsize=10)
    ax.set_yticks(y, labels)
    ax.set_xlim(0, 0.75)
    ax.set_ylim(-0.55, 2.85)
    ax.set_xlabel("Puntuación en prueba sellada")
    ax.grid(axis="x", color=GRID, linewidth=0.65)
    ax.set_axisbelow(True)
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


def approved_annotation_views() -> None:
    """Render approved thesis views from archived values; preserve all PCA fits and use exact quarter-turn image reindexing."""
    r = np.linspace(0, 4.25, 600)
    etas = [1, 1.90395977, 2.75]
    colors = ['#216b80', '#b45143', '#7b6fa5']
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 3.0), constrained_layout=True)
    for e, c in zip(etas, colors):
        axes[0].plot(r, np.exp(-0.5 * ((r - e) / 0.3) ** 2), color=c, label=f'η = {e:.2f}'.replace('.', ','))
    axes[0].set(xlabel='Radio r (píxeles)', ylabel='Envolvente gₛ(r)', xlim=(0, 4.25), ylim=(0, 1.06))
    axes[0].legend(frameon=False, fontsize=8)
    xy = np.linspace(-3.5, 3.5, 401)
    xx, yy = np.meshgrid(xy, xy)
    rr = np.hypot(xx, yy)
    field = sum((np.exp(-0.5 * ((rr - e) / 0.3) ** 2) for e in etas))
    for ax in axes[1:]:
        ax.imshow(field, extent=(-3.5, 3.5, -3.5, 3.5), origin='lower', cmap='Blues', vmin=0, vmax=1.1)
        ax.set(xlabel='x (píxeles)', ylabel='y (píxeles)', xticks=[-3, 0, 3], yticks=[-3, 0, 3])
        ax.set_aspect('equal')
    axes[1].set_title('Tres anillos continuos', fontsize=10)
    axes[2].set_title('Cuadrícula de 7 × 7', fontsize=10)
    grid = np.arange(-3, 4)
    gx, gy = np.meshgrid(grid, grid)
    axes[2].scatter(gx, gy, s=12, c='#b45143', edgecolor='white', linewidth=0.25)
    fig.savefig(OUT / 'radial_basis_sampling.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    p = RESEARCH / 'runs/local/decoded_latent_transform_v1/decoded_latent_transform_v1'
    with np.load(p / 'selected_images_uint8.npz') as images:
        for name, angles in [('vae_rotation_0_90.png', [0, 90]), ('vae_rotation_180_270.png', [180, 270])]:
            fig, axes = plt.subplots(4, 3, figsize=(7.2, 8.3))
            for row, (angle, branch) in enumerate(((a, b) for a in angles for b in ['normal_vae', 'so2_vae'])):
                for col, suffix in enumerate(['input', 'transformed_input_recon', 'action']):
                    data = images[f'{branch}_rank12_angle{angle}_{suffix}']
                    if suffix == 'input':
                        data = np.rot90(data, angle // 90, axes=(1, 2))
                    axes[row, col].imshow(data.transpose(1, 2, 0))
                    axes[row, col].set_xticks([])
                    axes[row, col].set_yticks([])
                    for spine in axes[row, col].spines.values():
                        spine.set_visible(False)
                label = 'Base' if branch == 'normal_vae' else 'SO(2)'
                axes[row, 0].set_ylabel(f'{angle}°\n{label}', fontsize=11)
            for ax, title in zip(axes[0], ['Entrada rotada', 'Rotar entrada\ny reconstruir', 'Transformar latente\ny decodificar']):
                ax.set_title(title, fontsize=11, pad=10)
            fig.subplots_adjust(left=0.085, right=0.995, top=0.93, bottom=0.005, hspace=0.07, wspace=0.025)
            fig.savefig(OUT / name, dpi=230)
            plt.close(fig)
    summary = json.loads((p / 'decoded_latent_transform_summary.json').read_text())
    for filename, exact in [('latent_population_ratios.png', False), ('latent_exact_d4.png', True)]:
        fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.25), constrained_layout=True)
        for ax, key, title in zip(axes, ['action', 'canonical'], ['Acción sobre el latente', 'Canonización del latente']):
            for x, branch, color, label in [(0, 'normal_vae', BASE, 'Base'), (1, 'so2_vae', SO2, 'SO(2)')]:
                d = summary['branches'][branch]
                values = np.array(d['exact_quarter_aggregate'][f'{key}_ratio_per_patch'] if exact else [v[f'{key}_ratio'] for v in d['per_patch']])
                ax.scatter(x + np.linspace(-0.09, 0.09, len(values)), values, s=13, color=color, alpha=0.7)
                ax.plot([x - 0.17, x + 0.17], [np.median(values)] * 2, color=color, lw=2.4)
                ax.text(x, 0.98, f'{np.median(values):.3g}'.replace('.', ','), transform=ax.get_xaxis_transform(), ha='center', va='top', fontsize=10)
            ax.set_xticks([0, 1], ['VAE base', 'VAE-SO(2)'])
            ax.set_title(title)
            ax.set_ylabel('Razón de error (RMS)')
            ax.grid(axis='y', color=GRID, lw=0.6)
            ax.set_xlim(-0.45, 1.45)
            if exact and key == 'action':
                ax.set_yscale('log')
            ax.margins(y=0.2)
        fig.savefig(OUT / filename, dpi=300, bbox_inches='tight')
        plt.close(fig)
    html = (RESEARCH / 'runs/local/frozen_vae_rotation_orbits/rotation-orbits.html').read_text()
    pos = html.index('const DATA')
    data = json.JSONDecoder().raw_decode(html[html.index('=', pos) + 1:].lstrip())[0]
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 6.0), constrained_layout=True)
    for ax, name, color, title in zip(axes[0], ['Normal VAE', 'SO(2) VAE'], [BASE, SO2], ['VAE base', 'VAE-SO(2)']):
        xy = np.array(data['models'][name]['pca'])
        ax.plot(xy[:, 0], xy[:, 1], color=color, lw=1.4)
        ax.scatter(*xy[0], s=30, c='#26343c', zorder=3)
        ax.annotate('0°', xy[0], xytext=(5, 3), textcoords='offset points')
        ax.set(title=title, xlabel='PC1', ylabel='PC2')
        ax.set_aspect('equal', adjustable='box')
        ax.xaxis.set_major_locator(MaxNLocator(4))
        ax.yaxis.set_major_locator(MaxNLocator(4))
        ax.grid(color=GRID, lw=0.6)
    for name, key, color, label in [('Normal VAE', 'normal', BASE, 'VAE base'), ('SO(2) VAE', 'so2', SO2, 'VAE-SO(2)')]:
        axes[1, 0].plot(data['angles'], data['models'][name]['residual'], color=color, label=label, lw=1.3)
        axes[1, 1].plot(data['quarters']['angles'], data['quarters'][key], color=color, label=label, marker='o')
    axes[1, 0].set(title='Residual del parche 12', xlabel='Ángulo (grados)', ylabel='RMS relativa', xticks=[0, 90, 180, 270, 359])
    axes[1, 1].set(title='Cuartos de vuelta: 25 parches', xlabel='Ángulo (grados)', ylabel='RMS relativa', xticks=[0, 90, 180, 270])
    for ax in axes[1]:
        ax.legend(frameon=False, fontsize=9)
        ax.grid(color=GRID, lw=0.6)
    fig.savefig(OUT / 'latent_orbit_single_patch.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    spatial = data['spatial_pca']
    a = np.array(spatial['Normal VAE']['relative_edge_rms'])
    b = np.array(spatial['SO(2) VAE']['relative_edge_rms'])
    fig, ax = plt.subplots(figsize=(7.2, 3.1), constrained_layout=True)
    for v, w in zip(a, b):
        ax.plot([0, 1], [v, w], color='#aab7bd', lw=0.8, alpha=0.7)
    ax.scatter(np.zeros(25), a, color=BASE, s=20, label='VAE base')
    ax.scatter(np.ones(25), b, color=SO2, s=20, label='VAE-SO(2)')
    ax.set(xticks=[0, 1], xticklabels=['VAE base', 'VAE-SO(2)'], ylabel='RMS relativa de aristas', xlim=(-0.35, 1.35))
    ax.grid(axis='y', color=GRID, lw=0.6)
    fig.savefig(OUT / 'latent_spatial_pca_paired.png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(7.2, 3.1), constrained_layout=True)
    delta = b - a
    ax.bar(np.arange(25), delta, color=np.where(delta < 0, SO2, BASE))
    ax.axhline(0, c='#26343c', lw=0.8)
    ax.set(xlabel='Índice del parche fijo', ylabel='Diferencia SO(2) − base', xticks=[0, 4, 8, 12, 16, 20, 24])
    ax.grid(axis='y', color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    fig.savefig(OUT / 'latent_spatial_pca_delta.png', dpi=300, bbox_inches='tight')
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    style()
    fixed9()
    reconstruction_wsi()
    classification()
    training()
    approved_annotation_views()
    for name in ["vae_reconstructions_fixed9.png", "vae_test_wsi_distributions.png",
                 "tissue_label_efficiency_refined.png", "mil_test_metrics_refined.png",
                 "vae_training_curves_refined.png"]:
        path = OUT / name
        print(name, hashlib.sha256(path.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
