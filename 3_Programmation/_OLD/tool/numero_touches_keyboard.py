import keyboard

print("Press any key (ESC to quit):")

while True:
    event = keyboard.read_event()
    if event.event_type == keyboard.KEY_DOWN:
        print(f"Key pressed: {event.name} (code: {ord(event.name) if len(event.name) == 1 else 'N/A'})")
        if event.name == 'esc':
            break
