import curses

def middle(stdscr, string):
    height, width = stdscr.getmaxyx()
    x = (width // 2) - (len(string) // 2)

    lines = len(string) // width
    y = (height // 2) - (lines // 2)

    return x, y

def start_screen(stdscr):
    startMessage = "Press any button to start"
    x, y = middle(stdscr, startMessage)

    stdscr.clear()
    stdscr.addstr(y, x, startMessage)
    stdscr.refresh()
    stdscr.getkey()

def test_screen(stdscr):
    testText = "hello world"
    answer = []

    x, y = middle(stdscr, testText)

    stdscr.clear()
    stdscr.addstr(y, x, testText)
    stdscr.move(y, x)
    stdscr.refresh()

    charCounter = 0
    while True:
        if (charCounter == len(testText)):
            break

        key = stdscr.getkey()

        if (key == "KEY_BACKSPACE"):
            if (charCounter == 0):
                continue

            stdscr.addstr(y, x + charCounter - 1, testText[charCounter - 1], curses.color_pair(1))
            stdscr.move(y, x + charCounter - 1)
            answer.pop()

            charCounter -= 1
        else:
            answer.append(key)

            for i in range(len(answer)):
                if (answer[i] == testText[i]):
                    stdscr.addstr(y, x + i, answer[i], curses.color_pair(2))
                else:
                    if (key == " "):
                        stdscr.addstr(y, x + i, testText[i], curses.color_pair(3))
                    else:    
                        stdscr.addstr(y, x + i, answer[i], curses.color_pair(3))

            charCounter += 1

    end_screen(stdscr)

def end_screen(stdscr):
    endString = "Press Enter to restart / Press any other key to end"
    x, y = middle(stdscr, endString)

    stdscr.addstr(y  + y // 2, x, endString)
    stdscr.refresh()
    key = stdscr.getkey()
    if key == "\n":
        test_screen(stdscr)

def main(stdscr):
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    start_screen(stdscr)
    test_screen(stdscr)

curses.wrapper(main)