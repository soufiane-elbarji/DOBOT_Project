import DobotDllType as dType

# --- CONFIGURATION ---
COM_PORT = "COM3"  # Adjust to your Dobot's COM port
TOOLPATH_FILE = "temp/toolpath.txt"

CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"
}

def main():
    """Main function to connect, draw, and disconnect the Dobot."""
    # Load Dll
    api = dType.load()

    # Connect Dobot
    state = dType.ConnectDobot(api, COM_PORT, 115200)[0]
    print("Connect status:", CON_STR[state])

    if (state != dType.DobotConnect.DobotConnect_NoError):
        print("Failed to connect to Dobot. Please check the COM port and connection.")
        return

    print("Dobot connected. Starting drawing process...")
    
    # Clean Command Queued
    dType.SetQueuedCmdClear(api)

    # Set motion parameters for drawing
    # You can adjust these values for speed and precision
    dType.SetHOMEParams(api, 250, 0, 50, 0, isQueued=1)
    dType.SetPTPJointParams(api, 100, 100, 100, 100, 100, 100, 100, 100, isQueued=1)
    dType.SetPTPCommonParams(api, 50, 50, isQueued=1) # Velocity and Acceleration Ratios
    # Set jump height for MOVETO commands
    # The Z-limit should be higher than your move height
    dType.SetPTPJumpParams(api, 20, 50, isQueued=1) 

    # Async Home - this is the first command in the queue
    print("Homing robot...")
    dType.SetHOMECmd(api, temp=0, isQueued=1)
    
    # --- Read toolpath and queue commands ---
    lastIndex = dType.GetQueuedCmdCurrentIndex(api)[0]
    try:
        with open(TOOLPATH_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                parts = line.split(',')
                command = parts[0]
                x = float(parts[1])
                y = float(parts[2])
                z = float(parts[3])
                
                if command == "MOVETO":
                    # Use JUMP mode for pen-up moves. The Z value from the file is used.
                    lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, x, y, z, 0, isQueued=1)[0]
                elif command == "LINETO":
                    # Use linear move for drawing.
                    lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, x, y, z, 0, isQueued=1)[0]

    except FileNotFoundError:
        print("Error: {} not found. Please run 'run_drawing_process.py' first.".format(TOOLPATH_FILE))
        dType.DisconnectDobot(api)
        return
    except Exception as e:
        print("An error occurred while reading the toolpath file: {}".format(e))
        dType.DisconnectDobot(api)
        return

    # --- Execute the command queue ---
    print("Toolpath loaded. Starting execution...")
    dType.SetQueuedCmdStartExec(api)

    # Wait for Executing Last Command
    while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
        # Changed to .format() for Python 3.5 compatibility
        print("Executing command... Current index: {}/{}".format(dType.GetQueuedCmdCurrentIndex(api)[0], lastIndex), end='\r')

        dType.dSleep(200) # Wait and check status periodically

    # Stop to Execute Command Queued
    dType.SetQueuedCmdStopExec(api)
    print("\nDrawing complete.")

    # Disconnect Dobot
    dType.DisconnectDobot(api)
    print("Dobot disconnected.")

if __name__ == "__main__":
    main()
