#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import psutil
import requests
import schedule

# 環境変数から Slack Webhook URL を取得
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
if not SLACK_WEBHOOK_URL:
    raise RuntimeError("環境変数 SLACK_WEBHOOK_URL が設定されていません")

def get_cpu_temperature():
    """
    /sys/class/thermal/thermal_zone0/temp から温度を取得（ミリ度→℃）
    """
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp_str = f.read().strip()
        return float(temp_str) / 1000.0
    except FileNotFoundError:
        return None

def get_memory_usage():
    """
    メモリ使用率を psutil で取得
    """
    vm = psutil.virtual_memory()
    used_gb = vm.used / (1024 ** 3)
    total_gb = vm.total / (1024 ** 3)
    return vm.percent, used_gb, total_gb

def get_disk_usage(path="/"):
    """
    ディスク使用率・空き容量を psutil で取得
    """
    du = psutil.disk_usage(path)
    free_gb = du.free / (1024 ** 3)
    total_gb = du.total / (1024 ** 3)
    return du.percent, free_gb, total_gb

def post_to_slack(message: str):
    """
    Slack にメッセージを POST
    """
    payload = {"text": message}
    resp = requests.post(SLACK_WEBHOOK_URL, json=payload)
    resp.raise_for_status()

def job():
    """定期実行ジョブ：システム情報を取得して Slack へ送信"""
    cpu_temp = get_cpu_temperature()
    mem_pct, mem_used, mem_total = get_memory_usage()
    disk_pct, disk_free, disk_total = get_disk_usage()

    lines = [
        "*Raspberry Pi System Report*",
        f"• CPU Temperature: {cpu_temp:.1f}℃" if cpu_temp is not None else "• CPU Temperature: Unknown",
        f"• Memory Usage: {mem_pct:.1f}% ({mem_used:.2f}/{mem_total:.2f} GB)",
        f"• Disk Free: {disk_free:.2f}/{disk_total:.2f} GB ({100-disk_pct:.1f}% free)"
    ]
    message = "\n".join(lines)
    post_to_slack(message)
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Report sent to Slack")

if __name__ == "__main__":
    # 実行間隔の設定（例：1時間ごと）
    schedule.every(1).hour.do(job)
    print("Starting system report scheduler...")

    # 最初のレポートを即時実行
    job()

    # スケジューラループ
    while True:
        schedule.run_pending()
        time.sleep(1)
