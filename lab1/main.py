import tkinter as tk
from tkinter import colorchooser
from tkinter import ttk

ONE_THIRD = 1.0/3.0
ONE_SIXTH = 1.0/6.0
TWO_THIRD = 2.0/3.0

def _v(m1, m2, hue):
    hue = hue % 1.0
    if hue < ONE_SIXTH:
        return m1 + (m2-m1)*hue*6.0
    if hue < 0.5:
        return m2
    if hue < TWO_THIRD:
        return m1 + (m2-m1)*(TWO_THIRD-hue)*6.0
    return m1


def rgb_to_hls(r, g, b):
    maxc = max(r, g, b)
    minc = min(r, g, b)
    sumc = (maxc+minc)
    rangec = (maxc-minc)
    l = sumc/2.0
    if minc == maxc:
        return 0.0, l, 0.0
    if l <= 0.5:
        s = rangec / sumc
    else:
        s = rangec / (2.0-maxc-minc)  # Not always 2.0-sumc: gh-106498.
    rc = (maxc-r) / rangec
    gc = (maxc-g) / rangec
    bc = (maxc-b) / rangec
    if r == maxc:
        h = bc-gc
    elif g == maxc:
        h = 2.0+rc-bc
    else:
        h = 4.0+gc-rc
    h = (h/6.0) % 1.0
    return h, l, s

def hls_to_rgb(h, l, s):
    if s == 0.0:
        return l, l, l
    if l <= 0.5:
        m2 = l * (1.0+s)
    else:
        m2 = l+s-(l*s)
    m1 = 2.0*l - m2
    return (_v(m1, m2, h+ONE_THIRD), _v(m1, m2, h), _v(m1, m2, h-ONE_THIRD))


def rgb_to_cmyk(r, g, b):
    if (r, g, b) == (0, 0, 0):
        return 0, 0, 0, 1
    c = 1 - r / 255
    m = 1 - g / 255
    y = 1 - b / 255
    k = min(c, m, y)
    c = (c - k) / (1 - k)
    m = (m - k) / (1 - k)
    y = (y - k) / (1 - k)
    return round(c * 100), round(m * 100), round(y * 100), round(k * 100)

def cmyk_to_rgb(c, m, y, k):
    r = 255 * (1 - c / 100) * (1 - k / 100)
    g = 255 * (1 - m / 100) * (1 - k / 100)
    b = 255 * (1 - y / 100) * (1 - k / 100)
    return round(r), round(g), round(b)

def update_color_from_rgb(event=None):
    try:
        r = int(r_entry.get())
        g = int(g_entry.get())
        b = int(b_entry.get())
    except ValueError:
        return

    update_views(r, g, b)

def update_color_from_cmyk(event=None):
    try:
        c = int(c_entry.get())
        m = int(m_entry.get())
        y = int(y_entry.get())
        k = int(k_entry.get())
    except ValueError:
        return

    r, g, b = cmyk_to_rgb(c, m, y, k)
    update_views(r, g, b)

def update_color_from_hls(event=None):
    try:
        h = int(h_entry.get())
        l = int(l_entry.get())
        s = int(s_entry.get())
    except ValueError:
        return

    r, g, b = [round(x * 255) for x in hls_to_rgb(h / 360, l / 100, s / 100)]
    update_views(r, g, b)

def update_views(r, g, b):
    c, m, y, k = rgb_to_cmyk(r, g, b)
    h, l, s = rgb_to_hls(r / 255, g / 255, b / 255)

    h_entry.delete(0, tk.END)
    h_entry.insert(0, round(h * 360))

    l_entry.delete(0, tk.END)
    l_entry.insert(0, round(l * 100))

    s_entry.delete(0, tk.END)
    s_entry.insert(0, round(s * 100))

    c_entry.delete(0, tk.END)
    c_entry.insert(0, c)

    m_entry.delete(0, tk.END)
    m_entry.insert(0, m)

    y_entry.delete(0, tk.END)
    y_entry.insert(0, y)

    k_entry.delete(0, tk.END)
    k_entry.insert(0, k)

    color_display.config(bg=f'#{r:02x}{g:02x}{b:02x}')
    r_slider.set(r)
    g_slider.set(g)
    b_slider.set(b)

def choose_color():
    color_code = colorchooser.askcolor(title="Choose color")[0]
    if color_code:
        r, g, b = map(int, color_code)
        update_views(r, g, b)

app = tk.Tk()
app.title("Лаба 1")

ttk.Label(app, text="RGB").grid(column=0, row=0, padx=5, pady=5, sticky='w')
r_entry = ttk.Entry(app, width=5)
r_entry.grid(column=1, row=0)
r_slider = tk.Scale(app, from_=0, to=255, orient='horizontal', command=lambda e: update_color_from_rgb())
r_slider.grid(column=2, row=0, sticky='ew')

g_entry = ttk.Entry(app, width=5)
g_entry.grid(column=1, row=1)
g_slider = tk.Scale(app, from_=0, to=255, orient='horizontal', command=lambda e: update_color_from_rgb())
g_slider.grid(column=2, row=1, sticky='ew')

b_entry = ttk.Entry(app, width=5)
b_entry.grid(column=1, row=2)
b_slider = tk.Scale(app, from_=0, to=255, orient='horizontal', command=lambda e: update_color_from_rgb())
b_slider.grid(column=2, row=2, sticky='ew')


ttk.Label(app, text="CMYK").grid(column=0, row=3, padx=5, pady=5, sticky='w')
c_entry = ttk.Entry(app, width=5)
c_entry.grid(column=1, row=3)

m_entry = ttk.Entry(app, width=5)
m_entry.grid(column=1, row=4)

y_entry = ttk.Entry(app, width=5)
y_entry.grid(column=1, row=5)

k_entry = ttk.Entry(app, width=5)
k_entry.grid(column=1, row=6)

ttk.Label(app, text="HLS").grid(column=0, row=7, padx=5, pady=5, sticky='w')
h_entry = ttk.Entry(app, width=5)
h_entry.grid(column=1, row=7)

l_entry = ttk.Entry(app, width=5)
l_entry.grid(column=1, row=8)

s_entry = ttk.Entry(app, width=5)
s_entry.grid(column=1, row=9)

color_display = tk.Label(app, text="", bg="white", width=20, height=2)
color_display.grid(column=3, row=0, rowspan=10, padx=10, pady=5)

ttk.Button(app, text="Choose Color", command=choose_color).grid(column=0, row=10, columnspan=2, pady=10)

r_entry.bind("<Return>", update_color_from_rgb)
g_entry.bind("<Return>", update_color_from_rgb)
b_entry.bind("<Return>", update_color_from_rgb)

c_entry.bind("<Return>", update_color_from_cmyk)
m_entry.bind("<Return>", update_color_from_cmyk)
y_entry.bind("<Return>", update_color_from_cmyk)
k_entry.bind("<Return>", update_color_from_cmyk)

h_entry.bind("<Return>", update_color_from_hls)
l_entry.bind("<Return>", update_color_from_hls)
s_entry.bind("<Return>", update_color_from_hls)

app.mainloop()
