# coding=utf-8
"""
Implements PowerManagement functions using /sys/class/power_supply/*
See doc/linux for platform-specific details.
"""
__author__ = 'kulakov.ilya@gmail.com'

import os
import warnings
from power import common


POWER_SUPPLY_PATH = '/sys/class/power_supply'


if not os.access(POWER_SUPPLY_PATH, os.R_OK):
    raise RuntimeError("Unable to read {path}.".format(path=POWER_SUPPLY_PATH))


class PowerManagement(common.PowerManagementBase):
    @staticmethod
    def power_source_type(supply_path):
        """
        @param supply_path: Path to power supply
        @return: One of common.POWER_TYPE_*
        @raise: Runtime error if type of power source is not supported
        """
        with open(os.path.join(supply_path, 'type'), 'r') as type_file:
            type = type_file.readline().strip()
            if type == 'Mains':
                return common.POWER_TYPE_AC
            elif type == 'UPS':
                return common.POWER_TYPE_UPS
            elif type == 'Battery':
                return common.POWER_TYPE_BATTERY
            else:
                raise RuntimeError("Type of {path} ({type}) is not supported".format(path=supply_path, type=type))

    @staticmethod
    def is_ac_online(supply_path):
        """
        @param supply_path: Path to power supply
        @return: True if ac is online. Otherwise False
        """
        with open(os.path.join(supply_path, 'online'), 'r') as online_file:
            return online_file.readline().strip() == '1'

    @staticmethod
    def is_battery_present(supply_path):
        """
        @param supply_path: Path to power supply
        @return: True if battery is present. Otherwise False
        """
        with open(os.path.join(supply_path, 'present'), 'r') as present_file:
            return present_file.readline().strip() == '1'

    @staticmethod
    def is_battery_discharging(supply_path):
        """
        @param supply_path: Path to power supply
        @return: True if ac is online. Otherwise False
        """
        with open(os.path.join(supply_path, 'status'), 'r') as status_file:
            return status_file.readline().strip() == 'Discharging'

    @staticmethod
    def get_battery_state(supply_path):
        """
        @param supply_path: Path to power supply
        @return: Tuple (energy_full, energy_now, power_now)
        """
        with open(os.path.join(supply_path, 'energy_now'), 'r') as energy_now_file:
            with open(os.path.join(supply_path, 'power_now'), 'r') as power_now_file:
                with open(os.path.join(supply_path, 'energy_full'), 'r') as energy_full_file:
                    energy_now = float(energy_now_file.readline().strip())
                    power_now = float(power_now_file.readline().strip())
                    energy_full = float(energy_full_file.readline().strip())
                    return energy_full, energy_now, power_now

    def get_providing_power_source_type(self):
        """
        Looks through all power supplies in POWER_SUPPLY_PATH.
        If there is an AC adapter online returns POWER_TYPE_AC.
        If there is a discharging battery, returns POWER_TYPE_BATTERY.
        Since the order of supplies is arbitrary, whatever found first is returned.
        """
        for supply in os.listdir(POWER_SUPPLY_PATH):
            supply_path = os.path.join(POWER_SUPPLY_PATH, supply)
            try:
                type = self.power_source_type(supply_path)
                if type == common.POWER_TYPE_AC:
                    if self.is_ac_online(supply_path):
                        return common.POWER_TYPE_AC
                elif type == common.POWER_TYPE_BATTERY:
                    if self.is_battery_present(supply_path) and self.is_battery_discharging(supply_path):
                        return common.POWER_TYPE_BATTERY
                else:
                    warnings.warn("UPS is not supported.")
            except (RuntimeError, IOError) as e:
                warnings.warn("Unable to read properties of {path}: {error}".format(path=supply_path, error=str(e)))

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
        for supply in os.listdir(POWER_SUPPLY_PATH):
            supply_path = os.path.join(POWER_SUPPLY_PATH, supply)
            try:
                type = self.power_source_type(supply_path)
                if type == common.POWER_TYPE_AC:
                    if self.is_ac_online(supply_path):
                        return common.LOW_BATTERY_WARNING_NONE
                elif type == common.POWER_TYPE_BATTERY:
                    if self.is_battery_present(supply_path) and self.is_battery_discharging(supply_path):
                        energy_full, energy_now, power_now = self.get_battery_state(supply_path)
                        all_energy_full.append(energy_full)
                        all_energy_now.append(energy_now)
                        all_power_now.append(power_now)
                else:
                    warnings.warn("UPS is not supported.")
            except (RuntimeError, IOError) as e:
                warnings.warn("Unable to read properties of {path}: {error}".format(path=supply_path, error=str(e)))

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
        for supply in os.listdir(POWER_SUPPLY_PATH):
            supply_path = os.path.join(POWER_SUPPLY_PATH, supply)
            try:
                type = self.power_source_type(supply_path)
                if type == common.POWER_TYPE_AC:
                    if self.is_ac_online(supply_path):
                        return common.TIME_REMAINING_UNLIMITED
                elif type == common.POWER_TYPE_BATTERY:
                    if self.is_battery_present(supply_path) and self.is_battery_discharging(supply_path):
                        energy_full, energy_now, power_now = self.get_battery_state(supply_path)
                        all_energy_now.append(energy_now)
                        all_power_now.append(power_now)
                else:
                    warnings.warn("UPS is not supported.")
            except (RuntimeError, IOError) as e:
                warnings.warn("Unable to read properties of {path}: {error}".format(path=supply_path, error=str(e)))

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
