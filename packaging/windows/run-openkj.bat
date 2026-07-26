@echo off
setlocal
set "APP_DIR=%~dp0"
set "PATH=%APP_DIR%;%APP_DIR%bin;%PATH%"
set "GST_PLUGIN_PATH=%APP_DIR%lib\gstreamer-1.0"
set "GST_PLUGIN_SYSTEM_PATH_1_0="
set "GST_PLUGIN_SCANNER=%APP_DIR%libexec\gstreamer-1.0\gst-plugin-scanner.exe"
"%APP_DIR%openkj.exe" %*
endlocal
