# src/utilities/emulator_manager.py
import os
import subprocess
import time
import logging
import socket
from typing import List, Optional, Tuple

logger = logging.getLogger(__name__)

class EmulatorManager:
    def __init__(self):
        self.emulators: List[str] = []
        self.fixed_system_ports = [5554, 5556]  # Fixed ports for emulators
        self.processes = []  # Track emulator processes

    def _check_avd_exists(self, avd_name: str) -> bool:
        """Check if the specified AVD exists."""
        try:
            result = subprocess.run(
                ["emulator", "-list-avds"], capture_output=True, text=True
            )
            available_avds = result.stdout.splitlines()
            if avd_name not in available_avds:
                logger.error(f"AVD '{avd_name}' not found. Available AVDs: {available_avds}")
                return False
            return True
        except Exception as e:
            logger.error(f"Failed to check AVD list: {str(e)}")
            return False

    def _check_port_available(self, port: int) -> bool:
        """Check if the specified port is available and kill any conflicting emulator process."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("localhost", port))
                return True
            except socket.error as e:
                logger.warning(f"Port {port} is already in use, attempting to free it: {str(e)}")
                try:
                    result = subprocess.run(
                        ["lsof", "-i", f":{port}"], capture_output=True, text=True
                    )
                    if result.stdout:
                        lines = result.stdout.splitlines()
                        for line in lines[1:]:  # Skip header
                            pid = line.split()[1]  # Extract PID
                            subprocess.run(["kill", "-9", pid], check=True)
                            logger.info(f"Killed process {pid} using port {port}")
                    # Retry binding after killing
                    time.sleep(1)  # Give the system a moment to release the port
                    s.bind(("localhost", port))
                    return True
                except subprocess.CalledProcessError as e:
                    logger.error(f"Failed to free port {port}: {str(e)}")
                    return False

    def _restart_adb_server(self) -> bool:
        """Restart the ADB server safely."""
        try:
            # Stop the ADB server
            subprocess.run(["adb", "kill-server"], check=True)
            logger.info("Stopped ADB server")
        except subprocess.CalledProcessError as e:
            logger.warning(f"Failed to stop ADB server (might not be running): {str(e)}")

        try:
            # Start the ADB server
            result = subprocess.run(
                ["adb", "start-server"], capture_output=True, text=True, check=True
            )
            logger.info("Started ADB server")
            logger.debug(f"ADB start-server output: {result.stdout}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to start ADB server: {str(e)}")
            logger.error(f"ADB start-server stderr: {e.stderr}")
            return False

    def start_emulator(self, avd_name: str, index: int) -> Tuple[str, int]:
        """Start an Android emulator with a fixed system port and return UDID and system port."""
        if index >= len(self.fixed_system_ports):
            raise ValueError(f"Maximum number of emulators exceeded. Only {len(self.fixed_system_ports)} supported.")

        # Check if the AVD exists
        if not self._check_avd_exists(avd_name):
            raise ValueError(f"Cannot start emulator: AVD '{avd_name}' does not exist.")

        system_port = self.fixed_system_ports[index]

        # Check if the port is available
        if not self._check_port_available(system_port):
            raise RuntimeError(f"Cannot start emulator on port {system_port}: port remains in use after cleanup attempt")

        cmd = [
            "emulator",
            "-avd", avd_name,
            "-port", str(system_port),
            "-no-snapshot",
            "-no-audio",
            "-wipe-data",
            "-no-boot-anim",
            "-gpu", "swiftshader_indirect"
        ]
        try:
            # Start emulator without waiting for output
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            logger.info(f"Started emulator {avd_name} on system port {system_port} with PID {process.pid}")
            self.processes.append(process)  # Track the process for cleanup
            udid = f"emulator-{system_port}"
            self.emulators.append(udid)

            # Wait for emulator to boot and verify it’s connected via ADB
            start_time = time.time()
            timeout = 180  # Timeout of 180 seconds
            max_attempts = 3  # Retry ADB detection up to 3 times
            attempt = 0
            while time.time() - start_time < timeout and attempt < max_attempts:
                cmd = f"adb devices | grep {udid}"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if udid in result.stdout:
                    # Additional check: ensure the device is fully booted
                    boot_check = subprocess.run(
                        f"adb -s {udid} shell getprop sys.boot_completed",
                        shell=True, capture_output=True, text=True
                    )
                    if boot_check.stdout.strip() == "1":
                        logger.info(f"Emulator {udid} detected by ADB and fully booted")
                        break
                    logger.debug(f"Emulator {udid} detected by ADB but not fully booted yet")
                else:
                    attempt += 1
                    logger.debug(f"Emulator {udid} not detected by ADB (attempt {attempt}/{max_attempts})")
                    if attempt < max_attempts:
                        # Restart ADB server to resolve detection issues
                        if not self._restart_adb_server():
                            logger.warning("ADB server restart failed, continuing anyway")
                        time.sleep(5)  # Wait for ADB to stabilize
                time.sleep(5)
            else:
                # Log emulator output for debugging
                stdout, stderr = process.communicate(timeout=10)
                logger.error(f"Emulator stdout: {stdout}")
                logger.error(f"Emulator stderr: {stderr}")
                raise RuntimeError(f"Emulator {udid} failed to boot within {timeout} seconds after {max_attempts} attempts")
            return udid, system_port
        except Exception as e:
            logger.error(f"Failed to start emulator {avd_name}: {str(e)}")
            raise

    def stop_all_emulators(self):
        """Stop all running emulators."""
        for udid in self.emulators:
            try:
                subprocess.run(["adb", "-s", udid, "emu", "kill"], check=True)
                logger.info(f"Stopped emulator {udid}")
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to stop emulator {udid}: {str(e)}")
        # Terminate any tracked processes
        for process in self.processes:
            if process.poll() is None:  # Process is still running
                process.terminate()
                process.wait(timeout=5)
                logger.info(f"Terminated emulator process with PID {process.pid}")