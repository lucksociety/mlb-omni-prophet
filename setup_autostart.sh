#!/bin/bash

# Configuration
LABEL="com.antigravity.orchestrator"
SCRIPT_PATH="/Users/danielreiss/Desktop/Antigravity/MLB/orchestrator.py"
PYTHON_PATH=$(which python3)
WORKING_DIR="/Users/danielreiss/Desktop/Antigravity/MLB"
PLIST_PATH="$HOME/Library/LaunchAgents/$LABEL.plist"

echo "Setting up autostart for Orchestrator..."

# Create the plist file
cat <<EOF > "$PLIST_PATH"
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>$LABEL</string>
    <key>ProgramArguments</key>
    <array>
        <string>$PYTHON_PATH</string>
        <string>$SCRIPT_PATH</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>$WORKING_DIR</string>
    <key>StandardOutPath</key>
    <string>$WORKING_DIR/logs/launchd_stdout.log</string>
    <key>StandardErrorPath</key>
    <string>$WORKING_DIR/logs/launchd_stderr.log</string>
</dict>
</plist>
EOF

# Load the agent
launchctl unload "$PLIST_PATH" 2>/dev/null
launchctl load "$PLIST_PATH"

echo "Orchestrator has been registered and started via launchd."
echo "You can check status with: launchctl list | grep $LABEL"
echo "Logs are located in: $WORKING_DIR/logs/"
