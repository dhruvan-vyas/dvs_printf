import sys
import os
import time
import argparse
from typing import Callable, Any, List

# Core Module Imports
from dvs_printf import printf
from dvs_printf.colors import get_colors_names
from dvs_printf.loaders import LoadingBar, ShowLoading, Spinner # Assuming Spinner is also accessible here


def long_running_task(duration: int):
    """A dummy function to simulate a long-running, CPU-bound process."""
    start_time = time.time()
    while time.time() - start_time < duration:
        time.sleep(0.1)
    return f"Task completed successfully in {duration} seconds."


def run_printf_demo(style: str) -> None:
    """Runs a printf animation demo with a given style."""
    print(f"\n--- Running printf animation with style: {style} ---")
    printf(
        f"This is a demonstration of the '{style}' style.", 
        style=style, 
        color=("blue", "white"),
        speed=4
    )


def run_loader_demo() -> None:
    """Runs a full demonstration of the LoadingBar class."""
    print("\n--- Running LoadingBar Class Demo (Progress Bar) ---")
    
    # Use LoadingBar class, setting config parameters correctly
    loader = LoadingBar(
        title_text="Processing data with Loader...", 
        style='grow', 
        timing_color='yellow',
        bar_color='lightred',
        timeout=5
    )
    result = loader.run(long_running_task, duration=3)
    print(f"Loader Demo Result: {result}")


def run_spinner_demo() -> None:
    """Runs a full demonstration of the Spinner class using the ShowSpinner wrapper."""
    print("\n--- Running Spinner Class Demo (Dynamic Spinner) ---")
    
    # Use ShowSpinner wrapper for brevity and style
    result = ShowLoading( # ShowLoading is a generic runner, assuming it can launch Spinner
        long_running_task, 
        args=[3], # Duration of 3 seconds
        title_text="Analyzing data with Spinner...", 
        style='dots', 
        show_timer=True,
        title_color='yellow',
        spinner_color=["red", "yellow"],
        timeout=5
    )
    print(f"Spinner Demo Result: {result}")


def main() -> None:
    """Main function to parse arguments and run the selected demo."""
    parser = argparse.ArgumentParser(
        description="CLI for dvs_printf: Animated console output, Loaders, and Spinners."
    )
    
    parser.add_argument(
        "-s", "--style",
        dest="style",
        help="Run a specific printf animation style (e.g., 'typing', 'glitch').",
        metavar="STYLE_NAME"
    )

    parser.add_argument(
        "-d", "--demo",
        dest="demo_name",
        choices=['loader', 'spinner', 'colors'],
        help="Run a full demo for the specified class (loader, spinner, or colors table).",
        metavar="DEMO_NAME"
    )
    
    args = parser.parse_args()

    if args.style:
        run_printf_demo(args.style)
    elif args.demo_name == 'loader':
        run_loader_demo()
    elif args.demo_name == 'spinner':
        run_spinner_demo()
    elif args.demo_name == 'colors':
        print("\n--- Running Color Names Table (Full List) ---")
        # Assuming get_colors_names can print the table when called without return_dict
        get_colors_names(show_color_table=True, return_dict=False)
    else:
        # Default behavior: run a printf animation
        printf(style='help')
        # print("\nNo options provided. Running default printf animation...")
        # printf("Welcome to your CLI!", style="typing", color=("cyan", "white"), speed=0.08)
        
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # The custom exception hook should catch dvs_BaseException, but this ensures a clean exit for all errors.
        print(f"\nAn unhandled error occurred: {e}", file=sys.stderr)
        sys.exit(1)
