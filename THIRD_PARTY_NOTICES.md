# Third-party notices

OpenKJ Rewired retains the third-party source and license material already present in the OpenKJ tree. This file records the dependency strategy for the modernized build; it is not a relicensing notice.

| Dependency | Use | License / notice location |
| --- | --- | --- |
| Qt 6 (Qt 5 compatibility fallback) | Desktop UI, SQL, networking, SVG, concurrency | LGPLv3/GPLv3/commercial terms; see the Qt distribution and https://www.qt.io/licensing/ |
| GStreamer 1.x | Audio, video, CDG-related media pipeline | LGPL-2.1-or-later; see the installed GStreamer distribution and https://gstreamer.freedesktop.org/ |
| TagLib | Audio metadata | LGPL-2.1-or-later/MPL-1.1; see `src/taglib` and the TagLib distribution |
| spdlog | Logging | MIT; see `src/3rdparty/spdlog` when the submodule is initialized and https://github.com/gabime/spdlog |
| miniz | ZIP/archive support | MIT; see `src/miniz` source notices |

The complete GPL text and applicable notices remain in the repository. When adding a dependency, add its exact version, source form, license, and redistribution notice here before merging. Build-time downloads must not silently replace a system dependency without documenting the source and version.
