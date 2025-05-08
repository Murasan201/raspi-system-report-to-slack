# RasPi System Report to Slack

> Python script for Raspberry Pi that collects CPU temperature, memory usage, and disk free-space statistics, then sends a formatted report to Slack via an Incoming Webhook.

## Features

- Collect CPU temperature  
- Monitor memory usage (percentage and GB)  
- Check disk free space  
- Send formatted report to Slack channel via Incoming Webhook  

## Prerequisites

- Raspberry Pi running Linux (Raspbian, etc.)  
- Python 3.6+  
- Slack Incoming Webhook URL  

## Installation

1. Clone the repository:  
   ```bash
   git clone https://github.com/Murasan201/raspi-system-report-to-slack.git
   cd raspi-system-report-to-slack
   ```  
2. Install dependencies using the system package manager:  
   ```bash
   sudo apt-get update
   sudo apt-get install -y python3-psutil python3-requests
   ```  

   Or with pip in a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install psutil requests
   ```

## Configuration

Set your Slack Incoming Webhook URL as an environment variable:

```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/XXX/YYY/ZZZ"
```

## Usage

1. Make the script executable:

   ```bash
   chmod +x system_report.py
   ```

2. Run it manually for an immediate report:

   ```bash
   ./system_report.py
   ```

3. To schedule hourly execution via cron, edit the crontab for user **pi**:

   ```bash
   crontab -e
   ```

   Add this line:

   ```
   @hourly /home/pi/work/project/slack/raspi-system-report-to-slack/system_report.py
   ```

   The script will send one report immediately when invoked, so the cron job will produce exactly one report each hour.

## (Optional) Setup as a systemd Service

Create `/etc/systemd/system/raspi-system-report.service`:

```ini
[Unit]
Description=Raspberry Pi System Report to Slack
After=network.target

[Service]
ExecStart=/usr/bin/env bash -lc 'source /home/pi/work/project/slack/raspi-system-report-to-slack/venv/bin/activate && python3 /home/pi/work/project/slack/raspi-system-report-to-slack/system_report.py'
Restart=on-failure
User=pi
Environment=SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXX/YYY/ZZZ

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable raspi-system-report
sudo systemctl start raspi-system-report
```

## Contributing

Contributions welcome! Open issues or submit pull requests.

## License

MIT License
