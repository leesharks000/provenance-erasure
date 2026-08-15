#!/usr/bin/env python3
"""verify_offline.py — recompute the Self-Audit Module fixtures from cases.json.

Runs with no network, no dependencies, no site. If your implementation of the
module disagrees with these numbers, one of us is wrong and this tells you where.

    python3 verify_offline.py            # verify all cases
    python3 verify_offline.py --show     # print the arithmetic

WHAT THIS DOES NOT TEST. The atom set and weights are STIPULATED. This verifies
that an implementation computes the same arithmetic on the same table — not that
the table is the right table. That distinction is the difference between a
conformance test and a validity claim, and only the first is on offer here.
"""
import json, pathlib, sys

CASES = pathlib.Path(__file__).with_name("cases.json")
TOL = 0.005


def per(atoms, field):
    num = sum(a["weight"] for a in atoms if a[field])
    den = sum(a["weight"] for a in atoms)
    return 1 - num / den, num, den


def per_dim(atoms, field, dim):
    sel = [a for a in atoms if a["dim"] == dim]
    if not sel:
        return None
    return 1 - sum(a["weight"] for a in sel if a[field]) / sum(a["weight"] for a in sel)


def family(atom_set, renderings):
    k = len(renderings)
    n = len(atom_set)
    P = {r: {a: (a in present) for a in atom_set} for r, present in renderings.items()}
    acp = max(sum(P[r][a] for a in atom_set) / n for r in P)
    fc = sum(1 for a in atom_set if any(P[r][a] for r in P)) / n
    return k, fc, acp, fc - acp


def close(got, want):
    return want is None or abs(got - want) <= TOL


def main():
    show = "--show" in sys.argv
    fx = json.loads(CASES.read_text())
    fails = 0
    for c in fx["cases"]:
        print(f"\n── {c['id']} — {c['title']}")
        exp = c["expected"]

        if "atom_set" in c and isinstance(c["atom_set"][0], dict):
            atoms = c["atom_set"]
            p1, n1, den = per(atoms, "first_pass")
            p2, n2, _ = per(atoms, "under_challenge")
            checks = [("PER first pass", p1, exp.get("PER_first_pass")),
                      ("PER under challenge", p2, exp.get("PER_under_challenge")),
                      ("PER-M", per_dim(atoms, "first_pass", "M"), exp.get("PER_M")),
                      ("PER-C", per_dim(atoms, "first_pass", "C"), exp.get("PER_C")),
                      ("PER-D", per_dim(atoms, "first_pass", "D"), exp.get("PER_D")),
                      ("rho_T", p1 - p2 if exp.get("rho_T") else None, exp.get("rho_T"))]
            if show:
                print(f"   weights present {n1}/{den} first pass, {n2}/{den} under challenge")
            for name, got, want in checks:
                if got is None or want is None:
                    continue
                ok = close(got, want)
                fails += not ok
                print(f"   {'OK  ' if ok else 'FAIL'} {name:<22} got {got:.3f}  expected {want:.3f}")

        elif "renderings" in c:
            k, fc, acp, asi = family(c["atom_set"], c["renderings"])
            for name, got, want in (("k", k, exp.get("k")), ("FC", fc, exp.get("FC")),
                                    ("ACP", acp, exp.get("ACP")), ("ASI", asi, exp.get("ASI"))):
                ok = close(got, want)
                fails += not ok
                print(f"   {'OK  ' if ok else 'FAIL'} {name:<22} got {got:.3f}  expected {want:.3f}")
            if abs(asi) <= TOL and fc < 1 - TOL:
                print("   NOTE  ASI = 0 with FC < 1 — UNIFORM FAMILY ERASURE.")
                print("         ASI = 0 does not certify intact attribution. An implementation that")
                print("         reports this as a clean result has failed the fixture.")
        else:
            print("   (no recomputable arithmetic; recorded values only)")

    print(f"\n{'ALL FIXTURES VERIFY' if not fails else f'{fails} FAILURE(S)'}")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
