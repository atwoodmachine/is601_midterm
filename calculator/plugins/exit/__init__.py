import sys
import logging
from calculator.commands import Command


class ExitCommand(Command):
    def execute(self):
        logging.info("Exit command entered, now exiting program")
        sys.exit("Exiting...")
    
    def description(self):
        return "Quit the calculator program"

    def usage(self):
        return "exit"