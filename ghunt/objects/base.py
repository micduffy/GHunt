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
                raw = 'ewogICJjb29raWVzIjogewogICAgIkFQSVNJRCI6ICJidU83eGNmM0dQaC11bklVL0FhQV8tY1hod1dlOWw0TTdyIiwKICAgICJIU0lEIjogIkFvalFMQWJMZ1ZjVVVGOEVrIiwKICAgICJMU0lEIjogIm8uYWRzLmdvb2dsZS5jb218by5jYWxlbmRhci5nb29nbGUuY29tfG8uY29uc29sZS5jbG91ZC5nb29nbGUuY29tfG8uZHJpdmUuZ29vZ2xlLmNvbXxvLmdyb3Vwcy5nb29nbGUuY29tfG8ubGVucy5nb29nbGUuY29tfG8ubWFpbC5nb29nbGUuY29tfG8ubWVldC5nb29nbGUuY29tfG8ubXlhY2NvdW50Lmdvb2dsZS5jb218by5wYXNzd29yZHMuZ29vZ2xlLmNvbXxvLnBob3Rvcy5nb29nbGUuY29tfG8ucGxheS5nb29nbGUuY29tfHMuQVV8cy55b3V0dWJlOlhRaEVWdHZBcXphNmFJZXd6aTNUVXdtT3JYZGFqcVVoOW91Wk9oWUdjb0FIbWZDd1FxT0RsSWIwZDJsdmJDS0VVX0oxTEEuIiwKICAgICJTQVBJU0lEIjogImNQdE9BNmh1cDVaYjE3RXMvQTFLTk9YRFQzYjF3NGE0d1QiLAogICAgIlNJRCI6ICJYUWhFVms1eHI2enc0TmY2dHA4X1U3aktTV0ZueUppVnhOeDhkTmlsQ1NHbGVRSzJYOVlMR2NfUDhzR0RqMEdFQnc3SjJ3LiIsCiAgICAiU1NJRCI6ICJBa0pJYldzU0V2aWlyRzh1VSIsCiAgICAiX19TZWN1cmUtM1BTSUQiOiAiWFFoRVZrNXhyNnp3NE5mNnRwOF9VN2pLU1dGbnlKaVZ4Tng4ZE5pbENTR2xlUUsybHA0TmJzaTVlenhNaE5GVmNLWkdEUS4iLAogICAgIkNPTlNFTlQiOiAiWUVTK2NiLjIwMjIwMTE4LTA4LXAwLmZyK0ZYKzUxMCIsCiAgICAiUFJFRiI6ICJ0ej1FdXJvcGUuUGFyaXMmZjY9NDAwMDAwMDAmaGw9ZW4iCiAgfSwKICAib3NpZHMiOiB7CiAgICAiY2xvdWRjb25zb2xlIjogIlhRaEVWcDFzNVhpRnZfTGFVcUx5NmxMSVg3REN5T2t1M0hKY0xMdDBJU1BNd1ZMNndORGwxVVFBcGtPWjNRZ19NcWlTSHcuIiwKICAgICJjbCI6ICJYUWhFVnJ6V282TWRiQ2VVU0IyUmZ0eU8wTk1odkJaMk5zQlVkNVl0elRqb2M4eWx4ZURLV1djN0JybF9mUmJNaW5vbS1RLiIKICB9LAogICJhbmRyb2lkIjogewogICAgIm1hc3Rlcl90b2tlbiI6ICJhYXNfZXQvQUtwcElOYlFLNEd5YTVVUE8xbjRKdGNCNmptMGZFVWZSTVJyemlFU1F0TkZiZWM2ay0xSjZDbEU2ZW5XMHdrRENuVUdmVVpROW5LMTZkelRfS1o5Y3YwdzNyaEJHQXU3MGg3cnltVVE0TzlaVk51eFl3OUJIZlBqbUxLc3dhdWROWm9lVXVMZkduS3dmWDZjZjNHUXdrZWEwT3NJc0tpUHRGdjFUdnFvallHVG13ZUNpanVRZHRGMFJ2NHdhaVRRekFwalZVaUVEQlpia0tXWWpfSngxU009IiwKICAgICJhdXRob3JpemF0aW9uX3Rva2VucyI6IHsKICAgICAgInBsYXlnYW1lcyI6IHsKICAgICAgICAidG9rZW4iOiAieWEyOS5hMEFXWTdDa2tIemdNTlJnTG1BVjR1V2M0ZG0wSnZubktXckdJcTZ6T2NKSnU5VUxkUGZFN1BNY2otUmZUTFdEeTBXOTNhU3JISkdPdzE3MjNWWl8tU0VUcHNPV2RUYjRhNFh1UWVnMFB5bG1Ya2JvdnpNS0c5YjE3TFBWZXhIelhSZnNPaUUyTUtDWVNyakJLa2UxcU82cGloQTBDbExRQ1dEb29mdG14Zk02OEZIMVZrZHZXV0VMMC14V3ZqZW5kSnhPeEN4aThPY0dZdEtkQVZFVGFBRVdYVWl2VTUySUZNLU1YdXI4cUhack00dm8zbjU1WDY5S1NTSFJIWFBJVl9GV3hLZmtmY04xRC1oR0FaclpxVzNleU5SR3VpdlpQUVlyN0JjdElUOUsyRW9XNWdmbzVfMTZ5bzRTOGFDZ1lLQVVZU0FROFNGUUcxdERycFhYendMeWlNYVVvSlBjZFlQbnA2ZEEwMzIyIiwKICAgICAgICAiZXhwaXJ5IjogMTY4NjQzNDkyMwogICAgICB9CiAgICB9CiAgfQp9'
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