import curses, sys, signal

class Window():

    window = False
    colors = dict()

    # Initialize the Curses window
    def __init__(self, title):
        # Initialize the cursor mode
        self.window = curses.initscr()
        # Enable colors
        curses.start_color()
        curses.use_default_colors()
        # Disable keyboard input echo
        curses.noecho()
        # Do not require Enter to be pressed to get data
        curses.cbreak()
        # Let Curses handle special keys
        # self.window.keypad(1)
        # Set signal for terminal resize
        signal.signal(signal.SIGWINCH, self.resizeSignal)
        # Set signal for exit
        signal.signal(signal.SIGINT, self.quitSignal)
        # Define basic colors
        self.defineColor("Default", 0, -1)
        self.defineColor("Title", 231, 0)
        self.defineColor("Info", 231, 12)
        self.defineColor("Error", 231, 1)
        self.defineColor("Warning", 231, 3)
        self.defineColor("Success", 231, 2)
        self.defineColor("Input", 0, 11)
        # Draw title
        self.drawTitle(title)

    # Close the curses window
    def close(self):
        # End Curses
        curses.nocbreak()
        self.window.keypad(0)
        curses.echo()
        curses.endwin()

    # Resize signal
    def resizeSignal(self, signal, frame):
        # Refresh window
        self.window.refresh()

    # Quit signal
    def quitSignal(self, signal, frame):
        # Close window
        self.close()
        # Exit program
        sys.exit(0)

    # Define colors
    def defineColor(self, name, text, back):
        # Define the color
        curses.init_pair(len(self.colors), text, back)
        # Save the color
        self.colors[name] = len(self.colors)

    # Draw the title
    def drawTitle(self, title):
        # Draw the title
        self.printLine(0, "", "Title")
        self.printLine(1, title.upper(), "Title", "center")
        self.printLine(2, "", "Title")

    # Print a box of text
    def printBox(self, x, y, width, string, color = "Default", aligned = "left"):
        # Enlarge the string
        if (aligned == "left"):
            text = string + (" " * (width - len(string)))
        elif (aligned == "center"):
            spaceBefore = (width - len(string)) / 2
            spaceAfter = spaceBefore + (width - len(string)) % 2
            text = (" " * spaceBefore) + string + (" " * spaceAfter)
        elif (aligned == "right"):
            text = (" " * (width - len(string))) + string
        # Print the string
        self.printString(x, y, text, color)

    # Print error
    def printError(self, string):
        # Get the screen size
        height, width = self.window.getmaxyx()
        # Print the string
        self.printString(0, height - 1, string, "Error")

    # Print a full line on the screen (auto-fill)
    def printLine(self, y, string, color = "Default", aligned = "left"):
        # Get the screen size
        height, width = self.window.getmaxyx()
        # Enlarge the string
        if (aligned == "left"):
            text = string + (" " * (width - len(string)))
        elif (aligned == "center"):
            spaceBefore = (width - len(string)) / 2
            spaceAfter = spaceBefore + (width - len(string)) % 2
            text = (" " * spaceBefore) + string + (" " * spaceAfter)
        elif (aligned == "right"):
            text = (" " * (width - len(string))) + string
        # Print the string
        self.printString(0, y, text, color)

    # Print a string on the screen
    def printString(self, x, y, string, color = "Default"):
        # Print the string
        self.window.addstr(y, x, string, curses.color_pair(self.colors[color]))
        # Refresh window
        self.window.refresh()

    # Get a singel character
    def getChr(self):
        return self.window.getch()

    # Get a string
    def getString(self, length = 50):
        return self.window.getstr(y, x, length)

    # Get a character
    def getChar(self, x, y):
        # Enable echo mode
        curses.echo()
        # Get string
        while(True):
            # Mask previous text
            self.printBox(x, y, 1, " ", "Default")
            # Get text
            string = self.window.getstr(y, x, 1)
            if (string.isalnum() or len(string) == 0):
                break
        # Disable echo mode
        curses.noecho()
        # Return string
        if (len(string) == 0):
            return False
        else:
            return string

    # Get a string
    def getString(self, x, y, length = 50):
        # Enable echo mode
        curses.echo()
        # Get string
        while(True):
            # Mask previous text
            self.printBox(x, y, length, " ", "Default")
            # Get text
            string = self.window.getstr(y, x, length)
            if (string.isalnum() or len(string) == 0):
                break
        # Disable echo mode
        curses.noecho()
        # Return string
        if (len(string) == 0):
            return False
        else:
            return string

    # Get an integer
    def getInt(self, x, y, length = 50):
        # Enable echo mode
        curses.echo()
        # Get string
        while(True):
            # Mask previous text
            self.printBox(x, y, length, " ", "Default")
            # Get text
            string = self.window.getstr(y, x, length)
            if (string.isdigit() or len(string) == 0):
                break
        # Disable echo mode
        curses.noecho()
        # Return string
        if (len(string) == 0):
            return -1
        else:
            return int(string)

    # Wait for a specific key signal
    def waitForKey(self, key):
        # Wait for key
        while (True):
            if (self.getChr() == ord(key)):
                return True

    # Wait for quit signal
    def waitQuit(self):
        # Get the screen size
        height, width = self.window.getmaxyx()
        # Print the string
        self.printBox(0, height - 1, width - 1, "Press [q] to quit the program.", "Warning", "center")
        # Wait for key
        while (True):
            if (self.getChr() == ord('q')):
                return True

    # Draw a color map
    def drawColor(self):
        height, width = self.window.getmaxyx()
        for i in range(0, curses.COLORS):
            if (i != 0 and i % 60 == 0):
                self.getChr()
            self.defineColor(str(i), -1, i)
            self.printLine(i % 60, str(i), str(i))
