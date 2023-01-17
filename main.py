import PySimpleGUI as sg
import random
import re

# Simple script to read flash cards file and display contents
# Read in file contents

# read in yaml file
with open('terms.txt') as f:
    lines = f.readlines()

# load chapters for combo box
def load_chapters():
    pattern = r'[^,\.:A-Za-z0-9]+'
    chapters = []
    for line in lines:
        if '#' in line:
            line = line.replace('#','')
            line = re.sub(pattern, ' ', line)
            line = line.strip()
            chapters.append(line)
    return chapters

# read all the cards in the chapter
def load_cards(chapter):
    cards = {}
    in_chapter = False
    for line in lines:
        pattern = r'[^,\.:A-Za-z0-9]+'
        line = line.replace('#','')
        line = re.sub(pattern, ' ', line)
        line = line.strip()
        if in_chapter:
            if '#' in line:   # detect end of chapter words
                break
            else:
                items = line.strip().split(':')   # add words to dictionary
                if (len(items) == 2):
                    cards[items[0]] = items[1]
        elif chapter in line:
            in_chapter = True
            continue
    return cards

# select card
def choose_card(cards, rnd, ndx):

    count = len(cards)
    if ndx > count - 1:
        ndx = 0
    elif ndx < 0:
        ndx = count - 1
    if rnd:
        ndx = random.randint(0, count - 1)
    ks = list(cards.keys())
    crd = tuple((ks[ndx], cards[ks[ndx]], ndx))
    return crd

# ui layout
sg.theme('Dark Green 7')

layout = [
        # section 1
        [sg.Combo(load_chapters(), font=('Arial', 16), enable_events = True,
                  default_value='Select Chapter', size=(48, 1), key='-CHAPTER-')],
        # section 2
          [sg.Multiline(size=(35, 10), justification= 'center', border_width=0, background_color= "#0C231E",
            font=('Courier', 48), no_scrollbar = True, key='-text-') ],
        # section 3
        [sg.Checkbox('Random', font=('Arial', 16), default=True, enable_events=True, key="-RND-"),
         sg.Button('Prev', font=('Arial', 16), enable_events=True, key='-PREV-'),
         sg.Button('Show/Hide', font=('Arial', 16), enable_events=True, key='-SHOW-'),
         sg.Button('Next', font=('Arial', 16),enable_events=True, key='-NEXT-')]]


window = sg.Window('Python Flashcards', layout,size=(1000,800), grab_anywhere=False)

def update_display(txt):
    txt_len = len(txt)
    lines = 5
    if txt_len > 26:
        lines = int((10 - txt_len / 26) / 2)
    display_text = ""
    for i in range(lines):
        display_text=display_text + '\n'
    display_text = display_text + txt
    window['-text-'].update(display_text)

# initialize
chapters = load_chapters()
cards = load_cards(chapters[0])
card = choose_card(cards, False, 0)
show_def = False

# event loop
while True:

    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    elif event == '-CHAPTER-':
        cards = load_cards(values['-CHAPTER-'])
        card = choose_card(cards, False, 0)
        update_display(card[0])
    elif event == '-NEXT-':
        card = choose_card(cards, values['-RND-'], card[2] + 1)
        update_display(card[0])
        show_def = False
    elif event == '-PREV-':
        card = choose_card(cards, values['-RND-'], card[2] - 1)
        update_display(card[0])
        show_def = False
    elif event == '-SHOW-':
        show_def = not show_def
        if show_def:
            update_display(card[1])
        else:
            update_display(card[0])


window.close()
