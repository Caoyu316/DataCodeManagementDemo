"""Report entry point. Run from the extracted pack: python3 report.py pipeline.py."""
import sys
from runner import candidate
from validation import load

def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 report.py CANDIDATE.py")
    code = candidate(sys.argv[1])
    result = code.compare(code.extract(load()))
    print(result.to_string(index=False, float_format=lambda value: f"{value:.3f}"))

if __name__ == "__main__":
    main()
