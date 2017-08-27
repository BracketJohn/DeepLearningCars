"""Entrypoint to execute whole package from Command Line."""
import sys


if sys.version_info < (3,0):
    sys.exit('Sorry, Python < 3.0 is not supported')


from deepcars.simulation import main_menu

def start_sim():
    main_menu()

if __name__ == "__main__":
    main_menu()
