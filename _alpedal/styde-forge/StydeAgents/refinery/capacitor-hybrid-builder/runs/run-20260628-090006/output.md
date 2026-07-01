blueprint: capacitor-hybrid-builder
version: 1
domain: app-dev
status: loaded
project: styde-forge
capacitor: not detected
searching: E:\Stryde\_alpedal\styde-forge
evaluation:
  capacitor_config: not found
  package_json: not found
  android_manifest: not found
  ios_xcodeproj: not found
  hybrid_bridge: not present
result:
  ready: false
  reason: project is agent-training crucible, not hybrid app
  recommendation: create separate hybrid subproject or standalone scaffold
available_services:
  camera: capacitor_camera_plugin needed
  geolocation: capacitor_geolocation_plugin needed
  filesystem: capacitor_filesystem_plugin needed
  bridge: capacitor_echo_plugin or custom
deploy:
  android: capacitor_add_android_required
  ios: capacitor_add_ios_required
  livereload: capacitor_serve_with_livereload_flag