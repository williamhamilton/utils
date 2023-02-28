# ---------------------------------------------------------------------------------------------------------------------
# get_chrome_version.py
# Description: returns Chrome version or major version
# Created 19/2/23
# Author: William Hamilton
# Last Updated:
# Author:
# Suggestions:
#
#
# ---------------------------------------------------------------------------------------------------------------------

import re
import subprocess
import platform


def get_chrome_version():
    """
        Returns the version number of the Google Chrome browser installed on the system, or None if it is not found.
        On Windows, this function first checks the registry for the Chrome version, and if that fails, checks the file system.
        On macOS, this function checks the file system for the Chrome version.

        Returns:
            A string representing the version number of the Chrome browser, in the format 'major.minor.build.patch', or None if the version is not found.
        """
    system = platform.system()
    if system == 'Windows':
        # Check the registry for the Chrome version on Windows
        try:
            result = subprocess.run(['reg', 'query', r'HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon', '/v', 'version'],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
            match = re.search(r'\d+\.\d+\.\d+\.\d+', result.stdout)
            if match:
                return match.group(0)
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        # Check the file system for the Chrome version on Windows
        try:
            output = subprocess.check_output(['wmic', 'datafile',
                                              'where', 'name="C:\\\\Program Files (x86)\\\\Google\\\\Chrome\\\\Application\\\\chrome.exe" get Version'])
            match = re.search(r'\d+\.\d+\.\d+\.\d+', output.decode('utf-8'))
            if match:
                return match.group(0)
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
    elif system == 'Darwin':
        # Check the file system for the Chrome version on macOS
        try:
            output = subprocess.check_output(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'])
            match = re.search(r'\d+\.\d+\.\d+\.\d+', output.decode('utf-8'))
            if match:
                return match.group(0)
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

    # Chrome version not found
    return None

def get_chrome_major_version():
    chrome_version = get_chrome_version()
    chrome_major_version = chrome_version.split('.')[0]

    return chrome_major_version

if __name__ == "__main__":
    chrome_version = get_chrome_version()
    if chrome_version:
        print(f"Chrome version: {chrome_version}")
        print(f"Major Chrome version: {chrome_version.split('.')[0]}")
        print(get_chrome_major_version())
    else:
        print("Chrome not found")
