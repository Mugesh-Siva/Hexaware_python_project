import pytest

from services.customerServices.browseItems import search_menu_items


class TestCustomerSearch:
    def test_search_menu_items_returns_matching_items(self):
        result = search_menu_items("burger", page_number=0, page_size=10)

        assert result["success"] is True
        assert result["items"]
        assert any("burger" in item[1].lower() for item in result["items"])

    def test_search_menu_items_blank_term_is_rejected(self):
        result = search_menu_items("   ", page_number=0, page_size=10)

        assert result["success"] is False
        assert "required" in result["message"].lower() or "empty" in result["message"].lower()

    def test_search_menu_items_no_match_returns_empty_result(self):
        result = search_menu_items("zzzz-not-real-menu-name", page_number=0, page_size=10)

        assert result["success"] is True
        assert result["items"] == []
        assert result["total_count"] == 0
