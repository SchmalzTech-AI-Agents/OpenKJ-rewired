# OpenKJ Rewired

OpenKJ Rewired is a modernized, maintainable continuation of OpenKJ, a desktop karaoke show-hosting application for managing singers, song libraries, requests, rotation, karaoke media, and break music.

This project is a modified/modernized derivative of the original OpenKJ codebase. It respectfully preserves the foundation and prior work of the late **T. Isaac Lightburn** and the original OpenKJ contributors. They deserve clear attribution; the original contributors did not participate in this continuation unless explicitly stated in a future contribution record.

## Features

- Song database management with custom filename patterns
- Regular singers, rotation handling, requests, and export tools
- CDG karaoke playback, video playback, and break music
- Key, tempo, EQ, volume, and playback controls
- Recording where supported by the host platform and GStreamer
- Persistent settings, window geometry, splitter state, and table/header layouts
- Reset Column Widths behavior
- High-DPI-aware desktop UI with centralized visual styling and existing light/dark theme support
- Retired SongShop, payment, account, and purchase functionality remains absent

## Supported platforms

- Modern 64-bit Linux (validated locally on Ubuntu 24.04 toolchain packages)
- Windows 64-bit (GitHub Actions uses `windows-2022`)

macOS files remain in history as historical project material but are not a supported target of this rewired build.

## System requirements

Runtime requirements are Qt Widgets, Qt SQL, Qt Network, Qt SVG, GStreamer 1.x, TagLib, and spdlog. A working audio/video device and GStreamer plugins are required for media playback. Use a 64-bit OS and current graphics/audio drivers.

## Development prerequisites

- CMake 3.24 or newer
- C++20 compiler (GCC 13+, Clang 16+, or current MSVC/MinGW)
- Ninja 1.11+ recommended (Makefiles also work on Linux)
- Qt 6 development packages preferred; Qt 5.15 remains a compatibility fallback during migration
- GStreamer 1.x development packages and runtime plugins
- TagLib and spdlog development packages
- Python 3 for repository invariant tests
- Git with submodule support

## Linux dependency installation

On Ubuntu 24.04, install the toolchain and development packages:

```bash
sudo apt update
sudo apt install -y build-essential cmake ninja-build pkg-config python3 \
  qt6-base-dev qt6-tools-dev libqt6svg6-dev \
  libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev \
  libtag1-dev libspdlog-dev
```

If Qt 6 is unavailable on a distribution, install the equivalent Qt 5.15 development packages. CMake selects Qt 6 first and falls back to Qt 5.

## Linux build and test

Use a clean out-of-tree build:

```bash
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build --parallel
ctest --test-dir build --output-on-failure
```

When Ninja is unavailable, replace `-G Ninja` with `-G 'Unix Makefiles'`. The build uses system GStreamer and TagLib when available. spdlog uses the pinned CMake fallback by default because the existing code targets the bundled fmt ABI; set `-DOPENKJ_USE_SYSTEM_SPDLOG=ON` only after validating the distribution's spdlog/fmt combination.

Run after building:

```bash
QT_QPA_PLATFORM=offscreen ./build/openkj
```

The application is interactive and normally stays running until closed. Do not use an offscreen run as a media-playback test; verify playback with a real desktop session and installed GStreamer plugins.

## Windows build

Use a x64 Visual Studio Developer PowerShell or a MinGW environment with Qt 6 x64, GStreamer x64 development/runtime packages, CMake, and Ninja installed. From PowerShell:

```powershell
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build --parallel
ctest --test-dir build --output-on-failure
```

The Windows CI workflow installs a 64-bit Qt toolchain, installs current compatible GStreamer packages, builds with CMake/Ninja, runs tests, deploys Qt runtime files where available, and uploads a verifiable artifact. No 32-bit Windows matrix is retained.

## Packaging and deployment

Linux staging can be produced with:

```bash
cmake --install build --prefix "$PWD/dist"
```

For Windows, use `windeployqt` from the selected Qt installation and copy the matching GStreamer runtime DLLs and plugin directory beside the executable. CI packages these files into an artifact when the runner dependencies are available.

## Troubleshooting

- **Qt not found:** confirm `Qt6Config.cmake` or the Qt 5 equivalent is on `CMAKE_PREFIX_PATH`; delete the build directory after changing Qt installations.
- **GStreamer not found:** verify `pkg-config --modversion gstreamer-1.0` on Linux. On Windows, verify the x64 development package and that its include/lib locations are visible to CMake.
- **GStreamer starts but media is silent:** install the platform's base/good/bad/ugly plugin sets and check the selected audio device.
- **CMake uses stale dependencies:** remove `build/` and reconfigure; do not mix Qt architectures in one build directory.
- **Compiler errors after a Qt upgrade:** rebuild generated MOC/UIC files from a clean directory and check for a missing Qt module in the configure output.
- **High-DPI layout issues:** use a current Qt platform plugin and test at more than 100% display scaling; avoid hard-coded window sizes when adding UI.
- **Windows runtime failure:** run `windeployqt`, copy GStreamer DLLs/plugins matching the executable architecture, and ensure no 32-bit package is earlier on `PATH`.

## Licensing and attribution

OpenKJ Rewired is distributed under **GNU GPLv3**. The root `LICENSE`, `src/LICENSE`, and `src/cdg/LICENSE` files are preserved. Existing source copyright and attribution notices remain intact. New and modified code is part of this GPLv3 derivative unless a file states otherwise.

This work is based on OpenKJ and the original contributions of the late T. Isaac Lightburn and other OpenKJ contributors. OpenKJ Rewired does not claim that those contributors participated in this project.

See `THIRD_PARTY_NOTICES.md` for dependency notices and license locations. Do not add proprietary or credential-bearing files to this repository.

## Contributing

Keep changes incremental and buildable. Preserve karaoke workflow behavior, settings migration compatibility, table layout persistence/reset behavior, active-video clearing, and GPLv3 notices. Add a focused regression test for behavior changes, run configure/build/CTest, run `git diff --check`, and describe platform-specific limitations in the pull request. Do not reintroduce payment, account, purchase, SongShop, password, or card-data features.
