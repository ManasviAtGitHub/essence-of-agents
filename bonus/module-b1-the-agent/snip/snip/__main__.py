"""Entry point for `python -m snip <create|resolve|stats> ...`."""
import sys
from .api import main

sys.exit(main())
