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
        else:
            return "undefined"
    def RESET_EVENT(self, bytes):
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
        
        self.decoded['Message'] += ", Hardware Version: v" + HardwareVersion

        ##the firmware version has two different formats depending on the most significant bit
        FirmwareFormat = (bytes[4] >> 7) & 0x01

        ##FirmwareFormat of 0 is old format, 1 is new format
        ## old format is has two sections x.y
        ## new format has three sections x.y.z
        if (FirmwareFormat == 0):
            FirmwareVersion = bytes[4] + "." + bytes[5]
        else:
            FirmwareVersion = ((bytes[4] >> 2) & 0x1F) + "." + ((bytes[4] & 0x03) + ((bytes[5] >> 5) & 0x07)) + "." + (bytes[5] & 0x1F)
        self.decoded['Message'] += ", Firwamre Version: v" + FirmwareVersion
        return self.decoded

    def SUPERVISORY_EVENT(self, bytes):
        self.decoded['Message'] = "Event: Supervisory"
        ## note that the sensor state in the supervisory message is being depreciated, so those are not decoded here
        ## battery voltage is in the format x.y volts where x is upper nibble and y is lower nibble4

        BatteryLevel = ((bytes[4] >> 4) & 0x0f) + "." + (bytes[4] & 0x0f)

        self.decoded['Message'] += ", Battery Voltage: " + BatteryLevel + "V"
        # the accumulation count is a 16-bit value
        AccumulationCount = (bytes[9] * 256) + bytes[10]
        self.decoded['Message'] += ", Accumulation Count: " + AccumulationCount

        # decode bits for error code byte
        TamperSinceLastReset = (bytes[2] >> 4) & 0x01
        self.decoded['Message'] += ", Tamper Since Last Reset: " + TamperSinceLastReset

        CurrentTamperState = (bytes[2] >> 3) & 0x01
        self.decoded['Message'] += ", Current Tamper State: " + CurrentTamperState

        ErrorWithLastDownlink = (bytes[2] >> 2) & 0x01
        self.decoded['Message'] += ", Error With Last Downlink: " + ErrorWithLastDownlink

        BatteryLow = (bytes[2] >> 1) & 0x01
        self.decoded['Message'] += ",  " + BatteryLow

        RadioCommError = bytes[2] & 0x01
        self.decoded['Message'] += ", Radio Comm Error: " + RadioCommError

        return self.decoded
    def TAMPER_EVENT(self, bytes):
        self.decoded['Message'] = "Event: Tamper"

        TamperState = bytes[2]

        if (TamperState == 0):
            self.decoded['Message'] += ", State: Open"
        else:
            self.decoded['Message'] += ", State: Closed"
    def LINK_QUALITY_EVENT(self, bytes):
        self.decoded
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

    def Hex(self,decimal):
        sliced = slice(1)
        decimal = ('0' + str(decimal).upper()[sliced])
        return decimal