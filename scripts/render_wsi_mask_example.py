#!/usr/bin/env python3
"""Create the thesis WSI/mask example without loading the full mask in RAM.

The UBC-OCEAN supplemental masks can exceed 300 million pixels.  This script
decodes the non-interlaced RGB PNG row by row, reproduces the patch-level
10 % annotation / 95 % purity rule, and writes compact figure assets.
"""

from __future__ import annotations

import argparse
import struct
import zlib
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


PATCH_SIZE = 256
CLASS_COLORS = np.asarray(((255, 0, 0), (0, 170, 0), (0, 70, 255)), dtype=np.uint8)


def _png_header(path: Path) -> tuple[int, int]:
    with path.open("rb") as stream:
        if stream.read(8) != b"\x89PNG\r\n\x1a\n":
            raise ValueError(f"Not a PNG file: {path}")
        length, kind = struct.unpack(">I4s", stream.read(8))
        if length != 13 or kind != b"IHDR":
            raise ValueError("PNG does not begin with IHDR")
        width, height, depth, color_type, compression, filtering, interlace = struct.unpack(
            ">IIBBBBB", stream.read(13)
        )
    if (depth, color_type, compression, filtering, interlace) != (8, 2, 0, 0, 0):
        raise ValueError("Expected a non-interlaced, 8-bit RGB PNG mask")
    return width, height


def _idat_chunks(path: Path):
    with path.open("rb") as stream:
        stream.read(8)
        while True:
            header = stream.read(8)
            if not header:
                return
            length, kind = struct.unpack(">I4s", header)
            payload = stream.read(length)
            stream.read(4)  # CRC; the PNG decoder that produced the source verified it.
            if kind == b"IDAT":
                yield payload
            if kind == b"IEND":
                return


def _unfilter_row(encoded: bytes, previous: np.ndarray) -> np.ndarray:
    filter_type = encoded[0]
    filtered = np.frombuffer(encoded, dtype=np.uint8, offset=1).copy()
    if filter_type == 0:
        return filtered
    if filter_type == 1:
        # PNG Sub filter.  Channels form three independent prefix sums modulo 256.
        for channel in range(3):
            filtered[channel::3] = np.cumsum(
                filtered[channel::3], dtype=np.uint32
            ).astype(np.uint8)
        return filtered
    if filter_type == 2:
        return (filtered.astype(np.uint16) + previous).astype(np.uint8)
    raise ValueError(f"Unsupported PNG row filter {filter_type}; expected 0, 1, or 2")


def decode_mask(
    path: Path, target_width: int
) -> tuple[Image.Image, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    width, height = _png_header(path)
    target_height = round(height * target_width / width)
    source_x = np.minimum(
        ((np.arange(target_width) + 0.5) * width / target_width).astype(np.int64),
        width - 1,
    )
    source_y = np.minimum(
        ((np.arange(target_height) + 0.5) * height / target_height).astype(np.int64),
        height - 1,
    )
    target_rows: dict[int, list[int]] = {}
    for output_y, input_y in enumerate(source_y.tolist()):
        target_rows.setdefault(input_y, []).append(output_y)
    reduced = np.zeros((target_height, target_width, 3), dtype=np.uint8)

    grid_width = width // PATCH_SIZE
    grid_height = height // PATCH_SIZE
    annotated = np.zeros((grid_height, grid_width), dtype=np.uint32)
    class_counts = np.zeros((3, grid_height, grid_width), dtype=np.uint32)

    stride = width * 3 + 1
    decompressor = zlib.decompressobj()
    pending = bytearray()
    previous = np.zeros(width * 3, dtype=np.uint8)
    row_number = 0

    def consume_rows() -> None:
        nonlocal pending, previous, row_number
        while len(pending) >= stride and row_number < height:
            encoded = bytes(pending[:stride])
            del pending[:stride]
            row = _unfilter_row(encoded, previous)
            previous = row
            rgb = row.reshape(width, 3)

            for output_y in target_rows.get(row_number, ()):
                reduced[output_y] = rgb[source_x]

            if row_number < grid_height * PATCH_SIZE:
                patch_row = row_number // PATCH_SIZE
                grid = rgb[: grid_width * PATCH_SIZE].reshape(grid_width, PATCH_SIZE, 3)
                red, green, blue = grid[..., 0], grid[..., 1], grid[..., 2]
                nonblack = (red > 0) | (green > 0) | (blue > 0)
                annotated[patch_row] += nonblack.sum(axis=1, dtype=np.uint32)
                class_counts[0, patch_row] += (
                    nonblack & (red >= green) & (red >= blue)
                ).sum(axis=1, dtype=np.uint32)
                class_counts[1, patch_row] += (
                    nonblack & (green >= red) & (green >= blue)
                ).sum(axis=1, dtype=np.uint32)
                class_counts[2, patch_row] += (
                    nonblack & (blue >= red) & (blue >= green)
                ).sum(axis=1, dtype=np.uint32)
            row_number += 1

    for chunk in _idat_chunks(path):
        compressed = chunk
        while compressed:
            output = decompressor.decompress(compressed, stride * 8)
            compressed = decompressor.unconsumed_tail
            pending.extend(output)
            consume_rows()
            if not compressed and not output:
                break
    pending.extend(decompressor.flush())
    consume_rows()
    if row_number != height:
        raise ValueError(f"Decoded {row_number} mask rows; expected {height}")

    return Image.fromarray(reduced, "RGB"), annotated, class_counts, source_x, source_y


def render(
    thumbnail_path: Path,
    mask_path: Path,
    output_directory: Path,
    target_width: int,
) -> None:
    output_directory.mkdir(parents=True, exist_ok=True)
    mask, annotated, class_counts, _, _ = decode_mask(mask_path, target_width)
    target_height = mask.height

    with Image.open(thumbnail_path) as source_thumbnail:
        thumbnail = source_thumbnail.convert("RGB").resize(
            (target_width, target_height), Image.Resampling.LANCZOS
        )

    faded = Image.blend(thumbnail, Image.new("RGB", thumbnail.size, "white"), 0.58)
    overlay = faded.convert("RGBA")
    cells = Image.new("RGBA", overlay.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(cells)
    slide_width, slide_height = _png_header(mask_path)
    patch_area = PATCH_SIZE * PATCH_SIZE

    for patch_y in range(annotated.shape[0]):
        for patch_x in range(annotated.shape[1]):
            annotated_count = int(annotated[patch_y, patch_x])
            if annotated_count < 0.10 * patch_area:
                continue
            counts = class_counts[:, patch_y, patch_x]
            winner = int(np.argmax(counts))
            if int(counts[winner]) < 0.95 * annotated_count:
                continue
            x0 = round(patch_x * PATCH_SIZE * target_width / slide_width)
            y0 = round(patch_y * PATCH_SIZE * target_height / slide_height)
            x1 = round((patch_x + 1) * PATCH_SIZE * target_width / slide_width)
            y1 = round((patch_y + 1) * PATCH_SIZE * target_height / slide_height)
            color = tuple(int(value) for value in CLASS_COLORS[winner])
            draw.rectangle((x0, y0, x1, y1), fill=(*color, 132), outline=(*color, 230), width=1)

    overlay = Image.alpha_composite(overlay, cells).convert("RGB")
    thumbnail.save(output_directory / "wsi_11557_thumbnail.png", optimize=True)
    mask.save(output_directory / "wsi_11557_mask.png", optimize=True)
    overlay.save(output_directory / "wsi_11557_patch_overlay.png", optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("thumbnail", type=Path)
    parser.add_argument("mask", type=Path)
    parser.add_argument("output_directory", type=Path)
    parser.add_argument("--width", type=int, default=640)
    args = parser.parse_args()
    render(args.thumbnail, args.mask, args.output_directory, args.width)


if __name__ == "__main__":
    main()
