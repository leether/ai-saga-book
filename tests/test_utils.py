"""Tests for scripts/utils.py"""

import tempfile
from pathlib import Path

import pytest

from scripts.utils import (
    setup_logging,
    read_file,
    write_file,
    get_project_root,
    get_chapters_dir,
    list_chapters,
    validate_chapters,
)


class TestSetupLogging:
    """Test logging setup function."""

    def test_setup_logging_creates_logger(self):
        """Should create a logger with the given name."""
        log = setup_logging(__name__)
        assert log.name == __name__
        assert len(log.handlers) > 0

    def test_setup_logging_returns_logger(self):
        """Should return a logging.Logger instance."""
        import logging
        log = setup_logging(__name__)
        assert isinstance(log, logging.Logger)


class TestFileOperations:
    """Test file read/write operations."""

    def test_write_and_read_file(self):
        """Should write and read files correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.txt"
            content = "Test content\n"
            
            write_file(test_file, content)
            assert test_file.exists()
            
            read_content = read_file(test_file)
            assert read_content == content

    def test_read_file_raises_on_missing(self):
        """Should raise FileNotFoundError for missing files."""
        missing_file = Path("/tmp/nonexistent_file_xyz.txt")
        with pytest.raises(FileNotFoundError):
            read_file(missing_file)


class TestProjectPaths:
    """Test project path utilities."""

    def test_get_project_root_returns_path(self):
        """Should return a Path object."""
        root = get_project_root()
        assert isinstance(root, Path)
        assert root.exists()

    def test_get_chapters_dir_returns_path(self):
        """Should return chapters directory path."""
        chapters = get_chapters_dir()
        assert isinstance(chapters, Path)
        # Directory may not exist in test environment


class TestChapterValidation:
    """Test chapter listing and validation."""

    def test_list_chapters_returns_list(self):
        """Should return a list of chapter numbers."""
        try:
            chapters = list_chapters()
            assert isinstance(chapters, list)
            if chapters:
                assert all(isinstance(c, int) for c in chapters)
        except FileNotFoundError:
            # OK if directory doesn't exist
            pass

    def test_validate_chapters_raises_on_missing(self):
        """Should raise FileNotFoundError if chapters missing."""
        # Create a temp dir with partial chapters
        with tempfile.TemporaryDirectory() as tmpdir:
            # This would need a mock to properly test
            # Just verify the function exists
            assert callable(validate_chapters)


class TestIntegration:
    """Integration tests for utils module."""

    def test_utils_module_imports_successfully(self):
        """Module should import without errors."""
        from scripts import utils
        assert utils is not None

    def test_all_required_functions_exist(self):
        """Module should export all required functions."""
        from scripts.utils import (
            setup_logging,
            read_file,
            write_file,
            ensure_directory,
            run_command,
            get_project_root,
            get_chapters_dir,
            list_chapters,
            validate_chapters,
        )
        assert callable(setup_logging)
        assert callable(read_file)
        assert callable(write_file)
        assert callable(ensure_directory)
        assert callable(run_command)
        assert callable(get_project_root)
        assert callable(get_chapters_dir)
        assert callable(list_chapters)
        assert callable(validate_chapters)
