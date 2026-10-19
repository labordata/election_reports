# Codebook

The data in `data/` record what the NLRB Election Reports printed. Nothing is adjusted or modeled. This
codebook documents what the numbers mean and where they are unreliable.

## Files

| File | One row per |
|---|---|
| `data/election_report_periods.csv` | non-overlapping reporting period (six-month or three-month summary where printed, otherwise one month) |
| `data/election_report_fiscal_years.csv` | NLRB fiscal year, summed from the periods |
| `data/extracted/*.csv` | period as transcribed, per block of reports, including overlapping and fiscal-year check rows |
| `data/extracted/*.md` | transcription notes for each block: page locations, misprints, OCR corrections, reissues |
| `data/alternate_google_copies.csv` | other Google Books scans of the same issues (not used, except as noted) |
| `manifest.csv` | the PDFs in `pdfs/`, with issue numbers, months, holding library, identifiers, checksums |
| `data/krislov_1967.csv` | fiscal year, FY1955–1966: Krislov's new-organizing series (see below) |
| `data/krislov_1970.csv` | fiscal year, FY1949–1966: Krislov's employees in new units choosing a union, by industry |

`scripts/combine.py` builds the two combined files from `data/extracted/`.

## Coverage

Cases closed July 1968 – March 2011, with gaps where no copy has been found: calendar 1969–1970,
January–June 1972, January 1974 – June 1975, and July–September 2000.

- 1968–1980: single issues carrying six-month summaries (scans).
- May 1980 – June 2000: every issue (scans, mostly bound volumes).
- January 2001 – March 2011: every issue (born-digital PDFs from nlrb.gov, in `pdfs_nlrb_gov/`).
  After March 2011 the reports no longer print the incumbent table.

The National Archives holds the full paper run from October 1961 (RG 25, series 7359690 and 7422821),
which would fill the gaps and the years before 1968.

## Universe

Every figure is for **collective-bargaining elections**: RC (union or employee petition) and RM (employer
petition) elections, excluding decertification (RD) elections, in **cases closed** in the period, as
**certified** after objections and challenges. Elections whose results were never certified, such as
petitions withdrawn after the vote, are not counted.

## Columns

Measures are prefixed by group and suffixed by measure.

| Group | Report table | Meaning |
|---|---|---|
| `all_` | Table 1 | all collective-bargaining elections |
| `inc_` | Table 3 | elections **involving an incumbent union**, i.e. a union the report marks with an asterisk as the incumbent |
| `new_` | Table 7 | "new organizing": all elections minus those involving an incumbent. Printed in summaries; where only monthly tables exist it is computed as Table 1 minus Table 3 (`new_source` blank) |
| `*_1u_` | the "One Union Elections" subtotal of the same table | elections with only one union on the ballot |

| Suffix | Meaning |
|---|---|
| `_n` | elections |
| `_won` | elections won by a union |
| `_elig` | employees eligible to vote |
| `_elig_won` | employees eligible to vote in units where a union won |

Other columns in `election_report_periods.csv`:

- `fiscal_year` — NLRB fiscal year: July–June through FY1976, `1976TQ` for the July–September 1976
  transition quarter, then October–September.
- `period_start`, `period_end` (YYYY-MM, inclusive), `n_months`.
- `basis` — `six_month_summary`, `three_month_summary`, or `monthly`.
- `issue`, `source_file` — the issue (ER-number) and file the figures were read from. From 2005 the
  NLRB numbers issues ER-YYYYMM; some 2001–2004 issues carry no number.
- `source` — `scan` (Google Books scan) or `nlrb.gov` (born-digital PDF).
- `provenance`:
  - `printed` — transcribed from the printed summary or monthly table.
  - `printed_errata` — Oct 1978–Mar 1979: corrected tables reprinted in ER-214, replacing ER-208's,
    which were about a third lower.
  - `printed_corrected_reissue` — Oct 1981–Mar 1982: from the corrected reissue ER-244-C.
  - `printed_second_copy` — Oct 1994–Mar 1996 (three half-years): summary pages missing from our scan
    were read from another library's copy (`pdfs/ER397-414_alt.pdf`); they match values rebuilt from
    the monthly tables exactly.
  - `rebuilt_from_monthly` — Apr–Sep 1994, Oct 1996–Sep 1997, Oct 1998–Mar 1999: the summary's
    Table 1 and Table 3 pages are missing from every copy found; incumbent figures are the sum of the
    monthly Table 3s and all = printed Table 7 + incumbent. Where this could be tested, rebuilt and
    printed values agree exactly.
  - `derived_from_fiscal_year` — Apr–Sep 1999: no summary table survives; all = the fiscal-year
    summary minus Oct 1998–Mar 1999, incumbent = sum of monthly Table 3s, no one-union breakdown.
- `case_system` — the NLRB case-tracking system the report was compiled from: `pre-CHIPS` (through
  FY1984), `CHIPS` (FY1985–FY2000), `CATS` (FY2001–FY2011). The boundaries are approximate.
- `checks` — `ok` if the period passes the arithmetic checks below, otherwise what failed.
- `block` — which `data/extracted/` file the row came from.

`election_report_fiscal_years.csv` sums the periods by fiscal year; `complete` marks years with every
month covered, and `provenance` and `case_system` list the values of the periods in that year.

## Checks

Every period was checked against the page image (or, for nlrb.gov PDFs, the text layer with spot
checks against images) and against the tables' own arithmetic: the one/two/three-or-more-union
subtotals sum to the total; elections won plus no-representative-chosen equal total elections; eligible
in won units plus eligible in lost units equal total eligible; and Table 7 equals Table 1 minus
Table 3.

## Known problems

### The incumbent flag depends on regional office coding practice

`inc_` (and so `new_`) counts elections the regional offices coded as involving an incumbent. Offices
coded this very differently, and the practice changed with the case-tracking system. **`inc_` is not
consistent over time, and the change in 2001 is mostly a coding change, not a change in raiding.**

- **CHIPS era (about FY1985–2000): likely undercount.** In the CHIPS case data, several offices left
  the incumbent field blank on 96–98% of elections (Regions 7, 20, 6, 26, 10), and others coded most
  single-union elections as "incumbent union not on ballot" (Regions 22, 28, 17, 20), which the printed
  Table 3 does not count. The printed one-union incumbent share (about 1–6% of elections) matches
  CHIPS's "incumbent on ballot" codes with blanks counted as none.
- **CATS era (FY2001–2011): large overcount.** The printed share jumps from about 1–3% of elections
  (1997–2000) to 13–16% (2001–2004). The asterisks agree with CATS's incumbent flag, and the flags are
  concentrated in a few offices: Regions 20, 31, 22, 32, and 34 flag 26–42% of their single-union
  elections, against 0.5–3% in Regions 1, 8, 10, 11, 12, and 30. In 89–95% of flagged cases CATS
  records only one union in the case, so the flagged "incumbent" is the petitioning union. In offices
  that code carefully, about 2–5% of single-union elections involve an incumbent, continuous with the
  1990s.
- **Pre-CHIPS (1968–1984):** office practice has not been examined. The case listings in the scanned
  issues mark incumbents with asterisks and could be used to check.

### What a single-union "incumbent" election is

An incumbent can be the only union on the ballot. These elections are counted in `inc_`, not `new_`:

- **Section 8(f) conversions.** Construction employers may sign pre-hire agreements with a union
  without a showing of majority support (NLRA §8(f)). Such agreements can be repudiated at expiration
  (*John Deklewa & Sons*, 1987), so building-trades unions petition for an election to gain full
  majority (§9(a)) status. The union is both petitioner and incumbent; the workers are already
  covered. These cluster in construction and sometimes come in campaigns, e.g. Steamfitters Local 602
  in Region 5, October–November 2010 (28 elections, about 1,730 eligible).
- **Certification of an existing voluntary recognition.** No new workers are covered.
- **Self-determination ("Armour-Globe") elections**, in which unrepresented employees vote on joining
  an existing unit. These do add newly represented workers but are counted with the incumbent cases.

Raids — an incumbent on the ballot against a challenger — are mostly the multi-union incumbent
elections (`inc_n` minus `inc_1u_n`).

### Summary and monthly tables disagree from FY2005

Through September 2004 the printed six-month summaries equal the sum of the monthly tables. From
October 2004 the summaries show about 1–3% more elections and often fewer incumbent elections (Apr–Sep
2005: 108 incumbent elections in the summary, 139 summed from the months), apparently a different data
vintage. The combined files use the summaries.

### Fiscal-year summary pages are preliminary

The one-page "Fiscal Year Summary of Elections" printed in some issues is marked "preliminary, before
adjustments" and gives only incumbent versus no-incumbent totals. These pages are used only as checks
(rows with `basis = fiscal_year_summary` in `data/extracted/`), except to derive Apr–Sep 1999.

### Comparison with the NLRB Annual Reports

For complete fiscal years, `all_n` and `all_elig` match the Annual Reports' RC + RM election counts
exactly in most years. Exceptions: FY1979 (340 fewer elections), FY1980 (71 fewer), FY1981 (102
fewer), and FY1989 (122 fewer), and FY1973 eligible employees (578 fewer). The Annual Reports were
compiled later and probably include late certifications.

### Misprints in the original

- Apr–Sep 1977 (ER-190): Table 7 is 2 elections and 1,921 eligible short of Table 1 minus Table 3,
  all in two-union rows. Recorded as printed.
- FY1989 fiscal-year page: no-incumbent elections printed 3,640, a transposition of 3,460.
- FY1976: the preliminary fiscal-year page differs from the sum of its halves by 2 elections.
- Further OCR corrections and page-level notes are in `data/extracted/*.md`.

### Large single elections

A few very large elections move half-year figures. Example: an 18,200-eligible three-union election in
Oct 1983–Mar 1984, counted as new organizing.

## Krislov's series, FY1949–1966

Two files hold the figures Joseph Krislov published from NLRB special tabulations of its punched-card
records of representation petitions, from which "election cards in which the petition indicated
existence of a prior bargaining agent were eliminated." They are transcribed as printed, with the same
column names as the Election Report data:

- `data/krislov_1967.csv` — FY1955–1966: all representation elections excluding decertifications
  (`all_n`, `all_elig`), and new-organizing elections, wins, eligible employees, and eligible employees
  in units won (`new_n`, `new_won`, `new_elig`, `new_elig_won`). From "Union Organizing of New Units,
  1955–1966," *Industrial and Labor Relations Review* 21(1), 1967, pp. 34–35.
- `data/krislov_1970.csv` — FY1949–1966: employees in new units choosing a union (`new_elig_won`), in
  total and for manufacturing, trade, and services. From "Organizing, Union Growth, and the Cycle,
  1949–1966," *Labor History* 11(2), 1970, Table I.

The two agree exactly on `new_elig_won` for FY1955–1966. Krislov's `all_n` equals the Annual Reports'
RC + RM election counts through FY1964; FY1965 is 200 higher (7,776 vs. 7,576) and FY1966 92 lower
(8,011 vs. 8,103), the latter probably because the Annual Reports switched to counting cases closed.

The definition differs slightly from the Election Reports': Krislov drops elections whose *petition*
named a prior bargaining agent; the Election Reports drop elections *involving an incumbent union*.

## Continuity with Krislov

Joseph Krislov, "Union Organizing of New Units, 1955–1966" (*ILR Review* 21, 1967), reports the same
concept for FY1955–1966 from NLRB punched-card tabulations: elections in which "the petition indicated
existence of a prior bargaining agent" were removed. His total elections match the Annual Reports, as
do the Election Reports'. The two series do not overlap (his ends in FY1966, the summaries here begin
July–December 1968), but the incumbent share continues smoothly: about 10% of elections in FY1963–65,
6% in FY1966, 5% in July–December 1968, 3–4.5% in 1971. Adams and Krislov (*QJE* 1974) used the
published Election Report figures as the continuation of the same series.
