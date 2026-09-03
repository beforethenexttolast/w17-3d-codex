#!/usr/bin/env bash
# =====================================================================
# render.sh — render every model in 11_cad/ to out/, cleanly or not at all
# =====================================================================
#
#  Usage:   ./render.sh            render everything (STL + PNG preview)
#           ./render.sh --stl      STL only, skip the previews (much faster)
#           ./render.sh --table    render, then print the Markdown table
#                                  that goes in README.md
#
#  Outputs land in out/, which is gitignored. The repo .gitignore already
#  blocks *.stl and *.png everywhere, so nothing binary can be committed by
#  accident from here.
#
#  A "clean" render means: OpenSCAD reported Status: NoError, raised no
#  WARNING, and the resulting STL is non-empty. Anything else fails the
#  script, because a model that renders with warnings is a model whose
#  geometry you cannot reason about.
# =====================================================================

set -u -o pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT="$HERE/out"
OPENSCAD="${OPENSCAD:-/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD}"

WANT_PNG=1
WANT_TABLE=0
for arg in "$@"; do
  case "$arg" in
    --stl)   WANT_PNG=0 ;;
    --table) WANT_TABLE=1 ;;
    *) echo "unknown argument: $arg" >&2; exit 2 ;;
  esac
done

if [[ ! -x "$OPENSCAD" ]]; then
  echo "OpenSCAD not found at $OPENSCAD" >&2
  echo "Set OPENSCAD=/path/to/OpenSCAD and re-run." >&2
  exit 3
fi

mkdir -p "$OUT"
FAILED=0
RENDERED=0

# render <output-name> <scad file> [-D var=val ...]
render() {
  local name="$1"; shift
  local src="$1";  shift
  local stl="$OUT/$name.stl"
  local log; log="$(mktemp)"

  if ! "$OPENSCAD" --backend=manifold "$@" -o "$stl" "$HERE/$src" > "$log" 2>&1; then
    echo "  FAIL   $name  (OpenSCAD exited non-zero)"
    sed 's/^/         /' "$log"
    FAILED=$((FAILED + 1)); rm -f "$log"; return
  fi
  if grep -q "WARNING\|ERROR" "$log"; then
    echo "  WARN   $name"
    grep "WARNING\|ERROR" "$log" | sed 's/^/         /'
    FAILED=$((FAILED + 1)); rm -f "$log"; return
  fi
  if [[ ! -s "$stl" ]]; then
    echo "  EMPTY  $name  (rendered, but produced no geometry)"
    FAILED=$((FAILED + 1)); rm -f "$log"; return
  fi

  local status; status="$(grep -E '^ *Status:' "$log" | awk '{print $2}')"
  if [[ "$status" != "NoError" ]]; then
    echo "  FAIL   $name  (manifold status: ${status:-unknown})"
    FAILED=$((FAILED + 1)); rm -f "$log"; return
  fi
  rm -f "$log"

  if [[ "$WANT_PNG" == "1" ]]; then
    "$OPENSCAD" --backend=manifold "$@" \
      --render --imgsize 800,600 --colorscheme Tomorrow \
      -o "$OUT/$name.png" "$HERE/$src" >/dev/null 2>&1 \
      || echo "  (preview failed for $name — STL is still good)"
  fi

  echo "  ok     $name"
  RENDERED=$((RENDERED + 1))
}

# render_view <output-name> <scad file> [-D ...]
# A PNG only, rendered in PREVIEW mode rather than --render.
# This matters: the % modifier that draws the context ghosts (the PDB cell,
# both boards, the KO-01 band) is a PREVIEW-only construct -- a full --render
# drops it, which is exactly the property that keeps ghosts out of exported
# STLs. So the "context" and "section" views have no STL by design; looking
# at them is the whole point of them.
render_view() {
  local name="$1"; shift
  local src="$1";  shift
  if [[ "$WANT_PNG" == "0" ]]; then return; fi
  if "$OPENSCAD" --backend=manifold "$@" \
       --imgsize 1000,750 --colorscheme Tomorrow \
       -o "$OUT/$name.png" "$HERE/$src" >/dev/null 2>&1; then
    echo "  ok     $name  (view only, no STL)"
  else
    echo "  FAIL   $name  (view)"
    FAILED=$((FAILED + 1))
  fi
}

echo "Rendering W17 11_cad models -> out/"
echo

echo "second_floor_cage.scad"
render cage_all           second_floor_cage.scad
render cage_body          second_floor_cage.scad -D 'part="cage"'
render cage_clip          second_floor_cage.scad -D 'part="clip"'
render_view cage_context  second_floor_cage.scad -D 'render_mode="context"'
render_view cage_section  second_floor_cage.scad -D 'render_mode="section"'

echo "esp_tray.scad"
render esp_shoe           esp_tray.scad -D 'variant="shoe"'
render esp_bench_tray     esp_tray.scad -D 'variant="bench"'

echo "fit_check_coupons.scad"
for c in c1 c2 c3 c4; do
  render "coupon_$c"      fit_check_coupons.scad -D "coupon=\"$c\""
done

echo "gcs_box.scad"
render gcs_tray           gcs_box.scad -D 'part="tray"'
render gcs_bulkhead       gcs_box.scad -D 'part="bulkhead"'
render gcs_lid            gcs_box.scad -D 'part="lid"'
for s in tx ftdi wifi hub; do
  render "gcs_sled_$s"    gcs_box.scad -D 'part="sled"' -D "sled_for=\"$s\""
done

echo
echo "rendered: $RENDERED   failed: $FAILED"

if [[ "$WANT_TABLE" == "1" ]]; then
  echo
  echo "| Model | Triangles | Bounding box (mm) | X | L | Z |"
  echo "|---|---:|---|---|---|---|"
  for f in "$OUT"/*.stl; do
    [[ -e "$f" ]] || continue
    python3 "$HERE/tools/stl_stats.py" "$f" \
      | awk -F'\t' '{printf "| `%s` | %s | %s | %s | %s | %s |\n", $1,$2,$3,$4,$5,$6}'
  done
fi

exit $(( FAILED > 0 ? 1 : 0 ))
