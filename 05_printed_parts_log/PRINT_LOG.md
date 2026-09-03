# Print Log — W17 RC F1 printed parts

Running log of every print attempt (successes AND failures), newest entry on top.
Use the "Print attempt" template from `../PRINT_LOG_TEMPLATE.md`; IDs are `P-NNN`,
never reused. Test/calibration prints log in `../04_test_prints/` as `TP-NNN` instead.

Nothing has been printed **by this project's own logged process** — no `P-NNN` entry
exists below, and none should be invented.

---

## 2026-09-03 — note: the owner reports print-shop parts exist; inventory pending

**This is a note, not a print entry.** It has no `P-NNN`, because a `P-NNN` records a
print *this project ran and logged*, and none has been run.

On 2026-09-02 the owner stated, in the decision that moved mechanical design into this
repo: *"Some 3d models were printed and we may start test assembly."* Those prints were
not made by this process and nothing about them is recorded anywhere in this repo — not
which parts, not the material, not the settings, not the date, not the shop.

**So this log lists nothing.** Naming parts here on the strength of a sentence would put
unverified claims into the one file that is supposed to be the record of what physically
exists, which is the exact failure mode the append-only rule exists to prevent.

**What resolves it:** measurement **M-00** in
[`../w17-mechanical-measurement-session-prompt.md`](../w17-mechanical-measurement-session-prompt.md) —
a per-group tick sheet against `MODEL_INVENTORY.md` §REQUIRED, plus condition per part.
When it comes back, add the real parts here with what is genuinely known and mark every
unknown as unknown.

**Until then, treat every printed part as unidentified**, and in particular:

- a part whose **material and settings are unknown** is a *diagnostic* part, not a build
  part — a dry fit with it proves geometry, never durability;
- it may not be given a `P-NNN` retroactively; if it is used for a fit check, log that
  check as a `TP-NNN` in [`../04_test_prints/`](../04_test_prints) naming the part's
  unknown provenance;
- **A2 remains NOT-EXECUTED and Phase B remains BLOCKED.** Parts existing changes
  nothing about either.

---

<!-- Newest entry goes here -->
