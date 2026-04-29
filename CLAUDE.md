# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Model train hobby project with three independent subdirectories for layout infrastructure CAD, train car CAD, and embedded control firmware. Licensed under GPLv3.

## Repository Structure

- **CADlayout/** — FreeCAD parametric designs for layout infrastructure (cable clips, electrical boxes, power boxes). Each component has a `.FCStd` source file and exported `.stl` files for 3D printing.
- **CADtrains/** — FreeCAD parametric designs for train cars and station structures (caboose interior, station platform). The StationPlatform uses an embedded FreeCAD spreadsheet for parametric dimensions.
- **IOTtrains/** — ESP32 Arduino firmware for model railroad control via MQTT. Contains two PlatformIO projects:
  - **Station_OS/** — Touchscreen station control panel using an ESP32 CYD (Cheap Yellow Display). Uses LVGL for the UI and an Adafruit PCA9685 servo driver over I2C to control turnouts. Publishes/subscribes to MQTT topics for train orders and turnout commands.
  - **Switch_Control/** — JMRI-compatible MQTT turnout controller. Drives a single servo via ESP32Servo library. Follows JMRI topic conventions: `{root}/turnout/{device_id}/state` with `CLOSED`/`THROWN` payloads. Has configurable servo angles and connection parameters (see `PRODUCT_REQUIREMENTS.md`).

Each subdirectory has its own independent git repository while also being tracked in the parent repo.

## FreeCAD Workflow

- All 3D models use FreeCAD's parametric `.FCStd` format
- STL exports include both standard and "Meshed" variants optimized for printing
- Component variants are generated from parametric models (e.g., ElectricBox with 2/4/6/8 slot configurations)
- See the parent `CLAUDE.md` at `/home/abyrne/Projects/CLAUDE.md` for FreeCAD MCP tool reference and 3D printer specs (Prusa Core One, 250x210mm build plate)

## IOTtrains Build & Upload

Both projects use PlatformIO with the Arduino framework targeting `esp32dev`.

```bash
# Build
cd IOTtrains/Station_OS && pio run
cd IOTtrains/Switch_Control && pio run

# Upload to connected ESP32
pio run --target upload

# Serial monitor (115200 baud)
pio device monitor
```

Libraries are resolved from `~/Arduino/libraries` (set via `lib_extra_dirs` in `platformio.ini`). Key dependencies:
- **Station_OS:** lvgl, TFT_eSPI, XPT2046_Touchscreen, AsyncMqttClient, Adafruit_PWMServoDriver, Wire
- **Switch_Control:** AsyncMqttClient, ESP32Servo

### MQTT Architecture

Both projects communicate over MQTT with auto-reconnect via FreeRTOS timers. Station_OS connects to a SPROG-Pi4 WiFi network with broker at `192.168.6.1`. Switch_Control follows JMRI conventions with a configurable `mqTrains` root topic.

## Conventions

- Component directories are named in PascalCase (e.g., `CableClip`, `ElectricBox`, `StationPlatform`)
- FreeCAD files are named to match their directory
- STL files include the body/feature name from FreeCAD (e.g., `PowerBox-Pad003 (Meshed).stl`)
