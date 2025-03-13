import os
import pkgutil
import importlib
import inspect
import sys
import logging
import logging.config
from dotenv import load_dotenv
from calculator.commands import CommandHandler
from calculator.commands import Command
from calculator.historyManager import HistoryManager


class Calculator:
    def __init__(self):
        os.makedirs('logs', exist_ok=True)
        self.configure_logging()
        load_dotenv()
        self.settings = self.load_environment_variables()
        self.settings.setdefault('ENVIRONMENT', 'PRODUCTION')

        self.command_handler = CommandHandler()
        HistoryManager.initialize_history()
        

    def configure_logging(self):
        logging_conf_path = os.getenv('LOGGING_CONF_PATH', 'logging.conf')
        if os.path.exists(logging_conf_path):
            logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)
        else:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info("Logging configured.")

    def load_environment_variables(self):
            settings = {key: value for key, value in os.environ.items()}
            logging.info("Calculator: Environment variables loaded.")
            return settings

    def get_environment_variable(self, env_var: str = 'ENVIRONMENT'):
        return self.settings.get(env_var, None)

    def load_plugins(self):
        plugins_package = 'calculator.plugins'
        plugins_path = plugins_package.replace('.', '/')

        if not os.path.exists(plugins_path):
            logging.warning(f"Plugins path '{plugins_path}' not found")
            return

        for i, plugin_name, is_pkg in pkgutil.iter_modules([plugins_path]):
            if is_pkg:
                plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}')
                for item_name in dir(plugin_module):
                    item = getattr(plugin_module, item_name)

                    constructor_params = inspect.signature(item.__init__).parameters

                    try:
                        if issubclass(item, (Command)):
                            if 'command_handler' in constructor_params:
                                self.command_handler.register_command(plugin_name, item(self.command_handler))
                            else:
                                self.command_handler.register_command(plugin_name, item())
                    except TypeError:
                        continue
                    except ImportError as e:
                        logging.error(f"Error loading plugin {plugin_name}: {e}")

    def start(self):
        Calculator.load_plugins(self)
        logging.info("Calculator initialized")
        print("Calculator initialized\nType 'exit' to quit. Type 'menu' to see available commands.\n")

        while True:
            try:
                self.command_handler.handle_user_input(input("> ").strip())
            except KeyboardInterrupt:
                logging.info("Keyboard interrupt entered, now exiting program.")
                sys.exit(0)