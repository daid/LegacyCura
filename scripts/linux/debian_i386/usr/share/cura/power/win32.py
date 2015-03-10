# coding=utf-8
"""
Implements PowerManagement functions using GetSystemPowerStatus.
Requires Windows XP+.
Observing is not supported
"""
__author__ = 'kulakov.ilya@gmail.com'

from ctypes import Structure, wintypes, POINTER, windll, WinError, pointer, WINFUNCTYPE
import warnings
from power import common


# GetSystemPowerStatus
# Returns brief description of current system power status.
# Windows XP+
# REQUIRED.
GetSystemPowerStatus = None
try:
    GetSystemPowerStatus = windll.kernel32.GetSystemPowerStatus

    class SYSTEM_POWER_STATUS(Structure):
        _fields_ = [
            ('ACLineStatus', wintypes.c_ubyte),
            ('BatteryFlag', wintypes.c_ubyte),
            ('BatteryLifePercent', wintypes.c_ubyte),
            ('Reserved1', wintypes.c_ubyte),
            ('BatteryLifeTime', wintypes.DWORD),
            ('BatteryFullLifeTime', wintypes.DWORD)
            ]

    GetSystemPowerStatus.argtypes = [POINTER(SYSTEM_POWER_STATUS)]
    GetSystemPowerStatus.restype = wintypes.BOOL
except AttributeError as e:
    raise RuntimeError("Unable to load GetSystemPowerStatus."
                       "The system does not provide it (Win XP is required) or kernel32.dll is damaged.")


POWER_TYPE_MAP = {
    0: common.POWER_TYPE_BATTERY,
    1: common.POWER_TYPE_AC,
    255: common.POWER_TYPE_AC
}


class PowerManagement(common.PowerManagementBase):
    def get_providing_power_source_type(self):
        """
        Returns GetSystemPowerStatus().ACLineStatus

        @raise: WindowsError if any underlying error occures.
        """
        power_status = SYSTEM_POWER_STATUS()
        if not GetSystemPowerStatus(pointer(power_status)):
            raise WinError()
        return POWER_TYPE_MAP[power_status.ACLineStatus]

    def get_low_battery_warning_level(self):
        """
        Returns warning according to GetSystemPowerStatus().BatteryLifeTime/BatteryLifePercent

        @raise WindowsError if any underlying error occures.
        """
        power_status = SYSTEM_POWER_STATUS()
        if not GetSystemPowerStatus(pointer(power_status)):
            raise WinError()

        if POWER_TYPE_MAP[power_status.ACLineStatus] == common.POWER_TYPE_AC:
            return common.LOW_BATTERY_WARNING_NONE
        else:
            if power_status.BatteryLifeTime != -1 and power_status.BatteryLifeTime <= 600:
                return common.LOW_BATTERY_WARNING_FINAL
            elif power_status.BatteryLifePercent <= 22:
                return common.LOW_BATTERY_WARNING_EARLY
            else:
                return common.LOW_BATTERY_WARNING_NONE

    def get_time_remaining_estimate(self):
        """
        Returns time remaining estimate according to GetSystemPowerStatus().BatteryLifeTime
        """
        power_status = SYSTEM_POWER_STATUS()
        if not GetSystemPowerStatus(pointer(power_status)):
            raise WinError()

        if POWER_TYPE_MAP[power_status.ACLineStatus] == common.POWER_TYPE_AC:
            return common.TIME_REMAINING_UNLIMITED
        elif power_status.BatteryLifeTime == -1:
            return common.TIME_REMAINING_UNKNOWN
        else:
            return float(power_status.BatteryLifeTime) / 60.0

    def add_observer(self, observer):
        warnings.warn("Current system does not support observing.")
        pass

    def remove_observer(self, observer):
        warnings.warn("Current system does not support observing.")
        pass
