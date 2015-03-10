# coding=utf-8
"""
Implements PowerManagement functions using FreeBSD SYSCTL mechanism. 
FreeBSD portion written by Tomasz CEDRO (http://www.tomek.cedro.info)
"""
__author__ = 'cederom@tlen.pl'

import os
import warnings
from power import common
import subprocess

class PowerManagement(common.PowerManagementBase):
    @staticmethod
    def power_source_type():
        """
        FreeBSD use sysctl hw.acpi.acline to tell if Mains (1) is used or Battery (0).
        Beware, that on a Desktop machines this hw.acpi.acline oid may not exist.
        @return: One of common.POWER_TYPE_*
        @raise: Runtime error if type of power source is not supported
        """
        try:
            supply=int(subprocess.check_output(["sysctl","-n","hw.acpi.acline"]))
        except:
            return common.POWER_TYPE_AC
 
        if supply == 1:
            return common.POWER_TYPE_AC
        elif supply == 0:
            return common.POWER_TYPE_BATTERY
        else:
            raise RuntimeError("Unknown power source type!")


    @staticmethod
    def is_ac_online():
        """
        @return: True if ac is online. Otherwise False
        """
        try:
            supply=int(subprocess.check_output(["sysctl","-n","hw.acpi.acline"]))
        except:
            return True
        return supply == 1


    @staticmethod
    def is_battery_present():
        """
        TODO
        @return: True if battery is present. Otherwise False
        """
        return False


    @staticmethod
    def is_battery_discharging():
        """
        TODO
        @return: True if ac is online. Otherwise False
        """
        return False


    @staticmethod
    def get_battery_state():
        """
        TODO
        @return: Tuple (energy_full, energy_now, power_now)
        """
        energy_now = float(100.0)
        power_now = float(100.0)
        energy_full = float(100.0)
        return energy_full, energy_now, power_now


    def get_providing_power_source_type(self):
        """
        Looks through all power supplies in POWER_SUPPLY_PATH.
        If there is an AC adapter online returns POWER_TYPE_AC.
        If there is a discharging battery, returns POWER_TYPE_BATTERY.
        Since the order of supplies is arbitrary, whatever found first is returned.
        """
        type = self.power_source_type()
        if type == common.POWER_TYPE_AC:
            if self.is_ac_online():
                return common.POWER_TYPE_AC
            elif type == common.POWER_TYPE_BATTERY:
                if self.is_battery_present() and self.is_battery_discharging():
                    return common.POWER_TYPE_BATTERY
                else:
                    warnings.warn("UPS is not supported.")
        return common.POWER_TYPE_AC


    def get_low_battery_warning_level(self):
        """
        Looks through all power supplies in POWER_SUPPLY_PATH.
        If there is an AC adapter online returns POWER_TYPE_AC returns LOW_BATTERY_WARNING_NONE.
        Otherwise determines total percentage and time remaining across all attached batteries.
        """
        all_energy_full = []
        all_energy_now = []
        all_power_now = []
        try:
            type = self.power_source_type()
            if type == common.POWER_TYPE_AC:
                if self.is_ac_online():
                    return common.LOW_BATTERY_WARNING_NONE
            elif type == common.POWER_TYPE_BATTERY:
                if self.is_battery_present() and self.is_battery_discharging():
                    energy_full, energy_now, power_now = self.get_battery_state()
                    all_energy_full.append(energy_full)
                    all_energy_now.append(energy_now)
                    all_power_now.append(power_now)
            else:
                warnings.warn("UPS is not supported.")
        except (RuntimeError, IOError) as e:
            warnings.warn("Unable to read system power information!")

        try:
            total_percentage = sum(all_energy_full) / sum(all_energy_now)
            total_time = sum([energy_now / power_now * 60.0 for energy_now, power_now in zip(all_energy_now, all_power_now)])
            if total_time <= 10.0:
                return common.LOW_BATTERY_WARNING_FINAL
            elif total_percentage <= 22.0:
                return common.LOW_BATTERY_WARNING_EARLY
            else:
                return common.LOW_BATTERY_WARNING_NONE
        except ZeroDivisionError as e:
            warnings.warn("Unable to calculate low battery level: {error}".format(error=str(e)))
            return common.LOW_BATTERY_WARNING_NONE


    def get_time_remaining_estimate(self):
        """
        Looks through all power sources and returns total time remaining estimate
        or TIME_REMAINING_UNLIMITED if ac power supply is online.
        """
        all_energy_now = []
        all_power_now = []
        try:
            type = self.power_source_type()
            if type == common.POWER_TYPE_AC:
                if self.is_ac_online(supply_path):
                    return common.TIME_REMAINING_UNLIMITED
            elif type == common.POWER_TYPE_BATTERY:
                if self.is_battery_present() and self.is_battery_discharging():
                    energy_full, energy_now, power_now = self.get_battery_state()
                    all_energy_now.append(energy_now)
                    all_power_now.append(power_now)
            else:
                warnings.warn("UPS is not supported.")
        except (RuntimeError, IOError) as e:
            warnings.warn("Unable to read system power information!")

        if len(all_energy_now) > 0:
            try:
                return sum([energy_now / power_now * 60.0 for energy_now, power_now in zip(all_energy_now, all_power_now)])
            except ZeroDivisionError as e:
                warnings.warn("Unable to calculate time remaining estimate: {error}".format(error=str(e)))
                return common.TIME_REMAINING_UNKNOWN
        else:
            return common.TIME_REMAINING_UNKNOWN


    def add_observer(self, observer):
        warnings.warn("Current system does not support observing.")
        pass


    def remove_observer(self, observer):
        warnings.warn("Current system does not support observing.")
        pass
