# ==============================================================================
#  ULTIMATE CAMP TYCOON FISHING BOT SOFTWARE LICENSE
#  Copyright (c) 2026 Szabolcs Koleszár (kszabi1). All Rights Reserved.
#
#  TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION:
#
#  1. GRANT OF LICENSE:
#     Subject to the terms of this License, the Author hereby grants you a
#     personal, non-exclusive, non-transferable license to use, modify, and
#     run this software for non-commercial, educational, and personal purposes.
#
#  2. RESTRICTIONS:
#     - COMMERCIAL USE PROHIBITED: You may not sell, rent, lease, or otherwise
#       monetize this software or any modified version of it.
#     - REDISTRIBUTION PROHIBITED: You may not re-upload, distribute, or
#       host this source code on public repositories, forums, or marketplaces
#       without the express written permission of the Copyright Holder.
#
#  3. DISCLAIMER OF WARRANTY:
#     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#     IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#     FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#
#  4. EDUCATIONAL USE & LIABILITY DISCLAIMER:
#     THIS SOFTWARE IS INTENDED SOLELY FOR EDUCATIONAL PURPOSES. The Author
#     is NOT responsible for any consequences resulting from use.
#     
#     USE THIS SOFTWARE AT YOUR OWN RISK.
# ==============================================================================

import sys
import subprocess
import os
import platform
import time
import ctypes 

try:
    import pyautogui
    from pynput import keyboard
except ImportError:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyautogui", "pynput"])
        time.sleep(1)
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception:
        sys.exit(1)

# ==========================================
#           USER CONFIGURATION
# ==========================================

# --- 1. SENSITIVITY ---
TOLERANCE = 25       

# --- 2. SPEED ---
BURST_CLICKS = 30

# --- 3. ANTI-IDLE ---
JIGGLE_INTERVAL = 5.0


# ==========================================
#           SYSTEM CODE (AUTO-DETECT)
# ==========================================

SCREEN_SCALE = 1

COLOR_CAST_BLUE   = (0, 0, 172) 
COLOR_CAUGHT_BLUE = (133, 223, 251)  

IS_WINDOWS = platform.system() == "Windows"
IS_MAC = platform.system() == "Darwin"

if IS_WINDOWS:
    COLOR_HOOK_GREEN = (0, 179, 0)    # Windows Green
else:
    COLOR_HOOK_GREEN = (80, 176, 51)  # Mac Green

STATE_IDLE = 0
STATE_WAITING_CAST = 1
STATE_WAITING_BITE = 2  
STATE_REELING = 3     

pyautogui.PAUSE = 0    

current_state = STATE_IDLE
target_pos = None
running = True

def get_pixel_color(x, y):
    try:
        if IS_WINDOWS:
            dc = ctypes.windll.user32.GetDC(0)
            rgb_int = ctypes.windll.gdi32.GetPixel(dc, int(x), int(y))
            ctypes.windll.user32.ReleaseDC(0, dc)
            
            red = rgb_int & 255
            green = (rgb_int >> 8) & 255
            blue = (rgb_int >> 16) & 255
            return (red, green, blue)
            
        else:
            real_x = int(x * SCREEN_SCALE)
            real_y = int(y * SCREEN_SCALE)
            
            sw, sh = pyautogui.size()
            if real_x >= sw * SCREEN_SCALE or real_y >= sh * SCREEN_SCALE:
                real_x = int(x)
                real_y = int(y)

            pic = pyautogui.screenshot(region=(real_x, real_y, 1, 1))
            color = pic.getpixel((0, 0))
            if len(color) == 4: return (color[0], color[1], color[2])
            return color

    except Exception:
        return None

def colors_match(c1, c2, tolerance):
    if c1 is None or c2 is None: return False
    diff = abs(c1[0] - c2[0]) + abs(c1[1] - c2[1]) + abs(c1[2] - c2[2])
    return diff < (tolerance * 3)

def anti_idle_jiggle(start_pos):
    """Small wiggle to keep Mac awake."""
    x, y = start_pos
    pyautogui.moveTo(x + 5, y)
    time.sleep(0.05)
    pyautogui.moveTo(x, y)

def reset_mouse_after_catch(start_pos):
    """
    Refreshes the UI by moving the mouse away and back.
    This fixes the issue where the script stops seeing color after a few catches.
    """
    x, y = start_pos
    pyautogui.moveTo(x + 100, y + 200) 
    time.sleep(0.1) 
    pyautogui.moveTo(x, y)

def on_press(key):
    global running, current_state, target_pos
    try:
        if key.char == 's':
            if current_state == STATE_IDLE:
                pos = pyautogui.position()
                color = get_pixel_color(pos[0], pos[1])
                
                print(f"\n[OK] Position saved at: {pos}")
                print(f"[TEST] Bot sees color: {color}")
                print(f"[SYSTEM] Expecting Green: {COLOR_HOOK_GREEN}")
                
                if color == (0,0,0) or color == (31,31,31) or color == (255,255,255):
                    print("⚠️ WARNING: The bot sees BLACK or WHITE.")
                    if IS_WINDOWS:
                        print(" -> Try running the game in Windowed mode.")
                    if IS_MAC:
                        print(" -> Check Screen Recording permissions.")
                
                target_pos = pos
                current_state = STATE_WAITING_CAST
                print("\n--- BOT STARTED ---")
                print("Status: Waiting for Cast Button...")

        elif key.char == 'q':
            print("\nExiting...")
            running = False
            return False
            
    except AttributeError:
        pass

def main():
    global current_state
    
    os_name = platform.system()
    mode = "Fast API Mode" if IS_WINDOWS else "Mac Mode"
    
    print("========================================")
    print(f"   Ultimate Camp Tycoon Fishing Bot")
    print(f"      By: kszabi1")
    print(f"      System: {os_name} ({mode})")
    print("========================================")
    print(" INSTRUCTIONS:")
    print(" 1. Open Ultimate Camp Tycoon on Roblox.")
    print(" 2. Hover your mouse over the button (where the color is visible).")
    print(" 3. Press 's' to START.")
    print(" 4. Press 'q' to QUIT.")
    print("----------------------------------------")
    
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    last_cast_time = 0
    last_jiggle_time = time.time()
    last_seen_cast_button = time.time()

    while running:
        if current_state == STATE_IDLE or not target_pos:
            time.sleep(0.1)
            continue

        x, y = target_pos
        current_time = time.time()

        if current_state != STATE_REELING and (current_time - last_jiggle_time > JIGGLE_INTERVAL):
            anti_idle_jiggle((x, y))
            last_jiggle_time = current_time

        if current_state == STATE_REELING:
            current_color = get_pixel_color(x, y)
        
            if colors_match(current_color, COLOR_CAUGHT_BLUE, TOLERANCE):
                print("Fish Caught! Resetting...")
                reset_mouse_after_catch((x, y))
                current_state = STATE_WAITING_CAST
                last_seen_cast_button = time.time()
                continue

            if colors_match(current_color, COLOR_CAST_BLUE, TOLERANCE):
                current_state = STATE_WAITING_CAST
                continue

            for _ in range(BURST_CLICKS):
                pyautogui.click()

        else:
            current_color = get_pixel_color(x, y)
            if current_color is None: continue

            if current_state == STATE_WAITING_CAST:
                if colors_match(current_color, COLOR_CAST_BLUE, TOLERANCE):
                    last_seen_cast_button = time.time()
                    
                    if time.time() - last_cast_time > 1.0:
                        print("Casting Line!")
                        pyautogui.click()
                        last_cast_time = time.time()
                        time.sleep(1.0)
                        current_state = STATE_WAITING_BITE
                
                elif colors_match(current_color, COLOR_HOOK_GREEN, TOLERANCE):
                    current_state = STATE_REELING
                
                else:
                    if time.time() - last_seen_cast_button > 3.0:
                        print("⚠️ Not seeing button... refreshing mouse position.")
                        reset_mouse_after_catch((x, y))
                        last_seen_cast_button = time.time()

            elif current_state == STATE_WAITING_BITE:
                if colors_match(current_color, COLOR_HOOK_GREEN, TOLERANCE):
                    print("BITE! Reeling in...")
                    current_state = STATE_REELING
                
                elif colors_match(current_color, COLOR_CAST_BLUE, TOLERANCE):
                     if time.time() - last_cast_time > 2.0:
                        current_state = STATE_WAITING_CAST

            time.sleep(0.01)

if __name__ == "__main__":
    main()
