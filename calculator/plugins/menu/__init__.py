from calculator.commands import Command

class MenuCommand(Command):
    def __init__(self, command_handler):
        self.command_handler = command_handler
    
    def execute(self):
        all_commands = self.command_handler.commands
        print("---Available Calculator Commands---\n")

        for command_name, command_func in all_commands.items():
            print(f"{command_name}: {command_func.description()}\nUsage: {command_func.usage()}\n")
    
    def description(self):
        return "List all available commands"
    
    def usage(self):
        return "menu"