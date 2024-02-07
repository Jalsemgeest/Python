
import os
import importlib.util
import signal
import sys
import subprocess
import threading
from multiprocessing import Process

class Runner():

    def __init__(self, directory):
        self.directory = directory
        self.threads = {}

    @classmethod
    def initialize(cls, directory):
        return cls(directory)

    def list_python_files(self):
        """List all Python files in the specified directory."""
        python_files = []
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        return python_files

    def import_python_file_as_module(self, file_path):
        """Dynamically import a Python file as a module."""
        module_name = os.path.basename(file_path).replace('.py', '')
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module

    def run_scripts_in_directory(self):
        """Import and run all Python scripts in the specified directory."""
        python_files = self.list_python_files(self.directory)
        for file_path in python_files:
            module = self.import_python_file_as_module(file_path)
            # run_module_function(module)
    
    def start_process(self, filename):
        return subprocess.Popen(["python3", filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            # stdout, stderr = proc.communicate()  # This waits for the subprocess to complete
            # print(stdout)
            # if stderr:
            #     print(f"Errors:\n{stderr}")

    def run_file(self, file):
        # p = subprocess.Popen(["python3", file], start_new_session=True)
        # self.threads[file] = p
        p = self.start_process(file)
        self.threads[file] = p

    def list_processes(self):
        return self.threads.keys()

    def kill_process(self, target):
        process = self.threads[target]
        print(process)
        process.kill()
        del self.threads[target]
        print("Process killed successfully")

    def run(self):
        print(self.list_python_files(self.directory))
    
    @staticmethod
    def commands():
        print("What would you like to do?")
        print("l - list programs")
        print("ls - list threads")
        print("s <name> - start a program with the provided name")
        print("k <name> - kill the program with the provided name")
        print("q - quit the game")

if __name__ == "__main__":
    directory = "assistant-packages/" #input("Enter the directory path containing Python scripts: ")
    runner = Runner.initialize(directory=directory)

    Runner.commands()
    user_input = input("Command: ")
    while user_input != "q":
        if user_input == "l":
            print("Files:")
            files = runner.list_python_files()
            for file in files:
                print(file)
        elif user_input == "ls":
            print("Processes: ")
            processes = runner.list_processes()
            for process in processes:
                print(process)
        elif user_input.startswith("s"):
            file_target = user_input.split(" ")[1]
            files = runner.list_python_files()
            for file in files:
                if file_target in file:
                    runner.run_file(file)
                    break
        elif user_input.startswith("k"):
            file_target = user_input.split(" ")[1]
            processes = runner.list_processes()
            print("Processes are:")
            for process in processes:
                print(process)
                if file_target in process:
                    print(f"Killing {process}")
                    runner.kill_process(process)
                    break
        elif user_input == "q":
            print("Runner exiting.")
            break
        print(" ")
        Runner.commands()
        user_input = input("Command: ")
        

