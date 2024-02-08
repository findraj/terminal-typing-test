import curses

def prepare_text(stdscr, width, height, string: str, numberOfWords: int):
    stringSplit = string.split(" ")
    stringTrimmed = stringSplit[:numberOfWords]
    stringJoined = " ".join(stringTrimmed)

    return stringJoined

def start_screen(stdscr, width, height):
    startMessage = "Press any button to start"
    x = (width - len(startMessage)) // 2
    y = height // 2

    stdscr.clear()
    stdscr.addstr(y, x, startMessage)
    stdscr.refresh()
    stdscr.getkey()

def test_screen(stdscr, width, height):
    try:
        file = open("test-texts.txt", "r")
        numberOfWords = 20
        loadedText = file.read()
        #testText = prepare_text(stdscr, width, height, loadedText, numberOfWords)
        testText = loadedText
    except:
        testText = "hello world"
    answer = []

    x = 0
    y = (height - (len(testText) // width)) // 2

    stdscr.clear()
    stdscr.addstr(y, x, testText)
    stdscr.move(y, x)
    stdscr.refresh()

    words = 0
    correct = 0
    wordList = [[]]
    charCounter = 0
    while True:
        if (charCounter == len(testText)):
            break

        # show number of words
        stdscr.addstr(0, 0, f"words: {correct}")
        stdscr.addstr(1, 0, str(x))
        stdscr.addstr(2, 0, str(y))
        stdscr.addstr(3, 0, str(width))
        stdscr.addstr(4, 0, str(charCounter))
        stdscr.move(y, x)

        # wait for user to press a  key
        key = stdscr.getkey()

        # check if the presses key is Backspace
        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if (charCounter == 0):
                continue

            if x == 0:
                y -= 1
                x = width - 1
            else:
                x -= 1
            charCounter -= 1

            stdscr.addstr(y, x, testText[charCounter], curses.color_pair(1))
            answer.pop()
            wordList[words].pop()

            if testText[charCounter] == " ":
                if wordList[words].count(False) == 0:
                    correct -= 1
                wordList.pop()
                words -= 1

        else:
            # if the key Esc is pressed end the test
            if (ord(key) == 27):
                break

            if ((key == " ") & (testText[charCounter] == " ")):
                if wordList[words].count(False) == 0:
                    correct += 1
                wordList.append([])
                words += 1
            
            charCounter += 1

            answer.append(key)

            for i in range(charCounter // (width + 1) * width, charCounter):
                if (answer[i] == testText[i]):
                    stdscr.addstr(y, i % width, testText[i], curses.color_pair(2))
                    wordList[words].append(True)
                else:
                    stdscr.addstr(y, i % width, testText[i], curses.color_pair(3))
                    wordList[words].append(False)
            if x == width - 1:
                y +=1
                x = 0
            else:
                x += 1

    end_screen(stdscr, width, height)

def end_screen(stdscr, width, height):
    endMessage = "Press Enter to restart / Press any other key to end"
    x = (width - len(endMessage)) // 2
    y = height // 2

    stdscr.addstr(y  + y // 2, x, endMessage)
    stdscr.refresh()
    key = stdscr.getkey()
    if key == "\n":
        test_screen(stdscr)

def main(stdscr):
    # get the size of the screen
    height, width = stdscr.getmaxyx()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    start_screen(stdscr, width, height)
    test_screen(stdscr, width, height)

curses.wrapper(main)