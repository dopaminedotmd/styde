#!/bin/bash
# Firebase Test Lab integration script
set -euo pipefail

PROJECT_ID="${FIREBASE_PROJECT_ID:?Firebase project ID required}"
APK_PATH="${1:-android/app/build/outputs/apk/debug/app-debug.apk}"
RESULTS_DIR="${2:-.artifacts/firebase-test-lab}"

echo "==> Deploying to Firebase Test Lab"
echo "Project: $PROJECT_ID"
echo "APK: $APK_PATH"

gcloud config set project "$PROJECT_ID"

# Run instrumentation test matrix
gcloud firebase test android models list --verbosity=error 2>/dev/null || \
  echo "Warning: gcloud not fully configured"

echo "==> Submitting test matrix to Firebase Test Lab"

MATRIX_ID=$(gcloud firebase test android run \
  --type instrumentation \
  --app "$APK_PATH" \
  --test "android/app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk" \
  --device model=Pixel6,version=31,locale=en,orientation=portrait \
  --device model=Pixel7,version=33,locale=en,orientation=portrait \
  --device model=GalaxyS23,version=34,locale=en,orientation=portrait \
  --timeout 10m \
  --results-dir="$RESULTS_DIR" \
  --format=json \
  --verbosity=error 2>&1 | jq -r '.matrix.matrixId')

echo "Matrix ID: $MATRIX_ID"
echo "Monitor at: https://console.firebase.google.com/project/$PROJECT_ID/testlab/histories"

# Poll for completion
for i in $(seq 1 30); do
  STATUS=$(gcloud firebase test android matrices describe "$MATRIX_ID" \
    --format="json" --verbosity=error | jq -r '.state')
  echo "Poll $i/30: $STATUS"
  if [ "$STATUS" = "FINISHED" ]; then break; fi
  if [ "$STATUS" = "ERROR" ] || [ "$STATUS" = "INVALID" ]; then
    echo "Matrix failed with state: $STATUS"
    exit 1
  fi
  sleep 30
done

# Download results
echo "==> Downloading test results"
mkdir -p "$RESULTS_DIR"
gcloud firebase test android matrices describe "$MATRIX_ID" \
  --format="json" --verbosity=error | jq -r '.resultStorage.toolResultsHistory[0].historyId'
gcloud alpha firebase test android results download "$MATRIX_ID" "$RESULTS_DIR" --verbosity=error

echo "==> Firebase Test Lab run complete"
echo "Results: $RESULTS_DIR"
