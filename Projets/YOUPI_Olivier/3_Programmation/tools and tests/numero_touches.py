while True:
    key = input("Press a key (ESC to quit): ")
    print(f"Key pressed: {ord(key)}")
    if ord(key) == 27:  # ESC key to exit
        break

