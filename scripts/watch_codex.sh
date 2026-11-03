#!/bin/bash
# Watch a Codex pane while it generates images (checks both saved files and whether Codex has finished)
# Usage: watch_codex.sh <terminal handle> <images folder> <file names without .png...>
#   e.g.: watch_codex.sh term_xxxx images bg1 bg2 food_mon sperm_mon
# Text from the request that reappears on screen (e.g., a "done" marker) is never used as a signal
# Exit codes
#   0: all files saved + Codex finished ("esc to interrupt" absent twice in a row)
#   2: approval prompt detected -> tell the user
#   3: Codex stopped before every file was saved
#   1: timed out (MAX_MIN minutes, default 50)
T="$1"; DIR="$2"; shift 2; NAMES="$*"
if [ -z "$T" ] || [ -z "$DIR" ] || [ -z "$NAMES" ]; then echo "Usage: watch_codex.sh <handle> <folder> <file names...>"; exit 9; fi
TOTAL=$(echo $NAMES | wc -w | tr -d ' '); MAX=$(( ${MAX_MIN:-50} * 4 ))
START=$(date +%s); seen=""; idle=0; cnt=0
for i in $(seq 1 $MAX); do
  cnt=0
  for n in $NAMES; do
    f="$DIR/$n.png"
    # Count only files saved (modified) after start -> a regenerated file must be saved again to count
    if [ -f "$f" ] && [ "$(stat -f %m "$f")" -ge "$START" ]; then
      cnt=$((cnt+1))
      if [[ "$seen" != *"[$n]"* ]]; then seen="$seen[$n]"; echo "$(date +%H:%M:%S) $n.png saved ($cnt/$TOTAL)"; fi
    fi
  done
  screen=$(orca terminal read --terminal "$T" --screen 2>/dev/null)
  if echo "$screen" | grep -q -E "Allow|approve|Yes, proceed|Do you want|permission"; then
    echo "$(date +%H:%M:%S) approval prompt detected"; echo "$screen" | grep -v -E '^\s*$' | tail -30; exit 2
  fi
  if echo "$screen" | grep -q "esc to interrupt"; then idle=0; else idle=$((idle+1)); fi
  if [ "$idle" -ge 2 ]; then
    if [ "$cnt" -eq "$TOTAL" ]; then echo "$(date +%H:%M:%S) $TOTAL files saved, Codex finished"; code=0
    else echo "$(date +%H:%M:%S) Codex stopped (saved: $cnt/$TOTAL)"; code=3; fi
    echo "$screen" | grep -v -E '^\s*$' | tail -30; exit $code
  fi
  sleep 15
done
echo "Timed out (${MAX_MIN:-50} min). Saved: $cnt/$TOTAL"; exit 1
