import json
import os
from midiutil import MIDIFile
from typing import Dict, List, Optional

class Track:
    def __init__(self, track_data: Dict, track_idx: int):
        self.name = track_data.get('name', f'Track_{track_idx}')
        self.notes = track_data.get('notes', [])
        self.channel = track_data.get('channel', 0)
        self.track_number = track_data.get('track_number', track_idx)

    def validate(self) -> bool:
        if not self.notes:
            print(f"Warning: Track '{self.name}' has no notes.")
            return False
        for note in self.notes:
            if not all(k in note for k in ['note', 'velocity', 'start_time', 'duration']):
                print(f"Error: Invalid note format in track '{self.name}'.")
                return False
        return True

class InstrumentMapper:
    def __init__(self, config_path: str = 'instrument_config.json'):
        self.drum_mappings = {
            '22in Kick': 36, '707 Snare': 38, '707 CH': 42, '909 Clap': 39
        }
        self.instrument_mappings = {
            'FL Slayer': 26, '3xOsc': 34, 'Sytrus': 49
        }
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    self.drum_mappings.update(config.get('drum_mappings', {}))
                    self.instrument_mappings.update(config.get('instrument_mappings', {}))
            except json.JSONDecodeError:
                print(f"Warning: Invalid JSON in {config_path}. Using default mappings.")

    def get_mapping(self, track_name: str) -> tuple[int, Optional[int]]:
        if track_name in self.drum_mappings:
            return self.drum_mappings[track_name], 9  # Drum channel
        return self.instrument_mappings.get(track_name, 0), None

class MidiGenerator:
    def __init__(self, json_path: str, output_path: str, ticks_per_beat: int = 96):
        self.json_path = json_path
        self.output_path = output_path
        self.ticks_per_beat = ticks_per_beat
        self.midi_file: Optional[MIDIFile] = None
        self.tracks: List[Track] = []
        self.bpm: float = 126.0
        self.instrument_mapper = InstrumentMapper()

    def load_json(self) -> None:
        try:
            with open(self.json_path, 'r') as f:
                data = json.load(f)
            self.bpm = data.get('bpm', 126.0)
            self.ticks_per_beat = data.get('ticks_per_beat', 96)
            self.tracks = [Track(t, i) for i, t in enumerate(data.get('tracks', []))]
        except FileNotFoundError:
            raise FileNotFoundError(f"JSON file '{self.json_path}' not found.")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in '{self.json_path}'.")

    def generate_midi(self) -> None:
        if not self.tracks:
            raise ValueError("No tracks to process.")
        self.midi_file = MIDIFile(len(self.tracks))
        self.midi_file.addTempo(0, 0, self.bpm)

        for track in self.tracks:
            if not track.validate():
                continue
            self.midi_file.addTrackName(track.track_number, 0, track.name)
            note_number, drum_channel = self.instrument_mapper.get_mapping(track.name)
            channel = drum_channel if drum_channel is not None else track.channel
            self.midi_file.addProgramChange(track.track_number, channel, 0, note_number if drum_channel is None else 0)
            for note in track.notes:
                self.midi_file.addNote(
                    track.track_number,
                    channel,
                    note['note'] if drum_channel is None else note_number,
                    note['start_time'] / self.ticks_per_beat,
                    note['duration'] / self.ticks_per_beat,
                    note['velocity']
                )

    def save_midi(self) -> None:
        try:
            with open(self.output_path, 'wb') as output_file:
                self.midi_file.writeFile(output_file)
            print(f"MIDI file generated: {self.output_path}")
        except IOError as e:
            raise IOError(f"Failed to write MIDI file '{self.output_path}': {e}")

    def run(self) -> None:
        self.load_json()
        self.generate_midi()
        self.save_midi()

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Usage: python json_to_midi.py <input.json> <output.mid>")
        sys.exit(1)
    generator = MidiGenerator(sys.argv[1], sys.argv[2])
    try:
        generator.run()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
