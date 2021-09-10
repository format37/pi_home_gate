#### pi_home_gate
open/close door telegram report
### components:
rpi zero w   
camera   
Reed switch   
### Run on startup
```
sudo nano /etc/rc.local
```
Before exit:
```
python3 /home/pi/gate.py
```
