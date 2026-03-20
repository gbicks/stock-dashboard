#!/usr/bin/env python3
"""Audit yfinance field availability across representative tickers.

Outputs written to ./data:
- field_samples.json: raw per-ticker field samples and errors
- field_inventory.csv: aggregated field reliability across tickers
- audit_summary.md: human-readable summary with suggested tiers
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yfinance as yf


DEFAULT_TICKERS = ["AAPL", "MSFT", "TSLA", "SPY", "BABA", "PLTR"]
DEFAULT_PERIODS = ["1d", "5d", "1mo", "1y"]


@dataclass
class FieldObservation:
    ticker: str
    source_object: str
    field_name: str
    value_type: str
    non_null: bool
    sample_value: str


def is_nullish(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, float) and str(value) == "nan":
        return True
    if isinstance(value, str) and value.strip() == "":
        return True
    return False


def type_name(value: Any) -> str:
    if value is None:
        return "NoneType"
    return type(value).__name__


def preview_value(value: Any, limit: int = 120) -> str:
    if value is None:
        return "None"
    if isinstance(value, (int, float, bool, str)):
        text = str(value)
    elif isinstance(value, (list, tuple, set)):
        text = f"{type(value).__name__}(len={len(value)})"
    elif isinstance(value, dict):
        text = f"dict(keys={len(value)})"
    else:
        text = type(value).__name__

    if len(text) > limit:
        return text[: limit - 3] + "..."
    return text


def safe_call(label: str, fn):
    try:
        return fn(), None
    except Exception as exc:  # noqa: BLE001
        return None, f"{label}: {exc}"


def extract_dict_fields(ticker: str, source_object: str, payload: dict[str, Any]) -> list[FieldObservation]:
    rows: list[FieldObservation] = []
    for key, value in payload.items():
        rows.append(
            FieldObservation(
                ticker=ticker,
                source_object=source_object,
                field_name=key,
                value_type=type_name(value),
                non_null=not is_nullish(value),
                sample_value=preview_value(value),
            )
        )
    return rows


def extract_history_fields(ticker: str, period: str, history_df) -> list[FieldObservation]:
    rows: list[FieldObservation] = []
    source = f"history:{period}"

    if history_df is None:
        return rows

    row_count = int(len(history_df.index))
    rows.append(
        FieldObservation(
            ticker=ticker,
            source_object=source,
            field_name="__rows__",
            value_type="int",
            non_null=row_count > 0,
            sample_value=str(row_count),
        )
    )

    if row_count == 0:
        return rows

    for col in history_df.columns:
        series = history_df[col]
        first_non_null = None
        for item in series.tolist():
            if not is_nullish(item):
                first_non_null = item
                break

        rows.append(
            FieldObservation(
                ticker=ticker,
                source_object=source,
                field_name=str(col),
                value_type=type_name(first_non_null),
                non_null=first_non_null is not None,
                sample_value=preview_value(first_non_null),
            )
        )

    return rows


def extract_statement_fields(ticker: str, source_object: str, statement_df) -> list[FieldObservation]:
    rows: list[FieldObservation] = []
    if statement_df is None:
        return rows

    row_count = int(len(statement_df.index))
    col_count = int(len(statement_df.columns))

    rows.append(
        FieldObservation(
            ticker=ticker,
            source_object=source_object,
            field_name="__rows__",
            value_type="int",
            non_null=row_count > 0,
            sample_value=str(row_count),
        )
    )
    rows.append(
        FieldObservation(
            ticker=ticker,
            source_object=source_object,
            field_name="__columns__",
            value_type="int",
            non_null=col_count > 0,
            sample_value=str(col_count),
        )
    )

    if row_count == 0 or col_count == 0:
        return rows

    first_col = statement_df.columns[0]
    for idx in statement_df.index.tolist()[:80]:
        value = statement_df.loc[idx, first_col]
        rows.append(
            FieldObservation(
                ticker=ticker,
                source_object=source_object,
                field_name=str(idx),
                value_type=type_name(value),
                non_null=not is_nullish(value),
                sample_value=preview_value(value),
            )
        )

    return rows


def extract_dataframe_column_fields(ticker: str, source_object: str, frame_df) -> list[FieldObservation]:
    rows: list[FieldObservation] = []
    if frame_df is None:
        return rows

    row_count = int(len(frame_df.index))
    col_count = int(len(frame_df.columns))

    rows.append(
        FieldObservation(
            ticker=ticker,
            source_object=source_object,
            field_name="__rows__",
            value_type="int",
            non_null=row_count > 0,
            sample_value=str(row_count),
        )
    )
    rows.append(
        FieldObservation(
            ticker=ticker,
            source_object=source_object,
            field_name="__columns__",
            value_type="int",
            non_null=col_count > 0,
            sample_value=str(col_count),
        )
    )

    if row_count == 0 or col_count == 0:
        return rows

    for col in frame_df.columns.tolist():
        series = frame_df[col]
        first_non_null = None
        for item in series.tolist():
            if not is_nullish(item):
                first_non_null = item
                break

        rows.append(
            FieldObservation(
                ticker=ticker,
                source_object=source_object,
                field_name=str(col),
                value_type=type_name(first_non_null),
                non_null=first_non_null is not None,
                sample_value=preview_value(first_non_null),
            )
        )

    return rows


def aggregate_inventory(observations: list[FieldObservation], ticker_count: int) -> list[dict[str, str]]:
    grouped: dict[tuple[str, str], list[FieldObservation]] = defaultdict(list)
    for obs in observations:
        grouped[(obs.source_object, obs.field_name)].append(obs)

    rows: list[dict[str, str]] = []
    for (source_object, field_name), items in grouped.items():
        seen_tickers = sorted({item.ticker for item in items})
        non_null_count = sum(1 for item in items if item.non_null)
        value_types = sorted({item.value_type for item in items})

        sample_value = ""
        for item in items:
            if item.non_null and item.sample_value:
                sample_value = item.sample_value
                break
        if not sample_value and items:
            sample_value = items[0].sample_value

        rows.append(
            {
                "source_object": source_object,
                "field_name": field_name,
                "seen_in": str(len(seen_tickers)),
                "ticker_count": str(ticker_count),
                "seen_rate": f"{len(seen_tickers) / ticker_count:.2f}",
                "non_null_count": str(non_null_count),
                "non_null_rate": f"{non_null_count / ticker_count:.2f}",
                "value_types": "|".join(value_types),
                "sample_value": sample_value,
            }
        )

    rows.sort(key=lambda row: (row["source_object"], row["field_name"]))
    return rows


def tier_label(rate: float) -> str:
    if rate >= 0.90:
        return "Tier 1"
    if rate >= 0.60:
        return "Tier 2"
    return "Tier 3"


def write_outputs(
    output_dir: Path,
    tickers: list[str],
    errors: dict[str, list[str]],
    raw_samples: dict[str, dict[str, Any]],
    inventory_rows: list[dict[str, str]],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    samples_path = output_dir / "field_samples.json"
    inventory_path = output_dir / "field_inventory.csv"
    summary_path = output_dir / "audit_summary.md"

    with samples_path.open("w", encoding="utf-8") as f:
        json.dump(
            {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "tickers": tickers,
                "errors": errors,
                "samples": raw_samples,
            },
            f,
            indent=2,
            sort_keys=True,
        )

    with inventory_path.open("w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "source_object",
            "field_name",
            "seen_in",
            "ticker_count",
            "seen_rate",
            "non_null_count",
            "non_null_rate",
            "value_types",
            "sample_value",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(inventory_rows)

    top_rows = sorted(
        inventory_rows,
        key=lambda row: (
            float(row["non_null_rate"]),
            float(row["seen_rate"]),
            row["source_object"],
            row["field_name"],
        ),
        reverse=True,
    )

    with summary_path.open("w", encoding="utf-8") as f:
        f.write("# yfinance Field Audit Summary\n\n")
        f.write(f"Generated: {datetime.now(timezone.utc).isoformat()}\n\n")
        f.write(f"Tickers audited: {', '.join(tickers)}\n\n")

        total_error_count = sum(len(v) for v in errors.values())
        f.write(f"Provider/runtime errors observed: {total_error_count}\n\n")

        if total_error_count:
            f.write("## Error Highlights\n")
            for ticker in tickers:
                if errors.get(ticker):
                    f.write(f"- {ticker}: {errors[ticker][0]}\n")
            f.write("\n")

        f.write("## Most Reliable Fields (Top 25 by non_null_rate)\n")
        for row in top_rows[:25]:
            rate = float(row["non_null_rate"])
            tier = tier_label(rate)
            f.write(
                "- "
                f"{row['source_object']}.{row['field_name']} "
                f"| non_null_rate={row['non_null_rate']} "
                f"| seen_rate={row['seen_rate']} "
                f"| {tier}\n"
            )

        f.write("\n## Notes\n")
        f.write("- Tier 1 fields are safest for UI defaults.\n")
        f.write("- Tier 2 fields are useful but need null-safe rendering.\n")
        f.write("- Tier 3 fields are best kept out of primary UI paths.\n")


def run_audit(tickers: list[str], periods: list[str], output_dir: Path) -> None:
    observations: list[FieldObservation] = []
    errors: dict[str, list[str]] = defaultdict(list)
    raw_samples: dict[str, dict[str, Any]] = defaultdict(dict)

    for ticker in tickers:
        stock = yf.Ticker(ticker)

        fast_info, err = safe_call("fast_info", lambda: dict(stock.fast_info))
        if err:
            errors[ticker].append(err)
        else:
            raw_samples[ticker]["fast_info"] = fast_info
            observations.extend(extract_dict_fields(ticker, "fast_info", fast_info))

        info, err = safe_call("info", lambda: stock.info)
        if err:
            errors[ticker].append(err)
        else:
            raw_samples[ticker]["info"] = info
            observations.extend(extract_dict_fields(ticker, "info", info))

        for period in periods:
            history_df, err = safe_call(
                f"history:{period}",
                lambda p=period: stock.history(
                    period=p,
                    interval="1d",
                    auto_adjust=False,
                    prepost=False,
                    actions=False,
                ),
            )
            if err:
                errors[ticker].append(err)
            else:
                raw_samples[ticker][f"history:{period}"] = {
                    "rows": int(len(history_df.index)),
                    "columns": [str(c) for c in history_df.columns.tolist()],
                }
                observations.extend(extract_history_fields(ticker, period, history_df))

        for source_name, getter in [
            ("income_stmt", lambda: stock.income_stmt),
            ("balance_sheet", lambda: stock.balance_sheet),
            ("cashflow", lambda: stock.cashflow),
        ]:
            frame, err = safe_call(source_name, getter)
            if err:
                errors[ticker].append(err)
            else:
                if hasattr(frame, "shape"):
                    raw_samples[ticker][source_name] = {
                        "rows": int(frame.shape[0]),
                        "columns": int(frame.shape[1]),
                    }
                observations.extend(extract_statement_fields(ticker, source_name, frame))

        for source_name, getter in [
            ("recommendations", lambda: stock.recommendations),
            ("actions", lambda: stock.actions),
        ]:
            frame, err = safe_call(source_name, getter)
            if err:
                errors[ticker].append(err)
            else:
                if hasattr(frame, "columns"):
                    raw_samples[ticker][source_name] = {
                        "rows": int(len(frame.index)),
                        "columns": [str(c) for c in frame.columns.tolist()],
                    }
                observations.extend(extract_dataframe_column_fields(ticker, source_name, frame))

    inventory_rows = aggregate_inventory(observations, len(tickers))
    write_outputs(output_dir, tickers, errors, raw_samples, inventory_rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit yfinance field availability across tickers.")
    parser.add_argument(
        "--tickers",
        nargs="+",
        default=DEFAULT_TICKERS,
        help="Ticker symbols to sample (space separated).",
    )
    parser.add_argument(
        "--periods",
        nargs="+",
        default=DEFAULT_PERIODS,
        help="History periods to audit via stock.history.",
    )
    parser.add_argument(
        "--output-dir",
        default="data",
        help="Directory for generated artifacts.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tickers = [ticker.upper() for ticker in args.tickers]
    periods = args.periods
    output_dir = Path(args.output_dir)

    run_audit(tickers=tickers, periods=periods, output_dir=output_dir)
    print(f"Audit complete. Outputs written to: {output_dir}")


if __name__ == "__main__":
    main()
