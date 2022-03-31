#!/usr/bin/python

## global variable



class Decoder():
    RESET_EVENT = "00"
    SUPERVISORY_EVENT = "01"
    TAMPER_EVENT = "02"
    LINK_QUALITY_EVENT = "FB"
    RATE_LIMIT_EXCEEDED_EVENT = "FC"
    TEST_MESSAGE_EVENT = "FD"
    DOWNLINK_ACK_EVENT = "FF"
    DOOR_WINDOW_EVENT = "03"
    PUSH_BUTTON_EVENT = "06"
    CONTACT_EVENT = "07"
    WATER_EVENT = "08"
    TEMPERATURE_EVENT = "09"
    TILT_EVENT = "0A"
    ATH_EVENT = "0D"
    ABM_EVENT = "0E"
    TILT_HP_EVENT = "0F"
    ULTRASONIC_EVENT = "10"
    SENSOR420MA_EVENT = "11"
    THERMOCOUPLE_EVENT = "13"
    VOLTMETER_EVENT = "14"
    CUSTOM_SENSOR_EVENT = "15"
    GPS_EVENT = "16"
    HONEYWELL5800_EVENT = "17"
    MAGNETOMETER_EVENT = "18"
    VIBRATION_LB_EVENT = "19"
    VIBRATION_HB_EVENT = "1A"
    decoded = {}
    def Generic_Decoder(self, bytes):
        #ProtocolVersion = (bytes[0] >> 4) & 0x0f
        #PacketCounter = bytes[0] & 0x0f

        Eventtype = self.Hex(bytes[1])
        if(Eventtype == self.PUSH_BUTTON_EVENT):
            return self.PUSH_BUTTON(bytes)
        elif(Eventtype == self.RESET_EVENT):
            return self.RESET(bytes)
        elif(Eventtype == self.SUPERVISORY_EVENT):
            return self.SUPERVISORY(bytes)
        elif(Eventtype == self.TAMPER_EVENT):
            return self.TAMPER(bytes)
        elif(Eventtype == self.LINK_QUALITY_EVENT):
            return self.LINK_QUALITY(bytes)
        elif(Eventtype == self.DOOR_WINDOW_EVENT):
            return self.DOOR_WINDOW(bytes)
        elif(Eventtype == self.CONTACT_EVENT):
            return self.CONTACT(bytes)
        elif(Eventtype == self.WATER_EVENT):
            return self.WATER(bytes)
        elif(Eventtype == self.TEMPERATURE_EVENT):
            return self.TEMPERATURE(bytes)
        elif(Eventtype == self.TILT_EVENT):
            return self.TILT(bytes)
        elif(Eventtype == self.ULTRASONIC_EVENT):
            return self.ULTRASONIC(bytes)
        elif(Eventtype == self.SENSOR420MA_EVENT):
            return self.SENSOR420MA(bytes)
        elif(Eventtype == self.THERMOCOUPLE_EVENT):
            return self.THERMOCOUPLE(bytes)
        elif(Eventtype == self.ATH_EVENT):
            return self.ATH(bytes)
        elif(Eventtype == self.ABM_EVENT):
            return self.ABM(bytes)
        elif(Eventtype == self.DOWNLINK_ACK_EVENT):
            return self.DOWNLINK_ACK(bytes)
        else:
            return "undefined"

    def RESET(self, bytes):
        self.decoded['Message'] = "Event Reset"
        DeviceTypeByte = self.Hex(bytes[2])
        
        if(DeviceTypeByte == '01'):
            DeviceType = "Door/Window Sensor"
        elif(DeviceTypeByte == "02"):
            DeviceType = "Door/Window High Security" 
        elif(DeviceTypeByte == "03"):
            DeviceType = "Contact Sensor" 
        elif(DeviceTypeByte == "04"):
            DeviceType = "No-Prope Temperature Sensor" 
        elif(DeviceTypeByte == "05"):
            DeviceType = "External-Probe Temperature Sensor" 
        elif(DeviceTypeByte == "06"):
            DeviceType = "Single Push Button" 
        elif(DeviceTypeByte == "07"):
            DeviceType = "Dual Push Button" 
        elif(DeviceTypeByte == "08"):
            DeviceType = "Acceleration-Based Movement Sensor" 
        elif(DeviceTypeByte == "09"):
            DeviceType = "Tilt Sensor" 
        elif(DeviceTypeByte == "0A"):
            DeviceType = "Water Sensor" 
        elif(DeviceTypeByte == "0B"):
            DeviceType = "Tank Level Float Sensor" 
        elif(DeviceTypeByte == "0C"):
            DeviceType = "Glass Break Sensor" 
        elif(DeviceTypeByte == "0D"):
            DeviceType = "Ambient Light Sensor" 
        elif(DeviceTypeByte == "0E"):
            DeviceType = "Air Temperature and Humidity Sensor "            
        elif(DeviceTypeByte == "0F"):
            DeviceType = "High-Precision Tilt Sensor"
        elif(DeviceTypeByte == "10"):
            DeviceType = "Ultrasonic Level Sensor"
        elif(DeviceTypeByte == "11"):
            DeviceType = "4-20mA Current Loop Sensor" 
        elif(DeviceTypeByte == "12"):
            DeviceType = "Ext-Probe Air Temp and Humidity Sensor" 
        elif(DeviceTypeByte == "13"):
            DeviceType = "Thermocouple Temperature Sensor" 
        elif(DeviceTypeByte == "14"):
            DeviceType = "Voltage Sensor" 
        elif(DeviceTypeByte == "15"):
            DeviceType = "Custom Sensor" 
        elif(DeviceTypeByte == "16"):
            DeviceType = "GPS" 
        elif(DeviceTypeByte == "17"):
            DeviceType = "Honeywell 5800 Bridge" 
        elif(DeviceTypeByte == "18"):
            DeviceType = "Magnetometer" 
        elif(DeviceTypeByte == "19"):
            DeviceType = "Vibration Sensor - Low Frequency" 
        elif(DeviceTypeByte == "1A"):
            DeviceType = "Vibration Sensor - High Frequency" 
        else:
            DeviceType = "Device Undefined"
        self.decoded['message'] += ", Device Tyoe: " + DeviceType
        ## the hardware version has the major version in the upper nibble, and the minor version in the lower nibble   
        HardwareVersion = (bytes[3] >> 4 & 0x0f) + "." + (bytes[3] & 0x0f)
        
        self.decoded['Message'] += ", Hardware Version: v" + str(HardwareVersion)

        ##the firmware version has two different formats depending on the most significant bit
        FirmwareFormat = (bytes[4] >> 7) & 0x01

        ##FirmwareFormat of 0 is old format, 1 is new format
        ## old format is has two sections x.y
        ## new format has three sections x.y.z
        if (FirmwareFormat == 0):
            FirmwareVersion = bytes[4] + "." + bytes[5]
        else:
            FirmwareVersion = ((bytes[4] >> 2) & 0x1F) + "." + ((bytes[4] & 0x03) + ((bytes[5] >> 5) & 0x07)) + "." + (bytes[5] & 0x1F)
        self.decoded['Message'] += ", Firwamre Version: v" + str(FirmwareVersion)
        return self.decoded

    def SUPERVISORY(self, bytes):
        self.decoded['Message'] = "Event: Supervisory"
        ## note that the sensor state in the supervisory message is being depreciated, so those are not decoded here
        ## battery voltage is in the format x.y volts where x is upper nibble and y is lower nibble4

        BatteryLevel = str(((bytes[4] >> 4) & 0x0f)) + "." + str((bytes[4] & 0x0f))

        self.decoded['Message'] += ", Battery Voltage: " + BatteryLevel + "V"
        # the accumulation count is a 16-bit value
        AccumulationCount = (bytes[9] * 256) + bytes[10]
        self.decoded['Message'] += ", Accumulation Count: " + str(AccumulationCount)

        # decode bits for error code byte
        TamperSinceLastReset = (bytes[2] >> 4) & 0x01
        self.decoded['Message'] += ", Tamper Since Last Reset: " + str(TamperSinceLastReset)

        CurrentTamperState = (bytes[2] >> 3) & 0x01
        self.decoded['Message'] += ", Current Tamper State: " + str(CurrentTamperState)

        ErrorWithLastDownlink = (bytes[2] >> 2) & 0x01
        self.decoded['Message'] += ", Error With Last Downlink: " + str(ErrorWithLastDownlink)

        BatteryLow = (bytes[2] >> 1) & 0x01
        self.decoded['Message'] += ",  " + BatteryLow

        RadioCommError = bytes[2] & 0x01
        self.decoded['Message'] += ", Radio Comm Error: " + str(RadioCommError)

        return self.decoded
    def TAMPER(self, bytes):
        self.decoded['Message'] = "Event: Tamper"

        TamperState = bytes[2]

        if (TamperState == 0):
            self.decoded['Message'] += ", State: Open"
        else:
            self.decoded['Message'] += ", State: Closed"
    def LINK_QUALITY(self, bytes):
        self.decoded['Message'] = "Event: Link Quality"

        CurrentSubBand = bytes[2]
        self.decoded['Message'] += ", Current Sub-Band: " + str(CurrentSubBand)

        RSSILastDownlink = bytes[3]
        self.decoded['Message'] += ", RSSI of Last Downlink" + str(RSSILastDownlink)

        SNRLastDownlink = bytes[4]
        self.decoded['Message'] += ", SNR of Last Downlink: " + str(SNRLastDownlink)
        return self.decoded
        
    def DOOR_WINDOW(self, bytes):
        self.decoded['Message'] = "Event: Door/Window"

        SensorState = bytes[2]

        if(SensorState == 0):
            self.decoded["Message"] += ", State: Closed"
        else:
            self.decoded['Message'] += ", State: Open"
        return self.decoded

    def PUSH_BUTTON(self, bytes):
        
        self.decoded['Message'] = "Event: Push Event"
        ButtonID = self.Hex(bytes[2])
        if(ButtonID == '01'):
            ButtonReference = "Button 1"
        elif(ButtonID == '02'):    
            ButtonReference = "Button 2"
        elif(ButtonID == '03'):
            ButtonReference = "Button 1"
        elif(ButtonID == '12'):
            ButtonReference = "Both Buttons"
        else:
            ButtonReference = "Undefined"
        self.decoded['Message'] += ", Button ID: " + ButtonReference
        ButtonState = bytes[3]
        if(ButtonState == 0):
            SensorStateDescription = "Pressed"
        elif(ButtonState == 1):
            SensorStateDescription = "Released"
        elif(ButtonState == 2):
            SensorStateDescription = "Held"
        else:
            SensorStateDescription = "Undefined"
        self.decoded['Message'] += ", Button State: " + SensorStateDescription
        return self.decoded
    def CONTACT(self, bytes):
        self.decoded['Message'] = "Event: Dry Contact"

        ContactState = bytes[2]

        if (ContactState == 0):
            SensorState = "Contacts  Shorted"
        else:
            SensorState = "Contacts Opened"
        return self.decoded

    def WATER(self, bytes):
        self.decoded['Message'] = "Event: Water"

        SensorState = bytes[2]

        if(SensorState == 0):
            self.decoded['Message'] += ", State: Water Present"
        else:
            self.decoded['Message'] += ", State: Water Not Present"
        
        WaterRelativeResistance = bytes[3]

        self.decoded['Message'] += ", Relative Resistance: " + str(WaterRelativeResistance)

        return self.decoded
    def TEMPERATURE(self, bytes):
        self.decoded['Message'] = "Event: Temperature"

        TemperatureEvent = bytes[2];

        if (TemperatureEvent == 0):
            TemperatureEventDescription = "Periodic Report"
        elif (TemperatureEvent == 1):
            TemperatureEventDescription = "Temperature Over Upper Threshold"
        elif (TemperatureEvent == 2):
            TemperatureEventDescription = "Temperature Under Lower Threshold"
        elif (TemperatureEvent == 3):
            TemperatureEventDescription = "Temperature Report-on-Change Increase"
        elif (TemperatureEvent == 4):
            TemperatureEventDescription = "Temperature Report-on-Change Decrease"
        else: TemperatureEventDescription = "Undefined"
        
        self.decoded['Message'] = ", Temperature Event: " + TemperatureEventDescription
        ## current temperature reading
        CurrentTemperature = self.Convert(bytes[3], 0)
        self.decoded['Message'] += ", Current Temperature: " + str(CurrentTemperature)

        ## relative temp measurement for use with an alternative calibration table
        RelativeMeasurement = self.Convert(bytes[4], 0)
        self.decoded['Message'] += ", Relative Measurement: " + str(RelativeMeasurement)
        return self.decoded

    def TILT(self, bytes):
        self.decoded['Message'] = "Event: Tilt"

        TiltEvent = bytes[2]

        if (TiltEvent == 0):
            TiltEventDescription = "Transitioned to Vertical"
        elif(TiltEvent == 1):
            TiltEventDescription = "Transitioned to Horizontal"
        elif(TiltEvent == 2):
            TiltEventDescription = "Report-on-Change Toward Vertical"
        elif(TiltEvent == 3):
            TiltEventDescription = "Report-on-Change Toward Horizontal"
        else: 
            TiltEventDescription = "Undefined"
        self.decoded['Message'] += ", Tilt Event: " + TiltEventDescription

        TiltAngle = bytes[3]

        self.decoded['Message'] += ", Tilt Angle: " + str(TiltAngle)

        return self.decoded

    def ATH(self, bytes):
        self.decoded['Message'] = "event: Air Temperature/Humidity"

        ATHEvent = bytes[2]

        if (ATHEvent == 0):
            ATHDescription = "Periodic Report"
        elif(ATHEvent == 1): 
            ATHDescription = "Temperature has Risen Above Upper Threshold"
        elif(ATHEvent == 2):
            ATHDescription = "Temperature has Fallen Below Lower Threshold"
        elif(ATHEvent == 3):
            ATHDescription = "Temperature Report-on-Change Increase"
        elif(ATHEvent == 4):
            ATHDescription = "Temperature Report-on-Change Decrease"
        elif(ATHEvent == 5):
            ATHDescription = "Humidity has Risen Above Upper Threshold"
        elif(ATHEvent == 6):
            ATHDescription = "Humidity has Fallen Below Lower Threshold"
        elif(ATHEvent == 7):
            ATHDescription = "Humidity Report-on-Change Increase"
        elif(ATHEvent == 8):
            ATHDescription = "Humidity Report-on-Change Decrease"
        else:
            ATHDescription = "Undefined"
        
        self.decoded['Message'] += ", ATH Event: " + ATHDescription

        ## integer and fractional values between two bytes
        Temperature = Convert((bytes[3]) + ((bytes[4] >> 4) / 10), 1);
        self.decoded['Message'] += ", Temperature: " + str(Temperature)

        Humidity = +(bytes[5] + ((bytes[6]>>4) / 10)).toFixed(1);
        self.decoded['Message'] += ", Humidity: " + str(Humidity)

        return self.decoded

    def ABM(self, bytes):
        self.decoded['Message'] = "Event: Acceleration-Based movement"

        ABMEvent = bytes[2]

        if(ABMEvent == 0):
            ABMEventDescription = "Movement Started"
        else:
            ABMEventDescription = "Movement Stopped"
        
        self.decoded['Message'] = ", ABM Event: " + ABMEventDescription
        return self.decoded

    def TILT(self, bytes):
        self.decoded['Message'] = "Event: High-Precision Tilt"

        TiltEvent = bytes[2]

        if(TiltEvent == 0):
            TiltEventDescription = "Periodic Report"
        elif(TiltEvent == 1):
            TiltEventDescription = "Transitioned Toward 0-Degree Vertical Orientation"
        elif(TiltEvent == 2):
            TiltEventDescription = "Transitioned Away From 0-Degree Vertical Orientation"
        elif(TiltEvent == 3):
            TiltEventDescription = "Report-on-Change Toward 0-Degree Vertical Orientation"
        elif(TiltEvent == 4):
            TiltEventDescription = "Report-on-Change Away From 0-Degree Vertical Orientation"
        else:
            TiltEventDescription = "Undefined"
        self.decoded['Message'] += ", Tilt HP Event: " + TiltEventDescription

        ## integer and fractional values between two bytes
        Angle = +round((bytes[3] + bytes[4] / 10), 1)
        self.decoded['Message'] = ", Angle: " + str(Angle)

        Temperature = self.Convert(bytes[5], 0)
        self.decoded['Message'] = ", Temperature: " + str(Temperature)

        return self.decoded

    def ULTRASONIC(self, bytes):
        self.decoded['Message'] = "Event: Ultrasonic Level"

        UltrasonicEvent = bytes[2]

        if(UltrasonicEvent == 0):
            UltrasonicEventDescription = "Periodic Report"
        elif(UltrasonicEvent == 1):
            UltrasonicEventDescription = "Distance has Risen Above Upper Threshold"
        elif(UltrasonicEvent == 2):
            UltrasonicEventDescription = "Distance has Fallen Below Lower Threshold"
        elif(UltrasonicEvent == 3):
            UltrasonicEventDescription = "Report-on-Change Increase"
        elif(UltrasonicEvent == 4):
            UltrasonicEventDescription = "Report-on-Change Decrease"
        else:
            UltrasonicEventDescription = "Undefined"

        self.decoded['Message'] += ", Ultrasonic Event: " + UltrasonicEventDescription

        #  distance is calculated across 16-bits
        Distance = ((bytes[3] * 256) + bytes[4])

        self.decoded['Message'] += ", Distance: " + str(Distance)

        return self.decoded

    def SENSOR420MA(self, bytes):

        self.decoded['Message'] = "Event: 4-20mA"

        Sensor420mAEvent = bytes[2]

        if(Sensor420mAEvent == 0):
            Sensor420mAEventDescription = "Periodic Report"
        elif(Sensor420mAEvent == 1):
            Sensor420mAEventDescription = "Analog Value has Risen Above Upper Threshold"
        elif(Sensor420mAEvent == 2):
            Sensor420mAEventDescription = "Analog Value has Fallen Below Lower Threshold"
        elif(Sensor420mAEvent == 3):
            Sensor420mAEventDescription = "Report on Change Increase"
        elif(Sensor420mAEvent == 4):
            Sensor420mAEventDescription = "Report on Change Decrease"
        else:
            Sensor420mAEventDescription = "Undefined"

        self.decoded['Message'] += ", 4-20mA Event: " + Sensor420mAEventDescription

        Analog420Measurement = ((bytes[3] * 256) + bytes[4]) / 100

        self.decoded['Message'] += ", Current Measurement in mA " + str(Analog420Measurement)

        return self.decoded

    def THERMOCOUPLE(self, bytes):

        self.decoded['Message'] = "Event: Thermocouple"

        ThermocoupleEvent = bytes[2]

        if(ThermocoupleEvent == 0):
            ThermocoupleEventDescription = "Periodic Report"
        elif(ThermocoupleEvent == 1):
            ThermocoupleEventDescription = "Analog Value has Risen Above Upper Threshold"
        elif(ThermocoupleEvent == 2):
            ThermocoupleEventDescription = "Analog Value has Fallen Below Lower Threshold"
        elif(ThermocoupleEvent == 3):
            ThermocoupleEventDescription = "Report on Change Increase"
        elif(ThermocoupleEvent == 4):
            ThermocoupleEventDescription = "Report on Change Decrease"
        else:
            ThermocoupleEventDescription = "Undefined"

        self.decoded['Message'] += ", thermacouple Event: " + ThermocoupleEventDescription

        Tempertature = int(((bytes[3] *256) + bytes[4]) / 16)

        self.decoded['Message'] += ", Temperature: " + str(Tempertature) + "C"

        Faults = bytes[5]

        FaultColdOutsideRange = (Faults >> 7) & 0x01
        FaultHotOutsideRange = (Faults >> 6) & 0x01
        FaultColdAboveThresh = (Faults >> 5) & 0x01
        FaultColdBelowThresh = (Faults >> 4) & 0x01
        FaultTCTooHigh = (Faults >> 3) & 0x01
        FaultTCTooLow = (Faults >> 2) & 0x01
        FaultVoltageOutsideRange = (Faults >> 1) & 0x01
        FaultOpenCircuit = Faults & 0x01

        if (Faults == 0):
            self.decoded["Message"] += ", Fault: None"
        else:
            if (FaultColdOutsideRange):
                self.decoded['Message'] += ", Fault: The cold-Junction temperature is outside of the normal operating range"

            elif (FaultHotOutsideRange):
                self.decoded['Message'] += ", Fault: The hot junction temperature is outside of the normal operating range"

            elif (FaultColdAboveThresh):
                self.decoded['Message'] += ", Fault: The cold-Junction temperature is at or above than the cold-junction temperature high threshold"

            elif (FaultColdBelowThresh):
                self.decoded['Message'] += ", Fault: The Cold-Junction temperature is lower than the cold-junction temperature low threshold"

            elif (FaultTCTooHigh):
                self.decoded['Message'] += ", Fault: The thermocouple temperature is too high"

            elif (FaultTCTooLow):
                self.decoded['Message'] += ", Fault: Thermocouple temperature is too low"

            elif (FaultVoltageOutsideRange):
                self.decoded['Message'] += ", Fault: The input voltage is negative or greater than VDD"

            elif (FaultOpenCircuit):
                self.decoded['Message'] += ", Fault: An open circuit such as broken thermocouple wires has been detected"
        return self.decoded
    
    def DOWNLINK_ACK(self, bytes):

        self.decoded['Message'] = "Event: Downlink Acknowledge"

        DownLinkEvent = bytes[2]
        if(DownLinkEvent == 1):
            DownlinkEventDescription = "Message Invalid"
        else:
            DownlinkEventDescription = "Message Valid"
        
        self.decoded['Message'] += ", Downlink: " + DownlinkEventDescription
        
        return self.decoded

        
    def Hex(self,decimal):
        sliced = slice(1)
        decimal = ('0' + str(decimal).upper()[sliced])
        return decimal
    def Convert(self, number, mode):
        if(mode == 0):
            if (number > 127):
                result = number - 256
            else:
                result = number
        if(mode == 1):
            if (number >127):
                result = -+round((number - 128), 1)
            else:
                result = +round(number, 1)
        return result