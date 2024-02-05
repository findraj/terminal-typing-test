import curses

def middle(stdscr, string):
    height, width = stdscr.getmaxyx()
    x = (width // 2) - (len(string) // 2)

    lines = len(string) // width
    y = (height // 2) - (lines // 2)

    return x, y

def prepare_text(stdscr, string: str, numberOfWords: int):
    height, width = stdscr.getmaxyx()
    stringSplit = string.split(" ")
    stringTrimmed = stringSplit[:numberOfWords]
    #stringJoined = " ".join(stringTrimmed)

    length = 0
    line = []
    finalString = []

    for word in stringSplit:
        length += len(word)
        if (length < (width - 1)):
            line.append(word)
        else:
            finalString.append(" ".join(line))
            line = []
            length = 0

    return finalString

def start_screen(stdscr):
    startMessage = "Press any button to start"
    x, y = middle(stdscr, startMessage)

    stdscr.clear()
    stdscr.addstr(y, x, startMessage)
    stdscr.refresh()
    stdscr.getkey()

def test_screen(stdscr):
    height, width = stdscr.getmaxyx()

    try:
        file = open("test-texts.txt", "r")
        numberOfWords = 4
        loadedText = file.read()
        testText = prepare_text(stdscr, loadedText, numberOfWords)
        testText = testText[0]
    except:
        testText = "hello world"
    answer = []

    x, y = middle(stdscr, testText)

    stdscr.clear()
    stdscr.addstr(y, x, testText)
    stdscr.move(y, x)
    stdscr.refresh()

    score = 0
    isCorrect = False
    charCounter = 0
    while True:
        if (charCounter == len(testText)):
            break

        key = stdscr.getkey()
        stdscr.addstr(0, 0, str(score))

        if (key == "KEY_BACKSPACE"):
            if (charCounter == 0):
                continue

            stdscr.addstr(y, x + charCounter - 1, testText[charCounter - 1], curses.color_pair(1))
            stdscr.move(y, x + charCounter - 1)
            answer.pop()

            if (testText[charCounter - 1] == " "):
                score -= 1

            charCounter -= 1
        else:
            if ((key == " ") & isCorrect):
                score += 1

            answer.append(key)

            for i in range(len(answer)):
                if (answer[i] == testText[i]):
                    stdscr.addstr(y, x + i, answer[i], curses.color_pair(2))
                    isCorrect = True
                else:
                    stdscr.addstr(y, x + i, testText[i], curses.color_pair(3))
                    isCorrect = False

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