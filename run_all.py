#test commit
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
from colorama import init, Fore, Back, Style


class Run_All:
    def __init__(self):
        init(autoreset=True)
        
        backend_process = None
        frontend_process = None
        
        parser = argparse.ArgumentParser()
        parser.add_argument('--host', action='store_true', help='Run frontend with --host flag')
        parser.add_argument('--prod', action='store_true', help='Run frontend in production mode using npm run preview')
        args = parser.parse_args()
        
        try:
            npm_path, node_path = self.check_prerequisites()
            
            self.print_separator()
            self.print_status("Starting backend server...", "info")
            backend_process = self.run_backend()
            time.sleep(2)

            self.print_separator()
            self.print_status("Starting frontend server...", "info")
            mode = []
            if args.prod:
                mode.append("Production")
            else:
                mode.append("Development")
            if args.host:
                mode.append("Hosted")
                
            self.print_status(f"Frontend Mode: {' + '.join(mode)}", "info")
            
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
                        self.print_status("Backend process exited", "error")
                    if frontend_process.poll() is not None:
                        self.print_status("Frontend process exited", "error")
                        self.print_status("Attempting to restart frontend...", "warning")
                        frontend_process = self.run_frontend(npm_path, node_path, use_host=args.host, prod=args.prod)
                        frontend_thread = Thread(target=self.monitor_output, args=(frontend_process, "Frontend"), daemon=True)
                        frontend_thread.start()
                    time.sleep(1)
            except KeyboardInterrupt:
                self.print_status("\nReceived shutdown signal...", "info")

        except KeyboardInterrupt:
            self.print_status("\nReceived shutdown signal...", "info")
        except Exception as e:
            self.print_status(f"An error occurred: {e}", "error")
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
        self.print_status("Checking prerequisites...", "info")
        try:
            npm_path = self.find_npm()
            node_path = self.find_node()
            self.print_status(f"Found npm at: {npm_path}", "success")
            self.print_status(f"Found node at: {node_path}", "success")
            client_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'client')
            if not os.path.exists(os.path.join(client_dir, 'node_modules', 'vite')):
                self.print_status("Installing Vite locally...", "info")
                subprocess.run(
                    [npm_path, 'install', '--save-dev', 'vite'],
                    cwd=client_dir,
                    check=True,
                    capture_output=True,
                    text=True
                )
                self.print_status("Vite installed successfully", "success")
            if not os.path.exists(os.path.join(client_dir, 'node_modules')):
                self.print_status("Installing frontend dependencies...", "info")
                subprocess.run(
                    [npm_path, 'install'],
                    cwd=client_dir,
                    check=True,
                    capture_output=True,
                    text=True
                )
                self.print_status("Frontend dependencies installed successfully", "success")
        except Exception as e:
            self.print_status(f"Error during setup: {e}", "error")
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
            self.print_status(f"Error starting frontend: {e}", "error")
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

    def format_log_message(self, message):
        """Format and colorize log messages based on type and content"""
        
        # Handle uvicorn/fastapi specific messages
        if 'INFO:' in message:
            if 'Uvicorn' in message:
                return f"{Fore.GREEN}✓ INFO: Server started at {message.split('on')[1].strip()}{Style.RESET_ALL}"
            elif 'Application startup' in message:
                return f"{Fore.GREEN}✓ INFO: {message.split('INFO:')[1].strip()}{Style.RESET_ALL}"
            elif 'Watching for file changes' in message:
                return f"{Fore.GREEN}✓ INFO: {message.split('INFO:')[1].strip()}{Style.RESET_ALL}"
            elif 'Started server process' in message:
                pid = message.split('[')[1].split(']')[0]
                return f"{Fore.GREEN}✓ INFO: Server process initialized [{pid}]{Style.RESET_ALL}"
            elif 'Started reloader process' in message:
                pid = message.split('[')[1].split(']')[0]
                return f"{Fore.GREEN}✓ INFO: Started auto-reload service [{pid}]{Style.RESET_ALL}"
            else:
                return f"{Fore.GREEN}✓ INFO: {message.split('INFO:')[1].strip()}{Style.RESET_ALL}"

        # For scraper messages
        if any(spider in message for spider in ['Amazon.eg', 'ElBadr', 'ALFrensia', 'OLX']):
            return self.format_scraper_message(message)

        # Translate technical messages to human-readable format
        translations = {
            'Will watch for changes in these directories': 'Watching for file changes in',
            'Started reloader process': 'Started auto-reload service',
            'Started server process': 'Server process initialized',
            'Waiting for application startup': 'Initializing application',
            'Application startup complete': 'Server ready',
            'Found': 'Successfully found',
            'Requesting page': 'Searching page',
            'Failed to fetch': 'Failed to access',
            'not found': 'reached end of results',
        }

        # Apply translations
        for tech, human in translations.items():
            if tech in message:
                message = message.replace(tech, human)

        # Add icons for different message types
        icons = {
            'INFO': '✓',
            'ERROR': '✗',
            'WARNING': '⚠',
            'DEBUG': 'ℹ',
        }

        # Color mappings
        colors = {
            'INFO': f"{Fore.GREEN}",
            'ERROR': f"{Fore.RED}",
            'WARNING': f"{Fore.YELLOW}",
            'DEBUG': f"{Fore.CYAN}",
        }

        # Add progress indicators for spider messages
        if 'Spider' in message:
            if 'Searching page' in message:
                message = f"🔍 {message}"
            elif 'Successfully found' in message:
                message = f"📦 {message}"
            elif 'Failed' in message:
                message = f"❌ {message}"

        # Colorize log levels with icons
        for level, color in colors.items():
            if level in message:
                icon = icons.get(level, '')
                message = message.replace(level, f"{color}{icon} {level}{Style.RESET_ALL}")

        # Format spider names
        spiders = {
            'Amazon.eg': f"{Fore.YELLOW}Amazon.eg{Style.RESET_ALL}",
            'ElBadr': f"{Fore.BLUE}ElBadr{Style.RESET_ALL}",
            'ALFrensia': f"{Fore.MAGENTA}ALFrensia{Style.RESET_ALL}",
            'OLX': f"{Fore.CYAN}OLX{Style.RESET_ALL}"
        }
        
        for spider, colored in spiders.items():
            if spider in message:
                message = message.replace(f"[{spider}", f"[{colored}")

        # Format HTTP responses
        if 'HTTP' in message:
            status_match = re.search(r'(\d{3}) (OK|ERROR)', message)
            if status_match:
                code, status = status_match.groups()
                if code.startswith('2'):
                    message = f"✓ API Request successful ({Fore.GREEN}{code}{Style.RESET_ALL})"
                elif code.startswith('4'):
                    message = f"⚠ API Request failed ({Fore.YELLOW}{code}{Style.RESET_ALL})"
                elif code.startswith('5'):
                    message = f"✗ Server error ({Fore.RED}{code}{Style.RESET_ALL})"

        # Highlight URLs
        urls = re.findall(r'(https?://\S+)', message)
        for url in urls:
            message = message.replace(url, f"{Fore.CYAN}{url}{Style.RESET_ALL}")

        return message

    def format_scraper_message(self, message):
        """Special formatting for scraper messages"""
        # Spider name formatting
        spiders = {
            'Amazon.eg': (Fore.YELLOW, '🛒'),
            'ElBadr': (Fore.BLUE, '🏪'),
            'ALFrensia': (Fore.MAGENTA, '🏬'),
            'OLX': (Fore.CYAN, '📦')
        }
        
        formatted = message

        # Extract spider name
        spider_name = next((name for name in spiders.keys() if name in message), None)
        if spider_name:
            color, icon = spiders[spider_name]
            # Clean up the message format
            formatted = formatted.replace(f"INFO:scrapers.{spider_name.lower()}.{spider_name.lower()}_spyder:", '')
            formatted = formatted.replace(f"ERROR:scrapers.{spider_name.lower()}.{spider_name.lower()}_spyder:", '')
            formatted = formatted.replace(f"[ {spider_name} Spider ]", f"{icon} {color}{spider_name}{Style.RESET_ALL}")

        # Format different message types
        if "Searching page" in formatted:
            formatted = formatted.replace("Searching page", f"{Fore.CYAN}Scanning page{Style.RESET_ALL}")
            formatted = re.sub(r'(page \d+)', f"{Fore.WHITE}\\1{Style.RESET_ALL}", formatted)
        elif "Successfully found" in formatted:
            match = re.search(r'Successfully found (\d+)', formatted)
            if match:
                count = match.group(1)
                formatted = f"Found {Fore.GREEN}{count}{Style.RESET_ALL} items"
        elif "Failed to access" in formatted:
            formatted = formatted.replace("Failed to access", f"{Fore.RED}Failed{Style.RESET_ALL}")
            if "503" in formatted:
                formatted += f" ({Fore.RED}server error{Style.RESET_ALL})"
        elif "reached end of results" in formatted:
            page = re.search(r'Page (\d+)', formatted)
            if page:
                formatted = f"{Fore.YELLOW}Reached last page ({page.group(1)}){Style.RESET_ALL}"

        # Clean up URLs
        urls = re.findall(r'(https?://\S+)', formatted)
        for url in urls:
            short_url = re.sub(r'https?://(www\.)?', '', url)
            short_url = re.sub(r'\?.+$', '', short_url)
            formatted = formatted.replace(url, f"{Fore.CYAN}{short_url}{Style.RESET_ALL}")

        return formatted.strip()

    def format_output(self, prefix, line, is_error=False):
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix_color = Fore.RED if is_error else (Fore.BLUE if prefix == "Backend" else Fore.GREEN)
        
        # Add service icons
        service_icon = "🖥️ " if prefix == "Backend" else "🌐 "
        
        formatted = f"{Fore.WHITE}[{timestamp}]{Style.RESET_ALL} {service_icon}[{prefix_color}{prefix}{Style.RESET_ALL}] "
        formatted += self.format_log_message(line)
        return formatted

    def print_separator(self):
        print(f"\n{Fore.BLUE}{'='*50}{Style.RESET_ALL}\n")

    def print_status(self, message, status="info"):
        colors = {
            "info": Fore.BLUE,
            "success": Fore.GREEN,
            "error": Fore.RED,
            "warning": Fore.YELLOW
        }
        color = colors.get(status, Fore.WHITE)
        print(f"{color}➜ {message}{Style.RESET_ALL}")

    def monitor_output(self, process, prefix):
        output_buffer = deque(maxlen=100)
        buffer_lock = threading.Lock()
        
        def read_stream(stream, is_error=False):
            while True:
                line = stream.readline()
                if not line:
                    break
                line = self.clean_output(line.strip())
                if line:
                    # Special handling for server URLs
                    if "Local:" in line or "Network:" in line:
                        if "Local:" in line:
                            local_match = re.search(r'(https?://\S+)', line)
                            if local_match:
                                self.print_status(f"🌐 Development server ready at {local_match.group(1)}", "success")
                        if "Network:" in line:
                            network_match = re.search(r'(https?://\S+)', line)
                            if network_match:
                                self.print_status(f"🔗 Network access URL: {network_match.group(1)}", "success")
                        continue

                    formatted_line = self.format_output(prefix, line, is_error)
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
