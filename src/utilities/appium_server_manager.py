import subprocess
import time
import logging
from typing import List

logger = logging.getLogger(__name__)

class AppiumServerManager:
    def __init__(self, base_port: int = 4723, host: str = "127.0.0.1"):
        self.base_port = base_port
        self.host = host
        self.servers: List[subprocess.Popen] = []

    def start_server(self, port: int = None) -> int:
        """Start an Appium server on the specified port."""
        if port is None:
            port = self.base_port
        cmd = [
            "appium",
            "--port", str(port),
            "--address", self.host,
            "--log-level", "info",
            "--log", f"logs/appium_{port}.log"
        ]
        try:
            server = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.servers.append(server)
            logger.info(f"Started Appium server on {self.host}:{port}")
            return port
        except Exception as e:
            logger.error(f"Failed to start Appium server on port {port}: {str(e)}")
            raise

    def stop_all_servers(self):
        """Stop all running Appium servers."""
        for server in self.servers:
            if server.poll() is None:  # If server is still running
                server.terminate()
                try:
                    server.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    server.kill()
                logger.info("Stopped Appium server")

    def wait_for_server(self, port: int, timeout: int = 30) -> bool:
        """Wait for the Appium server to be ready."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                with subprocess.Popen(["nc", "-z", self.host, str(port)]):
                    return True
            except:
                time.sleep(1)
        return False