"""Test C06P literature matrix validation."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src/bibliography"))
from validate_literature_matrix import validate_bib


def test_validate_bib_passes():
    """Validation should pass with 45+ verified refs."""
    result = validate_bib("bibliography/c06p_candidates.bib")
    assert result["total"] >= 45, f"Expected 45+, got {result['total']}"
    assert result["n_2021_2026"] >= 20
    assert result["epsr_count"] >= 8
    assert result["duplicate_dois"] == 0
    assert result["active_entries"] >= 45


def test_arritt_clark_rejected():
    """Arritt-Clark citation must be REJECT."""
    with open("bibliography/c06p_candidates.bib") as f:
        content = f.read()
    assert "REJECT" in content
    assert "arritt" in content.lower()


def test_no_duplicate_dois():
    """All DOIs must be unique."""
    import re
    with open("bibliography/c06p_candidates.bib") as f:
        content = f.read()
    dois = re.findall(r'doi=\{([^}]+)\}', content)
    assert len(dois) == len(set(dois))


def test_bib_file_exists():
    """BibTeX file must exist."""
    assert Path("bibliography/c06p_candidates.bib").exists()
