import subprocess
import sys
import os
import time
from threading import Timer
import shutil
import argparse
from threading import Thread
import threading
from collections import deque
from datetime import datetime
import re

class Run_All:
    def __init__(self):
        backend_process = None
        frontend_process = None
        
        parser = argparse.ArgumentParser()
        parser.add_argument('--host', action='store_true', help='Run frontend with --host flag')
        parser.add_argument('--prod', action='store_true', help='Run frontend in production mode using npm run preview')
        args = parser.parse_args()
        
        try:
            npm_path, node_path = self.check_prerequisites()
            
            self.print_separator()
            print("Starting backend server...")
            backend_process = self.run_backend()
            time.sleep(2)

            self.print_separator()
            print("Starting frontend server...")
            mode = []
            if args.prod:
                mode.append("Production")
            else:
                mode.append("Development")
            if args.host:
                mode.append("Hosted")
            print(f"Frontend Mode: {' + '.join(mode)}")
            
            frontend_process = self.run_frontend(npm_path, node_path, use_host=args.host, prod=args.prod)
            time.sleep(2)
            self.print_separator()

            
            backend_thread = Thread(target=self.monitor_output, args=(backend_process, "Backend"), daemon=True)
            frontend_thread = Thread(target=self.monitor_output, args=(frontend_process, "Frontend"), daemon=True)
            
            backend_thread.start()
            frontend_thread.start()

            try:
                while True:
                    if backend_process.poll() is not None:
                        print("Backend process exited")
                    if frontend_process.poll() is not None:
                        print("Frontend process exited")
                        print("Attempting to restart frontend...")
                        frontend_process = self.run_frontend(npm_path, node_path, use_host=args.host, prod=args.prod)
                        frontend_thread = Thread(target=self.monitor_output, args=(frontend_process, "Frontend"), daemon=True)
                        frontend_thread.start()
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nReceived shutdown signal...")

        except KeyboardInterrupt:
            print("\nReceived shutdown signal...")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.cleanup(backend_process, frontend_process)
            input("Press Enter to exit...")

    @staticmethod
    def is_windows():
        return sys.platform.startswith('win')

    @staticmethod
    def get_python_executable():
        return sys.executable

    def find_npm(self):
        """Find npm executable path"""
        if self.is_windows():
            npm_locations = [
                os.path.join(os.getenv('APPDATA'), 'npm', 'npm.cmd'),
                os.path.join(os.getenv('ProgramFiles'), 'nodejs', 'npm.cmd'),
                os.path.join(os.getenv('ProgramFiles(x86)'), 'nodejs', 'npm.cmd'),
                os.path.join(os.getenv('LOCALAPPDATA'), 'Programs', 'nodejs', 'npm.cmd'),
            ]
            for location in npm_locations:
                if os.path.exists(location):
                    return location
            npm_cmd = shutil.which('npm.cmd') or shutil.which('npm')
            if npm_cmd:
                return npm_cmd
            raise EnvironmentError(
                "npm not found. Please install Node.js and npm, then add them to your PATH.\n"
                "Download from: https://nodejs.org/"
            )
        else:
            npm_path = shutil.which('npm')
            if not npm_path:
                raise EnvironmentError(
                    "npm not found. Please install Node.js and npm.\n"
                    "On Linux: sudo apt install nodejs npm\n"
                    "On macOS: brew install node"
                )
            return npm_path

    def find_node(self):
        """Find node executable path"""
        if self.is_windows():
            node_locations = [
                os.path.join(os.getenv('ProgramFiles'), 'nodejs', 'node.exe'),
                os.path.join(os.getenv('ProgramFiles(x86)'), 'nodejs', 'node.exe'),
                os.path.join(os.getenv('LOCALAPPDATA'), 'Programs', 'nodejs', 'node.exe'),
            ]
            for location in node_locations:
                if os.path.exists(location):
                    return location
            node_cmd = shutil.which('node.exe') or shutil.which('node')
            if node_cmd:
                return node_cmd
            raise EnvironmentError("Node.js not found. Please install Node.js")
        else:
            node_path = shutil.which('node')
            if not node_path:
                raise EnvironmentError("Node.js not found")
            return node_path

    def check_prerequisites(self):
        """Check if all required tools are installed"""
        print("Checking prerequisites...")
        try:
            npm_path = self.find_npm()
            node_path = self.find_node()
            print(f"Found npm at: {npm_path}")
            print(f"Found node at: {node_path}")
            client_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'client')
            if not os.path.exists(os.path.join(client_dir, 'node_modules', 'vite')):
                print("Installing Vite locally...")
                subprocess.run(
                    [npm_path, 'install', '--save-dev', 'vite'],
                    cwd=client_dir,
                    check=True,
                    capture_output=True,
                    text=True
                )
                print("Vite installed successfully")
            if not os.path.exists(os.path.join(client_dir, 'node_modules')):
                print("Installing frontend dependencies...")
                subprocess.run(
                    [npm_path, 'install'],
                    cwd=client_dir,
                    check=True,
                    capture_output=True,
                    text=True
                )
                print("Frontend dependencies installed successfully")
        except Exception as e:
            print(f"Error during setup: {e}")
            sys.exit(1)
        return npm_path, node_path

    def run_backend(self):
        python_exe = self.get_python_executable()
        backend_command = [python_exe, 'server/run.py']
        return subprocess.Popen(
            backend_command,
            cwd=os.path.dirname(os.path.abspath(__file__)),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

    def run_frontend(self, npm_path, node_path, use_host=False, prod=False):
        client_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'client')
        try:
            if self.is_windows():
                if prod:
                    command = f'"{npm_path}" run preview'
                    if use_host:
                        command += ' -- --host'
                else:
                    command = f'"{npm_path}" run dev'
                    if use_host:
                        command += ' -- --host'
                return subprocess.Popen(
                    command,
                    cwd=client_dir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    shell=True,
                    env={
                        **os.environ,
                        'NODE_ENV': 'production' if prod else 'development',
                        'FORCE_COLOR': '1'
                    }
                )
            else:
                if prod:
                    command = [npm_path, 'run', 'preview']
                    if use_host:
                        command.extend(['--', '--host'])
                else:
                    command = [npm_path, 'run', 'dev']
                    if use_host:
                        command.extend(['--', '--host'])
                return subprocess.Popen(
                    command,
                    cwd=client_dir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    env={
                        **os.environ,
                        'NODE_ENV': 'production' if prod else 'development',
                        'FORCE_COLOR': '1'
                    }
                )
        except Exception as e:
            print(f"Error starting frontend: {e}")
            raise

    @staticmethod
    def clean_output(text):
        replacements = {
            'âžœ': '→',
            '➜': '→',
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    @staticmethod
    def print_separator():
        print("\n" + "=" * 50 + "\n")

    def monitor_output(self, process, prefix):
        
        
        output_buffer = deque(maxlen=100)
        buffer_lock = threading.Lock()
        
        def format_output(prefix, line, is_error=False):
            timestamp = datetime.now().strftime("%H:%M:%S")
            return f"[{timestamp}][{prefix}] {line}"
        
        def read_stream(stream, is_error=False):
            while True:
                line = stream.readline()
                if not line:
                    break
                line = self.clean_output(line.strip())
                if line:
                    # Detect and highlight port/IP information
                    if prefix == "Frontend" and ("localhost:" in line or "Network: " in line):
                        # Extract and format network information
                        if "Local:" in line:
                            local_match = re.search(r'(https?://\S+)', line)
                            if local_match:
                                print(f"\n➜ Local URL: {local_match.group(1)}")
                        if "Network:" in line:
                            network_match = re.search(r'(https?://\S+)', line)
                            if network_match:
                                print(f"➜ Network URL: {network_match.group(1)}\n")
                    
                    formatted_line = format_output(prefix, line, is_error)
                    with buffer_lock:
                        output_buffer.append(formatted_line)
                        print(formatted_line)
        
        threading.Thread(target=read_stream, args=(process.stdout,), daemon=True).start()
        threading.Thread(target=read_stream, args=(process.stderr, True), daemon=True).start()

    @staticmethod
    def cleanup(backend_process, frontend_process):
        print("\nShutting down servers...")
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()


Run_All()
