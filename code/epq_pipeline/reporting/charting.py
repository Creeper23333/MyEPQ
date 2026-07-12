"""Chart rendering for forecast comparison outputs."""

from __future__ import annotations

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path


def draw_forecast_chart(predictions: pd.DataFrame, output_path: Path) -> None:
    plot_df = predictions.tail(min(180, len(predictions))).reset_index(drop=True)
    series = {
        "Actual": (plot_df["actual"].to_numpy(dtype=float), (28, 28, 28)),
        "Rolling": (plot_df["rolling_historical"].to_numpy(dtype=float), (75, 120, 184)),
        "GARCH": (plot_df["garch_1_1"].to_numpy(dtype=float), (210, 102, 45)),
        "Lagged Linear": (plot_df["lagged_linear_regression"].to_numpy(dtype=float), (115, 88, 188)),
        "Random Forest": (plot_df["random_forest"].to_numpy(dtype=float), (44, 145, 95)),
    }
    if "lstm" in plot_df:
        series["LSTM"] = (plot_df["lstm"].to_numpy(dtype=float), (185, 65, 65))

    all_values = np.concatenate([values for values, _ in series.values()])
    min_y = float(np.nanmin(all_values)) * 0.92
    max_y = float(np.nanmax(all_values)) * 1.08
    if max_y <= min_y:
        max_y = min_y + 0.01

    width, height = 1200, 720
    margin_left, margin_right = 90, 40
    margin_top, margin_bottom = 90, 95
    plot_width = width - margin_left - margin_right
    plot_height = height - margin_top - margin_bottom

    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    draw.text((margin_left, 28), "Hyperliquid BTC 30-day Realised Volatility Forecasts", fill=(20, 20, 20), font=font)
    draw.text((margin_left, 52), "Out-of-sample test window, last 180 observations shown", fill=(80, 80, 80), font=font)

    axis_color = (130, 130, 130)
    grid_color = (225, 225, 225)
    draw.line((margin_left, margin_top, margin_left, margin_top + plot_height), fill=axis_color)
    draw.line((margin_left, margin_top + plot_height, margin_left + plot_width, margin_top + plot_height), fill=axis_color)

    for index in range(6):
        y_value = min_y + (max_y - min_y) * index / 5
        y = margin_top + plot_height - int((y_value - min_y) / (max_y - min_y) * plot_height)
        draw.line((margin_left, y, margin_left + plot_width, y), fill=grid_color)
        draw.text((15, y - 6), f"{y_value:.3f}", fill=(80, 80, 80), font=font)

    def point(row_index: int, value: float) -> tuple[int, int]:
        x = margin_left + int(row_index / max(1, len(plot_df) - 1) * plot_width)
        y = margin_top + plot_height - int((value - min_y) / (max_y - min_y) * plot_height)
        return x, y

    for label, (values, color) in series.items():
        points = [point(index, float(value)) for index, value in enumerate(values) if np.isfinite(value)]
        if len(points) > 1:
            draw.line(points, fill=color, width=3 if label == "Actual" else 2)

    legend_x = margin_left
    legend_y = height - 65
    for label, (_, color) in series.items():
        draw.line((legend_x, legend_y + 8, legend_x + 35, legend_y + 8), fill=color, width=4)
        draw.text((legend_x + 44, legend_y), label, fill=(30, 30, 30), font=font)
        legend_x += 170

    first_date = plot_df["date"].iloc[0]
    last_date = plot_df["date"].iloc[-1]
    draw.text((margin_left, height - 35), str(first_date.date()), fill=(80, 80, 80), font=font)
    draw.text((margin_left + plot_width - 80, height - 35), str(last_date.date()), fill=(80, 80, 80), font=font)
    image.save(output_path)

