# 🎣 Ultimate Camp Tycoon Fishing Bot

**A robust, external auto-fishing bot designed specifically for Ultimate Camp Tycoon on Roblox.**

![Python](https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS-lightgrey?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Working-brightgreen?style=for-the-badge)

## 📖 Features

* **🖥️ Cross-Platform Auto-Detect:** Automatically detects if you are on **Windows** or **macOS** and adjusts the target colors accordingly:
    * *Windows Target:* Green `(0, 179, 0)`
    * *Mac Target:* Green `(80, 176, 51)`
* **🧠 Smart UI Refresh (Stuck Prevention):**
    * If the game stops registering the button hover (common bug in Roblox), the bot automatically moves the mouse away and back to "wake up" the button.
* **💤 Anti-Idle System:**
    * Micro-movements prevent your computer from sleeping or the game from kicking you for inactivity.
* **⚡ Fast Reeling:**
    * Uses burst clicking to reel in fish instantly.

---

## 💎 Support & Donate

If this script help you save time or progress faster, consider supporting the project! Your contributions keep the updates coming.

<div align="center">

| **Platform** | **Link / Address** |
| :--- | :--- |
| <img src="https://ko-fi.com/img/githubbutton_sm.svg" height="25"> | [**ko-fi.com/kszabi1**](https://ko-fi.com/kszabi1) |
| <img src="https://assets.streamlinehq.com/image/private/w_300,h_300,ar_1/f_auto/v1/icons/logos/revolut-7xg5qi3x0rl0zrcr2o59a6.png/revolut-bn5ndnkw98s301h6dhk6wf.png?_a=DATAg1AAZAA0" height="20"> **Revolut** | [**@undrgng**](https://revolut.me/undrgng) |
| <img src="https://cryptologos.cc/logos/bitcoin-btc-logo.png" height="20"> **Bitcoin (BTC)** | `13JDDqEENnJTmnFvk1UprztdQSrnHzzuxG` |
| <img src="https://cryptologos.cc/logos/ethereum-eth-logo.png" height="20"> **Ethereum (ETH)** | `0xc69ee4baa9fc0e243581ba8bb296419e4302cbde` |
| <img src="https://cryptologos.cc/logos/litecoin-ltc-logo.png" height="20"> **Litecoin (LTC)** | `LdRC52bfnBeabj29YbUdukZdWDN57t4ZwA` |

</div>

---

## ⚙️ Installation

1.  Make sure you have **Python 3.x** installed.
2.  Download `ultimate_camp_tycoon_fishing_bot.py` to your computer.

---

## 🎮 How to Use

1.  Open [**Ultimate Camp Tycoon**](https://www.roblox.com/games/10412238489/Ultimate-Camp-Tycoon-RE-CAMPED) in Roblox.
2.  Go to the **Fishing Position** and start the mini game.
3.  Run the script in your terminal/command prompt:
    ```bash
    python ultimate_camp_fishing.py
    ```
4.  **Hover your mouse cursor** directly over the "Cast" / "Reel" button.
    * ⚠️ **Important:** Do not place the mouse on the fishing rod icon! Place it on the **solid color** (Blue) part of the button.
5.  Press **`s`** on your keyboard to **START**.
    * *The bot will save the color under your mouse and begin automation.*
6.  Press **`q`** to **QUIT** the script.

---

## 🔧 Troubleshooting

### "The bot sees BLACK (0,0,0) or WHITE (255,255,255)"
This means the bot cannot see the game screen due to permission or display mode issues.

* **Windows:**
    * Try running the game in **Windowed Mode** (not Fullscreen).
    * Make sure your display scaling is set to 100% if possible (though the bot tries to handle this).
* **macOS:**
    * You must grant **Screen Recording** permissions to your Terminal (iTerm2, Terminal, or VS Code).
    * Go to: `System Settings` -> `Privacy & Security` -> `Screen Recording` -> Enable for your terminal.

### "The mouse moves away randomly?"
**This is a feature, not a bug.**
If the bot doesn't see the "Cast" button for more than 3 seconds (or after a catch), it deliberately moves the mouse down and back. This forces the game to update the button's "Hover" color, which often gets stuck during long AFK sessions.

---

## 🚀 100% AFK & Background Mode (Advanced)

If you want the bot to run without occupying your mouse on your main screen, or if you want to run it 24/7 on a server, use these methods.

### 🏠 Option 1: Your Own PC - Run in Background (RDP Trick)
This method allows the bot to run inside a "separate window" on your own computer. The bot clicks inside that window while you can do other work on your main desktop.

**1. Enable Remote Desktop:**
* Go to `Settings` -> `System` -> `Remote Desktop` -> **Turn On**.

**2. Connect:**
* Press `Win + R`, type: `mstsc` and hit Enter.
* Computer: `127.0.0.1` (this is your own local IP).
* Username/Password: Your current Windows login details.

**3. Run:**
* Inside the Remote Desktop window, open Roblox and start the bot (`python ultimate_camp_fishing.py`).

**⚠️ IMPORTANT TRICK (Do not Minimize):**
Do **NOT** minimize the Remote Desktop window to the taskbar! If you minimize it, Windows stops rendering graphics, and the bot will stop seeing colors ("blind mode").

* **The Fix:** Instead of minimizing, resize the window to be smaller and move it aside, OR create a **New Virtual Desktop** (`Win + Tab` -> "New Desktop") and drag the RDP window there. You can then switch back to your main desktop while the bot works in the background.

---

### ☁️ Option 2: VPS / Cloud Server (24/7)
If you are using a Windows VPS (Virtual Private Server), you **cannot** simply close the Remote Desktop window with the "X". If you do, the server locks the screen (stops GUI), and the bot freezes.

**The Correct Way to Disconnect:**
1.  Create a new file on your VPS desktop named `keep_alive.bat`.
2.  Right-click -> Edit, and paste this code:
    ```bat
    for /f "skip=1 tokens=3" %%s in ('query user %USERNAME%') do (
      %windir%\System32\tscon.exe %%s /dest:console
    )
    ```
3.  When you want to leave, **Run this file as Administrator**.
4.  This will disconnect your session immediately, but the server screen will **remain active** in the cloud, allowing the bot to keep fishing forever.

---

## ⚠️ Disclaimer

**EDUCATIONAL USE ONLY.**
Use this script at your own risk. The author is not responsible for any game bans or account suspensions.
