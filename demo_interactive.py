"""
Interactive Demo for Phase I Todo App
Run this to test the application interactively
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.main import main

if __name__ == "__main__":
    print("\n" + "="*60)
    print("PHASE I TODO APP - INTERACTIVE DEMO")
    print("="*60)
    print("\nThis is the actual application you'll demo in the video.")
    print("Follow the demo script to record your 90-second video.")
    print("\nPress Ctrl+C at any time to exit.")
    print("="*60 + "\n")

    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo ended. Good luck with your recording!")
