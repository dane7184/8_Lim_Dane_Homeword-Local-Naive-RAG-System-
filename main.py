import sys
from pathlib import Path

# Add app to path so relative imports work seamlessly
sys.path.insert(0, str(Path(__file__).parent / "app"))

from app.main import main

if __name__ == "__main__":
    main()
