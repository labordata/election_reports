"""Combine the per-block extractions into one non-overlapping period series and fiscal-year totals.

Each block CSV in data/extracted/ has summary rows (six- or three-month) and monthly rows for months
no summary in that block covered, plus fiscal-year rows that are only checks. Blocks overlap at
their edges, so: keep every summary row, drop monthly rows for months any summary covers, and
fail loudly if a month is still covered twice.
"""

import glob
import pathlib

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
MEASURES = ["n", "won", "elig", "elig_won"]
GROUPS = ["all", "all_1u", "inc", "inc_1u", "new", "new_1u"]
COLS = [f"{g}_{m}" for g in GROUPS for m in MEASURES]


def months(start, end):
    return list(pd.period_range(start, end, freq="M"))


def fiscal_year(month):
    """NLRB fiscal year: July-June through FY1976, the Jul-Sep 1976 transition quarter, then Oct-Sep."""
    if month < pd.Period("1976-07", "M"):
        return str((month + 6).year)
    if month < pd.Period("1976-10", "M"):
        return "1976TQ"
    return str((month + 3).year)


def case_system(period_end):
    """Case-tracking system the NLRB compiled the reports from (boundaries approximate; see CODEBOOK)."""
    if period_end <= "1984-09":
        return "pre-CHIPS"
    if period_end <= "2000-09":
        return "CHIPS"
    return "CATS"


# Six-month rows that are not straight transcriptions of a printed summary table. Keys are
# (period_start, period_end). See data/extracted/*.md for the details of each.
PROVENANCE = {
    ("1978-10", "1979-03"): "printed_errata",  # ER-214 reprints corrected tables replacing ER-208's
    ("1981-10", "1982-03"): "printed_corrected_reissue",  # ER-244-C replaces ER-244
    ("1994-04", "1994-09"): "rebuilt_from_monthly",
    ("1994-10", "1995-03"): "printed_second_copy",
    ("1995-04", "1995-09"): "printed_second_copy",
    ("1995-10", "1996-03"): "printed_second_copy",
    ("1996-10", "1997-03"): "rebuilt_from_monthly",
    ("1997-04", "1997-09"): "rebuilt_from_monthly",
    ("1998-10", "1999-03"): "rebuilt_from_monthly",
    ("1999-04", "1999-09"): "derived_from_fiscal_year",
}

# er_fill_* only confirms rows already in other blocks; er_2000_2001 found nothing new.
SKIP = {"er_fill_1994_1999", "er_2000_2001"}
rows = pd.concat(
    [
        pd.read_csv(f, dtype=str).assign(block=pathlib.Path(f).stem)
        for f in sorted(glob.glob(str(ROOT / "data/extracted/*.csv")))
        if pathlib.Path(f).stem not in SKIP
    ],
    ignore_index=True,
)
for c in COLS:
    rows[c] = pd.to_numeric(rows[c], errors="coerce")

summaries = rows[rows.basis.isin(["six_month_summary", "three_month_summary"])]
summaries = summaries.drop_duplicates(["period_start", "period_end"])
covered = {m for _, r in summaries.iterrows() for m in months(r.period_start, r.period_end)}

monthly = rows[rows.basis == "monthly"]
monthly = monthly[[pd.Period(r.period_start, "M") not in covered for _, r in monthly.iterrows()]]
monthly = monthly.drop_duplicates(["period_start"])

periods = pd.concat([summaries, monthly]).sort_values("period_start").reset_index(drop=True)

seen = {}
for _, r in periods.iterrows():
    for m in months(r.period_start, r.period_end):
        assert m not in seen, f"{m} covered by both {seen[m]} and {r.issue}"
        seen[m] = r.issue

# new organizing = all collective-bargaining elections minus those involving an incumbent,
# where Table 7 wasn't printed
for m in MEASURES:
    periods[f"new_{m}"] = periods[f"new_{m}"].fillna(periods[f"all_{m}"] - periods[f"inc_{m}"])
    periods[f"new_1u_{m}"] = periods[f"new_1u_{m}"].fillna(periods[f"all_1u_{m}"] - periods[f"inc_1u_{m}"])

periods["fiscal_year"] = [fiscal_year(pd.Period(s, "M")) for s in periods.period_start]
assert all(fiscal_year(pd.Period(e, "M")) == fy for e, fy in zip(periods.period_end, periods.fiscal_year))
periods["n_months"] = [len(months(s, e)) for s, e in zip(periods.period_start, periods.period_end)]
periods["provenance"] = [PROVENANCE.get((s, e), "printed") for s, e in zip(periods.period_start, periods.period_end)]
periods["case_system"] = periods.period_end.map(case_system)
periods["source"] = ["nlrb.gov" if b == "er_2001_2011" else "scan" for b in periods.block]

keep = ["fiscal_year", "period_start", "period_end", "n_months", "basis", "issue", "source_file", "source", "provenance", "case_system", *COLS, "new_source", "checks", "block"]
periods[keep].to_csv(ROOT / "data/election_report_periods.csv", index=False)

fy = periods.groupby("fiscal_year", sort=False).agg(
    n_months=("n_months", "sum"),
    issues=("issue", lambda s: " ".join(s.fillna(""))),
    provenance=("provenance", lambda s: ",".join(sorted(set(s)))),
    case_system=("case_system", lambda s: ",".join(sorted(set(s)))),
    **{c: (c, lambda s: s.sum(min_count=len(s))) for c in COLS},
)
fy["complete"] = fy.n_months.eq(12) | (fy.index == "1976TQ") & fy.n_months.eq(3)
fy.reset_index().to_csv(ROOT / "data/election_report_fiscal_years.csv", index=False)

gaps = [str(m) for m in months("1968-07", "2011-03") if m not in seen]
print(f"{len(periods)} periods, {len(seen)} months covered; missing {len(gaps)} months:")
print(pd.Series(gaps).groupby(pd.Series([g[:4] for g in gaps])).agg(lambda s: f"{s.iloc[0]}..{s.iloc[-1]}").to_string())
print(fy[["n_months", "complete", "all_n", "inc_n", "new_n", "all_elig", "inc_elig", "new_elig", "new_elig_won"]].to_string())
