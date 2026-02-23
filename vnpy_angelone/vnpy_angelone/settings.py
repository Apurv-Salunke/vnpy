from dataclasses import dataclass


@dataclass(slots=True)
class AngelOneSettings:
    """Typed gateway settings parsed from Trader's connection dialog."""

    api_key: str
    client_code: str
    pin: str
    totp_secret: str
    feed_token: str
    instrument_master_path: str
    paper_mode: bool
    paper_base_url: str
    timeout_seconds: int

    @classmethod
    def from_setting(cls, setting: dict) -> "AngelOneSettings":
        """Build validated settings object from untyped gateway setting dict."""
        paper_mode: bool = str(setting.get("Paper Mode", "True")) == "True"
        timeout_raw: str = str(setting.get("Timeout Seconds", 10))
        timeout_seconds: int = int(timeout_raw)

        return cls(
            api_key=str(setting.get("API Key", "")).strip(),
            client_code=str(setting.get("Client Code", "")).strip(),
            pin=str(setting.get("PIN", "")).strip(),
            totp_secret=str(setting.get("TOTP Secret", "")).strip(),
            feed_token=str(setting.get("Feed Token", "")).strip(),
            instrument_master_path=str(setting.get("Instrument Master Path", "")).strip(),
            paper_mode=paper_mode,
            paper_base_url=str(setting.get("Paper Base URL", "")).strip(),
            timeout_seconds=timeout_seconds,
        )

    def validate_required(self) -> tuple[bool, str]:
        """
        Return validation result for required fields.

        Feed token can be empty because it is often generated after login.
        """
        if not self.api_key:
            return False, "Missing API Key"
        if not self.client_code:
            return False, "Missing Client Code"
        if not self.pin:
            return False, "Missing PIN"
        if not self.totp_secret:
            return False, "Missing TOTP Secret"

        return True, ""
