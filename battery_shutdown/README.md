# Battery Safe-Shutdown

**Problem**
Running a server on battery (laptop/UPS) risks data corruption during outages.

**What it does**
- Monitors battery percentage on a schedule
- Triggers a **safe shutdown** when below a threshold
- Supports **dry-run** mode for testing
- Works with `upower`, `acpi`, or `/sys` as fallback
- Systemd service + timer for hands-off operation

**Quick start**
1) Put the script somewhere executable (e.g. `/usr/local/bin/shutdown_on_low_battery.sh`)
2) Install the systemd units (below), then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now shutdown-on-low-battery.timer
