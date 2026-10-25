from amanara.rag.text_cleaner import clean_extracted_text


def test_replaces_nonbreaking_spaces():
    assert clean_extracted_text("Solar\u00a0Park") == "Solar Park"


def test_normalizes_multiple_spaces():
    assert clean_extracted_text("Solar    Park") == "Solar Park"


def test_reduces_excessive_newlines():
    result = clean_extracted_text("Solar\n\n\n\nPark")
    assert result == "Solar\n\nPark"


def test_repairs_known_pdf_artifacts():
    text = "TheElectricityAct,2003allows powerConsumers"
    result = clean_extracted_text(text)

    assert "The Electricity Act, 2003" in result
    assert "2003 allows" in result
    assert "power Consumers" in result


def test_strips_leading_and_trailing_whitespace():
    assert clean_extracted_text("  Solar Park  ") == "Solar Park"


def test_empty_string_returns_empty_string():
    assert clean_extracted_text("") == ""
