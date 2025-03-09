
# AppiumFramework/src/drivers/driver_class.py

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.appium_service import AppiumService
from src.utilities.custom_logger import CustomLogger
import os
import socket
import time
import requests
import threading

logger = CustomLogger.get_logger(__name__)

class Driver:
    _thread_local = threading.local()

    def __init__(self, appium_port_base=4723, system_port_base=8200, udid=None, apk_path=None):
        self.appium_host = os.getenv("APPIUM_HOST", "127.0.0.1")
        self.appium_port = self.find_free_port(appium_port_base)
        self.system_port = self.find_free_port(system_port_base)
        self.udid = udid
        self.apk_path = os.getenv("APK_PATH", "/path/to/Android_Demo_app.apk")
        # Ensure capabilities are valid
        self.apk_path = apk_path or os.getenv("APK_PATH",
                                              "/Users/princeitam/Desktop/NewAppiumTestProject/tests/resources/Android_Demo_App.apk")
        if not os.path.exists(self.apk_path):
            raise ValueError(f"APK path {self.apk_path} does not exist")
        self.capabilities = {
            "platformName": "Android",
            "deviceName": "Android Emulator",
            "app": self.apk_path,
            "automationName": "UiAutomator2",
            "udid": self.udid,
            "systemPort": self.system_port,
            "noReset": True,
            "fullReset": False,
            "autoGrantPermissions": True,
            "appActivity": "com.code2lead.kwad.MainActivity"
        }
        logger.info(f"Initialized Driver with capabilities: {self.capabilities}")

    def _start_appium_service(self):
        if not hasattr(self._thread_local, 'appium_service') or not self._thread_local.appium_service.is_running:
            if self._is_port_in_use(self.appium_port):
                self.appium_port = self.find_free_port(self.appium_port + 1)
            self._thread_local.appium_service = AppiumService()
            self._thread_local.appium_service.start(args=['-p', str(self.appium_port), '-a', self.appium_host])
            logger.info(f"Thread {threading.current_thread().name}: Appium server started on {self.appium_host}:{self.appium_port}")

    def _is_port_in_use(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex((self.appium_host, port)) == 0

    def _is_appium_ready(self, timeout=60):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"http://{self.appium_host}:{self.appium_port}/status")
                if response.status_code == 200:
                    logger.info(f"Thread {threading.current_thread().name}: Appium server is ready!")
                    return True
            except requests.RequestException:
                time.sleep(1)
        raise RuntimeError(f"Appium server did not start within {timeout} seconds")

    def get_driver(self):
        if not hasattr(self._thread_local, 'driver') or self._thread_local.driver is None:
            self._start_appium_service()
            self._is_appium_ready()
            options = UiAutomator2Options()
            try:
                options.load_capabilities(self.capabilities)
            except Exception as e:
                logger.error(f"Failed to load capabilities: {e}")
                raise
            self._thread_local.driver = webdriver.Remote(f"http://{self.appium_host}:{self.appium_port}", options=options)
            logger.info(f"Thread {threading.current_thread().name}: Driver initialized for {self.udid}")
        return self._thread_local.driver

    def stop(self):
        if hasattr(self._thread_local, 'driver') and self._thread_local.driver:
            self._thread_local.driver.quit()
            self._thread_local.driver = None
            logger.info(f"Thread {threading.current_thread().name}: Driver stopped")
        if hasattr(self._thread_local, 'appium_service') and self._thread_local.appium_service.is_running:
            self._thread_local.appium_service.stop()
            logger.info(f"Thread {threading.current_thread().name}: Appium server on port {self.appium_port} stopped")

    @staticmethod
    def find_free_port(start_port):
        port = start_port
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex(("127.0.0.1", port)) != 0:
                    return port
            port += 1