import pytest
from scanner_handler import CheckQr


scanner = CheckQr()


@pytest.mark.parametrize(
    "qr_code, expected_color, is_in_db",
    [
        ("123", "Red", True),
        (
            "12345",
            "Green",
            False,
        ),
        (
            "1234567",
            "Fuzzy Wuzzy",
            True,
        ),
        (
            "1234",
            None,
            False,
        ),
    ],
    ids=[
        "len(qr_code) = 3 and in DB",
        "len(qr_code) = 5 and not in DB",
        "len(qr_code) = 7 and in DB",
        "len(qr_code) = 4 (invalid) and not in DB",
    ],
)
def test_scanner_handler(qr_code: str, expected_color: str, is_in_db: bool, mocker):
    mock_check_in_db = mocker.patch(
        "scanner_handler.CheckQr.check_in_db", return_value=is_in_db
    )
    mock_send_error = mocker.patch("scanner_handler.CheckQr.send_error")
    mock_can_add_device = mocker.patch("scanner_handler.CheckQr.can_add_device")

    scanner.check_scanned_device(qr_code)
    assert scanner.color == expected_color
    mock_check_in_db.assert_called_once()

    if len(qr_code) not in (3, 5, 7):
        mock_send_error.assert_called_once_with(
            f"Error: Wrong qr length {len(qr_code)}"
        )

    elif not is_in_db:
        mock_send_error.assert_called_once_with("Not in db")

    else:
        mock_can_add_device.assert_called_once_with(f"hallelujah {qr_code}")
