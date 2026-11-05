"""Optional live retrieval; NEVER runs on import or during rendering.
python3 fetch.py  (10-second wall-clock deadline; no retries or silent fallback)
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from urllib.request import Request, urlopen
from urllib.error import HTTPError

URL = "https://api.worldbank.org/v2/country/che;fra;deu/indicator/SP.POP.TOTL?date=2023:2024&format=json&per_page=100"


def fetch_once(url, destination):
    request = Request(url, headers={"Accept":"application/json", "User-Agent":"DCM-teaching-demo/2026"})
    try:
        response = urlopen(request, timeout=8)
    except HTTPError as error:
        response = error  # retain the actual error body as evidence
    with response:
        raw = response.read()
        status = response.status
        content_type = response.headers.get("Content-Type", "")
        final_url = response.geturl()
    destination = Path(destination)
    (destination / "response.json").write_bytes(raw)
    manifest = {"kind":"optional fresh response, not approved snapshot", "request_url":url,
                "final_url":final_url,"retrieved_utc":datetime.now(timezone.utc).isoformat(),
                "status":status,"content_type":content_type,"sha256":hashlib.sha256(raw).hexdigest()}
    (destination / "provenance.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print("LIVE",status,content_type, "saved to",destination,flush=True)
    if not 200 <= status < 300:
        raise ValueError("HTTP failure: inspect retained response; use approved snapshot for class")
    if "application/json" not in content_type.lower():
        raise ValueError("Unexpected content type; retained response is not labeled usable JSON")
    payload=json.loads(raw)
    from support import validate_envelope
    validate_envelope(payload)
    print("Envelope checked. Compare source values and keys before accepting a revised snapshot.")
    return payload


if __name__ == "__main__":
    parser=argparse.ArgumentParser(); parser.add_argument("--url",default=URL)
    parser.add_argument("--worker",type=Path,help=argparse.SUPPRESS); args=parser.parse_args()
    if args.worker:
        try: fetch_once(args.url,args.worker)
        except Exception as error: print("LIVE FAILED:",error);sys.exit(1)
    else:
        root=Path(__file__).resolve().parent / "data/live";root.mkdir(exist_ok=True)
        destination=Path(tempfile.mkdtemp(prefix=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ-"),dir=root))
        try:
            run=subprocess.run([sys.executable,str(Path(__file__).resolve()),"--url",args.url,"--worker",str(destination)],timeout=10)
            sys.exit(run.returncode)
        except subprocess.TimeoutExpired:
            print("LIVE TIMEOUT after 10 seconds. Explicitly load the approved OFFLINE snapshot; no retry.")
            sys.exit(1)
