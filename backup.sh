#!/bin/bash

echo "Backup script for PI Tablet"

BACKUP_DIR=~/pi-tablet-backups
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup_$DATE.tar.gz"

echo "Creating backup directory at $BACKUP_DIR if it doesn't exist..."
mkdir -p "$BACKUP_DIR"

# Create archive
cd ~/pi-tablet
tar -czf "$BACKUP_FILE" pi_tablet.db config.txt 2>/dev/null

if [ $? -eq 0 ]; then
    echo "Backup created successfully at $BACKUP_FILE"
    echo "File: $BACKUP_FILE"

    # Size
    SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo "Size: $SIZE"

    # Delete backups older than 7 days
    find "$BACKUP_DIR" -type f -name "backup_*.tar.gz" -mtime +7 -delete

    echo "Old backups deleted."
    ls -lh "$BACKUP_FILE"/backup_*.tar.gz 2>/dev/null
else
    echo "Error creating backup."
fi

echo "To get old backup."
echo "tar -xzf $BACKUP_FILE -C ~/pi-tablet"