import curses
import time
import random

def prepare_text(stdscr, string: str, numberOfWords: int):
    """
    Function to prepare text for testing

    string -- string containing raw text\n
    numberOfWords -- number of words in returning string\n
    return -- prepared string
    """
    stringSplit = string.split("\n")
    firstWord = random.randrange(0, len(stringSplit) - numberOfWords)
    stringTrimmed = stringSplit[firstWord:firstWord + numberOfWords]
    stringJoined = " ".join(stringTrimmed)

    return stringJoined

def start_screen(stdscr, width, height):
    """
    Function handling start screen.

    width -- width of the screen\n
    height -- height of the screen
    """
    startMessage = "Press any button to start"
    # calculating values to place a string
    x = (width - len(startMessage)) // 2
    y = height // 2

    stdscr.clear()
    stdscr.addstr(y, x, startMessage)
    stdscr.refresh()
    stdscr.getkey()

def test_screen(stdscr, width, height):
    """
    Function handling the testing.

    width -- width of the screen\n
    height -- height of the screen
    """
    # try to open file and load text from file
    try:
        file = open("test-texts.txt", "r")
        # number of words in the test
        numberOfWords = 100
        loadedText = file.read()
        testText = prepare_text(stdscr, loadedText, numberOfWords)
    except:
        testText = "hello world"
    # list where the answer will be stored
    answer = []

    # positions of the text
    x = 0
    y = (height - (len(testText) // width)) // 2

    stdscr.clear()
    stdscr.addstr(y, x, testText)
    stdscr.move(y, x)
    stdscr.refresh()

    wordIndex = 0
    correct = 0
    wordList = [[]]
    charCounter = 0
    startTime = time.time()
    elapsedTime = 0
    stdscr.nodelay(True)

    while True:
        if (elapsedTime == 30):
            break

        elapsedTime = round(time.time() - startTime)
        stdscr.addstr(0, 0, f"{30 - elapsedTime}")
        wpm = (correct * 60) // max(elapsedTime, 1)
        # show number of words
        stdscr.addstr(1, 0, f"WPM: {wpm}")
        stdscr.move(y, x)

        try:
            key = stdscr.getkey()
        except:
            continue

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

            if testText[charCounter] == " ":
                wordIndex -= 1
                if wordList[wordIndex].count(False) == 0:
                    correct -= 1
                wordList.pop()
            else:
                wordList[wordIndex].pop()

        else:
            # if the key Esc is pressed end the test
            if (ord(key) == 27):
                break

            if testText[charCounter] == " ":
                if wordList[wordIndex].count(False) == 0:
                    correct += 1
                wordList.append([])
                wordIndex += 1

            answer.append(key)

            if answer[charCounter] == testText[charCounter]:
                wordList[wordIndex].append(True)

            else:
                wordList[wordIndex].append(False)

            charCounter += 1

            for i in range(charCounter // (width + 1) * width, charCounter):
                if (answer[i] == testText[i]):
                    stdscr.addstr(y, i % width, testText[i], curses.color_pair(2))
                
                else:
                    stdscr.addstr(y, i % width, testText[i], curses.color_pair(3))
                    
            if x == width - 1:
                y +=1
                x = 0
            else:
                x += 1

    end_screen(stdscr, width, height)

def end_screen(stdscr, width, height):
    stdscr.nodelay(False)
    endMessage = "Press Enter to restart / Press any other key to end"
    x = (width - len(endMessage)) // 2
    y = height // 2

    stdscr.addstr(y  + y // 2, x, endMessage)
    stdscr.refresh()
    time.sleep(2)
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