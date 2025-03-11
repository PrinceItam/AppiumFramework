# AppiumFramework/tests/conftest.py

import os
import threading
import pytest
import pytest_html
import subprocess
import time
from datetime import datetime
from pathlib import Path
from src.utilities.custom_logger import CustomLogger
from src.drivers.driver_class import Driver
import allure

logger = CustomLogger.get_logger(__name__)

# Current directory of conftest.py
CURDIR = Path(__file__).parent
APK_PATH = CURDIR / "resources" / "Android_Demo_App.apk"

@pytest.fixture(scope="session", autouse=True)
def emulator_session():
    result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
    devices = [line.split('\t')[0] for line in result.stdout.splitlines() if '\t' in line]
    if devices:
        udid = devices[0]
        logger.info(f"Using existing emulator: {udid}")
        subprocess.run(['adb', '-s', udid, 'wait-for-device'], check=False)
    else:
        avd_name = os.getenv("AVD_NAME", "Emulator-5556")
        emulator_port = Driver.find_free_port(5554)
        logger.info(f"Starting emulator {avd_name} on port {emulator_port}")
        process = subprocess.Popen(
            ['emulator', '-avd', avd_name, '-port', str(emulator_port), '-no-snapshot', '-wipe-data'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        udid = f"emulator-{emulator_port}"
        start_time = time.time()
        timeout = 60
        while time.time() - start_time < timeout:
            result = subprocess.run(['adb', '-s', udid, 'shell', 'getprop', 'sys.boot_completed'],
                                    capture_output=True, text=True)
            if result.stdout.strip() == "1":
                logger.info(f"Emulator {udid} booted successfully")
                break
            time.sleep(2)
        else:
            process.terminate()
            raise RuntimeError(f"Emulator {udid} failed to start within {timeout} seconds")

    yield udid
    subprocess.run(['adb', '-s', udid, 'emu', 'kill'], check=False)
    logger.info(f"Emulator {udid} terminated")

@pytest.fixture(scope="class")
def driver(emulator_session, pytestconfig):
    logger.info(f"Setting up driver for UDID: {emulator_session}")
    apk_path = pytestconfig.getoption("--apk-path") or os.getenv("APK_PATH", str(APK_PATH))
    worker_id = os.environ.get('PYTEST_XDIST_WORKER', 'master')
    port_offset = int(worker_id.replace('gw', '')) if worker_id != 'master' else 0
    driver_obj = Driver(
        appium_port_base=4723 + port_offset,
        system_port_base=8200 + port_offset,
        udid=emulator_session
    )
    driver_obj.apk_path = apk_path
    driver_instance = driver_obj.get_driver()  # No try-except here, let it raise directly
    logger.info(f"Driver initialized successfully for {emulator_session}")
    yield driver_instance
    driver_obj.stop()
    logger.info(f"Driver stopped for {emulator_session}")

@pytest.fixture(autouse=True)
def method_setup(request):
    test_name = request.node.name
    logger.info(f"Thread {threading.current_thread().name}: Starting test: {test_name}")
    yield
    logger.info(f"Thread {threading.current_thread().name}: Finished test: {test_name}")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed and hasattr(item, "instance") and hasattr(item.instance, "driver"):
        try:
            from src.pages.base_page import BasePage
            page = BasePage(item.instance.driver)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"failure_{item.name}_{timestamp}"
            screenshot_path = page.screen_shot(screenshot_name)
            if screenshot_path and os.path.exists(screenshot_path):
                logger.error(f"Test {item.name} failed. Screenshot saved: {screenshot_path}")
                with open(screenshot_path, "rb") as image_file:
                    allure.attach(image_file.read(), name="Screenshot", attachment_type=allure.attachment_type.PNG)
                if "html" in item.config.pluginmanager.list_name_plugin():
                    if not hasattr(report, 'extra'):
                        report.extra = []
                    report.extra.append(pytest_html.extras.image(screenshot_path))
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")

def pytest_addoption(parser):
    parser.addoption("--apk-path", action="store", default=None, help="Path to the APK file")