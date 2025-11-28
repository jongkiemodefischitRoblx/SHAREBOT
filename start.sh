#!/data/data/com.termux/files/usr/bin/bash

# Jalankan bot di background, simpan log
nohup python bot.py > bot.log 2>&1 &
echo "SHAREBOT started! Logs are in bot.log"
