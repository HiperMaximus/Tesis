#!/usr/bin/env python3
"""Export accepted tissue and corrected-orbit results for the thesis."""

import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT.parent / "equivariant-vae"
TISSUE = RESEARCH / "runs/local/tissue_test_scored_v1/overall_status.json"
GEOMETRY = RESEARCH / "runs/local/corrected_rotation_geometry_v1/corrected_rotation_geometry_v1/rotation_geometry_summary.json"
BUDGETS = (250, 500, 1000, 2500, 5671)
BRANCHES = ("normal_vae", "so2_vae")
NAMES = {"normal_vae": "VAE base", "so2_vae": "VAE-SO(2)"}
CLASSES = ("Tumor", "Estroma", "Necrosis")
OUTPUTS = []


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def number(value, decimals=3):
    return f"{value:.{decimals}f}".replace(".", ",")


def integer(value):
    return f"{value:,}".replace(",", r"\,")


def write(relative, text):
    path = ROOT / "thesis" / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n")
    OUTPUTS.append(path)


def table(caption, short, label, spec, header, rows):
    return "\n".join([
        r"\begin{table}[htbp]", r"    \centering",
        f"    \\caption[{short}]{{{caption}}}", f"    \\label{{{label}}}",
        r"    \small", f"    \\begin{{tabular}}{{@{{}}{spec}@{{}}}}",
        r"        \toprule", "        " + header + r" \\", r"        \midrule",
        *["        " + row + r" \\" for row in rows],
        r"        \bottomrule", r"    \end{tabular}", r"\end{table}",
    ])


def class_rows(tissue, budgets):
    rows = []
    for budget in budgets:
        for branch in BRANCHES:
            metrics = tissue["branch_results"][branch]["budgets"][str(budget)]["metrics"]
            for label, row in zip(CLASSES, metrics["per_class"]):
                rows.append(" & ".join([
                    rf"\({integer(budget)}\)", NAMES[branch], label,
                    number(row["precision"]), number(row["recall"]),
                    number(row["f1"]), rf"\({integer(row['support'])}\)",
                ]))
    return rows


def confusion(tissue, budget):
    fig, axes = plt.subplots(1, 2, figsize=(8.5, 4.3))
    fig.subplots_adjust(left=0.12, right=0.97, top=0.88, bottom=0.30, wspace=0.55)
    for ax, branch in zip(axes, BRANCHES):
        metrics = tissue["branch_results"][branch]["budgets"][str(budget)]["metrics"]
        counts = np.asarray(metrics["confusion_matrix"])
        percentages = counts / counts.sum(axis=1, keepdims=True) * 100
        im = ax.imshow(percentages, cmap="Blues", vmin=0, vmax=100)
        ax.set_xticks(range(3), CLASSES, fontsize=10)
        ax.set_yticks(range(3), CLASSES, fontsize=10)
        ax.set_xlabel("Clase predicha", fontsize=11)
        ax.set_ylabel("Clase de referencia", fontsize=11)
        ax.set_title("VAE base" if branch == "normal_vae" else "VAE-SO(2)", fontsize=13)
        for row in range(3):
            for column in range(3):
                annotation = f"{counts[row, column]:,}".replace(",", " ") + "\n" + number(percentages[row, column], 1) + "%"
                ax.text(column, row, annotation, ha="center", va="center", fontsize=11,
                        color="white" if percentages[row, column] > 55 else "black")
    cax = fig.add_axes((0.25, 0.11, 0.50, 0.04))
    fig.colorbar(im, cax=cax, orientation="horizontal", ticks=(0, 25, 50, 75, 100))
    cax.set_xlabel("Porcentaje dentro de la clase de referencia", fontsize=11)
    output = ROOT / f"thesis/figures/experiments/tissue_confusion_budget_{budget}.png"
    fig.savefig(output, dpi=360, bbox_inches="tight", pad_inches=0.10)
    plt.close(fig)
    OUTPUTS.append(output)


def main():
    tissue = json.loads(TISSUE.read_text())
    geometry = json.loads(GEOMETRY.read_text())
    if tissue["status"] != "complete":
        raise ValueError("Tissue scoring is incomplete")
    if sha(GEOMETRY) != "aab68ca5b7cbe989ea1cd79740a64d83784441f85ffde09a6ee6ebebe7faf43c":
        raise ValueError("Corrected geometry does not match the accepted summary")
    for relative, meta in tissue["artifacts"].items():
        if sha(TISSUE.parent / relative) != meta["sha256"]:
            raise ValueError(f"Tissue artifact checksum mismatch: {relative}")
    rows = []
    for budget in BUDGETS:
        for branch in BRANCHES:
            m = tissue["branch_results"][branch]["budgets"][str(budget)]["metrics"]
            rows.append(" & ".join([rf"\({integer(budget)}\)", NAMES[branch],
                                    number(m["accuracy"]), number(m["balanced_accuracy"]),
                                    number(m["mean_cross_entropy"])]))
        confusion(tissue, budget)
    write("tables/tissue_global_metrics.tex", table(
        r"Métricas secundarias de segmentación en las mismas \(31\,572\) celdas de prueba. La exactitud es la fracción de aciertos; la exactitud balanceada es el promedio de la sensibilidad de las tres clases. La entropía cruzada es el promedio no ponderado por parche y mejora al disminuir; las otras dos medidas mejoran al aumentar.",
        "Métricas secundarias de segmentación por presupuesto.", "tab:tejido-metricas-secundarias", "rlrrr",
        r"Etiquetas/clase & Modelo & Exactitud & Exactitud bal. & Entropía cruzada", rows))
    write("tables/tissue_full_per_class.tex", table(
        r"Precisión, sensibilidad y F1 por clase en segmentación con \(5\,671\) etiquetas por clase. El soporte es el número de celdas de referencia; necrosis proviene de cinco WSI.",
        "Métricas por clase con el presupuesto completo.", "tab:tejido-clases-completo", "rllrrrr",
        "Etiquetas/clase & Modelo & Clase & Precisión & Sensibilidad & F1 & Soporte",
        class_rows(tissue, (5671,))))
    for budgets in ((250, 500), (1000, 2500)):
        tag = f"{budgets[0]}-{budgets[1]}"
        write(f"tables/tissue_classes_{tag}.tex", table(
            rf"Resultados por clase con \({integer(budgets[0])}\) y \({integer(budgets[1])}\) etiquetas por clase. Los soportes son los mismos para todos los modelos y presupuestos.",
            f"Resultados por clase: presupuestos {budgets[0]} y {budgets[1]}.", f"tab:tejido-clases-{tag}", "rllrrrr",
            "Etiquetas/clase & Modelo & Clase & Precisión & Sensibilidad & F1 & Soporte",
            class_rows(tissue, budgets)))
    rows = []
    for budget in BUDGETS:
        comparison = tissue["paired_normal_minus_so2"]["budgets"][str(budget)]
        for key, label in (("accuracy", "Exactitud"), ("balanced_accuracy", "Exactitud balanceada"),
                           ("mean_cross_entropy", "Entropía cruzada")):
            interval = comparison["pointwise_percentile_95"][key]
            rows.append(" & ".join([rf"\({integer(budget)}\)", label,
                rf"\({number(comparison['estimates'][key])}\)",
                rf"\([{number(interval['lower'])};{number(interval['upper'])}]\)"]))
    write("tables/tissue_secondary_intervals.tex", table(
        r"Diferencias VAE base menos VAE-\(\mathrm{SO}(2)\) e intervalos percentiles puntuales del 95\% para métricas secundarias. Se obtuvieron con el mismo bootstrap pareado y estratificado por WSI de la comparación primaria. Son intervalos exploratorios sin ajuste simultáneo.",
        "Diferencias e intervalos exploratorios de métricas secundarias.", "tab:tejido-secundarias-intervalos", "rlrr",
        r"Etiquetas/clase & Métrica & Diferencia & IC puntual 95\%", rows))
    med = lambda values: float(np.median(values))
    branches = [geometry["branches"][branch] for branch in BRANCHES]
    metric_rows = []
    for key, label in (("step_rms", r"RMS media de \(\Delta\mathbf z\)"),
                       ("second_rms", r"RMS media de \(\Delta^2\mathbf z\)")):
        metric_rows.append((label, [med(np.asarray(v["geometry"]["1"][key]).mean(axis=1)) for v in branches]))
    metric_rows.append(("Longitud RMS acumulada", [med(v["geometry"]["1"]["path_length"]) for v in branches]))
    for key, label in (("path_length", "Longitud relativa a la órbita RGB"),
                       ("local_linearity_ratio", "Linealidad local relativa a RGB"),
                       ("curvature_median", "Curvatura mediana relativa a RGB")):
        m = geometry["comparisons"][key]
        metric_rows.append((label, [m["normal_median"], m["so2_median"]]))
    harmonics = geometry["comparisons"]["harmonics"]
    metric_rows += [
        ("Fracción de energía en armónicos 1--6", [med(harmonics[f"{b}_low_fraction"]) for b in ("normal", "so2")]),
        ("Número efectivo de frecuencias", [med(harmonics[f"{b}_effective_count"]) for b in ("normal", "so2")]),
        ("Fracción de variación capturada por PC1--PC6", [med([r["cumulative_explained"][5] for r in v["local_pca"]]) for v in branches]),
    ]
    for threshold in (90, 95, 99):
        metric_rows.append((rf"Direcciones tangentes para el {threshold}\%", [med([r[f"span_dimension_{threshold}"] for r in v["tangents"]]) for v in branches]))
    metric_rows.append(("Fracción de energía tangente local en una dirección", [med([r["local_rank1_fraction"] for r in v["tangents"]]) for v in branches]))
    write("tables/orbit_descriptors.tex", table(
        r"Descriptores de las órbitas corregidas, muestreadas cada grado en los 25 parches fijos de validación. Cada cifra es una mediana entre parches. Las RMS de diferencias se promedian primero sobre los 360 ángulos; las razones respecto a RGB se calculan por parche antes de resumir. Las fracciones de energía armónica se refieren a la variación de la órbita latente completa.",
        "Descriptores de órbita y subespacios tangentes.", "tab:descriptores-orbitas", "lrr",
        r"Descriptor & VAE base & VAE-\(\mathrm{SO}(2)\)",
        [" & ".join([label] + [number(v, 0 if "Direcciones" in label else 3) for v in values]) for label, values in metric_rows]))
    provenance = {
        "tissue_summary": {"path":str(TISSUE.relative_to(RESEARCH)), "sha256":sha(TISSUE)},
        "corrected_geometry_summary": {"path":str(GEOMETRY.relative_to(RESEARCH)), "sha256":sha(GEOMETRY)},
        "derivation": "Stored accepted metrics; row-normalized confusion colors; medians and angle means of stored corrected geometry, without new inference.",
        "geometry_table_unrounded": dict(metric_rows),
        "outputs": {str(path.relative_to(ROOT / 'thesis')):sha(path) for path in OUTPUTS},
    }
    qa = ROOT / "build/thesis/revision-punto-09"
    qa.mkdir(parents=True, exist_ok=True)
    (qa / "source_output_audit.json").write_text(json.dumps(provenance, indent=2) + "\n")
    print(json.dumps({"outputs":provenance["outputs"]}, indent=2))


if __name__ == "__main__":
    main()
