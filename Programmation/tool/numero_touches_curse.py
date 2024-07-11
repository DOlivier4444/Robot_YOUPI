import curses

def main(stdscr):
    while True:
        key = stdscr.getch()
        stdscr.addstr(f"Key pressed: {key}\n")
        stdscr.refresh()
        if key == 27:  # ESC key to exit
            break

if __name__ == "__main__":
    curses.wrapper(main)

