import curses, random, time
from curses import wrapper

high_scores = [0]
play_continue = True

def delay(row, col, string, color_pair, scr):
    for char in string:
        scr.addstr(row, col, char, curses.color_pair(color_pair))
        col += 1
        scr.refresh()
        time.sleep(0.05)
    time.sleep(0.5)

def load(row, col, string, color_pair, scr):
    for char in string:
        scr.addstr(row, col, char, curses.color_pair(color_pair))
        col += 1
        scr.refresh()
        time.sleep(0.5)


def generating_screen(scr):
    global text
    scr.clear()
    delay(2, 2, "Generating Text", 1, scr)
    load(2, 19, ". . . . .", 1, scr)
    scr.clear(); scr.refresh()
    para1 = """A two-inch layer of freshly fallen snow covered the yard. Stacey peeked outside."""
    para2 = """Brenda never wanted to be famous. While most of her friends dreamed about being . """
    para3 = """Puppies are soft, cute, funny, and make a big mess. Every month or two our family ."""
    text_list = [para1,para2,para3]
    text = random.choice(text_list)

wpm_screen = True

def start_screen(scr):
    global wpm_screen, play_continue
    scr.clear(); time.sleep(1.5)
    delay(2, 15, "Welcome to Typing Test!", 4, scr)
    delay(4, 14, "Press any key to continue", 1, scr)
    scr.addstr(6, 19, "\"esc\" to exit")
    scr.addstr(8, 19, f"Highscore : {max(high_scores)}")

    scr.nodelay(False)
    key = scr.getkey()
    try:
        if ord(key) == 27: 
            wpm_screen = False
            play_continue = False
    except: pass
    scr.refresh()


def display_text(scr, current_text, target_text, wpm=0):
    scr.addstr(1, 3, target_text)
    scr.addstr(11, 3, f"WPM : {wpm}")
    col = 3
    for char in current_text:
        if char != target_text[col-3]: color = curses.color_pair(3)
        else: color = curses.color_pair(2)
        scr.addstr(1, col, char, color)
        col += 1


def words_per_min_test(scr):
    global wpm, text
    scr.clear()
    time.sleep(1.5)
    target = text
    current = []
    start_time = time.time()
    scr.nodelay(True)
    wpm = 0

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current)/(time_elapsed / 60))/5)

        scr.clear()
        display_text(scr, current, target, wpm)
        scr.addstr(15, 3, "Please type the above text")
        scr.addstr(17, 3, "\"esc\" to exit")
        scr.refresh()

        try: key = scr.getkey()
        except: continue

        if "".join(current) == target:
            scr.nodelay(False)
            high_scores.append(wpm)
            break
        try:
            if ord(key) == 27: break
        except: pass
        
        if key in ("\b", "KEY_BACKSPACE", "\x7f"):
            if len(current) > 0: current.pop()
        elif len(current) < len(target): current.append(key)
        

def main(scr):
    global wpm_screen, play_continue, wpm
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    while True:
        start_screen(scr)
        if wpm_screen:
            generating_screen(scr)
            words_per_min_test(scr)
            if max(high_scores) == wpm and wpm > 0:
                delay(20, 3, "Congratulations! It's a Highscore!", 1, scr)
                delay(22, 3, "Press any key to play again!", 1, scr)
            else:
                delay(20, 3, "Press any key to play again!", 1, scr)
            scr.nodelay(False)
            key = scr.getkey()
            try:
                if ord(key) == 27:
                    break
            except: pass
        if not play_continue:
            break
                
    
wrapper(main)
