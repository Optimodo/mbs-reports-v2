# PowerShell UTF-8 Encoding Setup Guide

## ✅ Test Results

Your UTF-8 encoding is now working correctly! All emojis, Unicode characters, and special symbols display properly in the console.

---

## How PowerShell Profile Works

### What is `$PROFILE`?

`$PROFILE` is a PowerShell script that runs **automatically** every time you start a new PowerShell session. Think of it like a `.bashrc` or `.zshrc` for PowerShell.

### Profile Location

When you edit `$PROFILE`, you're editing a file at:
```
C:\Users\<YourUsername>\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1
```

### Scope: All Projects, All Directories

**Yes!** The PowerShell profile is **user-level**, which means:

✅ **Works in ALL projects** - not just this one  
✅ **Works in ALL directories** - anywhere you open PowerShell  
✅ **Persists across sessions** - every new terminal window  
✅ **Automatic** - no need to manually set encoding each time  

### What You Added

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"
```

**Line 1**: Sets the console to use UTF-8 for all output  
**Line 2**: Tells Python to use UTF-8 for input/output encoding

---

## How It Works in Cursor/VS Code

### For Terminal Commands (like we use)

When I run commands using `run_terminal_cmd`, Cursor:
1. Opens a PowerShell session
2. PowerShell automatically loads your `$PROFILE`
3. The UTF-8 encoding is set
4. The command runs with proper encoding

**However**, I also set it manually with `chcp 65001` to ensure it's active, which is a good safety measure.

### For Integrated Terminals

If you open a terminal in Cursor/VS Code:
- **PowerShell terminals**: Will load `$PROFILE` automatically ✅
- **CMD terminals**: Won't load PowerShell profile (would need separate setup)
- **Git Bash/WSL**: Won't load PowerShell profile (different shell)

---

## Verification Commands

To check if your profile is loaded in any PowerShell session:

```powershell
# Check if profile exists
Test-Path $PROFILE

# View profile contents
Get-Content $PROFILE

# Check current encoding
[Console]::OutputEncoding

# Check Python encoding
$env:PYTHONIOENCODING
```

---

## Alternative: Windows Terminal

For the **best** experience, consider using **Windows Terminal** instead of PowerShell:

**Benefits**:
- Native UTF-8 support (no profile needed)
- Better rendering of emojis and special characters
- Tabs, panes, and modern features
- Free from Microsoft Store

With Windows Terminal, Unicode "just works" without any setup!

---

## Troubleshooting

### If encoding doesn't work in a new session:

1. **Check profile loaded**:
   ```powershell
   $PROFILE
   ```

2. **Manually load profile**:
   ```powershell
   . $PROFILE
   ```

3. **Check execution policy** (might block profile):
   ```powershell
   Get-ExecutionPolicy
   ```
   
   If it says "Restricted", change it:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

4. **Verify profile contents**:
   ```powershell
   notepad $PROFILE
   ```

---

## For Other Projects

**Good news**: You don't need to do anything!

Since the profile is user-level:
- ✅ Any new PowerShell window = encoding is set
- ✅ Any new project in Cursor = encoding is set
- ✅ Any directory you navigate to = encoding is set

The only exception is if you use a **different shell** (CMD, Git Bash, WSL), which would need their own setup.

---

## Summary

| Aspect | Status |
|--------|--------|
| Current encoding | ✅ Working (UTF-8) |
| Applies to all projects | ✅ Yes (user-level) |
| Persists across sessions | ✅ Yes (automatic) |
| Works in Cursor terminals | ✅ Yes (if PowerShell) |
| Works with emoji/Unicode | ✅ Fully supported |

---

## Test Script

Run `test_encoding.py` anytime to verify UTF-8 encoding is working:

```bash
python test_encoding.py
```

If you see all the emojis and special characters correctly, your encoding is properly configured!

---

**Your setup is now permanent and will work everywhere! 🚀**


