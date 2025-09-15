# FilterByDate Plugin for fman

A plugin for [fman](https://fman.io) that allows you to filter the current directory to show only files modified within specific time periods.

## Features

- Filter files by modification date:
  - **Today**: Show only files modified today
  - **3 Days**: Show files modified in the last 3 days
  - **7 Days**: Show files modified in the last 7 days
  - **30 Days**: Show files modified in the last 30 days
- Seamlessly switch between different filter periods
- Clear filter to return to normal directory view
- Preserve file operations (open, copy, move) in filtered views

## Installation

1. Copy the `FilterByDate` folder to your fman plugins directory:
   - Windows: `%APPDATA%\fman\Plugins\User\`
   - macOS: `~/Library/Application Support/fman/Plugins/User/`
   - Linux: `~/.config/fman/Plugins/User/`

2. Restart fman or reload plugins

## Usage

### Basic Usage

1. Navigate to any directory in fman
2. Press `Ctrl+Shift+P` to open the command palette
3. Type one of the following commands:
   - `Filter Today` - Show files modified today
   - `Filter 3 Days` - Show files from last 3 days
   - `Filter 7 Days` - Show files from last week
   - `Filter 30 Days` - Show files from last month

### Switching Filters

When you're already viewing filtered files, you can switch to a different time period:
- Simply run any other filter command
- The plugin will maintain the same base directory and apply the new filter

### Clearing Filters

To return to the normal directory view:
- Press `Ctrl+Shift+P` and run `Clear Date Filter`
- Or navigate away from the filtered view

### File Operations

While viewing filtered files, you can:
- **Open files**: Press Enter or double-click
- **Copy/Move files**: All standard fman operations work
- **View file properties**: Size, modification date are displayed correctly

## Technical Details

The plugin creates a custom filesystem with URLs in the format:
```
datefilter://<days>/<encoded_path>
```

Where:
- `<days>` is 0, 3, 7, or 30
- `<encoded_path>` is the URL-encoded original directory path

This design makes the plugin stateless - all necessary information is contained in the URL itself.

## Requirements

- fman file manager
- Python 3.6+

## License

This plugin is provided as-is for educational and personal use.