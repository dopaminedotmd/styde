#!/bin/bash
# BrowserStack App Automate integration
set -euo pipefail

BS_USERNAME="${BROWSERSTACK_USERNAME:?BrowserStack username required}"
BS_ACCESS_KEY="${BROWSERSTACK_ACCESS_KEY:?BrowserStack access key required}"
APP_PATH="${1:?App path required (apk/ipa)}"
PLATFORM="${2:-android}"
SUITE="${3:-smoke}"

echo "==> Uploading app to BrowserStack"
echo "App: $APP_PATH"
echo "Platform: $PLATFORM"
echo "Suite: $SUITE"

# Detect app type from path
if [[ "$APP_PATH" == *.apk ]]; then
  CUSTOM_ID="YourApp-Android-$(date +%s)"
elif [[ "$APP_PATH" == *.ipa ]]; then
  CUSTOM_ID="YourApp-iOS-$(date +%s)"
else
  echo "Unknown app type. Use .apk or .ipa"
  exit 1
fi

UPLOAD_RESPONSE=$(curl -s -u "$BS_USERNAME:$BS_ACCESS_KEY" \
  -X POST "https://api-cloud.browserstack.com/app-automate/upload" \
  -F "file=@$APP_PATH" \
  -F "custom_id=$CUSTOM_ID")

APP_URL=$(echo "$UPLOAD_RESPONSE" | jq -r '.app_url // .error')
if [ "$APP_URL" = "null" ]; then
  echo "Upload failed: $UPLOAD_RESPONSE"
  exit 1
fi
echo "App URL: $APP_URL"

# Build browser stack test config
cat > .artifacts/browserstack-config.json << JSONEOF
{
  "app": "$APP_URL",
  "devices": ["Google Pixel 7-13.0", "Samsung Galaxy S23-14.0"],
  "deviceLogs": true,
  "networkLogs": true,
  "debug": true,
  "project": "YourApp",
  "build": "Build $(date +%Y%m%d-%H%M)",
  "local": false,
  "localIdentifier": null,
  "callbackURL": null,
  "suite": "$SUITE"
}
JSONEOF

# Trigger test execution on BrowserStack
echo "==> Triggering BrowserStack App Automate"
RUN_RESPONSE=$(curl -s -u "$BS_USERNAME:$BS_ACCESS_KEY" \
  -X POST "https://api-cloud.browserstack.com/app-automate/run" \
  -H "Content-Type: application/json" \
  -d "$(cat .artifacts/browserstack-config.json)")

BUILD_ID=$(echo "$RUN_RESPONSE" | jq -r '.build_id // .error')
echo "Build ID: $BUILD_ID"
echo "Dashboard: https://app-automate.browserstack.com/dashboard/v2/builds/$BUILD_ID"

# Wait for completion
echo "==> Waiting for BrowserStack build to complete..."
for i in $(seq 1 60); do
  BUILD_STATUS=$(curl -s -u "$BS_USERNAME:$BS_ACCESS_KEY" \
    "https://api-cloud.browserstack.com/app-automate/builds/$BUILD_ID" | jq -r '.status')
  echo "Poll $i/60: $BUILD_STATUS"
  if [ "$BUILD_STATUS" = "done" ]; then
    echo "Build complete"
    break
  fi
  if [ "$BUILD_STATUS" = "failed" ] || [ "$BUILD_STATUS" = "error" ]; then
    echo "Build failed"
    exit 1
  fi
  sleep 10
done

# Download reports
mkdir -p .artifacts/browserstack/reports
curl -s -u "$BS_USERNAME:$BS_ACCESS_KEY" \
  "https://api-cloud.browserstack.com/app-automate/builds/$BUILD_ID/report" \
  > .artifacts/browserstack/reports/build-report.json

echo "==> BrowserStack run complete"
