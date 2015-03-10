# coding=utf-8
"""
Implements PowerManagement functions using IOPowerSources.
Requires Mac OS X 10.6+
See doc/darwin for platform-specific details.
"""
__author__ = 'kulakov.ilya@gmail.com'

import weakref
import warnings
import objc
from Foundation import *
from power import common


# Generated in Mac OS X 10.8.2 using the following command:
# gen_bridge_metadata -c '-l/System/Library/Frameworks/IOKit.framework/IOKit -I/System/Library/Frameworks/IOKit.framework/Headers/ps/' /System/Library/Frameworks/IOKit.framework/Headers/ps/IOPowerSources.h /System/Library/Frameworks/IOKit.framework/Headers/ps/IOPSKeys.h
#
# Following keas are added manually, because public headers misses their definitions:
# http://opensource.apple.com/source/IOKitUser/IOKitUser-514.16.50/pwr_mgt.subproj/IOPMLibPrivate.h
# - kIOPMUPSPowerKey
# - kIOPMBatteryPowerKey
# - kIOPMACPowerKey
# - kIOPSProvidesTimeRemaining
IO_POWER_SOURCES_BRIDGESUPPORT = """<?xml version='1.0'?>
<!DOCTYPE signatures SYSTEM "file://localhost/System/Library/DTDs/BridgeSupport.dtd">
<signatures version='1.0'>
    <depends_on path="/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation" />
    <string_constant name='kIOPSACPowerValue' value='AC Power'/>
    <string_constant name='kIOPSBatteryFailureModesKey' value='BatteryFailureModes'/>
    <string_constant name='kIOPSBatteryHealthConditionKey' value='BatteryHealthCondition'/>
    <string_constant name='kIOPSBatteryHealthKey' value='BatteryHealth'/>
    <string_constant name='kIOPSBatteryPowerValue' value='Battery Power'/>
    <string_constant name='kIOPSCheckBatteryValue' value='Check Battery'/>
    <string_constant name='kIOPSCommandDelayedRemovePowerKey' value='Delayed Remove Power'/>
    <string_constant name='kIOPSCommandEnableAudibleAlarmKey' value='Enable Audible Alarm'/>
    <string_constant name='kIOPSCommandStartupDelayKey' value='Startup Delay'/>
    <string_constant name='kIOPSCurrentCapacityKey' value='Current Capacity'/>
    <string_constant name='kIOPSCurrentKey' value='Current'/>
    <string_constant name='kIOPSDeadWarnLevelKey' value='Shutdown Level'/>
    <string_constant name='kIOPSDesignCapacityKey' value='DesignCapacity'/>
    <string_constant name='kIOPSDesignCycleCountKey' value='DesignCycleCount' />
    <string_constant name='kIOPSDynamicStorePath' value='/IOKit/PowerSources'/>
    <string_constant name='kIOPSFailureCellImbalance' value='Cell Imbalance'/>
    <string_constant name='kIOPSFailureChargeFET' value='Charge FET'/>
    <string_constant name='kIOPSFailureChargeOverCurrent' value='Charge Over-Current'/>
    <string_constant name='kIOPSFailureChargeOverTemp' value='Charge Over-Temperature'/>
    <string_constant name='kIOPSFailureDataFlushFault' value='Data Flush Fault'/>
    <string_constant name='kIOPSFailureDischargeFET' value='Discharge FET'/>
    <string_constant name='kIOPSFailureDischargeOverCurrent' value='Discharge Over-Current'/>
    <string_constant name='kIOPSFailureDischargeOverTemp' value='Discharge Over-Temperature'/>
    <string_constant name='kIOPSFailureExternalInput' value='Externally Indicated Failure'/>
    <string_constant name='kIOPSFailureFuseBlown' value='Fuse Blown'/>
    <string_constant name='kIOPSFailureOpenThermistor' value='Open Thermistor'/>
    <string_constant name='kIOPSFailurePeriodicAFEComms' value='Periodic AFE Comms'/>
    <string_constant name='kIOPSFailurePermanentAFEComms' value='Permanent AFE Comms'/>
    <string_constant name='kIOPSFailureSafetyOverVoltage' value='Safety Over-Voltage'/>
    <string_constant name='kIOPSFairValue' value='Fair'/>
    <string_constant name='kIOPSGoodValue' value='Good'/>
    <string_constant name='kIOPSHardwareSerialNumberKey' value='Hardware Serial Number'/>
    <string_constant name='kIOPSHealthConfidenceKey' value='HealthConfidence'/>
    <string_constant name='kIOPSInternalBatteryType' value='InternalBattery'/>
    <string_constant name='kIOPSInternalType' value='Internal'/>
    <string_constant name='kIOPSIsChargedKey' value='Is Charged'/>
    <string_constant name='kIOPSIsChargingKey' value='Is Charging'/>
    <string_constant name='kIOPSIsFinishingChargeKey' value='Is Finishing Charge'/>
    <string_constant name='kIOPSIsPresentKey' value='Is Present'/>
    <string_constant name='kIOPSLowWarnLevelKey' value='Low Warn Level'/>
    <string_constant name='kIOPSMaxCapacityKey' value='Max Capacity'/>
    <string_constant name='kIOPSMaxErrKey' value='MaxErr'/>
    <string_constant name='kIOPSNameKey' value='Name'/>
    <string_constant name='kIOPSNetworkTransportType' value='Ethernet'/>
    <string_constant name='kIOPSNotifyLowBattery' value='com.apple.system.powersources.lowbattery'/>
    <string_constant name='kIOPSOffLineValue' value='Off Line'/>
    <string_constant name='kIOPSPermanentFailureValue' value='Permanent Battery Failure'/>
    <string_constant name='kIOPSPoorValue' value='Poor'/>
    <string_constant name='kIOPSPowerAdapterCurrentKey' value='Current'/>
    <string_constant name='kIOPSPowerAdapterFamilyKey' value='FamilyCode'/>
    <string_constant name='kIOPSPowerAdapterIDKey' value='AdapterID'/>
    <string_constant name='kIOPSPowerAdapterRevisionKey' value='AdapterRevision'/>
    <string_constant name='kIOPSPowerAdapterSerialNumberKey' value='SerialNumber'/>
    <string_constant name='kIOPSPowerAdapterSourceKey' value='Source'/>
    <string_constant name='kIOPSPowerAdapterWattsKey' value='Watts'/>
    <string_constant name='kIOPSPowerSourceIDKey' value='Power Source ID'/>
    <string_constant name='kIOPSPowerSourceStateKey' value='Power Source State'/>
    <string_constant name='kIOPSProvidesTimeRemaining' value='Battery Provides Time Remaining' />
    <string_constant name='kIOPSSerialTransportType' value='Serial'/>
    <string_constant name='kIOPSTimeRemainingNotificationKey' value='com.apple.system.powersources.timeremaining'/>
    <string_constant name='kIOPSTimeToEmptyKey' value='Time to Empty'/>
    <string_constant name='kIOPSTimeToFullChargeKey' value='Time to Full Charge'/>
    <string_constant name='kIOPSTransportTypeKey' value='Transport Type'/>
    <string_constant name='kIOPSTypeKey' value='Type'/>
    <string_constant name='kIOPSUPSManagementClaimed' value='/IOKit/UPSPowerManagementClaimed'/>
    <string_constant name='kIOPSUPSType' value='UPS'/>
    <string_constant name='kIOPSUSBTransportType' value='USB'/>
    <string_constant name='kIOPSVendorDataKey' value='Vendor Specific Data'/>
    <string_constant name='kIOPSVoltageKey' value='Voltage'/>
    <string_constant name="kIOPMUPSPowerKey" value="UPS Power" />
    <string_constant name="kIOPMBatteryPowerKey" value="Battery Power" />
    <string_constant name="kIOPMACPowerKey" value="AC Power" />
    <enum name='kIOPSLowBatteryWarningEarly' value='2'/>
    <enum name='kIOPSLowBatteryWarningFinal' value='3'/>
    <enum name='kIOPSLowBatteryWarningNone' value='1'/>
    <enum name='kIOPSTimeRemainingUnknown' value='-1'/>
    <enum name='kIOPSTimeRemainingUnlimited' value='-2'/>
    <function name='IOPSCopyExternalPowerAdapterDetails'>
        <retval type='^{__CFDictionary=}' already_retained='true'/>
    </function>
    <function name='IOPSCopyPowerSourcesInfo'>
        <retval type='@' already_retained='true'/>
    </function>
    <function name='IOPSCopyPowerSourcesList'>
        <arg type='@'/>
        <retval type='^{__CFArray=}' already_retained='true'/>
    </function>
    <function name='IOPSGetBatteryWarningLevel'>
        <retval type='i'/>
    </function>
    <function name='IOPSGetPowerSourceDescription'>
        <arg type='@'/>
        <arg type='@'/>
        <retval type='^{__CFDictionary=}'/>
    </function>
    <function name='IOPSGetProvidingPowerSourceType'>
        <arg type='@'/>
        <retval type='^{__CFString=}'/>
    </function>
    <function name='IOPSGetTimeRemainingEstimate'>
        <retval type='d'/>
    </function>
    <function name='IOPSNotificationCreateRunLoopSource'>
        <arg type='^?' function_pointer='true'>
            <arg type='^v'/>
            <retval type='v'/>
        </arg>
        <arg type='^v'/>
        <retval type='^{__CFRunLoopSource=}' already_retained='true'/>
    </function>
</signatures>"""

objc.parseBridgeSupport(
    IO_POWER_SOURCES_BRIDGESUPPORT,
    globals(),
    objc.pathForFramework("/System/Library/Frameworks/IOKit.framework")
)


POWER_TYPE_MAP = {
    kIOPMACPowerKey: common.POWER_TYPE_AC,
    kIOPMBatteryPowerKey: common.POWER_TYPE_BATTERY,
    kIOPMUPSPowerKey: common.POWER_TYPE_UPS
}


WARNING_LEVEL_MAP = {
    kIOPSLowBatteryWarningNone: common.LOW_BATTERY_WARNING_NONE,
    kIOPSLowBatteryWarningEarly: common.LOW_BATTERY_WARNING_EARLY,
    kIOPSLowBatteryWarningFinal: common.LOW_BATTERY_WARNING_FINAL
}


class PowerSourcesNotificationsObserver(NSObject):
    """
    Manages NSThread instance which is used to run NSRunLoop with only source - IOPSNotificationCreateRunLoopSource.
    Thread is automatically spawned when first observer is added and stopped when last observer is removed.
    Does not keep strong references to observers.

    @note: Method names break PEP8 convention to conform PyObjC naming conventions
    """
    def init(self):
        self = super(PowerSourcesNotificationsObserver, self).init()
        if self is not None:
            self._weak_observers = []
            self._thread = None
            self._lock = objc.object_lock(self)
        return self

    def startThread(self):
        """Spawns new NSThread to handle notifications."""
        if self._thread is not None:
            return
        self._thread = NSThread.alloc().initWithTarget_selector_object_(self, 'runPowerNotificationsThread', None)
        self._thread.start()

    def stopThread(self):
        """Stops spawned NSThread."""
        if self._thread is not None:
            self.performSelector_onThread_withObject_waitUntilDone_('stopPowerNotificationsThread', self._thread, None, objc.YES)
            self._thread = None

    def runPowerNotificationsThread(self):
        """Main method of the spawned NSThread. Registers run loop source and runs current NSRunLoop."""
        pool = NSAutoreleasePool.alloc().init()

        @objc.callbackFor(IOPSNotificationCreateRunLoopSource)
        def on_power_source_notification(context):
            with self._lock:
                for weak_observer in self._weak_observers:
                    observer = weak_observer()
                    if observer:
                        observer.on_power_source_notification()

        self._source = IOPSNotificationCreateRunLoopSource(on_power_source_notification, None)
        CFRunLoopAddSource(NSRunLoop.currentRunLoop().getCFRunLoop(), self._source, kCFRunLoopDefaultMode)
        while not NSThread.currentThread().isCancelled():
            NSRunLoop.currentRunLoop().runMode_beforeDate_(NSDefaultRunLoopMode, NSDate.distantFuture())
        del pool


    def stopPowerNotificationsThread(self):
        """Removes the only source from NSRunLoop and cancels thread."""
        assert NSThread.currentThread() == self._thread

        CFRunLoopSourceInvalidate(self._source)
        self._source = None
        NSThread.currentThread().cancel()

    def addObserver(self, observer):
        """
        Adds weak ref to an observer.

        @param observer: Instance of class that implements on_power_source_notification()
        """
        with self._lock:
            self._weak_observers.append(weakref.ref(observer))
            if len(self._weak_observers) == 1:
                self.startThread()

    def removeObserver(self, observer):
        """
        Removes an observer.

        @param observer: Previously added observer
        """
        with self._lock:
            self._weak_observers.remove(weakref.ref(observer))
            if len(self._weak_observers) == 0:
                self.stopThread()


class PowerManagement(common.PowerManagementBase):
    notifications_observer = PowerSourcesNotificationsObserver.alloc().init()

    def __init__(self, cf_run_loop=None):
        """
        @param cf_run_loop: If provided, all notifications are posted within this loop
        """
        super(PowerManagement, self).__init__()
        self._cf_run_loop = cf_run_loop

    def on_power_source_notification(self):
        """
        Called in response to IOPSNotificationCreateRunLoopSource() event.
        """
        for weak_observer in self._weak_observers:
            observer = weak_observer()
            if observer:
                observer.on_power_sources_change(self)
                observer.on_time_remaining_change(self)


    def get_providing_power_source_type(self):
        """
        Uses IOPSCopyPowerSourcesInfo and IOPSGetProvidingPowerSourceType to get providing power source type.
        """
        blob = IOPSCopyPowerSourcesInfo()
        type = IOPSGetProvidingPowerSourceType(blob)
        return POWER_TYPE_MAP[type]

    def get_low_battery_warning_level(self):
        """
        Uses IOPSGetBatteryWarningLevel to get battery warning level.
        """
        warning_level = IOPSGetBatteryWarningLevel()
        return WARNING_LEVEL_MAP[warning_level]

    def get_time_remaining_estimate(self):
        """
        In Mac OS X 10.7+
        Uses IOPSGetTimeRemainingEstimate to get time remaining estimate.

        In Mac OS X 10.6
        IOPSGetTimeRemainingEstimate is not available.
        If providing power source type is AC, returns TIME_REMAINING_UNLIMITED.
        Otherwise looks through all power sources returned by IOPSGetProvidingPowerSourceType
        and returns total estimate.
        """
        if IOPSGetTimeRemainingEstimate is not None: # Mac OS X 10.7+
            estimate = float(IOPSGetTimeRemainingEstimate())
            if estimate == -1.0:
                return common.TIME_REMAINING_UNKNOWN
            elif estimate == -2.0:
                return common.TIME_REMAINING_UNLIMITED
            else:
                return estimate / 60.0
        else: # Mac OS X 10.6
            warnings.warn("IOPSGetTimeRemainingEstimate is not preset", RuntimeWarning)
            blob = IOPSCopyPowerSourcesInfo()
            type = IOPSGetProvidingPowerSourceType(blob)
            if type == common.POWER_TYPE_AC:
                return common.TIME_REMAINING_UNLIMITED
            else:
                estimate = 0.0
                for source in IOPSCopyPowerSourcesList(blob):
                    description = IOPSGetPowerSourceDescription(blob, source)
                    if kIOPSIsPresentKey in description and description[kIOPSIsPresentKey] and kIOPSTimeToEmptyKey in description and description[kIOPSTimeToEmptyKey] > 0.0:
                        estimate += float(description[kIOPSTimeToEmptyKey])
                if estimate > 0.0:
                    return float(estimate)
                else:
                    return common.TIME_REMAINING_UNKNOWN

    def add_observer(self, observer):
        """
        Spawns thread or adds IOPSNotificationCreateRunLoopSource directly to provided cf_run_loop
        @see: __init__
        """
        super(PowerManagement, self).add_observer(observer)
        if len(self._weak_observers) == 1:
            if not self._cf_run_loop:
                PowerManagement.notifications_observer.addObserver(self)
            else:
                @objc.callbackFor(IOPSNotificationCreateRunLoopSource)
                def on_power_sources_change(context):
                    self.on_power_source_notification()

                self._source = IOPSNotificationCreateRunLoopSource(on_power_sources_change, None)
                CFRunLoopAddSource(self._cf_run_loop, self._source, kCFRunLoopDefaultMode)

    def remove_observer(self, observer):
        """
        Stops thread and invalidates source.
        """
        super(PowerManagement, self).remove_observer(observer)
        if len(self._weak_observers) == 0:
            if not self._cf_run_loop:
                PowerManagement.notifications_observer.removeObserver(self)
            else:
                CFRunLoopSourceInvalidate(self._source)
                self._source = None
