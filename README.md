# Trains

Model train hobby project. Contains three independent subdirectories for layout infrastructure CAD, train car CAD, and embedded control firmware.

## Documentation

| Document | Description |
|----------|-------------|
| [docs/NYE_OPERATIONS.md](docs/NYE_OPERATIONS.md) | NY&E Railroad operations reference — stations, industries, motive power, operating rules |

## Repositories

| Directory | Description |
|-----------|-------------|
| [CADlayout](https://github.com/adbyrne/CADlayout) | FreeCAD parametric designs for layout infrastructure (cable clips, electrical boxes, servo mounts, spline brackets) |
| [CADtrains](https://github.com/adbyrne/CADtrains) | FreeCAD parametric designs for rolling stock and station structures (caboose interior, station platform) |
| [IOTtrains](https://github.com/adbyrne/IOTtrains) | ESP32 firmware and RPi5 server software for MQTT-based layout control. Includes Station_OS, Switch_Control, TO_Signal, and RR_Server (dispatcher app, fast clock) |

Each subdirectory has its own independent git repository.

## License

GNU General Public License v3.0
