import tkinter as tk
from tkinter import ttk, messagebox, colorchooser, filedialog
import threading, time, json, os, sys, random, platform
from collections import deque
import pyautogui
from pynput.keyboard import Key, KeyCode, Listener as KbListener
from pynput.mouse    import Button, Controller as MouseController, Listener as MouseListener
from datetime        import datetime
pyautogui.PAUSE    = 0
pyautogui.FAILSAFE = True
if platform.system() == "Windows":
    try:
        import ctypes
        ctypes.windll.winmm.timeBeginPeriod(1)
    except Exception:
        pass
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "Theenar.AutoClicker")
    except Exception:
        pass
if getattr(sys, "frozen", False):
    _PREF = os.path.dirname(sys.executable)
    if not os.access(_PREF, os.W_OK):
        _PREF = os.path.join(
            os.environ.get("APPDATA", os.path.expanduser("~")), "Theenar")
        os.makedirs(_PREF, exist_ok=True)
else:
    try:
        _PREF = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        _PREF = os.getcwd()
PROFILES_FILE = os.path.join(_PREF, "theenar_profiles.json")
SETTINGS_FILE = os.path.join(_PREF, "theenar_settings.json")
ICON_FILE = ""
BUNDLED_PROFILES = {
    "Default": {
        "speed_mode": "ms", "cps": 10.0, "ms": 100,
        "button": "Left", "click_type": "Single", "hold_ms": 100,
        "repeat_mode": "Infinite", "repeat_count": 100,
        "pos_mode": "Current", "fixed_x": 960, "fixed_y": 540,
        "hotkey": "-",
        "path_enabled": False, "path_mode": "Once", "waypoints": [],
        "once_stop_mode": "Autoclicker",
        "trigger_type": "Off",
        "trigger_px_x": 960, "trigger_px_y": 540,
        "trigger_color": [255, 255, 255],
        "trigger_tolerance": 15, "trigger_condition": "Matches",
        "hotkey_arms_trigger": True,
    },
}
THEMES_FILE = os.path.join(_PREF, "theenar_themes.json")
DOCS_FILE = os.path.join(_PREF, "theenar_docs.json")
THEME_KEYS = [
    "BG", "PANEL", "BORDER", "INPUT", "INPUT_B", "FG", "FG2",
    "ACCENT", "GREEN", "RED", "YELLOW",
    "CONSOLE", "CONSOLE_FG", "CYAN", "ORANGE", "TITLEBAR",
]
AETHS_SWATCHES = [
    ("BG",         "Background"),
    ("TITLEBAR",   "Title bar"),
    ("PANEL",      "Panels"),
    ("BORDER",     "Borders"),
    ("INPUT",      "Input fields"),
    ("INPUT_B",    "Buttons (subtle)"),
    ("FG",         "Text"),
    ("FG2",        "Text (muted)"),
    ("ACCENT",     "Accent"),
    ("GREEN",      "Start / On"),
    ("RED",        "Stop / Danger"),
    ("YELLOW",     "Capture"),
    ("CONSOLE",    "Console panel"),
    ("CONSOLE_FG", "Console text"),
    ("CYAN",       "Log \u00b7 mouse"),
    ("ORANGE",     "Log \u00b7 hold"),
]
BUNDLED_THEMES = {
    "Default": {
        "BG": "#1e1f22", "PANEL": "#2b2d31", "BORDER": "#3b3d42",
        "INPUT": "#383a3f", "INPUT_B": "#474a50",
        "FG": "#e3e5e8", "FG2": "#8e9297", "ACCENT": "#5865F2",
        "GREEN": "#23a559", "RED": "#da3633", "YELLOW": "#f0b132",
        "CONSOLE": "#111214", "CONSOLE_FG": "#e3e5e8",
        "CYAN": "#4fc3f7", "ORANGE": "#e37320",
        "TITLEBAR": "#2b2d31",
    },
    "Cherry": {
        "BG": "#fff5fa", "PANEL": "#ffe9f3", "BORDER": "#f4c4da",
        "INPUT": "#fff1f7", "INPUT_B": "#ffd6e7",
        "FG": "#6d2b4e", "FG2": "#b06f91", "ACCENT": "#ec5f9e",
        "GREEN": "#4cc1a0", "RED": "#ef5a73", "YELLOW": "#ffce73",
        "CONSOLE": "#2a1421", "CONSOLE_FG": "#ffe9f3",
        "CYAN": "#5bb6d6", "ORANGE": "#f08a6a",
        "TITLEBAR": "#ffe9f3",
    },
    "Theen": {
        "BG": "#f3f9ff", "PANEL": "#e3f1fd", "BORDER": "#bfdcf2",
        "INPUT": "#eef6ff", "INPUT_B": "#cce6fa",
        "FG": "#1e4060", "FG2": "#5e84a6", "ACCENT": "#2f93e0",
        "GREEN": "#4ac6a4", "RED": "#ee5d6e", "YELLOW": "#ffd166",
        "CONSOLE": "#11253a", "CONSOLE_FG": "#e3f1fd",
        "CYAN": "#56c5ee", "ORANGE": "#f3955f",
        "TITLEBAR": "#e3f1fd",
    },
}
def _clamp(v):
    return max(0, min(255, int(round(v))))
def _hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
def _rgb_to_hex(r, g, b):
    return "#%02x%02x%02x" % (_clamp(r), _clamp(g), _clamp(b))
INFO_TEXT = """\
--- Created by 0Thirteen1 (Theen) ---
Peenar autoclicker weheheheh

AUTOCLICKER SAFEGUARD
Touch the TOP LEFT of your screen to instantly stop the autoclicker









-SECTION: GENERAL-
Unspecific info without a designated section


0Thirteen1
        Me, creator, gay furry idk please be my friend I'm so lonely and NOT clingy please bro
        I mean I really only plan on giving this to one person, so there's not really a huge point for an info tab?
        I pretty much made this specifically for Those Who Remain but like... It's applicable for a lot of things

        FYI the -Paths- tab does not work for roblox, neither does a set position. It has to be "Current"
        This is because Roblox OBVOIUSLY has antiscript shit and I literally CANNOT find a workaround and the one time I tried I failed miserably so don't yap my ear off about it


Idle/Online
        This addition looks like a red/green dot depending on whether your autoclicker is currently online, or inactive (idle).
        It's both, in the -Clicker- tab, and at the top right, visible no matter which tab you're currently viewing.
        The whole purpose of it is just to show you if the autoclicker is on or not, makes life real easy


  Tabs  
        Similar to any browser or search engine, except you can't close or open them.
        These tabs keep the autoclicker organized into specific regions.
        (Clicker, Paths, Terminal, Info, Aeths)


        

==================




-SECTION: CLICKER-


  Profiles  
        Profiles are presets you can set within the autoclicker to save your current settings.

HOW TO SET A PROFILE
            1. To save a profile, click "New", type in the desired name, then click "Create".
            2. Now set the autoclicker to your desired settings, and click "Save".
            3. Once you have completed this, your profile should be saved and accessible through the drop-down "Profile" tab.


  Speed & Click  
        CPS - Clicks Per Second
        MS - Milliseconds.
        You are able to edit the speed of the autoclicker on the right of this toggle.

        Click (Left, Right, Middle) determines which mouse button is being pressed.
        Type (Single, Double) determines whether it's a single mouse click, or a double mouse click.

        Hold (x MS) determines how long, in milliseconds, the mouse press duration will last.


  Pin  
        This is located at the top right of the Clicker tab, below Profile.
        When active, the autoclicker will remain pinned at the top of every window.
        Allows easy visible access at any time.


  Repeat & Position  
        Repeat - how many times the autoclicker clicks before it stops.
                Infinite - it never stops on its own, you stop it yourself.
                Count - it stops automatically after an specific number of clicks.

        Position - where on the screen you're clicking.
                Current - wherever your cursor already is (this is the one to use for Roblox).
                Fixed - locks every click to a specific spot on the screen.
                Cap (Capture) - gives you a 3 second countdown, then automatically sets that spot as Fixed


  Hotkey  
        A single key that flips the autoclicker on and off without touching the buttons.
        Type a key into the box and hit "Apply". Leave the box empty if you don't want a hotkey at all. You still have to apply it.
        Works even when the autoclicker isn't the window you're clicked into or pinned, so you can toggle in the middle of a game.

        Delay - waits x many seconds after you hit start before the clicking actually kicks in.


  Start / Stop  
        The big green and red buttons.
        Do I HAVE to explain this to you?
        


  Trigger  
        Makes the autoclicker only fire when a chosen pixel on your screen is a certain color.
        Great for clicking only when something is there or not there

        Watch (X, Y) - the exact pixel it senses. 
        Use Cap to grab one with a countdown.

        Color - the color it's hunting for. Use Sample to steal the current color of that pixel.
        Tol - tolerance, basically how close the color has to be to count as a match. Higher = looser/more forgiving.
        Start condition - fire when the pixel matches the color, or when it doesn't match.
        Arm Trigger - starts the watching. While armed it clicks when the condition is true and stops when it isn't.
        HK toggle - decides if your hotkey arms the trigger, or just starts the clicker.


        

==================




-SECTION: PATHS-
Makes the autoclicker click a list of spots in order instead of just one.
(Reminder: this does NOT work in Roblox. Use Current position there.)


  Path Mode  
        The toggle that turns Paths on or off. Off means normal single-spot clicking.


  Modes  
        Loop - 1 > 2 > 3 > 1 > 2 > 3... in order, forever.
        Bounce - 1 > 2 > 3 > 2 > 1... back and forth.
        Random - picks a random waypoint every single click.
        Once - runs the whole list one time, then stops.

        FYI: Once is a REALLY good matchup with Trigger. 


  On finish stop  
        Only visible/usablw in "Once" mode. Decides what actually stops when the path finishes:
                AC - stops the autoclicker.
                Trigger - disarms the trigger but keeps clicking.
                Both - stops the whole thing.


  Waypoints  
        Each waypoint is one spot (X, Y) with an optional delay (in ms) before the next click.
        Add Waypoint - adds a new wavepoint.
        Capture (3s) - 3 second countdown, then it grabs the coordinates of your mouse.

        The arrows reorder them, the X deletes one, and Clear All clears the whole list.


        

==================




-SECTION: TERMINAL-
A live log of everything being printed


  The Terminal  
        CLICK is a click the autoclicker made itself.
        MOUSE is a real click you made with your own hand.
        KEY is a key you pressed.
        "h:" is how long the press was held, and the little triangle is the time detected since the last event similar to it.
        It keeps the last 500 lines and auto-scrolls. "Clear" wipes it clean.


  CPS  
        The clicks-per-second readout down in the bottom-left, measured live.
        Works for the autoclicker OR for flexing how fast you can click by hand.
        It only reads numbers, so it never slows the actual clicking down.


        

==================




-SECTION: INFO-
What is this place?
Where am I?
dragon yiff




==================




-SECTION: AETHS-
This is the tab for color customization. 
I've already put two, just a cherry cloud and a normal sky-blue cloud color scheme.


        Changes happen live in the app, having fun screwing around with it
        You should totally send me cool customizations if anyone sees this


"""
def fmt_dt(delta_sec):
    if delta_sec is None:
        return ""
    ms = delta_sec * 1000
    return f"\u0394{ms:.0f}ms" if ms < 1000 else f"\u0394{delta_sec:.1f}s"
class AutoClicker:
    def __init__(self):
        self.clicking     = False
        self.click_thread = None
        self.total_clicks = 0
        self.total_physical = 0
        self.speed_mode = tk.StringVar(value="CPS")
        self.cps_val    = tk.DoubleVar(value=10.0)
        self.ms_val     = tk.IntVar(value=100)
        self.click_button = tk.StringVar(value="Left")
        self.click_type   = tk.StringVar(value="Single")
        self.hold_ms      = tk.IntVar(value=0)
        self.repeat_mode  = tk.StringVar(value="Infinite")
        self.repeat_count = tk.IntVar(value=100)
        self.pos_mode = tk.StringVar(value="Current")
        self.fixed_x  = tk.IntVar(value=960)
        self.fixed_y  = tk.IntVar(value=540)
        self.toggle_key_str = tk.StringVar(value="F6")
        self._toggle_key    = Key.f6
        self._kb_listener   = None
        self.path_enabled   = tk.BooleanVar(value=False)
        self.path_mode      = tk.StringVar(value="Loop")
        self.path_waypoints = []
        self._path_idx      = 0
        self._path_dir      = 1
        self._once_path_consumed = False
        self.once_stop_mode = tk.StringVar(value="Autoclicker")
        self.on_click_log     = None
        self.on_key_log       = None
        self.on_mouse_log     = None
        self.on_status_change = None
        self.on_once_done     = None
        self.on_engine_note   = None
        self._last_click_time   = None
        self._last_any_click    = None
        self._last_key_time     = None
        self._key_press_times   = {}
        self._mouse_press_times = {}
        self._synthetic_until   = 0.0
        self._mouse_listener    = None
        self._mouse_ctrl        = MouseController()
        self._last_log_emit     = 0.0
        self._click_times       = deque(maxlen=2048)
    def get_interval(self):
        if self.speed_mode.get() == "CPS":
            return 1.0 / max(self.cps_val.get(), 0.01)
        return max(self.ms_val.get(), 1) / 1000.0
    def _get_path_pos(self):
        if not self.path_waypoints:
            return None, None, None
        wp = self.path_waypoints[self._path_idx % len(self.path_waypoints)]
        return wp["x"], wp["y"], (wp["delay"] if wp["delay"] > 0 else None)
    def _advance_path(self):
        n = len(self.path_waypoints)
        if n == 0:
            return False
        mode = self.path_mode.get()
        if mode == "Loop":
            self._path_idx = (self._path_idx + 1) % n
        elif mode == "Bounce":
            self._path_idx += self._path_dir
            if self._path_idx >= n:
                self._path_dir = -1
                self._path_idx = max(0, n - 2)
            elif self._path_idx < 0:
                self._path_dir = 1
                self._path_idx = min(n - 1, 1)
        elif mode == "Random":
            self._path_idx = random.randrange(n)
        elif mode == "Once":
            self._path_idx += 1
            if self._path_idx >= n:
                return True
        return False
    def _wait_until(self, deadline):
        SPIN = 0.0015
        while self.clicking:
            remaining = deadline - time.perf_counter()
            if remaining <= 0:
                return
            if remaining > 0.05:
                time.sleep(0.04)
            elif remaining > SPIN:
                time.sleep(remaining - SPIN)
            else:
                break
        while self.clicking and time.perf_counter() < deadline:
            pass

    def _do_click(self):
        btn_map = {"Left": Button.left, "Right": Button.right,
                   "Middle": Button.middle}
        count     = 0
        next_time = time.perf_counter()
        try:
            while self.clicking:
                cx, cy = pyautogui.position()
                if cx <= 0 and cy <= 0:
                    raise pyautogui.FailSafeException("Top-left corner")

                button = btn_map.get(self.click_button.get(), Button.left)
                double = self.click_type.get() == "Double"
                hold   = self.hold_ms.get() / 1000.0
                limit  = (self.repeat_count.get()
                          if self.repeat_mode.get() == "Count" else None)
                interval = self.get_interval()

                use_path = (self.path_enabled.get()
                            and bool(self.path_waypoints)
                            and not self._once_path_consumed)
                if use_path:
                    px, py, path_delay = self._get_path_pos()
                    self._mouse_ctrl.position = (px, py)
                    if path_delay:
                        interval = path_delay / 1000.0
                elif self.pos_mode.get() == "Fixed":
                    px, py = self.fixed_x.get(), self.fixed_y.get()
                    self._mouse_ctrl.position = (px, py)
                else:
                    px, py = cx, cy

                next_time += interval

                now   = time.time()
                delta = (now - self._last_click_time) if self._last_click_time else None
                self._last_click_time = now
                self._last_any_click  = now

                self._synthetic_until = time.perf_counter() + hold + 0.02
                if hold > 0:
                    _t0 = time.perf_counter()
                    self._mouse_ctrl.press(button)
                    time.sleep(hold)
                    self._mouse_ctrl.release(button)
                    measured_hold = time.perf_counter() - _t0
                elif double:
                    self._mouse_ctrl.click(button, 2)
                    measured_hold = 0.0
                else:
                    self._mouse_ctrl.click(button)
                    measured_hold = 0.0

                count += 1
                self.total_clicks += 1
                self._click_times.append(time.perf_counter())
                path_done = self._advance_path() if use_path else False

                if (self.on_click_log is not None
                        and (now - self._last_log_emit) >= 0.04):
                    self._last_log_emit = now
                    self.on_click_log({
                        "time": now, "button": self.click_button.get(),
                        "ctype": ("Double" if double else
                                  ("Hold"   if hold > 0 else "Single")),
                        "x": px, "y": py,
                        "hold_ms": int(round(measured_hold * 1000)),
                        "delta": delta,
                        "total": self.total_clicks,
                    })
                if limit and count >= limit:
                    self.clicking = False
                    if self.on_status_change:
                        self.on_status_change(False)
                    break
                if path_done:
                    stop_mode = self.once_stop_mode.get()
                    if stop_mode in ("Autoclicker", "Both"):
                        self.clicking = False
                        if self.on_status_change:
                            self.on_status_change(False)
                    elif stop_mode == "Trigger":
                        self._once_path_consumed = True
                    if self.on_once_done:
                        self.on_once_done()
                    if stop_mode in ("Autoclicker", "Both"):
                        break

                self._wait_until(next_time)
                late = time.perf_counter()
                if next_time < late:
                    next_time = late
        except pyautogui.FailSafeException:
            self.clicking = False
            if self.on_engine_note:
                self.on_engine_note("Fail-safe corner hit \u2014 emergency stop")
            if self.on_status_change:
                self.on_status_change(False)
        except Exception as err:
            self.clicking = False
            if self.on_engine_note:
                self.on_engine_note(f"Click thread stopped: {err}")
            if self.on_status_change:
                self.on_status_change(False)
    def start(self):
        if not self.clicking:
            self.clicking         = True
            self._last_click_time = None
            self._path_idx        = 0
            self._path_dir        = 1
            self._once_path_consumed = False
            self.click_thread     = threading.Thread(
                target=self._do_click, daemon=True)
            self.click_thread.start()
            if self.on_status_change:
                self.on_status_change(True)
    def stop(self):
        if self.clicking:
            self.clicking = False
            if self.on_status_change:
                self.on_status_change(False)
    def toggle(self):
        self.stop() if self.clicking else self.start()
    def _parse_hotkey(self, s):
        s = s.strip()
        attr = s.lower().replace(" ", "_")
        if hasattr(Key, attr):
            return getattr(Key, attr)
        if len(s) == 1:
            return KeyCode.from_char(s.lower())
        raise ValueError(s)
    def apply_hotkey(self, s):
        if (s or "").strip() == "":
            self._toggle_key = None
            return True
        try:
            self._toggle_key = self._parse_hotkey(s)
            return True
        except ValueError:
            return False
    def _key_name(self, key):
        try:
            return key.char or str(key)
        except AttributeError:
            return str(key).replace("Key.", "")
    def start_kb_listener(self, toggle_cb):
        def on_press(key):
            name = self._key_name(key)
            self._key_press_times[name] = time.time()
            if self._toggle_key is not None and key == self._toggle_key:
                toggle_cb()
        def on_release(key):
            name    = self._key_name(key)
            rel_t   = time.time()
            pre_t   = self._key_press_times.pop(name, None)
            hold_ms = int((rel_t - pre_t) * 1000) if pre_t else 0
            key_dt  = ((rel_t - self._last_key_time)
                       if self._last_key_time else None)
            self._last_key_time = rel_t
            if self.on_key_log:
                self.on_key_log({
                    "time":       rel_t,
                    "key":        name,
                    "hold_ms":    hold_ms,
                    "delta":      key_dt,
                    "is_toggle":  (self._toggle_key is not None
                                   and key == self._toggle_key),
                })
        self._kb_listener = KbListener(on_press=on_press,
                                       on_release=on_release)
        self._kb_listener.daemon = True
        self._kb_listener.start()
    def stop_kb_listener(self):
        if self._kb_listener:
            self._kb_listener.stop()
    def start_mouse_listener(self):
        BTN = {Button.left: "M1", Button.right: "M2", Button.middle: "M3"}
        def on_click(x, y, button, pressed):
            if time.perf_counter() < self._synthetic_until:
                return
            name = BTN.get(button, str(button))
            t    = time.time()
            if pressed:
                self._mouse_press_times[name] = t
            else:
                pre_t   = self._mouse_press_times.pop(name, None)
                hold_ms = int((t - pre_t) * 1000) if pre_t else 0
                delta   = ((t - self._last_any_click)
                           if self._last_any_click else None)
                self._last_any_click = t
                self.total_physical += 1
                self._click_times.append(time.perf_counter())
                if self.on_mouse_log:
                    self.on_mouse_log({
                        "time":    t, "button": name,
                        "x": x,   "y": y,
                        "hold_ms": hold_ms, "delta": delta,
                    })
        self._mouse_listener = MouseListener(on_click=on_click)
        self._mouse_listener.daemon = True
        self._mouse_listener.start()
    def stop_mouse_listener(self):
        if self._mouse_listener:
            self._mouse_listener.stop()
    def to_dict(self):
        mode = self.speed_mode.get()
        if mode == "ms":
            ms  = max(1, self.ms_val.get())
            cps = round(1000.0 / ms, 2)
        else:
            cps = max(0.01, self.cps_val.get())
            ms  = max(1, int(round(1000.0 / cps)))
        return {
            "speed_mode":   mode if mode in ("CPS", "ms") else "CPS",
            "cps":          cps,
            "ms":           ms,
            "button":       self.click_button.get(),
            "click_type":   self.click_type.get(),
            "hold_ms":      self.hold_ms.get(),
            "repeat_mode":  self.repeat_mode.get(),
            "repeat_count": self.repeat_count.get(),
            "pos_mode":     self.pos_mode.get(),
            "fixed_x":      self.fixed_x.get(),
            "fixed_y":      self.fixed_y.get(),
            "hotkey":       self.toggle_key_str.get(),
            "path_enabled": self.path_enabled.get(),
            "path_mode":    self.path_mode.get(),
            "waypoints":    list(self.path_waypoints),
            "once_stop_mode": self.once_stop_mode.get(),
        }
    def from_dict(self, d):
        self.speed_mode.set(d.get("speed_mode", "CPS"))
        self.cps_val.set(d.get("cps", 10.0))
        self.ms_val.set(d.get("ms", 100))
        self.click_button.set(d.get("button", "Left"))
        self.click_type.set(d.get("click_type", "Single"))
        self.hold_ms.set(d.get("hold_ms", 0))
        self.repeat_mode.set(d.get("repeat_mode", "Infinite"))
        self.repeat_count.set(d.get("repeat_count", 100))
        self.pos_mode.set(d.get("pos_mode", "Current"))
        self.fixed_x.set(d.get("fixed_x", 960))
        self.fixed_y.set(d.get("fixed_y", 540))
        self.toggle_key_str.set(d.get("hotkey", "F6"))
        self.path_enabled.set(d.get("path_enabled", False))
        self.path_mode.set(d.get("path_mode", "Loop"))
        self.path_waypoints = [dict(w) for w in d.get("waypoints", [])]
        self.once_stop_mode.set(d.get("once_stop_mode", "Autoclicker"))
class App(tk.Tk):
    BG      = "#1e1f22"
    PANEL   = "#2b2d31"
    BORDER  = "#3b3d42"
    INPUT   = "#383a3f"
    INPUT_B = "#474a50"
    FG      = "#e3e5e8"
    FG2     = "#8e9297"
    ACCENT  = "#5865F2"
    GREEN   = "#23a559"
    RED     = "#da3633"
    YELLOW  = "#f0b132"
    CONSOLE    = "#111214"
    CONSOLE_FG = "#e3e5e8"
    CYAN       = "#4fc3f7"
    ORANGE     = "#e37320"
    TITLEBAR   = "#2b2d31"
    FONT    = ("Segoe UI", 9)
    FONT_B  = ("Segoe UI", 9, "bold")
    MONO    = ("Consolas", 8)

    def _set_palette(self, theme):
        for k in THEME_KEYS:
            setattr(self, k, theme.get(k, getattr(App, k, "#000000")))
    def _full_theme(self, d):
        base = BUNDLED_THEMES["Default"]
        return {k: (d.get(k) or base[k]) for k in THEME_KEYS}
    def _ink(self, hexc):
        r, g, b = _hex_to_rgb(hexc)
        lum = 0.299 * r + 0.587 * g + 0.114 * b
        return "#1c1c20" if lum > 150 else "#ffffff"
    def _shade(self, hexc, f):
        r, g, b = _hex_to_rgb(hexc)
        if f <= 1:
            return _rgb_to_hex(r * f, g * f, b * f)
        t = f - 1
        return _rgb_to_hex(r + (255 - r) * t, g + (255 - g) * t, b + (255 - b) * t)
    def _mix(self, a, b, t):
        ar, ag, ab = _hex_to_rgb(a)
        br, bg, bb = _hex_to_rgb(b)
        return _rgb_to_hex(ar + (br - ar) * t, ag + (bg - ag) * t, ab + (bb - ab) * t)
    def _faint(self):
        return self._mix(self.FG2, self.BG, 0.5)
    def _load_themes_file(self):
        loaded = None
        try:
            if os.path.exists(THEMES_FILE):
                with open(THEMES_FILE, encoding="utf-8") as f:
                    loaded = json.load(f)
        except Exception:
            loaded = None
        if not loaded:
            self._themes = {k: dict(v) for k, v in BUNDLED_THEMES.items()}
            self._save_themes_file()
            return
        self._themes = loaded
        changed = False
        for name, theme in BUNDLED_THEMES.items():
            if name not in self._themes:
                self._themes[name] = dict(theme)
                changed = True
            else:
                for k, v in theme.items():
                    if k not in self._themes[name]:
                        self._themes[name][k] = v
                        changed = True
        if changed:
            self._save_themes_file()
    def _save_themes_file(self):
        try:
            with open(THEMES_FILE, "w", encoding="utf-8") as f:
                json.dump(self._themes, f, indent=2)
        except Exception as err:
            messagebox.showerror(
                "Theme Save Error",
                f"Could not save themes:\n{err}\n\nPath: {THEMES_FILE}",
            )
    def _remember_theme(self, name):
        self._settings["active_theme"] = name
        self._save_settings()
    def _init_active_theme(self):
        name = self._settings.get("active_theme")
        if not name or name not in self._themes:
            if "Default" in self._themes:
                name = "Default"
            elif self._themes:
                name = next(iter(self._themes))
            else:
                name = None
        if name is None:
            self._theme = {k: getattr(App, k) for k in THEME_KEYS}
        else:
            self._theme = self._full_theme(self._themes[name])
            self._current_theme.set(name)
        self._set_palette(self._theme)
    def _build_chrome(self):
        self._setup_combo_style()
        self.configure(bg=self.BG)
        self._build_tab_bar()
        self._content = tk.Frame(self, bg=self.BG)
        self._content.pack(fill="both", expand=True)
        self._clicker_frame  = tk.Frame(self._content, bg=self.BG)
        self._paths_frame    = tk.Frame(self._content, bg=self.BG)
        self._terminal_frame = tk.Frame(self._content, bg=self.BG)
        self._info_frame     = tk.Frame(self._content, bg=self.BG)
        self._aeths_frame    = tk.Frame(self._content, bg=self.BG)
        self._docs_frame     = tk.Frame(self._content, bg=self.BG)
        self._build_clicker_tab(self._clicker_frame)
        self._build_paths_tab(self._paths_frame)
        self._build_terminal(self._terminal_frame)
        self._build_info_tab(self._info_frame)
        self._build_aeths_tab(self._aeths_frame)
        self._build_docs_tab(self._docs_frame)
        self._show_tab(self._active_tab)
    def _apply_theme(self, theme):
        self._docs_capture_current()
        self._theme = self._full_theme(theme)
        self._set_palette(self._theme)
        for attr in ("_tab_bar", "_content"):
            w = getattr(self, attr, None)
            if w is not None:
                try:
                    w.destroy()
                except Exception:
                    pass
        self._build_chrome()
        self._apply_titlebar()
        self._sync_ui_after_load()
    def _load_selected_theme(self):
        name = self._current_theme.get()
        if name not in self._themes:
            return
        self._remember_theme(name)
        self._apply_theme(self._themes[name])
    def _save_current_theme(self):
        name = self._current_theme.get().strip()
        if not name:
            messagebox.showwarning("Theme", "No theme selected.")
            return
        self._themes[name] = dict(self._theme)
        self._save_themes_file()
        self._remember_theme(name)
        messagebox.showinfo("Theme", f"\u2714  Saved: {name}")
    def _new_theme(self):
        dlg = tk.Toplevel(self)
        dlg.title("New Theme")
        dlg.configure(bg=self.BG)
        dlg.resizable(False, False)
        dlg.grab_set()
        tk.Label(dlg, text="Theme name:", bg=self.BG, fg=self.FG,
                 font=self.FONT).pack(padx=16, pady=(14, 2), anchor="w")
        name_var = tk.StringVar()
        entry = self._mk_entry(dlg, name_var, width=22)
        entry.pack(padx=16, pady=(0, 12))
        entry.focus_set()
        def _ok(*_):
            name = name_var.get().strip()
            if not name:
                return
            self._themes[name] = dict(self._theme)
            self._save_themes_file()
            self._current_theme.set(name)
            self._remember_theme(name)
            dlg.destroy()
            self._apply_theme(self._themes[name])
        entry.bind("<Return>", _ok)
        bf = tk.Frame(dlg, bg=self.BG)
        bf.pack(pady=(0, 14))
        for text, cmd, bg in [("Create", _ok,         self.ACCENT),
                              ("Cancel", dlg.destroy,  self.BORDER)]:
            tk.Button(
                bf, text=text, command=cmd, bg=bg, fg=self._ink(bg),
                relief="flat",
                font=self.FONT_B if bg == self.ACCENT else self.FONT,
                bd=0, padx=14, pady=4,
            ).pack(side="left", padx=4)
    def _delete_theme(self):
        name = self._current_theme.get()
        if name not in self._themes:
            return
        if not messagebox.askyesno("Delete Theme", f"Delete \"{name}\"?"):
            return
        del self._themes[name]
        if not self._themes:
            self._themes = {k: dict(v) for k, v in BUNDLED_THEMES.items()}
        self._save_themes_file()
        new_name = "Default" if "Default" in self._themes else next(iter(self._themes))
        self._current_theme.set(new_name)
        self._remember_theme(new_name)
        self._apply_theme(self._themes[new_name])
    def _apply_titlebar(self):
        if platform.system() != "Windows":
            return
        try:
            import ctypes
            from ctypes import byref, sizeof, c_int
            self.update_idletasks()
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            dwm = ctypes.windll.dwmapi
            cap = getattr(self, "TITLEBAR", None) or self.PANEL
            r, g, b = _hex_to_rgb(cap)
            is_dark = (0.299 * r + 0.587 * g + 0.114 * b) <= 150
            dark = c_int(1 if is_dark else 0)
            for attr in (20, 19):
                dwm.DwmSetWindowAttribute(hwnd, attr, byref(dark), sizeof(dark))
            def _cref(hx):
                rr, gg, bb = _hex_to_rgb(hx)
                return c_int(rr | (gg << 8) | (bb << 16))
            cap_c = _cref(cap)
            txt_c = _cref(self._ink(cap))
            dwm.DwmSetWindowAttribute(hwnd, 35, byref(cap_c), sizeof(cap_c))
            dwm.DwmSetWindowAttribute(hwnd, 36, byref(txt_c), sizeof(txt_c))
            dwm.DwmSetWindowAttribute(hwnd, 34, byref(cap_c), sizeof(cap_c))
            ctypes.windll.user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0, 0x0027)
        except Exception:
            pass
    def _apply_icon(self):
        path = self._settings.get("icon_path")
        if not path or not os.path.exists(path):
            return
        try:
            if path.lower().endswith(".ico"):
                self.iconbitmap(default=path)
            else:
                img = tk.PhotoImage(file=path)
                self._icon_img = img
                self.iconphoto(True, img)
        except Exception:
            pass
    def _pick_theme_color(self, key):
        cur = self._theme.get(key, "#ffffff")
        try:
            res = colorchooser.askcolor(color=cur, parent=self,
                                        title=f"{key} colour")
        except Exception:
            res = colorchooser.askcolor(color=cur, title=f"{key} colour")
        if res and res[1]:
            new = dict(self._theme)
            new[key] = res[1]
            self._apply_theme(new)

    def _mk_sb(self, parent, var, from_, to, inc, width=5, font=None):
        return tk.Spinbox(
            parent, textvariable=var,
            from_=from_, to=to, increment=inc,
            width=width, font=font or ("Segoe UI", 8),
            bg=self.INPUT, fg=self.FG,
            insertbackground=self.FG,
            buttonbackground=self.INPUT_B,
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.BORDER,
            highlightcolor=self.ACCENT,
            selectbackground=self.ACCENT,
            selectforeground=self._ink(self.ACCENT),
        )
    def _mk_entry(self, parent, var, width=8):
        return tk.Entry(
            parent, textvariable=var, width=width,
            bg=self.INPUT, fg=self.FG,
            insertbackground=self.FG,
            relief="flat",
            highlightthickness=1,
            highlightbackground=self.BORDER,
            highlightcolor=self.ACCENT,
            selectbackground=self.ACCENT,
            selectforeground=self._ink(self.ACCENT),
            font=self.FONT,
        )
    def _setup_combo_style(self):
        self.option_add("*TCombobox*Listbox.background",       self.INPUT)
        self.option_add("*TCombobox*Listbox.foreground",       self.FG)
        self.option_add("*TCombobox*Listbox.selectBackground", self.ACCENT)
        self.option_add("*TCombobox*Listbox.selectForeground", self._ink(self.ACCENT))
        self.option_add("*TCombobox*Listbox.relief",           "flat")
        s = ttk.Style(self)
        s.theme_use("clam")
        for name in ("D.TCombobox", "P.TCombobox", "T2.TCombobox"):
            s.configure(name,
                fieldbackground=self.INPUT,
                background=self.INPUT_B,
                foreground=self.FG,
                insertcolor=self.FG,
                selectbackground=self.INPUT,
                selectforeground=self.FG,
                bordercolor=self.BORDER,
                lightcolor=self.BORDER,
                darkcolor=self.BORDER,
                arrowcolor=self.FG,
                padding=2,
                relief="flat",
            )
            s.map(name,
                fieldbackground=[("readonly", self.INPUT),
                                 ("focus",    self.INPUT),
                                 ("active",   self.INPUT)],
                foreground=[("readonly", self.FG),
                            ("focus",    self.FG),
                            ("active",   self.FG)],
                selectbackground=[("readonly", self.INPUT),
                                  ("focus",    self.INPUT)],
                selectforeground=[("readonly", self.FG),
                                  ("focus",    self.FG)],
                background=[("active", self.INPUT_B),
                            ("pressed", self.INPUT_B)],
                arrowcolor=[("active",  self.FG),
                            ("pressed", self.FG)],
                bordercolor=[("focus", self.BORDER), ("active", self.BORDER)],
                lightcolor=[("focus", self.BORDER), ("active", self.BORDER)],
                darkcolor=[("focus", self.BORDER), ("active", self.BORDER)],
            )
        if not getattr(self, "_combo_bound", False):
            self.bind_class("TCombobox", "<<ComboboxSelected>>",
                            lambda e: self.after(1, self.focus_set), add="+")
            self._combo_bound = True
    def __init__(self):
        super().__init__()
        self.ac = AutoClicker()
        self._pinned            = False
        self._capture_countdown = 0
        self._term_line_count   = 0
        self._start_pending_id  = None
        self._start_countdown_n = 0
        self._profiles        = {}
        self._settings        = {}
        self._current_profile = tk.StringVar(value="")
        self._load_settings()
        self._load_profiles_file()
        self._load_themes_file()
        self._current_theme = tk.StringVar(value="")
        self._init_active_theme()
        self._docs_dirty      = False
        self._docs_loading    = False
        self._docs_current_id = None
        self._doc_index       = {}
        self._doc_parent      = {}
        self._load_docs_file()
        self._trigger_armed  = False
        self._trigger_thread = None
        self._trig_type      = tk.StringVar(value="Off")
        self._trig_px_x      = tk.IntVar(value=960)
        self._trig_px_y      = tk.IntVar(value=540)
        self._trig_color     = (255, 255, 255)
        self._trig_tolerance = tk.IntVar(value=15)
        self._trig_condition = tk.StringVar(value="Matches")
        self._hotkey_arms_trigger = tk.BooleanVar(value=True)
        self._start_delay = tk.IntVar(value=0)
        self.title("Theenar")
        self.resizable(False, False)
        self.configure(bg=self.BG)
        self._active_tab = "clicker"
        self._build_chrome()
        self._apply_icon()
        self.after(60, self._apply_titlebar)
        self._update_loop()
        self._cps_tick()
        self._docs_autosave_tick()
        self.ac.on_click_log     = self._log_click
        self.ac.on_key_log       = self._log_key
        self.ac.on_mouse_log     = self._log_mouse
        self.ac.on_status_change = self._log_status
        self.ac.on_once_done     = self._on_once_done
        self.ac.on_engine_note   = self._log_note
        self.ac.start_kb_listener(self._hotkey_toggle)
        self.ac.start_mouse_listener()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.bind_all("<Button-1>", self._release_entry_focus, add="+")
        self._restore_last_profile()

    def _build_tab_bar(self):
        bar = tk.Frame(self, bg=self.PANEL,
                       highlightthickness=1,
                       highlightbackground=self.BORDER)
        bar.pack(fill="x")
        self._tab_bar = bar
        left = tk.Frame(bar, bg=self.PANEL)
        left.pack(side="left", padx=2, pady=1)
        self._tab_btns = {}
        for key, label in [("clicker",  "Clicker"),
                            ("paths",    "Paths"),
                            ("terminal", "Terminal"),
                            ("info",     "Info"),
                            ("aeths",    "Aeths"),
                            ("docs",     "Docs"),
                            ("widg",     "Widget")]:
            b = tk.Button(
                left, text=label,
                command=lambda k=key: self._show_tab(k),
                bg=self.PANEL, fg=self.FG2,
                relief="flat", cursor="hand2",
                font=("Segoe UI", 8, "bold"),
                activebackground=self.INPUT_B,
                activeforeground=self.FG,
                bd=0, padx=5, pady=2,
            )
            b.pack(side="left", padx=1)
            self._tab_btns[key] = b
        pill = tk.Frame(bar, bg=self.PANEL)
        pill.pack(side="right", padx=6, pady=1)
        self._tb_dot = tk.Label(pill, text="\u25cf", fg=self.RED,
                                bg=self.PANEL, font=("Segoe UI", 9))
        self._tb_dot.pack(side="left")
        self._tb_lbl = tk.Label(pill, text="IDLE", fg=self.RED,
                                bg=self.PANEL, font=("Segoe UI", 7, "bold"))
        self._tb_lbl.pack(side="left", padx=(2, 0))
    def _show_tab(self, key):
        self._active_tab = key
        widget_mode = (key == "widg")
        if widget_mode:
            self._content.pack_forget()
        else:
            if not self._content.winfo_manager():
                self._content.pack(fill="both", expand=True)
            for k, f in [("clicker",  self._clicker_frame),
                         ("paths",    self._paths_frame),
                         ("terminal", self._terminal_frame),
                         ("info",     self._info_frame),
                         ("aeths",    self._aeths_frame),
                         ("docs",     self._docs_frame)]:
                if k == key:
                    f.pack(fill="both", expand=True)
                else:
                    f.pack_forget()
        for k, btn in self._tab_btns.items():
            btn.config(
                bg=self.ACCENT if k == key else self.PANEL,
                fg=self._ink(self.ACCENT) if k == key else self.FG2,
            )
        self.wm_attributes("-topmost", self._pinned or widget_mode)
        self.update_idletasks()
        w = self.winfo_reqwidth()
        h = self.winfo_reqheight()
        self.minsize(w, h)
        self.maxsize(w, h)
        self.geometry(f"{w}x{h}")
    def _build_info_tab(self, parent):
        wrap = tk.Frame(parent, bg=self.BORDER,
                        highlightthickness=1, highlightbackground=self.BORDER)
        wrap.pack(fill="both", expand=True, padx=6, pady=6)
        txt = tk.Text(wrap, bg=self.CONSOLE, fg=self.CONSOLE_FG,
                      font=("Segoe UI", 8), relief="flat", wrap="word",
                      height=18, width=44, padx=10, pady=8, cursor="arrow",
                      selectbackground=self.ACCENT)
        sb = tk.Scrollbar(wrap, command=txt.yview, bg=self.PANEL,
                          troughcolor=self.BG, relief="flat")
        sb.pack(side="right", fill="y")
        txt.pack(side="left", fill="both", expand=True)
        txt.config(yscrollcommand=sb.set)
        txt.tag_configure("center", justify="center")
        txt.insert("1.0", INFO_TEXT)
        for line_num, line in enumerate(INFO_TEXT.splitlines(), start=1):
            if (
                "0Thirteen1" in line
                or "Peenar autoclicker" in line
                or "AUTOCLICKER SAFEGUARD" in line
                or "Touch the TOP" in line
                or "HOW TO SE" in line
                or "==================" in line
                or "-SECTION:" in line
                or "nfo without a desig" in line
                or "Idle/Online" in line
                or "  Profiles  " in line
                or "  Tabs  " in line
                or "  Pin  " in line
                or "  Speed & Click  " in line
                or "  Repeat & Position  " in line
                or "  Hotkey  " in line
                or "  Start / Stop  " in line
                or "  Trigger  " in line
                or "  Path Mode  " in line
                or "  Modes  " in line
                or "  On finish stop  " in line
                or "  Waypoints  " in line
                or "  The Log  " in line
                or "  CPS  " in line
                or "What is this place?" in line
                or "Where am I?" in line
                or "dragon yiff" in line
                or "This is the tab for color customization" in line
                or "I've already put two, just a cherry" in line
            ):
                txt.tag_add("center", f"{line_num}.0", f"{line_num}.end")
        txt.config(state="disabled")
    def _build_aeths_tab(self, parent):
        bar = tk.Frame(parent, bg=self.PANEL,
                       highlightthickness=1,
                       highlightbackground=self.BORDER)
        bar.pack(fill="x", padx=6, pady=(5, 0))
        tk.Label(bar, text="Theme:", bg=self.PANEL, fg=self.FG2,
                 font=("Segoe UI", 8)).pack(side="left", padx=(6, 3), pady=2)
        self._theme_cb = ttk.Combobox(
            bar, textvariable=self._current_theme,
            width=13, state="readonly",
            style="P.TCombobox", font=("Segoe UI", 8),
        )
        self._theme_cb["values"] = list(self._themes.keys())
        self._theme_cb.pack(side="left", padx=(0, 4), pady=2)
        self._theme_cb.bind("<<ComboboxSelected>>",
                            lambda e: self._load_selected_theme())
        for text, cmd, col in [
            ("Save", self._save_current_theme, self.BORDER),
            ("New",  self._new_theme,          self.ACCENT),
            ("Del",  self._delete_theme,        self.BORDER),
        ]:
            tk.Button(
                bar, text=text, command=cmd,
                bg=col, fg=self._ink(col) if col == self.ACCENT else self.FG,
                relief="flat", cursor="hand2",
                font=("Segoe UI", 8),
                activebackground=self.INPUT_B, activeforeground=self.FG,
                bd=0, padx=7, pady=2,
            ).pack(side="left", padx=2, pady=2)
        head = tk.Frame(parent, bg=self.BG)
        head.pack(fill="x", padx=6, pady=(4, 0))
        tk.Label(head, text="Changes apply live",
                 bg=self.BG, fg=self.FG2,
                 font=("Segoe UI", 7)).pack(side="left")
        wrap = tk.Frame(parent, bg=self.BORDER,
                        highlightthickness=1, highlightbackground=self.BORDER)
        wrap.pack(fill="both", expand=True, padx=6, pady=(4, 4))
        canvas = tk.Canvas(wrap, bg=self.PANEL, highlightthickness=0, height=300)
        sb = tk.Scrollbar(wrap, command=canvas.yview, bg=self.PANEL,
                          troughcolor=self.BG, relief="flat")
        inner = tk.Frame(canvas, bg=self.PANEL)
        inner_id = canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.config(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        def _resize(_=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(inner_id, width=canvas.winfo_width())
        inner.bind("<Configure>", _resize)
        canvas.bind("<Configure>", _resize)
        def _wheel(e):
            try:
                canvas.yview_scroll(int(-e.delta / 120), "units")
            except tk.TclError:
                pass
        canvas.bind("<Enter>",
                    lambda e: canvas.bind_all("<MouseWheel>", _wheel))
        canvas.bind("<Leave>",
                    lambda e: canvas.unbind_all("<MouseWheel>"))
        for key, label in AETHS_SWATCHES:
            cur = self._theme.get(key, "#000000")
            row = tk.Frame(inner, bg=self.PANEL)
            row.pack(fill="x", padx=8, pady=3)
            tk.Label(row, text=label, bg=self.PANEL, fg=self.FG,
                     font=("Segoe UI", 8), width=16,
                     anchor="w").pack(side="left")
            sw = tk.Label(row, bg=cur, width=4, cursor="hand2",
                          relief="flat", bd=0, highlightthickness=1,
                          highlightbackground=self.FG2)
            sw.pack(side="left", padx=(0, 8), ipady=4)
            sw.bind("<Button-1>", lambda e, k=key: self._pick_theme_color(k))
            hexlbl = tk.Label(row, text=cur.upper(), bg=self.PANEL,
                              fg=self.FG2, font=("Consolas", 8), cursor="hand2")
            hexlbl.pack(side="left")
            hexlbl.bind("<Button-1>",
                        lambda e, k=key: self._pick_theme_color(k))
        foot = tk.Frame(parent, bg=self.BG)
        foot.pack(fill="x", padx=6, pady=(0, 6))

    # ================================ DOCS ================================
    def _load_docs_file(self):
        default = {"id": "root", "type": "folder", "name": "Docs",
                   "children": []}
        data = None
        try:
            if os.path.exists(DOCS_FILE):
                with open(DOCS_FILE, encoding="utf-8") as f:
                    data = json.load(f)
        except Exception:
            data = None
        if data and isinstance(data.get("tree"), dict):
            self._docs_tree_root = data["tree"]
            self._docs_current_id = data.get("current")
        else:
            self._docs_tree_root = default
        self._docs_tree_root.setdefault("children", [])
        if not self._docs_tree_root["children"]:
            welcome = {
                "id": self._docs_new_id(), "type": "doc", "name": "Welcome",
                "text": ("UwU\n\n"
                         "Make folders and notes with the buttons up top (folders can hold folders yay) "
                         "(folders can hold folders). Type in this box (can edit this text or delete this note), "
                         "select text and hit B / I / U / A / \u25a0 to format it."
                         "\n\nAlso I'm not putting this in the info tab I'm too lazy just ask me if you need help :3"
                         "Btw you can't bold and italicize at the same time."
                         "\n\nEverything autosaves to theenar_docs.json."),
                "tags": {},
            }
            self._docs_tree_root["children"].append(welcome)
            self._docs_current_id = welcome["id"]

    def _docs_new_id(self):
        return "n%08x" % random.getrandbits(32)

    def _docs_save_file(self):
        self._docs_capture_current()
        data = {"tree": self._docs_tree_root, "current": self._docs_current_id}
        try:
            with open(DOCS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            self._docs_dirty = False
            if hasattr(self, "_docs_status") and self._docs_status.winfo_exists():
                self._docs_status.config(text="\u2714 Saved", fg=self.GREEN)
        except Exception as err:
            messagebox.showerror(
                "Docs Save Error",
                f"Could not save docs:\n{err}\n\nPath: {DOCS_FILE}")

    def _docs_mark_dirty(self, *_):
        self._docs_dirty = True
        if hasattr(self, "_docs_status") and self._docs_status.winfo_exists():
            self._docs_status.config(text="\u25cf Editing\u2026", fg=self.FG2)

    def _docs_autosave_tick(self):
        if getattr(self, "_docs_dirty", False):
            try:
                self._docs_save_file()
            except Exception:
                pass
        self.after(4000, self._docs_autosave_tick)

    def _build_docs_tab(self, parent):
        self._doc_index = {}
        self._doc_parent = {}
        ops = tk.Frame(parent, bg=self.PANEL, highlightthickness=1,
                       highlightbackground=self.BORDER)
        ops.pack(fill="x", padx=6, pady=(5, 0))
        for txt, cmd in [("\U0001f4c1+ Folder", lambda: self._docs_new("folder")),
                         ("\U0001f4c4+ Note",   lambda: self._docs_new("doc")),
                         ("Rename", self._docs_rename),
                         ("Delete", self._docs_delete)]:
            tk.Button(ops, text=txt, command=cmd,
                      bg=self.BORDER, fg=self.FG, relief="flat", cursor="hand2",
                      font=("Segoe UI", 8),
                      activebackground=self.INPUT_B, activeforeground=self.FG,
                      bd=0, padx=6, pady=2).pack(side="left", padx=2, pady=2)
        self._docs_status = tk.Label(ops, text="", bg=self.PANEL, fg=self.FG2,
                                     font=("Segoe UI", 8))
        self._docs_status.pack(side="right", padx=6)

        body = tk.Frame(parent, bg=self.BG)
        body.pack(fill="both", expand=True, padx=6, pady=(4, 6))

        left = tk.Frame(body, bg=self.BORDER, highlightthickness=1,
                        highlightbackground=self.BORDER)
        left.pack(side="left", fill="y")
        self._docs_setup_tree_style()
        self._docs_tree = ttk.Treeview(left, show="tree", height=13,
                                       style="Docs.Treeview",
                                       selectmode="browse")
        self._docs_tree.column("#0", width=150, stretch=False)
        tsb = tk.Scrollbar(left, command=self._docs_tree.yview,
                           bg=self.PANEL, troughcolor=self.BG, relief="flat")
        self._docs_tree.config(yscrollcommand=tsb.set)
        tsb.pack(side="right", fill="y")
        self._docs_tree.pack(side="left", fill="y")
        self._docs_tree.bind("<<TreeviewSelect>>", self._docs_on_select)

        right = tk.Frame(body, bg=self.BG)
        right.pack(side="left", fill="both", expand=True, padx=(6, 0))
        fmt = tk.Frame(right, bg=self.PANEL, highlightthickness=1,
                       highlightbackground=self.BORDER)
        fmt.pack(fill="x")
        # Title lives on its own row so a long note name can never push the
        # formatting buttons off the edge; the shown name is also truncated.
        title_row = tk.Frame(fmt, bg=self.PANEL)
        title_row.pack(fill="x")
        self._docs_title_var = tk.StringVar(value="")
        tk.Label(title_row, textvariable=self._docs_title_var, bg=self.PANEL,
                 fg=self.FG, font=("Segoe UI", 8, "bold"), anchor="w").pack(
            side="left", fill="x", expand=True, padx=(6, 6), pady=(2, 0))
        brow = tk.Frame(fmt, bg=self.PANEL)
        brow.pack(fill="x")

        def fbtn(label, cmd, fnt=None):
            tk.Button(brow, text=label, command=cmd, width=2,
                      bg=self.BORDER, fg=self.FG, relief="flat", cursor="hand2",
                      font=fnt or ("Segoe UI", 8, "bold"),
                      activebackground=self.INPUT_B, activeforeground=self.FG,
                      bd=0, padx=3, pady=1).pack(side="left", padx=1, pady=2)
        fbtn("B", lambda: self._docs_toggle("bold"))
        fbtn("I", lambda: self._docs_toggle("italic"),
             ("Segoe UI", 8, "italic"))
        fbtn("U", lambda: self._docs_toggle("underline"))
        fbtn("A", self._docs_text_color)
        fbtn("\u25a0", self._docs_highlight)
        tk.Button(brow, text="Clear", command=self._docs_clear_fmt,
                  bg=self.BORDER, fg=self.FG2, relief="flat", cursor="hand2",
                  font=("Segoe UI", 8),
                  activebackground=self.INPUT_B, activeforeground=self.FG,
                  bd=0, padx=6, pady=1).pack(side="left", padx=(4, 1), pady=2)
        tk.Button(brow, text="Save", command=self._docs_save_file,
                  bg=self.ACCENT, fg=self._ink(self.ACCENT), relief="flat",
                  cursor="hand2", font=("Segoe UI", 8, "bold"),
                  activebackground=self._shade(self.ACCENT, 0.8),
                  bd=0, padx=8, pady=1).pack(side="right", padx=(1, 4), pady=2)

        ed = tk.Frame(right, bg=self.BORDER, highlightthickness=1,
                      highlightbackground=self.BORDER)
        ed.pack(fill="both", expand=True, pady=(4, 0))
        self._docs_txt = tk.Text(
            ed, bg=self.INPUT, fg=self.FG, insertbackground=self.FG,
            relief="flat", wrap="word", height=13, width=40,
            padx=8, pady=6, font=("Segoe UI", 10),
            selectbackground=self.ACCENT, undo=True)
        esb = tk.Scrollbar(ed, command=self._docs_txt.yview,
                           bg=self.PANEL, troughcolor=self.BG, relief="flat")
        self._docs_txt.config(yscrollcommand=esb.set)
        esb.pack(side="right", fill="y")
        self._docs_txt.pack(side="left", fill="both", expand=True)
        self._docs_txt.tag_configure("bold",      font=("Segoe UI", 10, "bold"))
        self._docs_txt.tag_configure("italic",    font=("Segoe UI", 10, "italic"))
        self._docs_txt.tag_configure("underline", underline=True)
        self._docs_txt.bind("<<Modified>>", self._docs_on_modified)

        self._docs_refresh_tree()
        cid = self._docs_current_id
        if cid and cid in self._doc_index \
                and self._doc_index[cid]["type"] == "doc":
            self._docs_tree.selection_set(cid)
            self._docs_tree.see(cid)
            self._docs_open(cid)
        else:
            self._docs_current_id = None
            self._docs_txt.config(state="disabled")
            self._docs_set_title("Select or make a note \u2192")

    def _docs_setup_tree_style(self):
        st = ttk.Style(self)
        st.configure("Docs.Treeview",
                     background=self.INPUT, fieldbackground=self.INPUT,
                     foreground=self.FG, borderwidth=0, relief="flat",
                     rowheight=22, font=("Segoe UI", 9))
        st.map("Docs.Treeview",
               background=[("selected", self.ACCENT)],
               foreground=[("selected", self._ink(self.ACCENT))])

    def _docs_refresh_tree(self):
        open_ids = set()
        if getattr(self, "_docs_tree", None) is not None \
                and self._docs_tree.winfo_exists():
            for iid in list(self._doc_index):
                try:
                    if iid != "root" and self._docs_tree.item(iid, "open"):
                        open_ids.add(iid)
                except Exception:
                    pass
            self._docs_tree.delete(*self._docs_tree.get_children())
        self._doc_index = {"root": self._docs_tree_root}
        self._doc_parent = {}

        def add(node, parent_iid):
            self._doc_index[node["id"]] = node
            icon = "\U0001f4c1 " if node["type"] == "folder" else "\U0001f4c4 "
            self._docs_tree.insert(
                parent_iid, "end", iid=node["id"], text=icon + node["name"],
                open=(node["id"] in open_ids or not open_ids))
            if node["type"] == "folder":
                for ch in node.get("children", []):
                    self._doc_parent[ch["id"]] = node["id"]
                    add(ch, node["id"])
        for ch in self._docs_tree_root.get("children", []):
            self._doc_parent[ch["id"]] = "root"
            add(ch, "")

    def _docs_target_folder(self):
        sel = self._docs_tree.selection()
        if not sel:
            return self._docs_tree_root
        node = self._doc_index.get(sel[0])
        if not node:
            return self._docs_tree_root
        if node["type"] == "folder":
            return node
        pid = self._doc_parent.get(node["id"], "root")
        return self._doc_index.get(pid, self._docs_tree_root)

    def _docs_prompt(self, title, initial=""):
        dlg = tk.Toplevel(self)
        dlg.title(title)
        dlg.configure(bg=self.BG)
        dlg.resizable(False, False)
        dlg.grab_set()
        tk.Label(dlg, text=title, bg=self.BG, fg=self.FG,
                 font=self.FONT).pack(padx=16, pady=(14, 2), anchor="w")
        var = tk.StringVar(value=initial)
        entry = self._mk_entry(dlg, var, width=24)
        entry.pack(padx=16, pady=(0, 12))
        entry.focus_set()
        entry.select_range(0, "end")
        result = {"name": None}
        def _ok(*_):
            n = var.get().strip()
            if n:
                result["name"] = n
            dlg.destroy()
        entry.bind("<Return>", _ok)
        bf = tk.Frame(dlg, bg=self.BG)
        bf.pack(pady=(0, 14))
        for text, cmd, bg in [("OK", _ok, self.ACCENT),
                              ("Cancel", dlg.destroy, self.BORDER)]:
            tk.Button(bf, text=text, command=cmd, bg=bg, fg=self._ink(bg),
                      relief="flat",
                      font=self.FONT_B if bg == self.ACCENT else self.FONT,
                      bd=0, padx=14, pady=4).pack(side="left", padx=4)
        self.wait_window(dlg)
        return result["name"]

    def _docs_new(self, kind):
        parent = self._docs_target_folder()
        default = "New Folder" if kind == "folder" else "New Note"
        name = self._docs_prompt(
            "Folder name:" if kind == "folder" else "Note name:", default)
        if not name:
            return
        node = {"id": self._docs_new_id(), "type": kind, "name": name}
        if kind == "folder":
            node["children"] = []
        else:
            node["text"] = ""
            node["tags"] = {}
        parent.setdefault("children", []).append(node)
        self._docs_refresh_tree()
        self._docs_tree.selection_set(node["id"])
        self._docs_tree.see(node["id"])
        if kind == "doc":
            self._docs_open(node["id"])
        self._docs_mark_dirty()
        self._docs_save_file()

    def _docs_rename(self):
        sel = self._docs_tree.selection()
        if not sel:
            return
        node = self._doc_index.get(sel[0])
        if not node:
            return
        name = self._docs_prompt("New name:", node["name"])
        if not name:
            return
        node["name"] = name
        self._docs_refresh_tree()
        self._docs_tree.selection_set(node["id"])
        if self._docs_current_id == node["id"]:
            self._docs_set_title(name)
        self._docs_mark_dirty()
        self._docs_save_file()

    def _docs_delete(self):
        sel = self._docs_tree.selection()
        if not sel:
            return
        node = self._doc_index.get(sel[0])
        if not node:
            return
        kind = ("folder (and everything in it)"
                if node["type"] == "folder" else "note")
        if not messagebox.askyesno(
                "Delete", f"Delete this {kind}?\n\n\"{node['name']}\""):
            return
        pid = self._doc_parent.get(node["id"], "root")
        parent = self._doc_index.get(pid, self._docs_tree_root)
        parent["children"] = [c for c in parent.get("children", [])
                              if c["id"] != node["id"]]
        if (self._docs_current_id == node["id"]
                or self._docs_is_descendant(node, self._docs_current_id)):
            self._docs_current_id = None
            self._docs_txt.config(state="normal")
            self._docs_txt.delete("1.0", "end")
            self._docs_txt.config(state="disabled")
            self._docs_set_title("Select or make a note \u2192")
        self._docs_refresh_tree()
        self._docs_mark_dirty()
        self._docs_save_file()

    def _docs_is_descendant(self, node, target_id):
        if not target_id or node["type"] != "folder":
            return False
        for ch in node.get("children", []):
            if ch["id"] == target_id or self._docs_is_descendant(ch, target_id):
                return True
        return False

    def _docs_on_select(self, _=None):
        sel = self._docs_tree.selection()
        if not sel:
            return
        nid = sel[0]
        if nid == self._docs_current_id:
            return
        self._docs_capture_current()
        node = self._doc_index.get(nid)
        if node and node["type"] == "doc":
            self._docs_open(nid)
        else:
            self._docs_current_id = None
            self._docs_txt.config(state="normal")
            self._docs_txt.delete("1.0", "end")
            self._docs_txt.config(state="disabled")
            self._docs_set_title(
                (node["name"] + "  (folder)") if node else "")

    def _docs_open(self, nid):
        node = self._doc_index.get(nid)
        if not node or node["type"] != "doc":
            return
        self._docs_current_id = nid
        self._docs_loading = True
        self._docs_txt.config(state="normal")
        self._docs_txt.delete("1.0", "end")
        self._docs_txt.insert("1.0", node.get("text", ""))
        for tag, idxs in node.get("tags", {}).items():
            if tag.startswith("fg_"):
                self._docs_txt.tag_configure(tag, foreground=tag[3:])
            elif tag.startswith("bg_"):
                self._docs_txt.tag_configure(tag, background=tag[3:])
            for i in range(0, len(idxs) - 1, 2):
                try:
                    self._docs_txt.tag_add(tag, idxs[i], idxs[i + 1])
                except Exception:
                    pass
        self._docs_set_title(node["name"])
        self._docs_txt.edit_modified(False)
        self._docs_loading = False

    def _docs_capture_current(self):
        nid = getattr(self, "_docs_current_id", None)
        if not nid:
            return
        node = getattr(self, "_doc_index", {}).get(nid)
        if not node or node.get("type") != "doc":
            return
        if not (getattr(self, "_docs_txt", None) is not None
                and self._docs_txt.winfo_exists()):
            return
        node["text"] = self._docs_txt.get("1.0", "end-1c")
        tags = {}
        for t in self._docs_txt.tag_names():
            if t == "sel":
                continue
            ranges = self._docs_txt.tag_ranges(t)
            if ranges:
                tags[t] = [str(r) for r in ranges]
        node["tags"] = tags

    def _docs_selection(self):
        try:
            return (self._docs_txt.index("sel.first"),
                    self._docs_txt.index("sel.last"))
        except tk.TclError:
            return None

    def _docs_toggle(self, tag):
        rng = self._docs_selection()
        if not rng:
            return
        a, b = rng
        if tag in self._docs_txt.tag_names(a):
            self._docs_txt.tag_remove(tag, a, b)
        else:
            self._docs_txt.tag_add(tag, a, b)
        self._docs_mark_dirty()

    def _docs_text_color(self):
        res = colorchooser.askcolor(parent=self, title="Text color")
        if res and res[1]:
            self._docs_apply_color("fg_", res[1], foreground=res[1])

    def _docs_highlight(self):
        res = colorchooser.askcolor(parent=self, title="Highlight color")
        if res and res[1]:
            self._docs_apply_color("bg_", res[1], background=res[1])

    def _docs_apply_color(self, prefix, hexc, **cfg):
        rng = self._docs_selection()
        if not rng:
            return
        a, b = rng
        for t in self._docs_txt.tag_names():
            if t.startswith(prefix):
                self._docs_txt.tag_remove(t, a, b)
        tag = prefix + hexc
        self._docs_txt.tag_configure(tag, **cfg)
        self._docs_txt.tag_add(tag, a, b)
        self._docs_mark_dirty()

    def _docs_clear_fmt(self):
        rng = self._docs_selection()
        if not rng:
            return
        a, b = rng
        for t in self._docs_txt.tag_names():
            if t == "sel":
                continue
            self._docs_txt.tag_remove(t, a, b)
        self._docs_mark_dirty()

    def _docs_on_modified(self, _=None):
        if getattr(self, "_docs_loading", False):
            self._docs_txt.edit_modified(False)
            return
        if self._docs_txt.edit_modified():
            self._docs_txt.edit_modified(False)
            if self._docs_current_id:
                self._docs_mark_dirty()

    def _docs_set_title(self, text):
        text = text or ""
        shown = text if len(text) <= 30 else text[:29] + "\u2026"
        self._docs_title_var.set(shown)
    # ============================== END DOCS ==============================
    def _build_clicker_tab(self, parent):
        self._build_profiles_bar(parent)
        self._build_clicker_ui(parent)
        self._build_trigger_section(parent)

    def _build_profiles_bar(self, parent):
        bar = tk.Frame(parent, bg=self.PANEL,
                       highlightthickness=1,
                       highlightbackground=self.BORDER)
        bar.pack(fill="x", padx=6, pady=(5, 0))
        tk.Label(bar, text="Profile:", bg=self.PANEL, fg=self.FG2,
                 font=("Segoe UI", 8)).pack(side="left", padx=(6, 3), pady=2)
        self._profile_cb = ttk.Combobox(
            bar, textvariable=self._current_profile,
            width=13, state="readonly",
            style="P.TCombobox", font=("Segoe UI", 8),
        )
        self._profile_cb.pack(side="left", padx=(0, 4), pady=2)
        self._profile_cb.bind("<<ComboboxSelected>>",
                              lambda e: self._load_selected_profile())
        self._refresh_profile_list()
        for text, cmd, col in [
            ("Save", self._save_current_profile, self.BORDER),
            ("New",  self._new_profile,          self.ACCENT),
            ("Del",  self._delete_profile,        self.BORDER),
        ]:
            tk.Button(
                bar, text=text, command=cmd,
                bg=col, fg=self._ink(col) if col == self.ACCENT else self.FG,
                relief="flat", cursor="hand2",
                font=("Segoe UI", 8),
                activebackground=self.INPUT_B, activeforeground=self.FG,
                bd=0, padx=7, pady=2,
            ).pack(side="left", padx=2, pady=2)

    def _section(self, parent, title):
        wrap = tk.Frame(parent, bg=self.PANEL,
                        highlightthickness=1,
                        highlightbackground=self.BORDER)
        wrap.pack(fill="x", padx=6, pady=(0, 2))
        tk.Label(wrap, text=title, bg=self.PANEL, fg=self.FG2,
                 font=("Segoe UI", 7, "bold")).pack(
            anchor="w", padx=6, pady=(2, 0))
        inner = tk.Frame(wrap, bg=self.PANEL)
        inner.pack(fill="x", padx=6, pady=(0, 2))
        return inner
    def _row(self, parent, label, builder):
        row = tk.Frame(parent, bg=self.PANEL)
        row.pack(fill="x", pady=1)
        tk.Label(row, text=label, bg=self.PANEL, fg=self.FG,
                 font=self.FONT, width=8, anchor="w").pack(side="left")
        builder(row)
        return row
    def _spinbox(self, parent, var, from_, to, inc, width=8, fmt=None):
        sb = self._mk_sb(parent, var, from_, to, inc,
                         width=width, font=self.FONT)
        if fmt:
            sb.config(format=fmt)
        sb.pack(side="left", padx=(0, 3))
        return sb
    def _combo(self, parent, var, values, width=9):
        cb = ttk.Combobox(parent, textvariable=var, values=values,
                          width=width, state="readonly",
                          style="D.TCombobox", font=self.FONT)
        cb.pack(side="left", padx=(0, 3))
        return cb
    def _entry(self, parent, var, width=8):
        e = self._mk_entry(parent, var, width=width)
        e.pack(side="left", padx=(0, 3))
        return e
    def _lbl(self, parent, text):
        tk.Label(parent, text=text, bg=self.PANEL, fg=self.FG2,
                 font=self.FONT).pack(side="left", padx=(2, 2))

    def _build_clicker_ui(self, parent):
        stats = tk.Frame(parent, bg=self.PANEL,
                         highlightthickness=1,
                         highlightbackground=self.BORDER)
        stats.pack(fill="x", padx=6, pady=(4, 2))
        self.status_dot = tk.Label(stats, text="\u25cf", fg=self.RED,
                                   bg=self.PANEL, font=("Segoe UI", 10))
        self.status_dot.pack(side="left", padx=(6, 2), pady=2)
        self.status_lbl = tk.Label(stats, text="IDLE", fg=self.RED,
                                   bg=self.PANEL, font=self.FONT_B,
                                   width=7, anchor="w")
        self.status_lbl.pack(side="left")
        tk.Label(stats, text="Clicks:", fg=self.FG2, bg=self.PANEL,
                 font=self.FONT).pack(side="left", padx=(8, 2))
        self.clicks_lbl = tk.Label(stats, text="0", fg=self.FG,
                                   bg=self.PANEL, font=self.FONT_B,
                                   width=7, anchor="w")
        self.clicks_lbl.pack(side="left")
        self._pin_btn = tk.Button(
            stats, text="\U0001f4cc Pin", command=self._toggle_pin,
            bg=self.PANEL, fg=self.FG2, relief="flat", cursor="hand2",
            font=("Segoe UI", 7),
            activebackground=self.INPUT_B, activeforeground=self.FG,
            bd=0, padx=5,
        )
        self._pin_btn.pack(side="right", padx=(0, 2))
        tk.Button(
            stats, text="Reset", command=self._reset_counter,
            bg=self.PANEL, fg=self.FG2, relief="flat", cursor="hand2",
            font=("Segoe UI", 7),
            activebackground=self.PANEL, activeforeground=self.FG,
            bd=0, padx=5,
        ).pack(side="right")

        s = self._section(parent, "SPEED & CLICK")
        def speed_builder(p):
            mf = tk.Frame(p, bg=self.PANEL)
            mf.pack(side="left", padx=(0, 5))
            self._cps_btn = tk.Button(
                mf, text="CPS",
                command=lambda: self._set_speed_mode("CPS"),
                bg=self.ACCENT, fg=self._ink(self.ACCENT), relief="flat",
                cursor="hand2", font=("Segoe UI", 8, "bold"),
                bd=0, padx=6, pady=2,
            )
            self._cps_btn.pack(side="left")
            self._ms_btn = tk.Button(
                mf, text="ms",
                command=lambda: self._set_speed_mode("ms"),
                bg=self.BORDER, fg=self.FG2, relief="flat",
                cursor="hand2", font=("Segoe UI", 8, "bold"),
                bd=0, padx=6, pady=2,
            )
            self._ms_btn.pack(side="left")
            self._cps_sb = self._spinbox(p, self.ac.cps_val,
                                         0.01, 999.99, 0.5,
                                         width=7, fmt="%.2f")
            self._ms_sb = self._spinbox(p, self.ac.ms_val,
                                        1, 60000, 10, width=7)
            self._ms_sb.pack_forget()
            self._speed_unit = tk.Label(p, text="clicks/sec",
                                        bg=self.PANEL, fg=self.FG2,
                                        font=("Segoe UI", 8))
            self._speed_unit.pack(side="left")
        self._row(s, "Speed", speed_builder)
        def click_row(p):
            self._combo(p, self.ac.click_button,
                        ["Left", "Right", "Middle"], width=7)
            self._lbl(p, "Type:")
            self._combo(p, self.ac.click_type,
                        ["Single", "Double"], width=7)
            self._lbl(p, "Hold:")
            self._spinbox(p, self.ac.hold_ms, 0, 2000, 10, width=5)
            self._lbl(p, "ms")
        self._row(s, "Click", click_row)

        s = self._section(parent, "REPEAT & POSITION")
        def repeat_builder(p):
            self._combo(p, self.ac.repeat_mode,
                        ["Infinite", "Count"], width=8)
            self._lbl(p, "Count:")
            self._spinbox(p, self.ac.repeat_count,
                          1, 999999, 10, width=7)
        self._row(s, "Repeat", repeat_builder)
        def pos_builder(p):
            self._combo(p, self.ac.pos_mode,
                        ["Current", "Fixed"], width=7)
            self._lbl(p, "X:")
            self._spinbox(p, self.ac.fixed_x, 0, 9999, 1, width=5)
            self._lbl(p, "Y:")
            self._spinbox(p, self.ac.fixed_y, 0, 9999, 1, width=5)
            self.cap_btn = tk.Button(
                p, text="\U0001f4cd Cap 3s", width=13,
                command=self._start_capture,
                bg=self.BORDER, fg=self.FG, relief="flat",
                cursor="hand2", font=("Segoe UI", 8),
                activebackground=self.INPUT_B, activeforeground=self.FG,
                bd=0, padx=4, pady=1,
            )
            self.cap_btn.pack(side="left", padx=(4, 0))
        self._row(s, "Position", pos_builder)

        s = self._section(parent, "HOTKEY")
        def hk_builder(p):
            self._entry(p, self.ac.toggle_key_str, width=6)
            tk.Button(
                p, text="Apply", command=self._apply_hotkey,
                bg=self.BORDER, fg=self.FG, relief="flat",
                cursor="hand2", font=self.FONT,
                activebackground=self.INPUT_B, activeforeground=self.FG,
                bd=0, padx=6, pady=2,
            ).pack(side="left", padx=(2, 8))
            self._lbl(p, "Delay:")
            self._spinbox(p, self._start_delay, 0, 60, 1, width=3)
            self._lbl(p, "s")
        self._row(s, "Toggle", hk_builder)

        bf = tk.Frame(parent, bg=self.BG)
        bf.pack(fill="x", padx=6, pady=(3, 2))
        self._start_btn = tk.Button(
            bf, text="\u25b6  START", command=self._start,
            bg=self.GREEN, fg=self._ink(self.GREEN), relief="flat",
            font=("Segoe UI", 10, "bold"), cursor="hand2",
            activebackground=self._shade(self.GREEN, 0.72), bd=0, pady=5,
        )
        self._start_btn.pack(side="left", fill="x", expand=True,
                             padx=(0, 4))
        tk.Button(
            bf, text="\u25a0  STOP", command=self._stop,
            bg=self.RED, fg=self._ink(self.RED), relief="flat",
            font=("Segoe UI", 10, "bold"), cursor="hand2",
            activebackground=self._shade(self.RED, 0.72), bd=0, pady=5,
        ).pack(side="left", fill="x", expand=True)
        tk.Label(
            parent,
            text="Top-left corner of your monitor = emergency stop",
            bg=self.BG, fg=self.FG2, font=("Segoe UI", 7),
        ).pack(pady=(0, 1))

    def _build_trigger_section(self, parent):
        wrap = tk.Frame(parent, bg=self.PANEL,
                        highlightthickness=1,
                        highlightbackground=self.BORDER)
        wrap.pack(fill="x", padx=6, pady=(0, 4))
        tk.Label(wrap, text="TRIGGER", bg=self.PANEL, fg=self.FG2,
                 font=("Segoe UI", 7, "bold")).pack(
            anchor="w", padx=6, pady=(2, 0))
        inner = tk.Frame(wrap, bg=self.PANEL)
        inner.pack(fill="x", padx=6, pady=(0, 3))
        tr = tk.Frame(inner, bg=self.PANEL)
        tr.pack(fill="x", pady=(1, 1))
        tk.Label(tr, text="Type:", bg=self.PANEL, fg=self.FG,
                 font=self.FONT, width=7, anchor="w").pack(side="left")
        for val, lbl in [("Off", "Off"), ("Pixel", "Pixel Color")]:
            tk.Radiobutton(
                tr, text=lbl,
                variable=self._trig_type, value=val,
                command=self._on_trig_type_change,
                bg=self.PANEL, fg=self.FG,
                selectcolor=self.INPUT,
                activebackground=self.PANEL, activeforeground=self.FG,
                font=("Segoe UI", 8), bd=0,
            ).pack(side="left", padx=(0, 10))
        self._trig_pixel_frame = tk.Frame(inner, bg=self.PANEL)
        self._build_trig_pixel(self._trig_pixel_frame)
        self._arm_row = tk.Frame(inner, bg=self.PANEL)
        self._arm_btn = tk.Button(
            self._arm_row, text="\u25b6  Arm Trigger",
            command=self._toggle_trigger,
            bg=self.ACCENT, fg=self._ink(self.ACCENT), relief="flat",
            cursor="hand2", font=("Segoe UI", 8, "bold"),
            activebackground=self._shade(self.ACCENT, 0.8), bd=0, padx=8, pady=2,
        )
        self._arm_btn.pack(side="left", padx=(0, 6))
        self._hk_mode_btn = tk.Button(
            self._arm_row,
            text="\U0001f511 HK: Arm",
            command=self._toggle_hotkey_arms_trigger,
            bg=self.ACCENT, fg=self._ink(self.ACCENT), relief="flat",
            cursor="hand2", font=("Segoe UI", 8, "bold"),
            activebackground=self._shade(self.ACCENT, 0.8), bd=0, padx=6, pady=2,
        )
        self._hk_mode_btn.pack(side="left", padx=(0, 6))
        self._trig_status = tk.Label(
            self._arm_row, text="",
            bg=self.PANEL, fg=self.FG2, font=("Segoe UI", 8),
        )
        self._trig_status.pack(side="left")
        self._on_trig_type_change()

    def _build_trig_pixel(self, parent):
        r1 = tk.Frame(parent, bg=self.PANEL)
        r1.pack(fill="x", pady=1)
        tk.Label(r1, text="Watch:", bg=self.PANEL, fg=self.FG,
                 font=self.FONT, width=7, anchor="w").pack(side="left")
        for lbl, var in [("X", self._trig_px_x), ("Y", self._trig_px_y)]:
            tk.Label(r1, text=lbl, bg=self.PANEL, fg=self.FG2,
                     font=self.FONT).pack(side="left")
            self._mk_sb(r1, var, 0, 9999, 1, width=5).pack(
                side="left", padx=(2, 4))
        tk.Button(
            r1, text="\U0001f4cd Cap", command=self._capture_trigger_pos,
            bg=self.BORDER, fg=self.FG, relief="flat", cursor="hand2",
            font=("Segoe UI", 8),
            activebackground=self.INPUT_B, bd=0, padx=5, pady=1,
        ).pack(side="left")
        r2 = tk.Frame(parent, bg=self.PANEL)
        r2.pack(fill="x", pady=1)
        tk.Label(r2, text="Color:", bg=self.PANEL, fg=self.FG,
                 font=self.FONT, width=7, anchor="w").pack(side="left")
        self._color_swatch = tk.Label(r2, bg="#ffffff", width=3,
                                      relief="flat", cursor="hand2")
        self._color_swatch.pack(side="left", padx=(0, 4), ipady=5)
        self._color_swatch.bind("<Button-1>", lambda e: self._pick_color())
        self._color_hex_lbl = tk.Label(r2, text="#ffffff",
                                       bg=self.PANEL, fg=self.FG2,
                                       font=("Segoe UI", 8))
        self._color_hex_lbl.pack(side="left", padx=(0, 6))
        tk.Button(
            r2, text="Sample", command=self._sample_pixel,
            bg=self.BORDER, fg=self.FG, relief="flat", cursor="hand2",
            font=("Segoe UI", 8),
            activebackground=self.INPUT_B, bd=0, padx=5, pady=1,
        ).pack(side="left", padx=(0, 6))
        tk.Label(r2, text="Tol:", bg=self.PANEL, fg=self.FG2,
                 font=self.FONT).pack(side="left")
        self._mk_sb(r2, self._trig_tolerance, 0, 128, 5, width=4).pack(
            side="left", padx=(2, 0))
        r3 = tk.Frame(parent, bg=self.PANEL)
        r3.pack(fill="x", pady=1)
        tk.Label(r3, text="Start:", bg=self.PANEL, fg=self.FG,
                 font=self.FONT, width=7, anchor="w").pack(side="left")
        ttk.Combobox(
            r3, textvariable=self._trig_condition,
            values=["Matches", "Doesn't Match"],
            width=13, state="readonly",
            style="T2.TCombobox", font=self.FONT,
        ).pack(side="left")
    def _on_trig_type_change(self, *_):
        self._trig_pixel_frame.pack_forget()
        self._arm_row.pack_forget()
        if self._trig_type.get() == "Pixel":
            self._trig_pixel_frame.pack(fill="x")
            if not self._trigger_armed:
                self._trig_status.config(text="Ready \u2014 arm to start watching")
            self._arm_row.pack(fill="x", pady=(3, 0))
        self._update_hk_mode_btn()

    def _toggle_hotkey_arms_trigger(self):
        new = not self._hotkey_arms_trigger.get()
        self._hotkey_arms_trigger.set(new)
        self._update_hk_mode_btn()
    def _update_hk_mode_btn(self):
        if self._trig_type.get() == "Off":
            self._hk_mode_btn.pack_forget()
            return
        self._arm_btn.pack(side="left", padx=(0, 6))
        self._hk_mode_btn.pack(side="left", padx=(0, 6))
        if self._hotkey_arms_trigger.get():
            self._hk_mode_btn.config(
                text="\U0001f511 HK: Arm",
                bg=self.ACCENT, fg=self._ink(self.ACCENT),
                activebackground=self._shade(self.ACCENT, 0.8),
            )
        else:
            self._hk_mode_btn.config(
                text="\U0001f511 HK: AC",
                bg=self.BORDER, fg=self.FG,
                activebackground=self.INPUT_B,
            )

    def _capture_trigger_pos(self):
        def _tick(n):
            if n > 0:
                self._trig_status.config(text=f"Move mouse\u2026 {n}s")
                self.after(1000, lambda: _tick(n - 1))
            else:
                x, y = pyautogui.position()
                self._trig_px_x.set(x)
                self._trig_px_y.set(y)
                self._sample_pixel()
                self._trig_status.config(text=f"Captured ({x}, {y})")
        _tick(2)
    def _sample_pixel(self):
        try:
            r, g, b = pyautogui.pixel(self._trig_px_x.get(),
                                      self._trig_px_y.get())
            self._set_trig_color(r, g, b)
        except Exception:
            pass
    def _pick_color(self):
        r, g, b = self._trig_color
        result = colorchooser.askcolor(
            f"#{r:02x}{g:02x}{b:02x}", title="Pick trigger color")
        if result and result[0]:
            self._set_trig_color(*(int(c) for c in result[0]))
    def _set_trig_color(self, r, g, b):
        self._trig_color = (r, g, b)
        h = f"#{r:02x}{g:02x}{b:02x}"
        self._color_swatch.config(bg=h)
        self._color_hex_lbl.config(text=h)

    def _toggle_trigger(self):
        if self._trigger_armed:
            self._disarm_trigger()
        else:
            self._arm_trigger()
    def _arm_trigger(self):
        self._trigger_armed = True
        self._arm_btn.config(text="\u25a0  Disarm",
                             bg=self.RED, fg=self._ink(self.RED),
                             activebackground=self._shade(self.RED, 0.72))
        t = threading.Thread(target=self._pixel_trigger_loop, daemon=True)
        self._trigger_thread = t
        t.start()
    def _disarm_trigger(self):
        self._trigger_armed = False
        self._arm_btn.config(text="\u25b6  Arm Trigger",
                             bg=self.ACCENT, fg=self._ink(self.ACCENT),
                             activebackground=self._shade(self.ACCENT, 0.8))
        self.after(0, lambda: self._trig_status.config(text="Disarmed"))
    def _pixel_trigger_loop(self):
        prev_met = False
        while self._trigger_armed:
            try:
                r, g, b = pyautogui.pixel(self._trig_px_x.get(),
                                          self._trig_px_y.get())
                tr, tg, tb = self._trig_color
                dist  = max(abs(r - tr), abs(g - tg), abs(b - tb))
                match = dist <= self._trig_tolerance.get()
                want  = self._trig_condition.get() == "Matches"
                met   = (match == want)
                mark  = "\u2713" if match else "\u2717"
                txt   = f"#{r:02x}{g:02x}{b:02x}  dist={dist}  {mark}"
                self.after(0, lambda t=txt: self._trig_status.config(text=t))

                if met:
                    if (not prev_met) or (not self.ac.clicking):
                        self.after(0, self._start)
                else:
                    if prev_met:
                        self.after(0, self._stop)
                prev_met = met
            except Exception:
                pass
            time.sleep(0.1)

    _PATH_MODE_DESC = {
        "Loop":   "1\u21922\u21923\u21921\u21922\u2192\u2026  cycles forward forever",
        "Bounce": "1\u21922\u21923\u21922\u21921\u2192\u2026  reverses at each end",
        "Random": "picks a random waypoint each click",
        "Once":   "1\u21922\u21923  then stops based on On finish stop setting",
    }
    def _build_paths_tab(self, parent):
        top = tk.Frame(parent, bg=self.PANEL,
                       highlightthickness=1,
                       highlightbackground=self.BORDER)
        top.pack(fill="x", padx=6, pady=(6, 3))
        ctrl = tk.Frame(top, bg=self.PANEL)
        ctrl.pack(side="left", padx=6, pady=5)
        self._path_enable_btn = tk.Button(
            ctrl, text="\u25cb  Path Mode: OFF",
            command=self._toggle_path_mode,
            bg=self.BORDER, fg=self.FG2, relief="flat",
            cursor="hand2", font=("Segoe UI", 9, "bold"),
            activebackground=self.INPUT_B, bd=0, padx=8, pady=3,
        )
        self._path_enable_btn.pack(anchor="w")
        mode_row = tk.Frame(ctrl, bg=self.PANEL)
        mode_row.pack(anchor="w", pady=(3, 0))
        tk.Label(mode_row, text="Mode:", bg=self.PANEL, fg=self.FG2,
                 font=("Segoe UI", 8)).pack(side="left", padx=(0, 4))
        for m in ["Loop", "Bounce", "Random", "Once"]:
            tk.Radiobutton(
                mode_row, text=m,
                variable=self.ac.path_mode, value=m,
                command=self._on_path_mode_change,
                bg=self.PANEL, fg=self.FG,
                selectcolor=self.INPUT,
                activebackground=self.PANEL, activeforeground=self.FG,
                font=("Segoe UI", 8), bd=0,
            ).pack(side="left", padx=(0, 5))
        self._mode_desc_lbl = tk.Label(
            ctrl,
            text=self._PATH_MODE_DESC["Loop"],
            bg=self.PANEL, fg=self._faint(),
            font=("Segoe UI", 7),
        )
        self._mode_desc_lbl.pack(anchor="w", pady=(2, 0))
        self._once_stop_frame = tk.Frame(ctrl, bg=self.PANEL)
        tk.Label(self._once_stop_frame, text="On finish stop:",
                 bg=self.PANEL, fg=self.FG2,
                 font=("Segoe UI", 8)).pack(side="left", padx=(0, 4))
        self._once_stop_btns = {}
        for mode_val, mode_lbl in [("Autoclicker", "AC"),
                                    ("Trigger", "Trigger"),
                                    ("Both", "Both")]:
            btn = tk.Button(
                self._once_stop_frame, text=mode_lbl,
                command=lambda v=mode_val: self._set_once_stop_mode(v),
                relief="flat", cursor="hand2",
                font=("Segoe UI", 8, "bold"),
                bd=0, padx=6, pady=2,
                bg=self.ACCENT if self.ac.once_stop_mode.get() == mode_val else self.BORDER,
                fg=self._ink(self.ACCENT) if self.ac.once_stop_mode.get() == mode_val else self.FG2,
                activebackground=self.INPUT_B, activeforeground=self.FG,
            )
            btn.pack(side="left", padx=2)
            self._once_stop_btns[mode_val] = btn
        self._update_once_stop_visibility()
        self._wp_count_lbl = tk.Label(
            top, text="0 waypoints",
            bg=self.PANEL, fg=self.FG2, font=("Segoe UI", 8),
        )
        self._wp_count_lbl.pack(side="right", padx=8)
        list_outer = tk.Frame(parent, bg=self.BORDER,
                              highlightthickness=1,
                              highlightbackground=self.BORDER)
        list_outer.pack(fill="both", expand=True, padx=6, pady=(0, 3))
        self._wp_canvas = tk.Canvas(list_outer, bg=self.BG,
                                    highlightthickness=0)
        wp_sb = tk.Scrollbar(list_outer, orient="vertical",
                             command=self._wp_canvas.yview,
                             bg=self.PANEL, troughcolor=self.BG,
                             relief="flat")
        wp_sb.pack(side="right", fill="y")
        self._wp_canvas.pack(side="left", fill="both", expand=True)
        self._wp_canvas.configure(yscrollcommand=wp_sb.set)
        self._wp_list_frame = tk.Frame(self._wp_canvas, bg=self.BG)
        self._wp_canvas_win = self._wp_canvas.create_window(
            (0, 0), window=self._wp_list_frame, anchor="nw")
        self._wp_list_frame.bind(
            "<Configure>",
            lambda e: self._wp_canvas.configure(
                scrollregion=self._wp_canvas.bbox("all")))
        self._wp_canvas.bind(
            "<Configure>",
            lambda e: self._wp_canvas.itemconfig(
                self._wp_canvas_win, width=e.width))
        hdr = tk.Frame(self._wp_list_frame, bg=self.PANEL)
        hdr.pack(fill="x", padx=2, pady=(2, 0))
        for text, w in [("#", 2), ("  X", 6), ("  Y", 6),
                        ("  Delay ms", 9), ("", 18)]:
            tk.Label(hdr, text=text, bg=self.PANEL, fg=self.FG2,
                     font=("Segoe UI", 7, "bold"),
                     width=w, anchor="w").pack(side="left", padx=2)
        self._wp_rows = []
        self._rebuild_wp_list()
        bot = tk.Frame(parent, bg=self.BG)
        bot.pack(fill="x", padx=6, pady=(0, 6))
        tk.Button(
            bot, text="\uff0b  Add Waypoint",
            command=lambda: self._add_waypoint(),
            bg=self.GREEN, fg=self._ink(self.GREEN), relief="flat",
            cursor="hand2", font=("Segoe UI", 8, "bold"),
            activebackground=self._shade(self.GREEN, 0.72), bd=0, padx=10, pady=4,
        ).pack(side="left")
        tk.Button(
            bot, text="\U0001f4cd Capture (3 s)",
            command=self._add_wp_at_mouse,
            bg=self.BORDER, fg=self.FG, relief="flat",
            cursor="hand2", font=("Segoe UI", 8),
            activebackground=self.INPUT_B, bd=0, padx=8, pady=4,
        ).pack(side="left", padx=(4, 0))
        tk.Button(
            bot, text="Clear All",
            command=self._clear_waypoints,
            bg=self.BORDER, fg=self.FG2, relief="flat",
            cursor="hand2", font=("Segoe UI", 8),
            activebackground=self.INPUT_B, bd=0, padx=8, pady=4,
        ).pack(side="right")
    def _on_path_mode_change(self):
        self._update_mode_desc()
        self._update_once_stop_visibility()
    def _update_once_stop_visibility(self):
        if self.ac.path_mode.get() == "Once":
            self._once_stop_frame.pack(anchor="w", pady=(3, 0))
        else:
            self._once_stop_frame.pack_forget()
    def _set_once_stop_mode(self, mode):
        self.ac.once_stop_mode.set(mode)
        for mode_val, btn in self._once_stop_btns.items():
            if mode_val == mode:
                btn.config(bg=self.ACCENT, fg=self._ink(self.ACCENT))
            else:
                btn.config(bg=self.BORDER, fg=self.FG2)
    def _update_mode_desc(self):
        self._mode_desc_lbl.config(
            text=self._PATH_MODE_DESC.get(self.ac.path_mode.get(), ""))
    def _toggle_path_mode(self):
        new = not self.ac.path_enabled.get()
        self.ac.path_enabled.set(new)
        self._path_enable_btn.config(
            text="\u25cf  Path Mode: ON"  if new else "\u25cb  Path Mode: OFF",
            bg=self.GREEN if new else self.BORDER,
            fg=self._ink(self.GREEN) if new else self.FG2,
        )
    def _rebuild_wp_list(self):
        for row_frame, *_ in self._wp_rows:
            row_frame.destroy()
        self._wp_rows.clear()
        for i, wp in enumerate(self.ac.path_waypoints):
            self._create_wp_row(i, wp)
        n = len(self.ac.path_waypoints)
        self._wp_count_lbl.config(
            text=f"{n} waypoint{'s' if n != 1 else ''}")
    def _create_wp_row(self, idx, wp):
        x_var   = tk.IntVar(value=wp["x"])
        y_var   = tk.IntVar(value=wp["y"])
        dly_var = tk.IntVar(value=wp.get("delay", 0))
        row_bg  = self.PANEL if idx % 2 == 0 else self.BG
        row = tk.Frame(self._wp_list_frame, bg=row_bg,
                       highlightthickness=1,
                       highlightbackground=self.BORDER)
        row.pack(fill="x", padx=2, pady=1)
        tk.Label(row, text=str(idx + 1), bg=row_bg, fg=self.FG2,
                 font=("Segoe UI", 8, "bold"),
                 width=2, anchor="center").pack(side="left", padx=(4, 2))
        for lbl, var, key in [("X", x_var, "x"), ("Y", y_var, "y")]:
            tk.Label(row, text=lbl, bg=row_bg, fg=self.FG2,
                     font=("Segoe UI", 8)).pack(side="left")
            sb = self._mk_sb(row, var, 0, 9999, 1, width=5)
            sb.pack(side="left", padx=(2, 4))
            var.trace_add("write",
                lambda *a, i=idx, v=var, k=key: self._update_wp(i, k, v))
        tk.Label(row, text="D", bg=row_bg, fg=self.FG2,
                 font=("Segoe UI", 8)).pack(side="left")
        dly_sb = self._mk_sb(row, dly_var, 0, 60000, 10, width=6)
        dly_sb.pack(side="left", padx=(2, 4))
        dly_var.trace_add("write",
            lambda *a, i=idx, v=dly_var: self._update_wp(i, "delay", v))
        for text, cmd, bg in [
            ("\U0001f4cd", lambda i=idx: self._capture_wp(i),   self.BORDER),
            ("\u2191",     lambda i=idx: self._move_wp(i, -1),  self.BORDER),
            ("\u2193",     lambda i=idx: self._move_wp(i,  1),  self.BORDER),
            ("\u2715",     lambda i=idx: self._remove_wp(i),    self.RED),
        ]:
            tk.Button(
                row, text=text, command=cmd, bg=bg,
                fg=self._ink(self.RED) if bg == self.RED else self.FG,
                relief="flat", cursor="hand2",
                font=("Segoe UI", 8),
                activebackground=self.INPUT_B, bd=0, padx=4,
            ).pack(side="left", padx=1)
        self._wp_rows.append((row, x_var, y_var, dly_var))
    def _update_wp(self, idx, key, var):
        if idx < len(self.ac.path_waypoints):
            try:
                self.ac.path_waypoints[idx][key] = var.get()
            except Exception:
                pass
    def _add_waypoint(self, x=960, y=540):
        self.ac.path_waypoints.append({"x": x, "y": y, "delay": 0})
        self._rebuild_wp_list()
    def _add_wp_at_mouse(self):
        def _tick(n):
            if n > 0:
                self._wp_count_lbl.config(text=f"Capturing in {n}s\u2026")
                self.after(1000, lambda: _tick(n - 1))
            else:
                x, y = pyautogui.position()
                self._add_waypoint(x, y)
        _tick(3)
    def _capture_wp(self, idx):
        def _tick(n):
            if n > 0:
                self._wp_count_lbl.config(
                    text=f"Capturing #{idx + 1} in {n}s\u2026")
                self.after(1000, lambda: _tick(n - 1))
            else:
                x, y = pyautogui.position()
                if idx < len(self.ac.path_waypoints):
                    self.ac.path_waypoints[idx].update({"x": x, "y": y})
                self._rebuild_wp_list()
        _tick(2)
    def _remove_wp(self, idx):
        if idx < len(self.ac.path_waypoints):
            self.ac.path_waypoints.pop(idx)
            self._rebuild_wp_list()
    def _move_wp(self, idx, direction):
        wps = self.ac.path_waypoints
        new = idx + direction
        if 0 <= new < len(wps):
            wps[idx], wps[new] = wps[new], wps[idx]
            self._rebuild_wp_list()
    def _clear_waypoints(self):
        self.ac.path_waypoints.clear()
        self._rebuild_wp_list()

    def _on_once_done(self):
        stop_mode = self.ac.once_stop_mode.get()
        if stop_mode in ("Trigger", "Both"):
            if self._trigger_armed:
                self._disarm_trigger()

    def _collect_profile(self):
        d = self.ac.to_dict()
        d["trigger_type"]        = self._trig_type.get()
        d["trigger_px_x"]        = self._trig_px_x.get()
        d["trigger_px_y"]        = self._trig_px_y.get()
        d["trigger_color"]       = list(self._trig_color)
        d["trigger_tolerance"]   = self._trig_tolerance.get()
        d["trigger_condition"]   = self._trig_condition.get()
        d["hotkey_arms_trigger"] = self._hotkey_arms_trigger.get()
        return d
    def _apply_profile(self, d):
        self.ac.from_dict(d)
        self._trig_type.set(d.get("trigger_type", "Off"))
        self._trig_px_x.set(d.get("trigger_px_x", 960))
        self._trig_px_y.set(d.get("trigger_px_y", 540))
        tc = d.get("trigger_color", [255, 255, 255])
        self._set_trig_color(int(tc[0]), int(tc[1]), int(tc[2]))
        self._trig_tolerance.set(d.get("trigger_tolerance", 15))
        self._trig_condition.set(d.get("trigger_condition", "Matches"))
        self._hotkey_arms_trigger.set(d.get("hotkey_arms_trigger", True))
        self.ac.apply_hotkey(self.ac.toggle_key_str.get())
        self._sync_ui_after_load()
    def _load_settings(self):
        self._settings = {}
        try:
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, encoding="utf-8") as f:
                    self._settings = json.load(f)
        except Exception:
            self._settings = {}
    def _save_settings(self):
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(self._settings, f, indent=2)
        except Exception:
            pass
    def _remember_last(self, name):
        self._settings["last_profile"] = name
        self._save_settings()
    def _restore_last_profile(self):
        name = self._settings.get("last_profile")
        if not name or name not in self._profiles:
            if "Default" in self._profiles:
                name = "Default"
            elif self._profiles:
                name = next(iter(self._profiles))
            else:
                return
        self._current_profile.set(name)
        self._apply_profile(self._profiles[name])
    def _load_profiles_file(self):
        loaded = None
        try:
            if os.path.exists(PROFILES_FILE):
                with open(PROFILES_FILE, encoding="utf-8") as f:
                    loaded = json.load(f)
        except Exception:
            loaded = None
        if loaded:
            self._profiles = loaded
        else:
            self._profiles = {k: dict(v) for k, v in BUNDLED_PROFILES.items()}
            self._save_profiles_file()
    def _save_profiles_file(self):
        try:
            with open(PROFILES_FILE, "w", encoding="utf-8") as f:
                json.dump(self._profiles, f, indent=2)
        except Exception as err:
            messagebox.showerror(
                "Profile Save Error",
                f"Could not save profiles:\n{err}\n\nPath: {PROFILES_FILE}",
            )
    def _refresh_profile_list(self):
        names = list(self._profiles.keys())
        self._profile_cb["values"] = names
        if names and not self._current_profile.get():
            self._current_profile.set(names[0])
    def _save_current_profile(self):
        name = self._current_profile.get().strip()
        if not name:
            messagebox.showwarning("Profile", "No profile selected.")
            return
        self._profiles[name] = self._collect_profile()
        self._save_profiles_file()
        self._refresh_profile_list()
        self._current_profile.set(name)
        self._remember_last(name)
        messagebox.showinfo("Profile", f"\u2714  Saved: {name}")
    def _new_profile(self):
        dlg = tk.Toplevel(self)
        dlg.title("New Profile")
        dlg.configure(bg=self.BG)
        dlg.resizable(False, False)
        dlg.grab_set()
        tk.Label(dlg, text="Profile name:", bg=self.BG, fg=self.FG,
                 font=self.FONT).pack(padx=16, pady=(14, 2), anchor="w")
        name_var = tk.StringVar()
        entry = self._mk_entry(dlg, name_var, width=22)
        entry.pack(padx=16, pady=(0, 12))
        entry.focus_set()
        def _ok(*_):
            name = name_var.get().strip()
            if not name:
                return
            self._profiles[name] = self._collect_profile()
            self._save_profiles_file()
            self._refresh_profile_list()
            self._current_profile.set(name)
            self._remember_last(name)
            dlg.destroy()
        entry.bind("<Return>", _ok)
        bf = tk.Frame(dlg, bg=self.BG)
        bf.pack(pady=(0, 14))
        for text, cmd, bg in [("Create", _ok,          self.ACCENT),
                               ("Cancel", dlg.destroy,  self.BORDER)]:
            tk.Button(
                bf, text=text, command=cmd, bg=bg, fg=self._ink(bg),
                relief="flat",
                font=self.FONT_B if bg == self.ACCENT else self.FONT,
                bd=0, padx=14, pady=4,
            ).pack(side="left", padx=4)
    def _load_selected_profile(self):
        name = self._current_profile.get()
        if name not in self._profiles:
            return
        self._apply_profile(self._profiles[name])
        self._remember_last(name)
    def _delete_profile(self):
        name = self._current_profile.get()
        if name not in self._profiles:
            return
        if not messagebox.askyesno("Delete Profile", f"Delete \"{name}\"?"):
            return
        del self._profiles[name]
        self._save_profiles_file()
        self._refresh_profile_list()
        names = list(self._profiles.keys())
        if names:
            self._current_profile.set(names[0])
            self._apply_profile(self._profiles[names[0]])
            self._remember_last(names[0])
        else:
            self._current_profile.set("")
    def _sync_ui_after_load(self):
        saved_mode = self.ac.speed_mode.get() or "CPS"
        self.ac.speed_mode.set("")
        self._set_speed_mode(saved_mode, convert=False)
        on = self.ac.path_enabled.get()
        self._path_enable_btn.config(
            text="\u25cf  Path Mode: ON"  if on else "\u25cb  Path Mode: OFF",
            bg=self.GREEN if on else self.BORDER,
            fg=self._ink(self.GREEN) if on else self.FG2,
        )
        self._update_mode_desc()
        self._update_once_stop_visibility()
        self._set_once_stop_mode(self.ac.once_stop_mode.get())
        self._rebuild_wp_list()
        self._on_trig_type_change()
        self._update_hk_mode_btn()

    def _build_terminal(self, parent):
        self._term_line_count = 0
        wrap = tk.Frame(parent, bg=self.BORDER,
                        highlightthickness=1,
                        highlightbackground=self.BORDER)
        wrap.pack(fill="both", expand=True, padx=6, pady=(5, 0))
        self._term = tk.Text(
            wrap, bg=self.CONSOLE, fg=self.CONSOLE_FG, font=self.MONO,
            relief="flat", state="disabled", wrap="none",
            height=16, width=51,
            selectbackground=self.ACCENT, cursor="arrow",
        )
        sb = tk.Scrollbar(wrap, command=self._term.yview,
                          bg=self.PANEL, troughcolor=self.BG,
                          relief="flat")
        sb.pack(side="right", fill="y")
        self._term.pack(side="left", fill="both", expand=True)
        self._term.config(yscrollcommand=sb.set)
        self._term.tag_config("ts",    foreground=self.ACCENT)
        self._term.tag_config("click", foreground=self.GREEN,
                              font=("Consolas", 8, "bold"))
        self._term.tag_config("mouse", foreground=self.CYAN,
                              font=("Consolas", 8, "bold"))
        self._term.tag_config("key",   foreground=self.YELLOW,
                              font=("Consolas", 8, "bold"))
        self._term.tag_config("start", foreground=self.GREEN,
                              font=("Consolas", 8, "bold"))
        self._term.tag_config("stop",  foreground=self.RED,
                              font=("Consolas", 8, "bold"))
        self._term.tag_config("sep",   foreground=self._mix(self.CONSOLE_FG, self.CONSOLE, 0.7))
        self._term.tag_config("muted", foreground=self._mix(self.CONSOLE_FG, self.CONSOLE, 0.55))
        self._term.tag_config("dim",   foreground=self._mix(self.CONSOLE_FG, self.CONSOLE, 0.3))
        self._term.tag_config("val",   foreground=self.CONSOLE_FG)
        self._term.tag_config("hold",  foreground=self.ORANGE)
        self._term.tag_config("dt",    foreground=self._mix(self.ACCENT, self.CONSOLE_FG, 0.35))
        self._term.tag_config("trig",  foreground=self.ACCENT,
                              font=("Consolas", 8, "bold"))
        bot = tk.Frame(parent, bg=self.BG)
        bot.pack(fill="x", padx=6, pady=(3, 6))
        tk.Label(bot, text="CPS", bg=self.BG, fg=self.FG2,
                 font=("Segoe UI", 7, "bold")).pack(side="left")
        self._cps_live_lbl = tk.Label(bot, text="0.0", bg=self.BG,
                                      fg=self.GREEN, width=7, anchor="w",
                                      font=("Consolas", 9, "bold"))
        self._cps_live_lbl.pack(side="left", padx=(4, 10))
        tk.Label(bot, text="\u00b7 500 line cap",
                 bg=self.BG, fg=self._faint(),
                 font=("Segoe UI", 7)).pack(side="left")
        tk.Button(
            bot, text="Clear", command=self._term_clear,
            bg=self.BORDER, fg=self.FG2, relief="flat", cursor="hand2",
            font=("Segoe UI", 8),
            activebackground=self.INPUT_B, activeforeground=self.FG,
            bd=0, padx=10, pady=2,
        ).pack(side="right")
        self._term_append([
            ("\u2501" * 44 + "\n", "sep"),
            ("  THEENAR  \u00b7  TERMINAL LOG\n", "dim"),
            ("\u2501" * 44 + "\n", "sep"),
            ("  ", "muted"), ("CLICK", "click"), (" synthetic   ", "muted"),
            ("MOUSE", "mouse"), (" physical   ", "muted"),
            ("KEY", "key"), ("\n", "muted"),
            ("  h:=held ms   \u0394=time since last same-type event\n", "muted"),
            ("\u2500" * 44 + "\n", "sep"),
        ])
    def _term_append(self, segments):
        def _do():
            self._term.config(state="normal")
            new_lines = sum(t.count("\n") for t, _ in segments)
            self._term_line_count += new_lines
            if self._term_line_count > 500:
                excess = self._term_line_count - 500
                self._term.delete("1.0", f"{excess + 1}.0")
                self._term_line_count = 500
            for text, tag in segments:
                self._term.insert("end", text, tag)
            self._term.config(state="disabled")
            self._term.see("end")
        self.after(0, _do)
    def _term_clear(self):
        self._term.config(state="normal")
        self._term.delete("1.0", "end")
        self._term.config(state="disabled")
        self._term_line_count = 0
        self._term_append([("  Log cleared.\n", "muted")])
    def _log_note(self, msg):
        ts = datetime.now().strftime("%H:%M:%S.%f")[:-4]
        self._term_append([(f" {ts} ", "ts"), ("NOTE ", "trig"),
                           (f" {msg}\n", "dim")])
    def _log_click(self, ev):
        ts   = datetime.fromtimestamp(ev["time"]).strftime("%H:%M:%S.%f")[:-4]
        btn  = ev["button"][0]
        ctyp = {"Single": "\u00b71", "Double": "\u00b72",
                "Hold":   "\u00b7H"}.get(ev["ctype"], "\u00b7?")
        dt   = fmt_dt(ev["delta"])
        segs = [(f" {ts} ", "ts"), ("CLICK", "click"),
                (f" {btn}{ctyp} {ev['x']},{ev['y']}", "val")]
        if ev["hold_ms"] > 0:
            segs += [(" h:", "dim"), (f"{ev['hold_ms']}ms", "hold")]
        if dt:
            segs += [(" ", "dim"), (dt, "dt")]
        segs += [(" ", "dim"), (f"#{ev['total']}\n", "muted")]
        self._term_append(segs)
    def _log_mouse(self, ev):
        ts  = datetime.fromtimestamp(ev["time"]).strftime("%H:%M:%S.%f")[:-4]
        dt  = fmt_dt(ev["delta"])
        segs = [(f" {ts} ", "ts"), ("MOUSE", "mouse"),
                (f" {ev['button']} {ev['x']},{ev['y']}", "val"),
                (" h:", "dim"), (f"{ev['hold_ms']}ms", "hold")]
        if dt:
            segs += [(" ", "dim"), (dt, "dt")]
        segs += [("\n", "dim")]
        self._term_append(segs)
    def _log_key(self, ev):
        ts  = datetime.fromtimestamp(ev["time"]).strftime("%H:%M:%S.%f")[:-4]
        key = ev["key"][:10]
        dt  = fmt_dt(ev.get("delta"))
        segs = [(f" {ts} ", "ts"), ("KEY  ", "key"),
                (f" {key:<10}", "val"),
                (" h:", "dim"), (f"{ev['hold_ms']}ms", "hold")]
        if dt:
            segs += [(" ", "dim"), (dt, "dt")]
        if ev["is_toggle"]:
            if self._trigger_armed:
                state = "\u2192 DISARMED"
                col   = "trig"
            elif (self._trig_type.get() != "Off"
                  and self._hotkey_arms_trigger.get()
                  and not self.ac.clicking):
                state = "\u2192 ARMED"
                col   = "trig"
            elif self.ac.clicking:
                state = "\u2192 ACTIVE"
                col   = "start"
            else:
                state = "\u2192  IDLE"
                col   = "stop"
            segs += [("  ", "dim"), (state + "\n", col)]
        else:
            segs += [("\n", "dim")]
        self._term_append(segs)
    def _log_status(self, active):
        ts = datetime.now().strftime("%H:%M:%S.%f")[:-4]
        if active:
            segs = [("\u2500" * 44 + "\n", "sep"),
                    (f" {ts} ", "ts"), ("\u25b6 STARTED\n", "start")]
        else:
            segs = [(f" {ts} ", "ts"), ("\u25a0 STOPPED\n", "stop"),
                    ("\u2500" * 44 + "\n", "sep")]
        self._term_append(segs)

    def _toggle_pin(self):
        self._pinned = not self._pinned
        self.wm_attributes("-topmost", self._pinned)
        self._pin_btn.config(
            bg=self.ACCENT if self._pinned else self.PANEL,
            fg=self._ink(self.ACCENT) if self._pinned else self.FG2,
            text="\U0001f4cc Pinned" if self._pinned else "\U0001f4cc Pin",
        )
    def _set_speed_mode(self, mode, convert=True):
        prev = self.ac.speed_mode.get()
        if prev == mode:
            return
        if convert and prev in ("CPS", "ms"):
            if mode == "ms":
                cps = self.ac.cps_val.get()
                self.ac.ms_val.set(max(1, int(round(1000.0 / max(cps, 0.01)))))
            else:
                ms = self.ac.ms_val.get()
                self.ac.cps_val.set(round(1000.0 / max(ms, 1), 2))
        if mode == "ms":
            self._cps_sb.pack_forget()
            self._ms_sb.pack(side="left", padx=(0, 3))
            self._speed_unit.config(text="ms per click")
            self._cps_btn.config(bg=self.BORDER, fg=self.FG2)
            self._ms_btn.config(bg=self.ACCENT, fg=self._ink(self.ACCENT))
        else:
            self._ms_sb.pack_forget()
            self._cps_sb.pack(side="left", padx=(0, 3))
            self._speed_unit.config(text="clicks/sec")
            self._ms_btn.config(bg=self.BORDER, fg=self.FG2)
            self._cps_btn.config(bg=self.ACCENT, fg=self._ink(self.ACCENT))
        self.ac.speed_mode.set(mode)
    def _start_capture(self):
        if self._capture_countdown > 0:
            return
        self._capture_countdown = 3
        self._capture_tick()
    def _capture_tick(self):
        n = self._capture_countdown
        if n > 0:
            self.cap_btn.config(
                text=f"\U0001f4cd {n}s\u2026",
                bg=self.YELLOW, fg=self._ink(self.YELLOW))
            self._capture_countdown -= 1
            self.after(1000, self._capture_tick)
        else:
            x, y = pyautogui.position()
            self.ac.fixed_x.set(x)
            self.ac.fixed_y.set(y)
            self.ac.pos_mode.set("Fixed")
            self._capture_countdown = 0
            self.cap_btn.config(
                text=f"\u2713 {x},{y}", bg=self.GREEN, fg=self._ink(self.GREEN))
            self.after(2200, lambda: self.cap_btn.config(
                text="\U0001f4cd Cap 3s", bg=self.BORDER, fg=self.FG))
    def _apply_hotkey(self):
        key_str = self.ac.toggle_key_str.get()
        if self.ac.apply_hotkey(key_str):
            self.ac.stop_kb_listener()
            self.ac.start_kb_listener(self._hotkey_toggle)
            if self.ac._toggle_key is None:
                messagebox.showinfo(
                    "Hotkey", "No toggle hotkey set (field is empty).")
            else:
                messagebox.showinfo("Hotkey Updated", f"Toggle key: {key_str}")
        else:
            messagebox.showerror(
                "Invalid Key",
                f"\"{key_str}\" not recognised.\n"
                "Examples: F6, F1, x, -, esc, space  (leave empty to disable)",
            )

    def _release_entry_focus(self, event):
        w = event.widget
        if isinstance(w, (tk.Entry, tk.Spinbox)):
            return
        try:
            cls = w.winfo_class()
        except Exception:
            cls = ""
        if cls in ("TCombobox", "Listbox", "ComboboxPopdownFrame",
                   "Entry", "Spinbox", "Text", "Treeview"):
            return
        cur = self.focus_get()
        if isinstance(cur, (tk.Entry, tk.Spinbox)):
            self.focus_set()

    def _start(self):
        if self.ac.clicking:
            return
        delay = self._start_delay.get()
        if delay > 0:
            if self._start_pending_id is not None:
                return
            self._run_start_countdown(delay)
        else:
            self.ac.start()
    def _run_start_countdown(self, n):
        self._start_countdown_n = n
        if n > 0:
            self._start_btn.config(
                text=f"\u25b6  Starting in {n}s\u2026",
                bg=self._shade(self.GREEN, 0.6))
            self._start_pending_id = self.after(
                1000, lambda: self._run_start_countdown(n - 1))
        else:
            self._start_pending_id  = None
            self._start_countdown_n = 0
            self._start_btn.config(text="\u25b6  START", bg=self.GREEN)
            self.ac.start()
    def _cancel_pending_start(self):
        if self._start_pending_id:
            self.after_cancel(self._start_pending_id)
            self._start_pending_id = None
        self._start_countdown_n = 0
        self._start_btn.config(text="\u25b6  START", bg=self.GREEN)
    def _stop(self):
        self._cancel_pending_start()
        self.ac.stop()
    def _reset_counter(self):
        self.ac.total_clicks = 0
    def _hotkey_toggle(self):
        def _check():
            if self._trigger_armed:
                self._disarm_trigger()
                return
            if self._start_countdown_n > 0:
                self._cancel_pending_start()
                return
            if self.ac.clicking:
                self._stop()
            else:
                if (self._trig_type.get() != "Off"
                        and self._hotkey_arms_trigger.get()):
                    self._arm_trigger()
                else:
                    self._start()
        self.after(0, _check)
    def _cps_tick(self):
        now = time.perf_counter()
        try:
            times = list(self.ac._click_times)
        except RuntimeError:
            self.after(100, self._cps_tick)
            return
        recent = [t for t in times if now - t <= 1.0]
        cps = 0.0
        if len(recent) >= 2:
            span = recent[-1] - recent[0]
            if span > 0:
                cps = (len(recent) - 1) / span
        self._cps_live_lbl.config(text=f"{cps:,.1f}")
        self.after(100, self._cps_tick)
    def _update_loop(self):
        active = self.ac.clicking
        col    = self.GREEN if active else self.RED
        txt    = "ACTIVE" if active else "IDLE"
        if self._trigger_armed and not active:
            col = self.ACCENT
            txt = "ARMED"
        self.status_dot.config(fg=col)
        self.status_lbl.config(text=txt, fg=col)
        self.clicks_lbl.config(text=f"{self.ac.total_clicks:,}")
        self._tb_dot.config(fg=col)
        self._tb_lbl.config(text=txt, fg=col)
        self.after(120, self._update_loop)
    def _on_close(self):
        self.ac.stop()
        self.ac.stop_kb_listener()
        self.ac.stop_mouse_listener()
        self._trigger_armed = False
        try:
            self._docs_save_file()
        except Exception:
            pass
        if self._current_profile.get():
            self._remember_last(self._current_profile.get())
        if self._current_theme.get():
            self._remember_theme(self._current_theme.get())
        self.destroy()
if __name__ == "__main__":
    app = App()
    app.mainloop()