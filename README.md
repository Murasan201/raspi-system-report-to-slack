# RasPi System Report to Slack

> Python script for Raspberry Pi that periodically collects CPU temperature, memory usage, and disk space statistics, then sends formatted reports to Slack via Incoming Webhooks.

## Features

- Collect CPU temperature  
- Monitor memory usage (percentage and GB)  
- Check disk free space  
- Send formatted report to Slack channel via Incoming Webhook  
- Schedule periodic reports (default: every hour)  

## Prerequisites

- Raspberry Pi running Linux (Raspbian, etc.)  
- Python 3.6+  
- Slack Incoming Webhook URL  

## Installation

1. Clone the repository:  
   ```bash
   git clone https://github.com/<your-username>/raspi-system-report-to-slack.git
   cd raspi-system-report-to-slack
   ```  
2. Install dependencies:  
   ```bash
   pip3 install -r requirements.txt
   ```  

Alternatively, install individually:  
```bash
pip3 install psutil schedule requests
```

## Configuration

Set the Slack Incoming Webhook URL as an environment variable:  
```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/XXX/YYY/ZZZ"
```

## Usage

Run the script:  
```bash
chmod +x system_report.py
./system_report.py
```  
The script sends an initial report immediately and then every hour by default.

### Customize Schedule

Modify the scheduling section in `system_report.py` to adjust frequency:  
```python
# e.g., every 30 minutes
schedule.every(30).minutes.do(job)
# or daily at 09:00
schedule.every().day.at("09:00").do(job)
```

## (Optional) Setup as a systemd Service

Create a `raspi-system-report.service` file in `/etc/systemd/system/`:

```ini
[Unit]
Description=Raspberry Pi System Report to Slack
After=network.target

[Service]
ExecStart=/usr/bin/env python3 /home/pi/raspi-system-report-to-slack/system_report.py
Restart=always
User=pi
Environment=SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXX/YYY/ZZZ

[Install]
WantedBy=multi-user.target
```

Enable and start the service:  
```bash
sudo systemctl daemon-reload
sudo systemctl enable raspi-system-report
sudo systemctl start raspi-system-report
```

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## Author

- Murasan  
  https://murasan-net.com/

## License

This project is licensed under the MIT License.
