"""Test configuration and collection utilities."""
import pytest
from typing import List
from _pytest.nodes import Item

def pytest_collection_modifyitems(items: List[Item]) -> None:
    """Automatically add markers based on test module names and characteristics."""
    for item in items:
        # Add component markers
        if "test_vector_store" in item.nodeid:
            item.add_marker(pytest.mark.vectorstore)
        elif "test_mcp" in item.nodeid:
            item.add_marker(pytest.mark.mcp)
        elif "test_chain" in item.nodeid:
            item.add_marker(pytest.mark.chain)
        elif "test_api" in item.nodeid:
            item.add_marker(pytest.mark.api)

        # Add test type markers
        if item.get_closest_marker("integration") is None:
            # Mark as unit test if not explicitly marked as integration
            item.add_marker(pytest.mark.unit)

        # Add performance markers
        if "test_performance" in item.nodeid or "benchmark" in item.nodeid:
            item.add_marker(pytest.mark.slow)
