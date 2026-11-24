"""Build the records table from quest/<category>/<quest>/<weapon>/regulation*/records.json."""

import json
import math
from pathlib import Path
import re
from tempfile import NamedTemporaryFile


ROOT = Path(__file__).resolve().parents[1]
SHAPE = 5.394
LOG_GAMMA = math.lgamma(SHAPE)


def gamma_cdf(x):
    """Return the CDF of a unit-scale gamma at x."""
    if x <= 0:
        return 0.0
    log_factor = SHAPE * math.log(x) - x - LOG_GAMMA
    if x < SHAPE + 1:
        term = total = 1 / SHAPE
        for i in range(1, 200):
            term *= x / (SHAPE + i)
            total += term
            if term < 1e-15 * total:
                break
        return math.exp(log_factor) * total

    # Continued fraction for the upper incomplete gamma, including the far tail.
    b = x + 1 - SHAPE
    c = 1e300
    d = fraction = 1 / b
    for i in range(1, 200):
        a = i * (SHAPE - i)
        b += 2
        d = 1 / (b + a * d)
        c = b + a / c
        step = c * d
        fraction *= step
        if abs(step - 1) < 1e-15:
            break
    log_survival = log_factor + math.log(fraction)
    return -math.expm1(log_survival)


def department_scores(times):
    """Fit the continuous best-time density. Input times are in centiseconds."""
    if len(times) == 1:
        # m = 1: the gamma MLE is scale = loss / SHAPE.
        return [-math.log2(gamma_cdf(SHAPE))]
    best = min(times)
    losses = [0.04 + (t - best) / best for t in times]
    mean_runs = len(times) ** 2

    def log_likelihood(log_scale):
        scale = math.exp(log_scale)
        total = 0.0
        for loss in losses:
            x = loss / scale
            total -= x + 2 * math.log1p((mean_runs - 1) * gamma_cdf(x))
        # log G'(t), summed over runners, up to terms independent of scale.
        return total - len(times) * SHAPE * log_scale

    # Bracket the maximum before refining it on a log scale.
    middle = math.log(max(losses) / SHAPE)
    step = 1.0
    direction = 1 if log_likelihood(middle + step) > log_likelihood(middle) else -1
    while log_likelihood(middle + direction * step) > log_likelihood(middle):
        middle += direction * step
        step *= 2
    left, right = middle - step, middle + step
    for _ in range(64):
        a = (2 * left + right) / 3
        b = (left + 2 * right) / 3
        if log_likelihood(a) < log_likelihood(b):
            left = a
        else:
            right = b
    scale = math.exp((left + right) / 2)
    return [max(0.0, -math.log2(gamma_cdf(loss / scale))) for loss in losses]


def parse_time(value):
    match = re.fullmatch(r"""(\d+)'([0-5]\d)"(\d{2})""", value)
    if not match:
        raise ValueError(f"invalid time: {value!r}")
    minutes, seconds, hundredths = map(int, match.groups())
    result = (60 * minutes + seconds) * 100 + hundredths
    if result <= 0:
        raise ValueError("time must be positive")
    return result


def build_records(source):
    records = []
    winners = {}
    for path in sorted(source.rglob("records.json")):
        try:
            category, quest, weapon, regulation_dir = path.parent.relative_to(source).parts
            regulation = re.fullmatch(r"regulation([A-Za-z0-9]+)", regulation_dir)
            if not regulation:
                raise ValueError(f"invalid regulation directory: {regulation_dir}")
            entries = json.loads(path.read_text(encoding="utf-8-sig"))
            if not isinstance(entries, list):
                raise ValueError("expected a JSON array")
            best = {}
            for entry in entries:
                hunter = entry["hunter"].strip()
                if not hunter:
                    raise ValueError("missing hunter name")
                time = parse_time(entry["time"])
                if hunter not in best or time < best[hunter][0]:
                    best[hunter] = (time, entry)
            if not best:
                continue
            runners = sorted(best, key=lambda hunter: (best[hunter][0], hunter))
            scores = department_scores([best[hunter][0] for hunter in runners])
            for hunter, score in zip(runners, scores):
                record = dict(best[hunter][1], hunter=hunter, quest=f"{category} {quest}",
                              weapon=weapon, regulation=regulation[1], score=score,
                              scoreCounted=False)
                records.append(record)
                key = (category, quest, hunter)
                if key not in winners or winners[key]["score"] < score:
                    winners[key] = record
        except (ValueError, TypeError, KeyError) as error:
            raise ValueError(f"{path}: {error}") from error
    for record in winners.values():
        record["scoreCounted"] = True
    return records


def main():
    source = ROOT / "quest"
    if not source.is_dir():
        raise SystemExit(f"Missing input directory: {source}")
    records = build_records(source)
    output = ROOT / "pages/data/records.json"
    data = json.dumps({"records": records}, ensure_ascii=False, indent=2, allow_nan=False)
    temp = NamedTemporaryFile(dir=output.parent, delete=False)
    staged = Path(temp.name)
    try:
        with temp:
            temp.write((data + "\n").encode("utf-8"))
        staged.replace(output)
    finally:
        staged.unlink(missing_ok=True)
    print(f"{len(records)} records -> {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
