# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BabyMinder is a standalone Python GUI application for tracking daily baby care tasks. It's a simple, fullscreen Tkinter application designed for quick touchscreen interaction on devices like tablets or Raspberry Pi displays.

## Running the Application

```bash
python babyminder.py
```

The application requires Python 3 with tkinter (usually included in standard Python installations).

## Architecture

### Single File Application
The entire application is contained in `babyminder.py` with a single `BabyTracker` class that manages:
- Tkinter UI with fullscreen interface
- JSON-based persistent storage in `~/.babytracker.json`
- Daily task tracking (soins/vitamines with boolean toggles)
- Diaper counter with both daily and cumulative totals
- Automatic daily reset at midnight

### Data Model
Data persists in JSON format at `~/.babytracker.json`:
```json
{
  "date": "YYYY-MM-DD",
  "soins": bool,
  "vitamines": bool,
  "couches_jour": int,
  "couches_total": int
}
```

### Key Behaviors
- **Midnight rollover**: The app checks every 60 seconds for date changes and automatically resets daily counters while preserving cumulative totals
- **Fullscreen mode**: Designed for dedicated display devices (exit button top-right)
- **Color-coded UI**: Toggle buttons turn green when completed, red when pending
- **No dependencies**: Uses only Python standard library (tkinter, json, datetime)

## Code Notes
- The application is in French (UI labels: "SOINS", "VITAMINES", "COUCHE")
- UI uses a dark theme (`#2c3e50` background) with large touch-friendly buttons
- All state changes immediately persist to disk via `save_data()`
