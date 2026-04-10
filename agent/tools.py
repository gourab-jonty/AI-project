"""
Jonty Tools Module
Provides action capabilities: calculator, alarms, file operations, etc.
"""

import subprocess
import os
import json
import time
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, List
import logging

logger = logging.getLogger(__name__)


class Tools:
    """Provides action capabilities for Jonty"""
    
    def __init__(self):
        """Initialize tools"""
        self.available_tools = {
            'calculator': self.calculate,
            'alarm': self.set_alarm,
            'open_file': self.open_file,
            'open_app': self.open_app,
            'get_time': self.get_time,
            'get_date': self.get_date,
            'search_files': self.search_files,
            'read_file': self.read_file,
            'list_directory': self.list_directory,
        }
        logger.info("Tools initialized")
    
    def execute(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a tool
        
        Args:
            tool_name: Name of the tool
            **kwargs: Tool arguments
            
        Returns:
            Result dictionary
        """
        if tool_name not in self.available_tools:
            return {
                'success': False,
                'error': f"Unknown tool: {tool_name}",
                'available_tools': list(self.available_tools.keys())
            }
        
        try:
            result = self.available_tools[tool_name](**kwargs)
            return {
                'success': True,
                'tool': tool_name,
                'result': result
            }
        except Exception as e:
            logger.error(f"Tool error ({tool_name}): {e}")
            return {
                'success': False,
                'tool': tool_name,
                'error': str(e)
            }
    
    def calculate(self, expression: str) -> str:
        """
        Perform calculation
        
        Args:
            expression: Math expression (e.g., "2 + 2 * 3")
            
        Returns:
            Result string
        """
        try:
            # Safe evaluation - only allow math operations
            allowed_chars = set('0123456789+-*/.() ')
            if not all(c in allowed_chars for c in expression):
                return f"Invalid characters in expression: {expression}"
            
            result = eval(expression)
            return f"{expression} = {result}"
        except Exception as e:
            return f"Calculation error: {str(e)}"
    
    def set_alarm(self, time_str: str, message: str = "Alarm!") -> str:
        """
        Set an alarm (simple implementation)
        
        Args:
            time_str: Time in "HH:MM" format
            message: Alarm message
            
        Returns:
            Status message
        """
        try:
            alarm_time = datetime.strptime(time_str, "%H:%M")
            now = datetime.now()
            
            # If time is in past, assume next day
            if alarm_time.time() < now.time():
                alarm_time = alarm_time.replace(day=now.day + 1)
            
            wait_seconds = (alarm_time - now).total_seconds()
            
            if wait_seconds <= 0:
                return "Time already passed"
            
            # Schedule alarm (in real app, this would be in background)
            return f"✓ Alarm set for {time_str} - {message} (wait: {int(wait_seconds/60)}m)"
        except ValueError:
            return "Invalid time format. Use HH:MM (24-hour format)"
    
    def open_file(self, filepath: str) -> str:
        """
        Open a file with default application
        
        Args:
            filepath: Path to file
            
        Returns:
            Status message
        """
        try:
            filepath = os.path.expanduser(filepath)
            if not os.path.exists(filepath):
                return f"File not found: {filepath}"
            
            # Cross-platform file opening
            if os.name == 'nt':  # Windows
                os.startfile(filepath)
            elif os.name == 'posix':  # Linux/Mac
                subprocess.run(['xdg-open' if os.uname().sysname == 'Linux' else 'open', filepath])
            
            return f"✓ Opening {filepath}"
        except Exception as e:
            return f"Error opening file: {str(e)}"
    
    def open_app(self, app_name: str) -> str:
        """
        Open an application
        
        Args:
            app_name: Application name (e.g., 'firefox', 'gedit')
            
        Returns:
            Status message
        """
        try:
            if os.name == 'nt':  # Windows
                subprocess.Popen(app_name)
            else:  # Linux/Mac
                subprocess.Popen(app_name)
            
            return f"✓ Launching {app_name}"
        except Exception as e:
            return f"Error launching app: {str(e)}"
    
    def get_time(self) -> str:
        """Get current time"""
        return datetime.now().strftime("%H:%M:%S")
    
    def get_date(self) -> str:
        """Get current date"""
        return datetime.now().strftime("%A, %B %d, %Y")
    
    def search_files(self, pattern: str, directory: str = "~") -> List[str]:
        """
        Search for files matching pattern
        
        Args:
            pattern: File name pattern (glob)
            directory: Search directory
            
        Returns:
            List of matching files
        """
        try:
            import glob
            directory = os.path.expanduser(directory)
            pattern_path = os.path.join(directory, f"**/{pattern}")
            
            results = glob.glob(pattern_path, recursive=True)
            return results[:20]  # Limit results
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []
    
    def read_file(self, filepath: str, lines: Optional[int] = None) -> str:
        """
        Read file contents
        
        Args:
            filepath: Path to file
            lines: Number of lines to read (None = all)
            
        Returns:
            File contents
        """
        try:
            filepath = os.path.expanduser(filepath)
            if not os.path.exists(filepath):
                return f"File not found: {filepath}"
            
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                if lines:
                    content = ''.join([f.readline() for _ in range(lines)])
                else:
                    content = f.read()
            
            # Truncate if too long
            if len(content) > 5000:
                content = content[:5000] + "\n... (truncated)"
            
            return content
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def list_directory(self, directory: str = ".") -> List[str]:
        """
        List directory contents
        
        Args:
            directory: Directory path
            
        Returns:
            List of items
        """
        try:
            directory = os.path.expanduser(directory)
            if not os.path.isdir(directory):
                return [f"Not a directory: {directory}"]
            
            items = []
            for item in os.listdir(directory)[:20]:  # Limit items
                full_path = os.path.join(directory, item)
                if os.path.isdir(full_path):
                    items.append(f"📁 {item}/")
                else:
                    items.append(f"📄 {item}")
            
            return items
        except Exception as e:
            return [f"Error listing directory: {str(e)}"]
    
    def get_all_tools_info(self) -> str:
        """Return formatted info about all available tools"""
        info = "AVAILABLE TOOLS:\n"
        
        tools_desc = {
            'calculator': 'Calculate math expressions: calculate(expression="2 + 2 * 3")',
            'alarm': 'Set alarm: set_alarm(time_str="14:30", message="Meeting reminder")',
            'open_file': 'Open file: open_file(filepath="~/Documents/file.pdf")',
            'open_app': 'Launch app: open_app(app_name="firefox")',
            'get_time': 'Get current time: get_time()',
            'get_date': 'Get current date: get_date()',
            'search_files': 'Search files: search_files(pattern="*.pdf", directory="~")',
            'read_file': 'Read file: read_file(filepath="~/file.txt", lines=10)',
            'list_directory': 'List files: list_directory(directory="~")',
        }
        
        for tool, desc in tools_desc.items():
            info += f"- {tool}: {desc}\n"
        
        return info
