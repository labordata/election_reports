# NLRB Election Reports, 1968–2011

Scans of the National Labor Relations Board's monthly *N.L.R.B. Election Report: Cases Closed*
(compiled by the NLRB Division of Administration), a U.S. government publication in the public
domain.

Each issue lists every representation election closed that month — union, employer, city and state,
case number, industry, unit, type of election, eligible employees, and votes — with incumbent unions
marked by an asterisk. Each issue also has summary tables for collective-bargaining (RC + RM)
elections:

- **Table 1** — outcome of all collective-bargaining elections and employees eligible to vote
- **Table 3** — elections *involving incumbent unions*
- **Table 7** — elections *involving new organizing* (all collective-bargaining elections minus those
  with an incumbent union), printed in the six-month and fiscal-year summaries
- Tables 2, 4, 8 — valid votes cast; Tables 5–6 — decertification elections

Tables 3 and 7 are the NLRB's own count of organizing in units with no incumbent union, which is
not available from the case-level microdata before 1984.

## Contents

`pdfs/` holds 47 files: single issues (`ER###.pdf`) and library-bound volumes of several issues
(`ER###-###.pdf`). `manifest.csv` lists, for each file, the issues it contains, the months of cases
closed, page count, holding library, HathiTrust and Google Books identifiers, and a SHA-256
checksum.

Issue numbers run one per month (ER-121 = cases closed December 1971), so the months in
`manifest.csv` are computed from issue numbers.

| Period | What is here |
|---|---|
| 1968–1980 | Issues carrying six-month summaries (Jul–Dec / Jan–Jun through 1976; then Oct–Mar / Apr–Sep), plus the July–September 1976 transition-quarter summary: ER-85, 115, 121, 133, 139, 145, 169, 175, 178, 184, 190, 196, 202, 208, 214, 220 |
| May 1980 – June 2000 | Every issue, ER-222 to ER-463, mostly as bound volumes |
| January 2001 – 2011 | Every issue, as born-digital PDFs from nlrb.gov, in `pdfs_nlrb_gov/` (the incumbent table ends in March 2011) |

**Not here:** ER-221 (April 1980); the 1968–1980 monthly issues between summaries (on HathiTrust
but not downloaded); and the issues HathiTrust does not have — ER-87–109 (February 1969 – December
1970), ER-122–132 except 130 (1972), and ER-146–166 (January 1974 – September 1975). The National
Archives holds the full paper run, October 1961 – 2000, unscanned, in Record Group 25: series
[7359690](https://catalog.archives.gov/id/7359690) (1961–1987) and
[7422821](https://catalog.archives.gov/id/7422821) (1988–2000).

See [CODEBOOK.md](CODEBOOK.md) for definitions and known problems — in particular, the incumbent
counts depend on regional office coding practice and are not consistent over time.

## Extracted data

`data/` holds the collective-bargaining summary tables transcribed from these PDFs:

- `data/election_report_periods.csv` — one row per non-overlapping period (six-month or
  transition-quarter summaries where printed, single months otherwise), July 1968 – March 2011, with
  totals and one-union subtotals for all collective-bargaining elections (`all_*`, Table 1), elections
  involving an incumbent union (`inc_*`, Table 3), and new organizing (`new_*`, Table 7, or Table 1
  minus Table 3 where Table 7 isn't printed). Measures are elections (`_n`), elections won (`_won`),
  employees eligible to vote (`_elig`), and eligible in units won (`_elig_won`).
- `data/election_report_fiscal_years.csv` — the same summed to NLRB fiscal years (July–June through
  FY1976, the July–September 1976 transition quarter, then October–September); `complete` marks
  years with every month covered.
- `data/extracted/` — the per-block transcriptions with page references, checks, and notes on
  misprints, corrected reissues, and rows rebuilt from monthly tables where summary pages are missing
  from the scans.

- `data/krislov_1967.csv`, `data/krislov_1970.csv` — Joseph Krislov's published NLRB series of
  elections in units with no prior bargaining agent, FY1955–1966 and FY1949–1966, which precede the
  Election Report summaries (figures only; see the codebook for citations).

`scripts/combine.py` rebuilds the two combined files from `data/extracted/`.

Every figure was read from the page images and checked against the tables' own arithmetic (subtotals
sum to totals; won plus no-representative equals total; Table 7 equals Table 1 minus Table 3). For
complete fiscal years the totals match the RC + RM election counts in the NLRB Annual Reports
exactly in most years; FY1979–81 and FY1989 run 1–5% below the Annual Reports.

## Provenance

The scans are Google Books digitizations of library copies (University of Illinois at
Urbana-Champaign, The Ohio State University, New York Public Library), catalogued in HathiTrust
under record [010360742](https://catalog.hathitrust.org/Record/010360742), and downloaded as full
PDFs from Google Books in October 2026. The OCR text layer is Google's. Pages in the 1990s volumes
are often scanned sideways, so their text layer is scrambled; read those tables from the page images.

The reports are works of the U.S. government and in the public domain. The scans were made by
Google from library copies; Google's attribution page is kept at the front of each PDF. Please
credit the holding libraries, HathiTrust, and Google Books when you use them, and use them for
non-commercial research.

## Related

- Joseph Krislov, "Union Organizing of New Units, 1955–1966," *Industrial and Labor Relations
  Review* 21(1), 1967 — the same NLRB "no prior bargaining agent" series for FY1955–66, from NLRB
  punched-card tabulations.
- Arvil V. Adams and Joseph Krislov, "New Union Organizing," *Quarterly Journal of Economics* 88(2),
  1974 — cites the NLRB Election Reports as the source of new-organizing data for later years.
