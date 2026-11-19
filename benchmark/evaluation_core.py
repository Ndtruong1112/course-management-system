"""Pure helpers for reproducible, manually reviewed model comparisons."""

from collections import defaultdict
from statistics import mean


def build_messages(question, context=""):
    content = question if not context else f"{question}\n\n[TÀI LIỆU THAM KHẢO]\n{context}"
    return [{"role": "user", "content": content}]


def validate_reviews(records, reviews):
    by_id = {row["id"]: row for row in records}
    if len(by_id) != len(records):
        raise ValueError("Duplicate result IDs")
    checked = {}
    for review in reviews:
        key = review.get("id")
        if key in checked or key not in by_id:
            raise ValueError(f"Duplicate or unknown review ID: {key}")
        verdict = review.get("verdict")
        if verdict not in ("pass", "fail", "pending"):
            raise ValueError(f"Invalid verdict: {key}")
        if verdict != "pending" and (by_id[key]["status"] != "ok"
                                     or not str(review.get("evidence", "")).strip()
                                     or not str(review.get("reviewer", "")).strip()):
            raise ValueError(f"Review requires a successful response and supporting evidence: {key}")
        for field in ("compile_status", "test_status"):
            if review.get(field, "not_run") not in ("pass", "fail", "not_run", "not_applicable"):
                raise ValueError(f"Invalid {field}: {key}")
        if verdict == "pass" and by_id[key].get("kind") == "code" and (
                review.get("compile_status") != "pass" or review.get("test_status") != "pass"):
            raise ValueError(f"Code pass requires recorded compile and test results: {key}")
        checked[key] = review
    return checked


def summarize(records, reviews):
    grouped = defaultdict(list)
    for row in records:
        grouped[row["variant"]].append(row)
    summary = {}
    for variant, items in grouped.items():
        ok = [row for row in items if row["status"] == "ok"]
        reviewed = [row for row in ok if reviews.get(row["id"], {}).get("verdict") in ("pass", "fail")]
        passed = sum(reviews[row["id"]]["verdict"] == "pass" for row in reviewed)
        elapsed = [row["elapsed_seconds"] for row in ok if isinstance(row.get("elapsed_seconds"), (int, float))]
        summary[variant] = {
            "attempts": len(items), "ok": len(ok), "errors": len(items) - len(ok),
            "reviewed": len(reviewed), "pending": len(ok) - len(reviewed), "passed": passed,
            "pass_rate_percent": round(100 * passed / len(reviewed), 1) if reviewed else None,
            "mean_seconds_successful": round(mean(elapsed), 2) if elapsed else None,
            "compile_checked": sum(reviews.get(row["id"], {}).get("compile_status") in ("pass", "fail") for row in ok),
            "tests_checked": sum(reviews.get(row["id"], {}).get("test_status") in ("pass", "fail") for row in ok),
            "compile_passed": sum(reviews.get(row["id"], {}).get("compile_status") == "pass" for row in ok),
            "tests_passed": sum(reviews.get(row["id"], {}).get("test_status") == "pass" for row in ok),
        }
    return summary


def paired_comparison(records, reviews, left, right):
    pairs = defaultdict(dict)
    for row in records:
        if row["variant"] in (left, right) and row["status"] == "ok":
            verdict = reviews.get(row["id"], {}).get("verdict")
            if verdict in ("pass", "fail"):
                pairs[(row["case_id"], row["repeat"])][row["variant"]] = verdict == "pass"
    complete = [pair for pair in pairs.values() if left in pair and right in pair]
    difference = None if not complete else round(
        100 * sum(int(pair[right]) - int(pair[left]) for pair in complete) / len(complete), 1)
    return {"left": left, "right": right, "paired_reviewed": len(complete),
            "difference_percentage_points": difference}
