"""Round-5 suite: build the three new negative fixtures from a known-good
document, then run every fixture and assert its expected verdict."""
import subprocess, sys, os
for _st in (sys.stdout, sys.stderr):
    try: _st.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass

S = os.path.dirname(os.path.abspath(__file__))
GOOD = open(os.path.join(S, "d_ok.md"), encoding="utf-8").read()

PREREG = "**Pre-registered:** predicted 12/24/24 of 60 · surprise above 30 served · cut: no named decision"
LB = "**Load-bearing persona:** P2, the executing agent"
assert PREREG in GOOD and LB in GOOD, "base fixture changed shape"

# f1: a figure that is stated but never claimed as a prediction.
open(os.path.join(S, "f_nopredicted.md"), "w", encoding="utf-8").write(
    GOOD.replace(PREREG,
                 "**Pre-registered:** historical baseline 12/24/24 of 60 · surprise above 30 "
                 "served · cut: no named decision", 1))

# f2: more frontier items predicted than the run has items. Built from the
# no-coverage fixture, because a frontier-only prediction is only valid there.
ZERO = open(os.path.join(S, "d_zero.md"), encoding="utf-8").read()
zp = [l for l in ZERO.splitlines() if l.startswith("**Pre-registered:**")][0]
zr = [l for l in ZERO.splitlines() if l.startswith("**Reckoning:**")][0]
open(os.path.join(S, "f_bigfrontier.md"), "w", encoding="utf-8").write(
    ZERO.replace(zp, zp.replace("predicted 0", "predicted 100"), 1)
        .replace(zr, zr.replace("predicted 0", "predicted 100"), 1))

# f3: a load-bearing persona who is not on the roster.
open(os.path.join(S, "f_badlb.md"), "w", encoding="utf-8").write(
    GOOD.replace(LB, "**Load-bearing persona:** P99, the executing agent", 1))

# f4: a load-bearing declaration naming nobody the roster knows.
open(os.path.join(S, "f_vaguelb.md"), "w", encoding="utf-8").write(
    GOOD.replace(LB, "**Load-bearing persona:** the person who runs it on a schedule", 1))

EXPECT = {
    # round-5 regressions
    "f_nopredicted.md": ("FAIL", "states no prediction"),
    "f_bigfrontier.md": ("FAIL", "frontier items are a subset"),
    "f_badlb.md": ("FAIL", "P99"),
    "f_vaguelb.md": ("FAIL", "names nobody on the roster"),
    # earlier rounds must still hold
    "d_ok.md": ("PASS", None),
    "e_commas.md": ("PASS", None),
    "d_zero.md": ("PASS", None),
    "e_baddenom.md": ("FAIL", None),
    "d_nosurprise.md": ("FAIL", None),
    "d_badsum.md": ("FAIL", None),
    "d_wrongsection.md": ("FAIL", None),
    "c_pct.md": ("FAIL", None),
    "c_vague.md": ("FAIL", None),
    "rk_badactual.md": ("FAIL", None),
    # pre-dates the counts-vs-percentages settlement: 20/40/40 against a 60-item budget
    "rk_ok.md": ("FAIL", "sums to 100"),
    "prereg_ok.md": ("FAIL", "sums to 100"),
}

bad = 0
for name, (want, needle) in EXPECT.items():
    path = os.path.join(S, name)
    if not os.path.exists(path):
        print(f"  SKIP {name} (missing)")
        continue
    r = subprocess.run([sys.executable, "scripts/verify.py", path],
                       capture_output=True, text=True, encoding="utf-8")
    got = "PASS" if r.returncode == 0 else "FAIL"
    out = (r.stdout or "") + (r.stderr or "")
    ok = got == want and (needle is None or needle.lower() in out.lower())
    if not ok:
        bad += 1
        print(f"  x {name}: want {want}", f"containing {needle!r}" if needle else "",
              f"-- got {got}")
        print("    " + "\n    ".join([l for l in out.splitlines() if "[FAIL]" in l][:3] or out.strip().splitlines()[:3]))
    else:
        print(f"  + {name} {got}")

# the shipped document must still pass
r = subprocess.run([sys.executable, "scripts/verify.py", "PERSONAS.md"],
                   capture_output=True, text=True, encoding="utf-8")
print(f"  {'+' if r.returncode == 0 else 'x'} PERSONAS.md "
      f"{'PASS' if r.returncode == 0 else 'FAIL'}")
if r.returncode != 0:
    bad += 1
    print(r.stdout, r.stderr)

print("\nSUITE", "FAILED" if bad else "PASSED", f"({bad} problems)")
sys.exit(1 if bad else 0)
