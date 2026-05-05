#!/usr/bin/env python3
"""Shared utilities for AI Saga book build tooling."""

from __future__ import annotations

import logging
import subprocess
import sys
from pathlib import Path
from typing import Optional


logger = logging.getLogger(__name__)


def setup_logging(name: str, level: int = logging.INFO) -> logging.Logger:
    """Configure logging with timestamp and level prefixes.
    
    Args:
        name: Logger name (typically __name__)
        level: Logging level (default: INFO)
        
    Returns:
        Configured logger instance
    """
    log = logging.getLogger(name)
    log.setLevel(level)
    
    if not log.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter(
            '[%(asctime)s] [%(levelname)s] %(message)s',
            datefmt='%H:%M:%S'
        ))
        log.addHandler(handler)
    
    return log


def ensure_directory(path: Path, log: logging.Logger | None = None) -> None:
    """Ensure directory exists, creating if necessary.
    
    Args:
        path: Directory path
        log: Optional logger instance
    """
    if log is None:
        log = logging.getLogger(__name__)
    
    path.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        raise IOError(f"Failed to create directory: {path}")


def read_file(path: Path, log: logging.Logger | None = None) -> str:
    """Read file with proper error handling.
    
    Args:
        path: File path
        log: Optional logger instance
        
    Returns:
        File contents as string
        
    Raises:
        FileNotFoundError: If file doesn't exist
        IOError: If read fails
    """
    if log is None:
        log = logging.getLogger(__name__)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    try:
        return path.read_text(encoding="utf-8")
    except IOError as e:
        log.error(f"Failed to read {path}: {e}")
        raise


def write_file(path: Path, content: str, log: logging.Logger | None = None) -> None:
    """Write file with proper error handling.
    
    Args:
        path: File path
        content: Content to write
        log: Optional logger instance
        
    Raises:
        IOError: If write fails
    """
    if log is None:
        log = logging.getLogger(__name__)
    
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        log.info(f"Wrote {len(content)} bytes to {path}")
    except IOError as e:
        log.error(f"Failed to write {path}: {e}")
        raise


def run_command(
    cmd: list[str],
    cwd: Optional[Path] = None,
    log: logging.Logger | None = None,
    check: bool = True
) -> subprocess.CompletedProcess:
    """Run shell command with error handling.
    
    Args:
        cmd: Command as list of arguments
        cwd: Working directory (optional)
        log: Optional logger instance
        check: Raise exception if command fails
        
    Returns:
        CompletedProcess with stdout/stderr
        
    Raises:
        subprocess.CalledProcessError: If command fails and check=True
    """
    if log is None:
        log = logging.getLogger(__name__)
    
    log.info(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode != 0:
            error_msg = result.stderr or result.stdout or f"Command exited with code {result.returncode}"
            if check:
                log.error(f"Command failed: {error_msg}")
                raise subprocess.CalledProcessError(
                    result.returncode,
                    cmd,
                    output=result.stdout,
                    stderr=result.stderr
                )
            else:
                log.warning(f"Command failed: {error_msg}")
        
        if result.stdout:
            log.debug(f"Command output: {result.stdout[:200]}")
        
        return result
    
    except Exception as e:
        log.error(f"Failed to run command: {e}")
        raise


def get_project_root() -> Path:
    """Get project root directory (parent of scripts folder).
    
    Returns:
        Path to project root
    """
    return Path(__file__).parent.parent


def get_chapters_dir() -> Path:
    """Get chapters directory (book/src).
    
    Returns:
        Path to chapters directory
    """
    return get_project_root() / "book" / "src"


def get_images_dir() -> Path:
    """Get images directory.
    
    Returns:
        Path to images directory
    """
    return get_project_root() / "images"


def list_chapters(log: logging.Logger | None = None) -> list[int]:
    """List all chapter numbers found in chapters directory.
    
    Args:
        log: Optional logger instance
        
    Returns:
        Sorted list of chapter numbers (1-34)
    """
    if log is None:
        log = logging.getLogger(__name__)
    
    chapters_dir = get_chapters_dir()
    if not chapters_dir.exists():
        raise FileNotFoundError(f"Chapters directory not found: {chapters_dir}")
    
    chapter_nums = []
    for md_file in sorted(chapters_dir.glob("ch*.md")):
        try:
            # Extract chapter number from filename ch01.md -> 1
            num = int(md_file.stem[2:])
            chapter_nums.append(num)
        except (ValueError, IndexError):
            continue
    
    return sorted(chapter_nums)


def validate_chapters(expected: int = 34, log: logging.Logger | None = None) -> bool:
    """Validate that all expected chapters exist.
    
    Args:
        expected: Expected number of chapters
        log: Optional logger instance
        
    Returns:
        True if all chapters found, raises otherwise
        
    Raises:
        FileNotFoundError: If chapters are missing
    """
    if log is None:
        log = logging.getLogger(__name__)
    
    chapters = list_chapters(log)
    if len(chapters) != expected:
        missing = [i for i in range(1, expected + 1) if i not in chapters]
        raise FileNotFoundError(
            f"Missing {len(missing)} chapters: {missing}"
        )
    
    log.info(f"✓ All {expected} chapters present")
    return True
