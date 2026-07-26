"""C07C: Fixed-vintage PJM forecast selector 2010-2022.

2014: vintage_key = eval_date, matched to operating_date = eval_date + 1
2015-2022: vintage_key = eval_utc, matched to operating_date directly
"""
import argparse
import pandas as pd
import pytz


def load_forecasts():
    eastern = pytz.timezone("America/New_York")
    utc_tz = pytz.UTC
    all_fcasts = []

    for year in range(2014, 2023):
        if year == 2014:
            fpath = "data/raw/pjm/pjm_day_ahead_forecast_2014_clean.csv"
        else:
            fpath = f"data/raw/pjm/forecast_history/pjm_forecast_{year}.csv"
        try:
            df = pd.read_csv(fpath)
        except FileNotFoundError:
            continue

        if "evaluated_at_utc" in df.columns:
            df["eval_utc"] = pd.to_datetime(df["evaluated_at_utc"], utc=True)
            df["target_utc"] = pd.to_datetime(df["forecast_hour_beginning_utc"], utc=True)
            df["fcast_mw"] = df["forecast_load_mw"]
            df["vintage_key"] = df["eval_utc"]
            df["eval_date"] = df["eval_utc"].dt.normalize()
            all_fcasts.append(df[["eval_utc", "eval_date", "vintage_key", "target_utc", "fcast_mw"]])
        else:
            df["eval_ept"] = pd.to_datetime(df["evaluated_at_ept"], format="mixed")
            df["eval_utc"] = (df["eval_ept"]
                .dt.tz_localize(eastern, ambiguous="infer")
                .dt.tz_convert(utc_tz))
            df["target_utc"] = pd.to_datetime(df["forecast_hour_beginning_utc"], utc=True, format="mixed")
            df["fcast_mw"] = df["day_ahead_forecast_mw"]
            df["eval_date"] = df["eval_utc"].dt.normalize()
            df["vintage_key"] = df["eval_date"]  # date only for 2014
            all_fcasts.append(df[["eval_utc", "eval_date", "vintage_key", "target_utc", "fcast_mw"]])

    return pd.concat(all_fcasts).sort_values(["vintage_key", "target_utc"])


def build_vintage_maps(fcasts):
    vt = {}; vmw = {}
    for vk, grp in fcasts.groupby("vintage_key"):
        vt[vk] = set(grp["target_utc"])
        vmw[vk] = dict(zip(grp["target_utc"], grp["fcast_mw"]))
    return vt, vmw


def select_vintages(timeline_path: str, output_path: str):
    eastern = pytz.timezone("America/New_York")
    utc_tz = pytz.UTC

    tl = pd.read_csv(timeline_path)
    tl["target_utc"] = pd.to_datetime(tl["target_time_utc"], utc=True)
    tl["op_date"] = pd.to_datetime(tl["operating_date"]).dt.date

    fcasts = load_forecasts()
    vintage_targets, vintage_mw = build_vintage_maps(fcasts)
    print(f"Forecasts: {len(fcasts)} rows, {len(vintage_targets)} vintages")

    op_dates = sorted(tl["op_date"].unique())
    results = []

    for op_date in op_dates:
        day_rows = tl[tl["op_date"] == op_date]
        targets = set(day_rows["target_utc"])
        expected = len(targets)

        origin_ept = eastern.localize(
            pd.Timestamp(str(op_date)) - pd.Timedelta(days=1)
        ).replace(hour=12, minute=0, second=0)
        origin_utc = origin_ept.astimezone(utc_tz)

        # Determine which vintage_key to look for:
        # 2014: vintage_key = eval_date; we need eval_date = op_date - 1
        # 2015-22: vintage_key = eval_utc; eligible = eval_utc <= origin_utc
        # Try both: first check for date-based match (2014), then time-based

        op_date_ts = pd.Timestamp(str(op_date), tz=utc_tz)

        # Candidate 1: date-based vintage (2014 style: eval_date = op_date - 1)
        candidate_date = op_date_ts - pd.Timedelta(days=1)
        vk_date = candidate_date.normalize()

        # Candidate 2: time-based eligible vintages (2015-22 style)
        eligible_time = sorted([vk for vk in vintage_targets if vk <= origin_utc], reverse=True)

        selected = None
        fallback = False
        latest_complete = False
        n_cand = len(eligible_time)

        # Try date-based match first (2014)
        if vk_date in vintage_targets:
            inter = targets & vintage_targets[vk_date]
            if len(inter) >= 0.875 * expected:
                selected = vk_date
                latest_complete = True
                n_cand = 1  # date-based match counts as 1 candidate

        # Try time-based match (2015-22)
        if selected is None and eligible_time:
            latest_complete = len(targets & vintage_targets[eligible_time[0]]) >= 0.875 * expected
            if latest_complete:
                selected = eligible_time[0]
            else:
                for vk in eligible_time:
                    if len(targets & vintage_targets[vk]) >= 0.875 * expected:
                        selected = vk
                        fallback = True
                        break

        if selected is not None:
            vintage_age = (origin_utc - selected).total_seconds() / 3600 if hasattr(selected, 'tzinfo') and selected.tzinfo else 0
            if not isinstance(vintage_age, (int, float)) or vintage_age < 0:
                vintage_age = 0
            mw_map = vintage_mw[selected]
            avail_hrs = len(mw_map)
        else:
            vintage_age = None
            mw_map = {}
            avail_hrs = 0

        if not eligible_time and selected is None:
            n_cand = 0

        for _, tr in day_rows.iterrows():
            fcast_val = mw_map.get(tr["target_utc"])
            if fcast_val is not None:
                reason = "NONE"
            elif not eligible_time and selected is None:
                reason = "NO_ELIGIBLE_VINTAGE"
            elif selected is None:
                reason = "NO_COMPLETE_VINTAGE"
            elif op_date == pd.Timestamp("2014-11-02").date():
                reason = "SOURCE_DATA_MISSING"
            else:
                reason = "NO_COMPLETE_VINTAGE"

            results.append({
                "operating_date": op_date,
                "target_time_utc": tr["target_utc"],
                "forecast_origin_utc": origin_utc,
                "selected_evaluated_at_utc": selected,
                "selected_vintage_id": str(selected) if selected else "",
                "vintage_age_hours": round(vintage_age, 1) if vintage_age is not None else None,
                "number_of_candidate_vintages": n_cand,
                "latest_candidate_complete": latest_complete,
                "older_vintage_fallback_used": fallback,
                "expected_target_hours": expected,
                "available_target_hours": avail_hrs,
                "pjm_forecast_mw": fcast_val,
                "pjm_forecast_available": fcast_val is not None,
                "pjm_missing_reason": reason,
            })

    result = pd.DataFrame(results)
    result.to_csv(output_path, index=False)
    print(f"Saved {len(result)} rows")
    qual = result.groupby("operating_date")["pjm_forecast_available"].all().sum()
    print(f"Qualifying days: {qual}/{len(op_dates)}")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeline", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    select_vintages(args.timeline, args.output)


if __name__ == "__main__":
    main()
