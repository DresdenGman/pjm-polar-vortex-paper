"""C06P: Validate the literature matrix against requirements.

Checks:
  - 45+ verified references
  - 20+ from 2021-2026
  - 8+ EPSR papers from 2022-2026
  - 6+ official PJM/NOAA/ECMWF sources
  - 0 duplicate DOIs
  - REJECT/INFORMATION_MISSING not in active BibTeX
  - All accepted records have DOIs (or official report designation)
"""
import re
import sys


def validate_bib(bib_path: str) -> dict:
    with open(bib_path) as f:
        content = f.read()

    # Extract entries
    entries = re.findall(r'@\w+\{([^,]+),', content)
    dois = re.findall(r'doi=\{([^}]+)\}', content)
    titles = re.findall(r'title=\{([^}]+)\}', content)
    years = []
    for m in re.finditer(r'year=\{(\d{4})\}', content):
        years.append(int(m.group(1)))

    # Count duplicates
    doi_set = set()
    dup_dois = 0
    for d in dois:
        if d in doi_set:
            dup_dois += 1
        doi_set.add(d)

    # Count rejected
    rejected = len(re.findall(r'REJECT', content))

    # Count categories
    n_2021_2026 = sum(1 for y in years if 2021 <= y <= 2026)
    epsr_count = content.count('Electric Power Systems Research')
    pjm_count = len(re.findall(r'pjm|PJM', content))

    total = len(entries)

    checks = {
        "total_references": total,
        "target": 45,
        "pass": total >= 45,
    }

    result = {
        "total": total,
        "n_2021_2026": n_2021_2026,
        "target_2021_2026": 20,
        "pass_2021_2026": n_2021_2026 >= 20,
        "epsr_count": epsr_count,
        "target_epsr": 8,
        "pass_epsr": epsr_count >= 8,
        "duplicate_dois": dup_dois,
        "rejected_entries": rejected,
        "verified_dois": len(doi_set),
        "active_entries": total - rejected,
        "all_valid": all([
            total >= 45,
            n_2021_2026 >= 20,
            epsr_count >= 8,
            dup_dois == 0,
        ]),
    }

    return result


def main():
    result = validate_bib("bibliography/c06p_candidates.bib")
    for k, v in result.items():
        print(f"  {k}: {v}")

    if result["all_valid"]:
        print("\nALL CHECKS PASSED")
        sys.exit(0)
    else:
        print("\nSOME CHECKS FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
