from typing import *
from pathlib import Path
import json
from dateutil.relativedelta import relativedelta
from datetime import datetime
import base64

from autoslot import Slots

from ghunt.errors import GHuntInvalidSession


class SmartObj(Slots):
    pass

class AndroidCreds(SmartObj):
    def __init__(self) -> None:
        self.master_token: str = ""
        self.authorization_tokens: Dict = {}

class GHuntCreds(SmartObj):
    """
        This object stores all the needed credentials that GHunt uses,
        such as cookies, OSIDs, keys and tokens.
    """
    
    def __init__(self, creds_path: str = "") -> None:
        self.cookies: Dict[str, str] = {}
        self.osids: Dict[str, str] = {}
        self.android: AndroidCreds = AndroidCreds()

        if not creds_path:
            cwd_path = Path().home()
            ghunt_folder = cwd_path / ".malfrats/ghunt"
            if not ghunt_folder.is_dir():
                ghunt_folder.mkdir(parents=True, exist_ok=True)
            creds_path = ghunt_folder / "creds.m"
        self.creds_path: str = creds_path

    def are_creds_loaded(self) -> bool:
        return all([self.cookies, self.osids, self.android.master_token])

    def load_creds(self, silent=False) -> None:
        """Loads cookies, OSIDs and tokens if they exist"""
        if Path(self.creds_path).is_file():
            try:
                # with open(self.creds_path, "r", encoding="utf-8") as f:
                #     raw = f.read()
                raw = 'ewogICJjb29raWVzIjogewogICAgIlNJRCI6ICJlQWpianpLenpFU2VJSlZsaEFJcU5CMmprRE5iNmU5UktOLVdLeXh6TE9FYzZRckZuaVA4V1k0WC1obGplRDhnclpaYmJRLiIsCiAgICAiX19TZWN1cmUtM1BTSUQiOiAiZUFqYmp6S3p6RVNlSUpWbGhBSXFOQjJqa0ROYjZlOVJLTi1XS3l4ekxPRWM2UXJGZnRnalY2c2F6ZzJKNGpYcHNoZHdBZy4iLAogICAgIkhTSUQiOiAiQS05a3dzSTFoMi1US18zRi0iLAogICAgIlNTSUQiOiAiQW9YNmhONXgtVlg3Y2JWcTQiLAogICAgIkFQSVNJRCI6ICJHcjhLb2x5TW12TGFzNU9PL0FzUUhGbHppU08zdDVwNUplIiwKICAgICJTQVBJU0lEIjogIkdpQmFCWnlGMEc4dzFrRkkvQUFRSGVuTk5xcDdyQlI0X3kiLAogICAgIkxTSUQiOiAicy5BVXxzLkZJfHMueW91dHViZTplQWpial8tcjd5czBIejVsR0JRU0tBbFNza05ocjBhcHBob2VwVV9CeDZDOHI0bTFVdnZESUJEMWRablNmMmRVa3d0dW9BLiIsCiAgICAiQ09OU0VOVCI6ICJZRVMrY2IuMjAyMjAxMTgtMDgtcDAuZnIrRlgrNTEwIiwKICAgICJQUkVGIjogInR6PUV1cm9wZS5QYXJpcyZmNj00MDAwMDAwMCZobD1lbiIKICB9LAogICJvc2lkcyI6IHsKICAgICJjbG91ZGNvbnNvbGUiOiAiZUFqYmoxZEJ1Wm1sbGF5YV9Ydm01LXdSOTRYSEgyQTNBdzJhSzAzRVNzR1pWdDhOQjUxbUktajhFU0tCYVRROXdDTlhsdy4iLAogICAgImNsIjogImVBamJqekF6TEV1WnJldXIwaUdRM3UwR3F3R3V2OGxvT01oQVc5NmpZUy1iVU1YaG9VaVhyVHJiMUhkUi1saFdkUXhvNmcuIgogIH0sCiAgImFuZHJvaWQiOiB7CiAgICAibWFzdGVyX3Rva2VuIjogImFhc19ldC9BS3BwSU5hdzV0a1lVQy02RUFkMTBQWFRaMEYtOW1LN0V5VUJnU1Z0WTlmQ29YbktQMTc1WUgxQW5aMXBpNDU4b1pMVlVjQ25SbUlPRE16TWx5U1FWckNFbjhBdm5ZU2JDMXpiLVB4akc3cGlQQ2drTElsUEwxTXRfNUsxN2paM3RsZ1dYUjVtRmFBdTVXTlUteWU3QnZzajNXUEZ5XzFpUmtjdmUwVl8zOGNSaDVHRTlPRktSazdnVkZjSkdwV2hQNVlYNXltUGpGbW83dWE1bEFUWFU4ND0iLAogICAgImF1dGhvcml6YXRpb25fdG9rZW5zIjoge30KICB9Cn0='
                data = json.loads(base64.b64decode(raw).decode())

                self.cookies = data["cookies"]
                self.osids = data["osids"]

                self.android.master_token = data["android"]["master_token"]
                self.android.authorization_tokens = data["android"]["authorization_tokens"]

            except Exception:
                raise GHuntInvalidSession("Stored session is corrupted.")
        else:
            raise GHuntInvalidSession("No stored session found.")
        
        if not self.are_creds_loaded():
            raise GHuntInvalidSession("Stored session is incomplete.")
        if not silent:
            print("[+] Stored session loaded !")

    def save_creds(self, silent=False):
        """Save cookies, OSIDs and tokens to the specified file."""
        data = {
            "cookies": self.cookies,
            "osids": self.osids,
            "android": {
                "master_token": self.android.master_token,
                "authorization_tokens": self.android.authorization_tokens
            }
        }

        with open(self.creds_path, "w", encoding="utf-8") as f:
            f.write(base64.b64encode(json.dumps(data, indent=2).encode()).decode())

        if not silent:
            print(f"\n[+] Creds have been saved in {self.creds_path} !")

### Maps

class Position(SmartObj):
    def __init__(self):
        self.latitude: float = 0.0
        self.longitude: float = 0.0

class MapsGuidedAnswer(SmartObj):
    def __init__(self):
        self.id: str = ""
        self.question: str = ""
        self.answer: str = ""

class MapsLocation(SmartObj):
    def __init__(self):
        self.id: str = ""
        self.name: str = ""
        self.address: str = ""
        self.position: Position = Position()
        self.tags: List[str] = []
        self.types: List[str] = []
        self.cost: int = 0 # 1-4

class MapsReview(SmartObj):
    def __init__(self):
        self.id: str = ""
        self.comment: str = ""
        self.rating: int = 0
        self.location: MapsLocation = MapsLocation()
        self.guided_answers: List[MapsGuidedAnswer] = []
        self.approximative_date: relativedelta = None

class MapsPhoto(SmartObj):
    def __init__(self):
        self.id: str = ""
        self.url: str = ""
        self.location: MapsLocation = MapsLocation()
        self.approximative_date: relativedelta = None
        self.exact_date: datetime = None

### Drive
class DriveExtractedUser(SmartObj):
    def __init__(self):
        self.gaia_id: str = ""
        self.name: str = ""
        self.email_address: str = ""
        self.role: str = ""
        self.is_last_modifying_user: bool = False