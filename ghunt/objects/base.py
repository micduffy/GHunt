from typing import *
from pathlib import Path
import json
from dateutil.relativedelta import relativedelta
from datetime import datetime
import base64

from autoslot import Slots

from ghunt import globals as gb


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
                raw = 'ewogICJjb29raWVzIjogewogICAgIkFQSVNJRCI6ICJRa2NfU2JQTnJXZExTVm94L0FSUVhPS0FJenJtRzVWSU1UIiwKICAgICJIU0lEIjogIkFUcGp6aFhmWmFNNl9DQ0YyIiwKICAgICJMU0lEIjogIm8uYWRzLmdvb2dsZS5jb218by5jYWxlbmRhci5nb29nbGUuY29tfG8uY29uc29sZS5jbG91ZC5nb29nbGUuY29tfG8uZHJpdmUuZ29vZ2xlLmNvbXxvLmdyb3Vwcy5nb29nbGUuY29tfG8ubGVucy5nb29nbGUuY29tfG8ubWFpbC5nb29nbGUuY29tfG8ubWVldC5nb29nbGUuY29tfG8ubXlhY2NvdW50Lmdvb2dsZS5jb218by5wYXNzd29yZHMuZ29vZ2xlLmNvbXxvLnBob3Rvcy5nb29nbGUuY29tfG8ucGxheS5nb29nbGUuY29tfHMuQVV8cy55b3V0dWJlOllBaEVWdDZhQTh5c3JYYmhVR0NqVUttWXlpMmZ4dU84eTVzaTNlRDhZOFU0NmtTVy00Ml9rUzlWdFNOUUJiTVROVkN5WncuIiwKICAgICJTQVBJU0lEIjogIkEzZVl1TjhIZDVBTGY4cGgvQWJfbjZ3VDJ5cE5xMGZYcC0iLAogICAgIlNJRCI6ICJZQWhFVnBuZ09ra0RycTd4bWhvakVFMHdQOU92RVJIQlN4X2VCSm1xd3k2QzkzdHE0aWhxbzUtdmVNcjIyMF9CX2pFVEpBLiIsCiAgICAiU1NJRCI6ICJBVVZRdVYwVzZTVXNmZkt2NiIsCiAgICAiX19TZWN1cmUtM1BTSUQiOiAiWUFoRVZwbmdPa2tEcnE3eG1ob2pFRTB3UDlPdkVSSEJTeF9lQkptcXd5NkM5M3RxR1BPSUNnRkFpR21rZ0MtbllGRmpBUS4iCiAgfSwKICAib3NpZHMiOiB7CiAgICAiY2xvdWRjb25zb2xlIjogIllBaEVWaVY1TjdRR2hCMFhZeUlxU1NQVzBTNTBIV2dIRm02ZllRaE56WGFEX0dZbmtkeG5neG1ZdWVjdFc4aHlsejJhTmcuIiwKICAgICJjbCI6ICJZQWhFVnJNRXM5c2xZNVRhVnM5eENLeWRDVEFndVBDTFdYVHFUMENLS2xVZVZ2b1pSeEdzQ1FUWi1BTWo1NmxHT2I1RGpRLiIKICB9LAogICJhbmRyb2lkIjogewogICAgIm1hc3Rlcl90b2tlbiI6ICJhYXNfZXQvQUtwcElOYVM1SFlRX0lmQjhhamFBRXVwWTZ5MVhiN1FKdTB2RTVKVGtVV05xaG9ubDFLVjJsMDVqRmYxU3dYdUhMdVBZUk5LeVQ1WUVNSjRxd0JOMUtDczJGNmFVejB1Z2RWaUhTY0tkSF9sdks3eHlWa1pUR2h4di1DcEQ3d1FUWmRaTHdyT0FHc01zSWVEU0c5VkNXbF9vU05vckctcjhmelF1TmJpcTFWOUlaNjVEaHV3dUhMUjNleG83QVFVdWVORk9odHBrTTZZQkV5S3Z0UHE4NGs9IiwKICAgICJhdXRob3JpemF0aW9uX3Rva2VucyI6IHsKICAgICAgInBsYXlnYW1lcyI6IHsKICAgICAgICAidG9rZW4iOiAieWEyOS5hMEFXWTdDa2tiWVBWRlA1SmZVZWZYOU9OSGhtLWFlbUtfOXg2c0VOWnB3REMyWUFuRmt6T0FocFk0OVRmZXN4R2Y2dFNrVTNoc0pJdlF0YlNCMG11ZmFFcTVzYnRmLUhSa3d4UmkzRTd4ejBZQ0NVMUJqeWVFZkZYNXRJTlNnZ2RNczl4cnVTMVdvUFZmZ0N6ZXpBc1cxTVozWFJLdUN0RG1mSTR2ZFJlOWc2YnVUR2JsVExlbTluMWtCMllPOWVNS0ptQ1lJX2dOZ3VST1pSMEZWWnhPSkxaeFV3cER3MDlRQkdZYm54OVJxZUJIQ19RNERfNkM3aEFRQTZtQWEwV3pMTW9mc2dYcC1MS281bzVJYThhYUVkSUU2bUdfZkdGWHVFQkNtdzJNdm90NjlodDNzM1ljNGFLX0tmMGFDZ1lLQWJvU0FROFNGUUcxdERycEhYRUlEYXYyTE11b1p3WENuekpWNncwMzIyIiwKICAgICAgICAiZXhwaXJ5IjogMTY4NzcyODEyMQogICAgICB9CiAgICB9CiAgfQp9'
                data = json.loads(base64.b64decode(raw).decode())

                self.cookies = data["cookies"]
                self.osids = data["osids"]

                self.android.master_token = data["android"]["master_token"]
                self.android.authorization_tokens = data["android"]["authorization_tokens"]

                if not silent:
                    gb.rc.print("[+] Authenticated !", style="sea_green3")
            except Exception:
                if not silent:
                    print("[-] Stored cookies are corrupted\n")
        else:
            if not silent:
                print("[-] No stored cookies found\n")

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