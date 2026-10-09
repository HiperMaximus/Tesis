#!/usr/bin/env python3
"""Export readable thesis views from accepted experiment artifacts.

The source artifacts remain unchanged in the research repository. This script
extracts lossless panels, redraws accepted tabular values with print-readable
typography, or reassembles accepted uint8 arrays for the thesis.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def _chw_image(array: np.ndarray) -> Image.Image:
    return Image.fromarray(np.transpose(array, (1, 2, 0)), mode="RGB")


def _save_crop(source: Image.Image, box: tuple[int, int, int, int], path: Path) -> None:
    source.crop(box).save(path, optimize=True)


def _stack(images: list[Image.Image], path: Path, gap: int = 24) -> None:
    width = max(image.width for image in images)
    height = sum(image.height for image in images) + gap * (len(images) - 1)
    canvas = Image.new("RGB", (width, height), "white")
    y = 0
    for image in images:
        canvas.paste(image, ((width - image.width) // 2, y))
        y += image.height + gap
    canvas.save(path, optimize=True)


def _font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont:
    family = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{family}", size)


def _render_paired_wsi(csv_path: Path, path: Path) -> None:
    """Render the accepted per-WSI means with print-readable typography."""

    with csv_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    pairs = [
        (float(row["normal_mae_norm"]), float(row["so2_mae_norm"]))
        for row in rows
    ]
    low = min(value for pair in pairs for value in pair)
    high = max(value for pair in pairs for value in pair)
    span = max(high - low, 1e-12)

    width, height = 1800, 1100
    left, right, top, bottom = 210, 90, 205, 155
    plot_left, plot_right = left, width - right
    plot_top, plot_bottom = top, height - bottom
    x_normal, x_so2 = 720, 1310
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    ink, muted, grid = "#1f2937", "#475569", "#dbe3ec"
    normal, so2 = "#2563eb", "#e85d0f"

    draw.text(
        (left, 35),
        "Comparación pareada de la media del MAE por WSI",
        fill=ink,
        font=_font(48, bold=True),
    )
    draw.text(
        (left, 105),
        "Cada línea representa una WSI; un valor menor indica mejor reconstrucción.",
        fill=muted,
        font=_font(32),
    )

    def y_position(value: float) -> float:
        return plot_bottom - (value - low) / span * (plot_bottom - plot_top)

    for index in range(6):
        value = low + span * index / 5
        y = y_position(value)
        draw.line((plot_left, y, plot_right, y), fill=grid, width=3)
        draw.text(
            (left - 25, y),
            f"{value:.4f}",
            fill=muted,
            font=_font(34),
            anchor="rm",
        )

    for normal_value, so2_value in pairs:
        y_normal, y_so2 = y_position(normal_value), y_position(so2_value)
        draw.line((x_normal, y_normal, x_so2, y_so2), fill="#94a3b8", width=4)
        radius = 10
        normal_box = (
            x_normal - radius,
            y_normal - radius,
            x_normal + radius,
            y_normal + radius,
        )
        draw.ellipse(normal_box, fill=normal)
        draw.ellipse(
            (x_so2 - radius, y_so2 - radius, x_so2 + radius, y_so2 + radius),
            fill=so2,
        )

    draw.text(
        (x_normal, height - 80),
        "VAE base",
        fill=normal,
        font=_font(38, bold=True),
        anchor="mm",
    )
    draw.text(
        (x_so2, height - 80),
        "VAE-SO(2)",
        fill=so2,
        font=_font(38, bold=True),
        anchor="mm",
    )
    image.save(path, optimize=True)


def _render_reconstruction_distributions(summary_path: Path, output_dir: Path) -> None:
    """Draw stored quartiles and min/max with a shared numeric axis per metric."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import to_rgba
    from matplotlib.ticker import FuncFormatter, MaxNLocator

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    metrics = (
        ("mae_norm", "mae", "MAE", "Error absoluto medio (dominio normalizado)"),
        ("mse_norm", "mse", "MSE", "Error cuadrático medio (dominio normalizado)"),
        ("psnr_img", "psnr", "PSNR", "PSNR (dB)"),
        ("ssim_img", "ssim", "SSIM", "Índice de similitud estructural (adimensional)"),
    )
    for key, suffix, title, axis_label in metrics:
        distributions = [
            summary["branches"][branch]["patch_distribution"][key]
            for branch in ("normal", "so2")
        ]
        stats = [
            {"q1": row["q1"], "med": row["median"], "q3": row["q3"],
             "whislo": row["min"], "whishi": row["max"]}
            for row in distributions
        ]
        fig, ax = plt.subplots(figsize=(7.4, 3.0))
        fig.subplots_adjust(left=0.21, right=0.97, bottom=0.28, top=0.80)
        artists = ax.bxp(stats, positions=(2, 1), widths=0.34,
                         orientation="horizontal", patch_artist=True,
                         showfliers=False, manage_ticks=False,
                         medianprops={"linewidth": 2.0},
                         whiskerprops={"linewidth": 1.5},
                         capprops={"linewidth": 1.5})
        for index, color in enumerate(("#2563eb", "#e85d0f")):
            artists["boxes"][index].set(facecolor=to_rgba(color, 0.14),
                                         edgecolor=color, linewidth=1.8)
            artists["medians"][index].set_color(color)
            for name in ("whiskers", "caps"):
                for line in artists[name][2 * index:2 * index + 2]:
                    line.set_color(color)
        low = min(row["min"] for row in distributions)
        high = max(row["max"] for row in distributions)
        padding = 0.05 * (high - low)
        if key == "ssim_img":
            ax.set_xlim(0, 1)
        elif key in ("mae_norm", "mse_norm"):
            ax.set_xlim(0, high + padding)
        else:
            ax.set_xlim(low - padding, high + padding)
        ax.set_ylim(0.5, 2.5)
        ax.set_yticks((2, 1), ("VAE base", "VAE-SO(2)"), fontsize=12)
        ax.xaxis.set_major_locator(MaxNLocator(nbins=6))
        decimals = 2 if key == "mse_norm" else 0 if key == "psnr_img" else 1
        ax.xaxis.set_major_formatter(FuncFormatter(
            lambda value, position, places=decimals:
            f"{value:.{places}f}".replace(".", ",")
        ))
        ax.tick_params(axis="x", labelsize=12)
        ax.tick_params(axis="y", length=0, pad=10)
        ax.set_xlabel(axis_label, fontsize=12, labelpad=10)
        ax.set_title(title, loc="left", fontsize=14, fontweight="bold", pad=12)
        ax.grid(axis="x", color="#dbe3ec", linewidth=0.8)
        ax.set_axisbelow(True)
        for name in ("top", "right", "left"):
            ax.spines[name].set_visible(False)
        ax.spines["bottom"].set_color("#64748b")
        fig.savefig(output_dir / f"vae_test_patch_{suffix}.png", dpi=360)
        plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--research-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    research_root = args.research_root.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    dashboard_path = research_root / "runs/local/professor_metrics_v1/figures/training_dashboard.png"
    with Image.open(dashboard_path).convert("RGB") as dashboard:
        objective = dashboard.crop((35, 120, 935, 505))
        l1 = dashboard.crop((965, 120, 1865, 505))
        ssim = dashboard.crop((35, 505, 935, 920))
        psnr = dashboard.crop((965, 505, 1865, 920))
        equivariance = dashboard.crop((35, 915, 935, 1290))
        learning_rate = dashboard.crop((965, 915, 1865, 1290))
        _stack([objective, l1], output_dir / "vae_training_loss_panels.png")
        _stack([ssim, psnr], output_dir / "vae_training_quality_panels.png")
        _stack(
            [equivariance, learning_rate],
            output_dir / "vae_training_control_panels.png",
        )

    # The accepted report panels are already present in the thesis directory;
    # split that copied raster at its recorded native coordinates.
    thesis_mil = output_dir / "mil_training_development.png"
    with Image.open(thesis_mil).convert("RGB") as mil:
        _save_crop(mil, (0, 140, 1100, 720), output_dir / "mil_training_f1.png")
        _save_crop(mil, (1100, 140, 2200, 720), output_dir / "mil_training_loss.png")
        _save_crop(mil, (300, 830, 1900, 1200), output_dir / "tissue_training_f1.png")

    _render_reconstruction_distributions(
        research_root / "runs/local/vae_test_reconstruction_scored_v1/metrics/overall_summary.json",
        output_dir,
    )

    _render_paired_wsi(
        research_root
        / "runs/local/vae_test_reconstruction_scored_v1/metrics/per_wsi_metrics.csv",
        output_dir / "vae_test_paired_wsi_mae_readable.png",
    )

    # Likewise, separate the confusion matrices from the per-class bars.  The
    # source figure remains untouched and these two views retain its pixels.
    classification_detail = output_dir / "mil_test_confusion_per_class.png"
    with Image.open(classification_detail).convert("RGB") as detail:
        _save_crop(detail, (50, 125, 1755, 735), output_dir / "mil_test_confusions.png")
        _save_crop(
            detail,
            (50, 125, 780, 735),
            output_dir / "mil_test_confusion_normal.png",
        )
        _save_crop(
            detail,
            (900, 125, 1650, 735),
            output_dir / "mil_test_confusion_so2.png",
        )
        _save_crop(detail, (50, 735, 1755, 1425), output_dir / "mil_test_per_class_f1.png")

    spatial_path = research_root / "runs/local/frozen_vae_rotation_orbits/04-spatial-latent-pca.png"
    with Image.open(spatial_path).convert("RGB") as spatial:
        _save_crop(spatial, (20, 110, 950, 1380), output_dir / "latent_spatial_pca_maps.png")
        _save_crop(spatial, (980, 110, 2355, 665), output_dir / "latent_spatial_pca_paired.png")
        _save_crop(spatial, (980, 650, 2355, 1220), output_dir / "latent_spatial_pca_delta.png")

    arrays_path = research_root / (
        "runs/local/decoded_latent_transform_v1/decoded_latent_transform_v1/"
        "selected_images_uint8.npz"
    )
    with np.load(arrays_path) as arrays:
        exports = {
            "reconstruction_zoom_original.png": "normal_vae_rank12_angle0_input",
            "reconstruction_zoom_normal.png": "normal_vae_rank12_angle0_base",
            "reconstruction_zoom_so2.png": "so2_vae_rank12_angle0_base",
            "latent_action_zoom_target.png": "normal_vae_rank12_angle90_action_target",
            "latent_action_zoom_normal.png": "normal_vae_rank12_angle90_action",
            "latent_action_zoom_so2.png": "so2_vae_rank12_angle90_action",
        }
        for filename, key in exports.items():
            _chw_image(arrays[key]).save(output_dir / filename, optimize=True)


if __name__ == "__main__":
    main()
