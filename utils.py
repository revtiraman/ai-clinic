import pandas as pd
import re

def parse_csv(csv_text):
    lines = csv_text.splitlines()
    headers = [h.strip().replace('"', '') for h in lines[0].split(',')]
    data = []
    current = {}
    dialogue_buffer = ""
    note_buffer = ""
    in_dialogue = in_note = False

    for line in lines[1:]:
        if line.startswith('virtassist,D2N') or line.startswith('aci,D2N'):
            if current and dialogue_buffer and note_buffer:
                current["dialogue"] = dialogue_buffer.strip().strip('"')
                current["note"] = note_buffer.strip().strip('"')
                data.append(current)
            parts = line.split(',')
            current = {"dataset": parts[0], "encounter_id": parts[1]}
            dialogue_buffer = ",".join(parts[2:]) or ""
            note_buffer = ""

            if dialogue_buffer.startswith('"') and not dialogue_buffer.endswith('"'):
                in_dialogue = True
            else:
                note_split = dialogue_buffer.rfind('",')
                if note_split != -1:
                    note_buffer = dialogue_buffer[note_split + 2:]
                    dialogue_buffer = dialogue_buffer[:note_split + 1]
                    in_note = note_buffer.startswith('"') and not note_buffer.endswith('"')
                in_dialogue = False
        else:
            if in_dialogue:
                dialogue_buffer += "\n" + line
                if line.endswith('"'):
                    note_split = dialogue_buffer.rfind('",')
                    if note_split != -1:
                        note_buffer = dialogue_buffer[note_split + 2:]
                        dialogue_buffer = dialogue_buffer[:note_split + 1]
                        in_dialogue = False
                        in_note = note_buffer.startswith('"') and not note_buffer.endswith('"')
            elif in_note:
                note_buffer += "\n" + line
                if line.endswith('"'):
                    in_note = False
            else:
                note_buffer += "\n" + line
                if line.endswith('"'):
                    in_note = False

    if current and dialogue_buffer and note_buffer:
        current["dialogue"] = dialogue_buffer.strip().strip('"')
        current["note"] = note_buffer.strip().strip('"')
        data.append(current)

    return data
