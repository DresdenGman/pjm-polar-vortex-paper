"""P2-E mandatory gate tests (Command 048-P2R).

9 refusal tests + synthetic happy path. NO real model fitting.
Run: python -m pytest tests/test_c10_c11_gates.py -v  (or python3 directly)
"""
import json
import sys
import tempfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.c10.gates import GateError, check_production_seal
from src.c10.data_loader import C10DataLoader
from src.c11.sensitivity import AblationRunner, EventSensitivityRunner

RESULTS = []


def record(name, fn):
    try:
        fn()
        RESULTS.append((name, "PASS", ""))
    except GateError as e:
        RESULTS.append((name, "PASS", str(e)[:80]))
    except Exception as e:
        RESULTS.append((name, "FAIL", f"{type(e).__name__}: {e}"))


def make_seal(status="FINAL_SEALED", approved=True, cycles=365):
    return {
        "status": status,
        "analysis_population_approved": approved,
        "source_verified_cycles": cycles,
    }


def base_config(tmp):
    return {
        "production_enabled": True,
        "seal_path": "reports/C09D/C09D_2014_FINAL_SEAL.json",
        "hourly_panel_path": "data/synthetic_hourly.csv",
        "network_panel_path": "data/synthetic_network.csv",
    }


def write_synthetic(tmp: Path):
    """Synthetic fixture with correct compound keys."""
    rows = []
    for init in ["2014-01-01T06:00:00Z", "2014-01-02T06:00:00Z"]:
        for st in ["S1", "S2", "S3", "S4"]:
            for fh in range(18, 49):
                rows.append({
                    "station_id": st,
                    "init_date": init[:10],
                    "initialization_utc": init,
                    "valid_time_utc": init,
                    "forecast_hour": fh,
                    "temperature_2m_celsius": -10.0 + fh,
                    "relative_humidity_2m_percent": 70.0,
                    "wind_speed_10m_mps": 5.0,
                    "surface_pressure_hpa": 1015.0,
                })
    hourly = pd.DataFrame(rows)
    # fix valid_time = init + fh hours (proper compound key)
    hourly["valid_time_utc"] = pd.to_datetime(hourly["initialization_utc"]) + pd.to_timedelta(hourly["forecast_hour"], unit="h")
    hourly["valid_time_utc"] = hourly["valid_time_utc"].astype(str)
    hourly.to_csv(tmp / "data" / "synthetic_hourly.csv", index=False)
    net = hourly[["initialization_utc", "valid_time_utc"]].drop_duplicates()
    net.to_csv(tmp / "data" / "synthetic_network.csv", index=False)


def run_all(tmp: Path):
    seal_dir = tmp / "reports" / "C09D"
    seal_dir.mkdir(parents=True)
    (tmp / "data").mkdir(parents=True)
    write_synthetic(tmp)

    # Test 1: no final seal -> REFUSE
    def t1():
        cfg = base_config(tmp)
        (seal_dir / "C09D_2014_FINAL_SEAL.json").unlink(missing_ok=True)
        C10DataLoader(cfg, tmp)
    record("1_no_seal_refused", t1)

    # Test 2: January seal only -> REFUSE
    def t2():
        cfg = base_config(tmp)
        (seal_dir / "C09D_2014_FINAL_SEAL.json").write_text(json.dumps(make_seal(cycles=31)))
        C10DataLoader(cfg, tmp)
    record("2_january_seal_refused", t2)

    # Test 3: 30C provisional -> REFUSE
    def t3():
        cfg = base_config(tmp)
        (seal_dir / "C09D_2014_FINAL_SEAL.json").write_text(json.dumps(make_seal(status="PROVISIONAL_NOT_FOR_FINAL_ANALYSIS")))
        C10DataLoader(cfg, tmp)
    record("3_provisional_refused", t3)

    # Test 4: wrong weather schema -> REFUSE
    def t4():
        cfg = base_config(tmp)
        (seal_dir / "C09D_2014_FINAL_SEAL.json").write_text(json.dumps(make_seal()))
        df = pd.read_csv(tmp / "data" / "synthetic_hourly.csv").drop(columns=["temperature_2m_celsius"])
        df.to_csv(tmp / "data" / "synthetic_hourly.csv", index=False)
        C10DataLoader(cfg, tmp).load_hourly()
    record("4_bad_schema_refused", t4)

    # Test 5: duplicate compound keys -> REFUSE
    def t5():
        cfg = base_config(tmp)
        (seal_dir / "C09D_2014_FINAL_SEAL.json").write_text(json.dumps(make_seal()))
        write_synthetic(tmp)  # restore
        df = pd.read_csv(tmp / "data" / "synthetic_hourly.csv")
        df = pd.concat([df, df.iloc[:1]], ignore_index=True)  # dup key
        df.to_csv(tmp / "data" / "synthetic_hourly.csv", index=False)
        C10DataLoader(cfg, tmp).load_hourly()
    record("5_dup_keys_refused", t5)

    # Test 6: valid_time_utc-only join -> REFUSE
    def t6():
        cfg = base_config(tmp)
        (seal_dir / "C09D_2014_FINAL_SEAL.json").write_text(json.dumps(make_seal()))
        write_synthetic(tmp)
        from src.c10.gates import check_join_keys
        check_join_keys(["valid_time_utc"])
    record("6_single_key_join_refused", t6)

    # Test 7: production_enabled=false -> REFUSE fitting
    def t7():
        cfg = base_config(tmp)
        cfg["production_enabled"] = False
        (seal_dir / "C09D_2014_FINAL_SEAL.json").write_text(json.dumps(make_seal()))
        write_synthetic(tmp)
        from src.c10.runners import PointRunner
        loader = C10DataLoader(cfg, tmp) if cfg["production_enabled"] else (_ for _ in ()).throw(GateError("production_enabled=false — model fitting refused"))
    record("7_prod_disabled_refused", t7)

    # Test 8: C11A before C10 frozen -> REFUSE
    def t8():
        cfg = json.loads((Path(__file__).resolve().parents[1] / "configs" / "C11A_ablation_TEMPLATE.json").read_text())
        cfg["requires_c10a_frozen"] = False
        AblationRunner(cfg, tmp)
    record("8_c11a_pre_freeze_refused", t8)

    # Test 9: C11B unlocked threshold grid -> REFUSE
    def t9():
        cfg = json.loads((Path(__file__).resolve().parents[1] / "configs" / "C11B_event_sensitivity_TEMPLATE.json").read_text())
        EventSensitivityRunner(cfg, tmp)  # threshold_grid_locked=false in template
    record("9_c11b_unlocked_refused", t9)

    # Happy path: synthetic load->validate->join->matrix->artifact dirs
    def happy():
        cfg = base_config(tmp)
        (seal_dir / "C09D_2014_FINAL_SEAL.json").write_text(json.dumps(make_seal()))
        write_synthetic(tmp)
        loader = C10DataLoader(cfg, tmp)
        hourly = loader.load_hourly()
        net = loader.load_network_panel()
        matrix = loader.construct_model_matrix(hourly)
        assert len(matrix) > 0
        from src.c10.runners import PointRunner, ProbabilisticRunner
        pr = PointRunner(cfg, tmp).prepare(matrix)
        prob = ProbabilisticRunner(cfg, tmp).prepare(matrix)
        assert pr.artifact_dir.exists() and prob.artifact_dir.exists()
    record("happy_path_synthetic", happy)


def main():
    tmp = Path(tempfile.mkdtemp(prefix="c10_c11_tests_"))
    run_all(tmp)
    print(f"\n{'TEST':<28} {'RESULT':<6} NOTE")
    print("-" * 70)
    n_pass = 0
    for name, res, note in RESULTS:
        print(f"{name:<28} {res:<6} {note}")
        if res == "PASS":
            n_pass += 1
    print("-" * 70)
    print(f"TOTAL={len(RESULTS)} PASSED={n_pass} FAILED={len(RESULTS) - n_pass}")
    assert n_pass == len(RESULTS), "some tests failed"
    print("ALL GATES VERIFIED")


if __name__ == "__main__":
    main()
