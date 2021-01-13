import tkinter as tk
import requests
from bs4 import BeautifulSoup

'''
BACKEND
'''

stats = ['RankedKDRatio', 'RankedWLRatio', 'PVPAccuracy', 'RankedKillsPerMatch', 'RankedKillsPerMinute', 'MMR']


def findStats(soup, stat):
    validChar = ['.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    if stat == 'MMR':
        stat1 = soup.find(text='MMR')
        stat = stat1.findNext('div').getText()
    else:
        stat = soup.find('div', {'data-stat': stat}).getText()
    trimmedStat = ''.join(ch for ch in stat.strip() if ch in validChar)
    return trimmedStat


def drawBars(player1val, player2val, yAlign):
    total = player1val + player2val
    player1length = 200 * (player1val / total)
    player2length = 200 * (player2val / total)
    canvas.create_rectangle(100, 250 + yAlign, 300 - player2length, 270 + yAlign, fill='gray25')
    p1 = tk.Label(window, text=player1val)
    p1.config(font=('verdana', 6, 'bold'), fg='black')
    canvas.create_window(150, 260 + yAlign, window=p1)

    canvas.create_rectangle(100 + player1length, 250 + yAlign, 300, 270 + yAlign, fill='orange')
    p2 = tk.Label(window, text=player2val)
    p2.config(font=('verdana', 6, 'bold'),  fg='black')
    canvas.create_window(250, 260 + yAlign, window=p2)


def calculate():
    global player1Input
    global player2Input
    p1Page = requests.get('https://r6.tracker.network/profile/' + p1Variable.get().lower() + '/' +
                                      player1Input.get())
    p1Soup = BeautifulSoup(p1Page.content, 'html.parser')
    p2Page = requests.get('https://r6.tracker.network/profile/' + p2Variable.get().lower() + '/' +
                                      player2Input.get())
    p2Soup = BeautifulSoup(p2Page.content, 'html.parser')
    p1Stats = {}
    p2Stats = {}
    yAlign = 0
    try:
        for stat in stats:
            p1Stats[stat] = findStats(p1Soup, stat)
            p2Stats[stat] = findStats(p2Soup, stat)
            drawBars(float(p1Stats[stat]), float(p2Stats[stat]), yAlign)
            yAlign += 50
    except AttributeError:
        invalid.place(x=153, y=170)
        return 0


def hideInvalid():
    invalid.place_forget()


'''
GUI
'''

window = tk.Tk()
window.title('R6HeadToHead by Daniel.T')
window.resizable(False, False)

canvas = tk.Canvas(window, width=400, height=600, bg='gray15')
canvas.pack()

invalid = tk.Label(window, text='Invalid username!')
invalid.config(font=('verdana', 6, 'bold'), fg='black')

header = tk.Label(window, text='R6HeadToHead')  # window label
header.config(font=('verdana', 30, 'bold'), bg='gray15', fg='white')
canvas.create_window(200, 40, window=header)

vs = tk.Label(window, text='VS')
vs.config(font=('verdana', 20, 'bold'), bg='gray15', fg='white')
canvas.create_window(200, 150, window=vs)

# TODO - STATS TRACKED BELOW - more efficient?

p1KD = tk.Label(window, text='KD')  # KD
p1KD.config(font=('verdana', 13, 'bold'), bg='gray15', fg='orange')
canvas.create_window(50, 260, window=p1KD)
p2KD = tk.Label(window, text='KD')
p2KD.config(font=('verdana', 13, 'bold'), bg='gray15', fg='orange')
canvas.create_window(350, 260, window=p2KD)

p1win = tk.Label(window, text='WIN %')  # Win percentage
p1win.config(font=('verdana', 13, 'bold'), bg='gray15', fg='orange')
canvas.create_window(50, 310, window=p1win)
p2win = tk.Label(window, text='WIN %')
p2win.config(font=('verdana', 13, 'bold'), bg='gray15', fg='orange')
canvas.create_window(350, 310, window=p2win)

p1HS = tk.Label(window, text='HS %')  # HS
p1HS.config(font=('verdana', 13, 'bold'), bg='gray15', fg='orange')
canvas.create_window(50, 360, window=p1HS)
p2HS = tk.Label(window, text='HS %')
p2HS.config(font=('verdana', 13, 'bold'), bg='gray15', fg='orange')
canvas.create_window(350, 360, window=p2HS)

p1killMatch = tk.Label(window, text='KILL/Ma')  # k/Ma
p1killMatch.config(font=('verdana', 13, 'bold'), bg='gray15', fg='orange')
canvas.create_window(50, 410, window=p1killMatch)
p2killMatch = tk.Label(window, text='KILL/Ma')
p2killMatch.config(font=('verdana', 13, 'bold'), bg='gray15', fg='orange')
canvas.create_window(350, 410, window=p2killMatch)


p1killMin = tk.Label(window, text='KILL/Mi')  # K/Min
p1killMin.config(font=('verdana', 13, 'bold'), bg='gray15', fg='orange')
canvas.create_window(50, 460, window=p1killMin)
p2killMin = tk.Label(window, text='KILL/Mi')
p2killMin.config(font=('verdana', 13, 'bold'), bg='gray15', fg='orange')
canvas.create_window(350, 460, window=p2killMin)

p1MMR = tk.Label(window, text='MMR')  # MMR
p1MMR.config(font=('verdana', 13, 'bold'), bg='gray15', fg='orange')
canvas.create_window(50, 510, window=p1MMR)
p2MMR = tk.Label(window, text='MMR')
p2MMR.config(font=('verdana', 13, 'bold'), bg='gray15', fg='orange')
canvas.create_window(350, 510, window=p2MMR)

canvas.create_line(100, 230, 100, 560, fill="black")
canvas.create_line(300, 230, 300, 560, fill="black")
canvas.create_line(200, 230, 200, 560, fill='white')


convert = [  # option lists
    'PC',
    'PS4',
    'XBOX'
    ]

p1Variable = tk.StringVar(window)
p1Variable.set(convert[0])

p2Variable = tk.StringVar(window)
p2Variable.set(convert[0])

p1Platform = tk.OptionMenu(window, p1Variable, *convert)
p1Platform.config(width=10, font=('Helvetica', 10, 'bold'), bg='gray15', fg='orange')
p1Platform.place(x=33, y=80)

p2Platform = tk.OptionMenu(window, p2Variable, *convert)
p2Platform.config(width=10, font=('Helvetica', 10, 'bold'), bg='gray15', fg='orange')
p2Platform.place(x=253, y=80)


player1Input = tk.Entry(window)  # user input
player1Input.place(x=30, y=140)
player2Input = tk.Entry(window)
player2Input.place(x=250, y=140)

defaultString = 'Enter username'
player1Input.insert(0, 'Keetgg')  # TODO - change both back to dS after testing
player2Input.insert(0, 'Mushymush9')

button = tk.Button(window, font=('verdana', 10, 'bold'), text="Enter", bg='gray15', fg='white',
                   command=lambda: [hideInvalid(), calculate()])
button.place(x=170, y=200)


'''
MAINLOOP
'''
while True:
    window.mainloop()
