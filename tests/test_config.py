"""Tests for the config module."""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config


class TestConfigConstants:
    def test_app_name_is_defined(self):
        assert hasattr(config, "APP_NAME")
        assert config.APP_NAME == "NUVEXA"

    def test_app_version_is_defined(self):
        assert hasattr(config, "APP_VERSION")
        assert isinstance(config.APP_VERSION, str)

    def test_app_tagline_is_defined(self):
        assert hasattr(config, "APP_TAGLINE")
        assert isinstance(config.APP_TAGLINE, str)
        assert len(config.APP_TAGLINE) > 0

    def test_db_name_is_defined(self):
        assert hasattr(config, "DB_NAME")
        assert isinstance(config.DB_NAME, str)


class TestModes:
    def test_modes_is_dict(self):
        assert isinstance(config.MODES, dict)

    def test_modes_has_required_keys(self):
        for key in ("assistant", "shopping", "therapist", "builder"):
            assert key in config.MODES

    def test_each_mode_has_required_fields(self):
        for mode_key, mode_data in config.MODES.items():
            assert "name" in mode_data, f"Mode '{mode_key}' missing 'name'"
            assert "icon" in mode_data, f"Mode '{mode_key}' missing 'icon'"
            assert "description" in mode_data, f"Mode '{mode_key}' missing 'description'"
            assert "system_prompt" in mode_data, f"Mode '{mode_key}' missing 'system_prompt'"

    def test_system_prompts_are_non_empty(self):
        for mode_key, mode_data in config.MODES.items():
            assert len(mode_data["system_prompt"]) > 0, f"Mode '{mode_key}' has empty system_prompt"


class TestAvatarStyles:
    def test_avatar_styles_is_list(self):
        assert isinstance(config.AVATAR_STYLES, list)

    def test_avatar_styles_not_empty(self):
        assert len(config.AVATAR_STYLES) > 0

    def test_default_avatar_style_in_list(self):
        assert "Stylized Futuristic Human" in config.AVATAR_STYLES
