# Plan: Implement Rotating Log Files for JavaMCP Server

## Overview
Add log rotation capability using Python's `RotatingFileHandler` to prevent log files from growing indefinitely when file logging is configured.

## Changes Required

### 1. Update LoggingConfig schema (`src/javamcp/config/schema.py`)
- [x] Add `max_bytes` field (default: 10MB) - maximum size before rotation
- [x] Add `backup_count` field (default: 5) - number of backup files to keep
- [x] Add validation to ensure values are positive integers

### 2. Update setup_logging function (`src/javamcp/logging/logger.py`)
- [x] Replace `FileHandler` with `RotatingFileHandler` when file logging is enabled
- [x] Configure rotation using `max_bytes` and `backup_count` from config
- [x] Import `RotatingFileHandler` from `logging.handlers`

### 3. Update tests (`tests/logging/test_logger.py`)
- [x] Update test to verify `RotatingFileHandler` is used instead of `FileHandler`
- [x] Add test for rotation configuration parameters
- [x] Add test to verify rotation behavior (write logs exceeding max_bytes)

### 4. Update documentation (if config examples exist)
- [ ] Add rotation parameters to example configuration files

## Technical Details
- Use `logging.handlers.RotatingFileHandler` from Python standard library
- Rotation creates backup files: `app.log`, `app.log.1`, `app.log.2`, etc.
- When `app.log` reaches `max_bytes`, it's renamed to `app.log.1` and a new `app.log` is created
- Oldest backup (`app.log.{backup_count}`) is deleted when limit is reached

## Default Configuration
- `max_bytes`: 10485760 (10 MB)
- `backup_count`: 5 (keep 5 backup files)
- Total max disk space: ~60 MB (10 MB × 6 files)
