### pi_home_gate
Open / Close door telegram report
#### components:
- Raspberry pi zero w   
- Camera   
- Reed switch   
#### Run on startup
```
#crontab -e
@reboot  /home/pi/start.sh
```
#### Don't forget
to set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT environments in [start.sh](https://github.com/format37/pi_home_gate/blob/master/start.sh)
