# json-to-midi-fl

A Python utility to convert JSON-formatted music data into MIDI files compatible with FL Studio and other DAWs.

## Description

`json-to-midi-fl` transforms JSON files containing musical track and note data into MIDI files. Designed for projects like *Herald of Darkness*, it supports multiple tracks, dynamic instrument mapping, and precise control over note timing and velocity. The script is modular, extensible, and includes error handling for robust operation.

## Features

- Converts JSON music data to MIDI with support for multiple tracks
- Maps track names to General MIDI instruments via a configurable JSON file
- Supports drum tracks (MIDI channel 10) and melodic instruments
- Handles note start times, durations, and velocities in ticks
- Includes error handling for JSON validation and file I/O
- Command-line interface for easy integration

## Installation

1. Ensure you have Python 3.6+ installed.
2. Install the required `midiutil` library:

```bash
pip install midiutil
```

3. Clone or download this repository.

## Usage

1. **Prepare your JSON file**: Create a JSON file (e.g., `input.json`) with your music data, following the structure described below.
2. **Run the script**:

```bash
python json_to_midi.py input.json output.mid
```

This generates `output.mid` from `input.json`.

3. **Import into FL Studio**:
   - Open FL Studio and go to `File > Import > MIDI File`.
   - Select `output.mid`.
   - Check `Create one channel per track` and set `Channel type: FLEX` for General MIDI compatibility.
   - Adjust instruments in the Channel Rack to match your desired sounds.

**Note**: Ensure your JSON includes notes spanning the entire song to avoid issues like single-beat tracks. For example, for an 8-bar song at 126 BPM with 96 ticks per beat, include notes every 96 ticks for beats or 384 ticks for measures.

## JSON Structure

The input JSON file must include:

- `ticks_per_beat`: Number of ticks per beat (e.g., 96).
- `bpm`: Tempo in beats per minute (e.g., 126.0).
- `tracks`: List of tracks, each with:
  - `track_number`: Track index (0-based).
  - `name`: Track name for instrument mapping (e.g., "22in Kick", "FL Slayer").
  - `channel`: MIDI channel (0-15, use 9 for drums).
  - `notes`: List of notes, each with:
    - `note`: MIDI note number (0-127).
    - `velocity`: Note velocity (0-127).
    - `start_time`: Start time in ticks.
    - `duration`: Duration in ticks.

### Example JSON

```json
{
    "ticks_per_beat": 96,
    "bpm": 126.0,
    "tracks": [
        {
            "track_number": 0,
            "name": "22in Kick",
            "channel": 9,
            "notes": [
                {"note": 36, "velocity": 100, "start_time": 0, "duration": 96},
                {"note": 36, "velocity": 100, "start_time": 192, "duration": 96},
                {"note": 36, "velocity": 100, "start_time": 384, "duration": 96}
            ]
        },
        {
            "track_number": 1,
            "name": "FL Slayer",
            "channel": 0,
            "notes": [
                {"note": 60, "velocity": 100, "start_time": 96, "duration": 96},
                {"note": 62, "velocity": 100, "start_time": 288, "duration": 96}
            ]
        }
    ]
}
```

## Instrument Mapping

Instrument mappings are defined in `instrument_config.json` and can be customized. Default mappings include:

| Track Name   | GM Number | Instrument         | Channel |
|--------------|-----------|--------------------|---------|
| 22in Kick    | 36        | Bass Drum 1        | 9       |
| 707 Snare    | 38        | Acoustic Snare     | 9       |
| 707 CH       | 42        | Closed Hi-Hat      | 9       |
| 909 Clap     | 39        | Hand Clap          | 9       |
| FL Slayer    | 26        | Electric Guitar    | User-defined |
| 3xOsc        | 34        | Electric Bass      | User-defined |
| Sytrus       | 49        | String Ensemble    | User-defined |

To add new instruments, update `instrument_config.json` with new `drum_mappings` or `instrument_mappings`.

## Customizing Instrument Mappings

1. Edit `instrument_config.json` to add or modify mappings.
2. Example addition:

```json
{
    "drum_mappings": {
        "New Kick": 35
    },
    "instrument_mappings": {
        "New Synth": 81
    }
}
```

3. The script will load these mappings automatically.

## Troubleshooting

- **Single-beat tracks**: Ensure your JSON includes multiple notes spanning the song’s duration.
- **Invalid JSON**: Check for syntax errors in your JSON file.
- **Missing instruments**: Verify track names match those in `instrument_config.json`.

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -m "Add new feature"`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Open a pull request.

Please include tests and update the README if necessary.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, open an issue on GitHub or contact the maintainer at [your.email@example.com].

## References

- [MIDIUtil Documentation](https://midiutil.readthedocs.io/en/1.2.1/index.html)
- [FL Studio MIDI Import Manual](https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/midi_import.htm)
- [General MIDI Specifications](https://www.midi.org/specifications-old/item/gm-level-1)
