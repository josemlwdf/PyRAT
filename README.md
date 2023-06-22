# PyRAT (Python RAT) - CTF Rootkit

PyRAT is a powerful CTF (Capture The Flag) rootkit designed to be used in cybersecurity competitions and educational settings. It is a feature-rich tool that provides various capabilities for privilege escalation, hiding processes and files, and maintaining persistent access on compromised systems.

``**Note:** The PyRAT CTF Rootkit is intended for educational purposes and authorized security assessments only. Do not use this tool for any malicious activities or unauthorized activities.``

## Features

- **Privilege Escalation:** PyRAT provides methods for escalating privileges on compromised systems, allowing users to gain root access and perform administrative actions.
- **Backdoor Access:** The rootkit opens a backdoor on the target system, providing a covert channel for remote access and control.
- **Remote Command Execution:** Users can remotely execute commands on the compromised system through the backdoor channel.
- **Customizable Configurations:** The rootkit's behavior and settings can be customized to suit specific requirements and scenarios.

## Requirements

- Python 3.6 or above
- Root or administrative privileges on the target system
- **Important:** Ensure compliance with legal and ethical guidelines. Obtain proper authorization before deploying the PyRAT CTF Rootkit.

## Installation

1. Clone the repository:

       git clone https://github.com/josewdf/pyrat.git
       cd pyrat
   
2. Deploy the rootkit:

Run the deployment script with root or administrative privileges to install the rootkit on the target system.
Review the deployment script (pyrat.py) and ensure it reflects your desired deployment settings.
Caution: Deploying the PyRAT rootkit on unauthorized systems is illegal and unethical. Obtain proper authorization and adhere to legal and ethical guidelines.
        
        sudo python3 pyrat.py

## Usage

Once the PyRAT CTF Rootkit is deployed on the target system, it operates silently in the background, providing the specified functionalities.
Refer to the rootkit's documentation or user manual for detailed instructions on using its features and interacting with the compromised system.
It is essential to exercise caution and ensure proper legal and ethical compliance when using the rootkit in CTF competitions or security assessments.

### To connect to the script using `nc` (netcat), follow these steps:

1. Open a terminal or command prompt.

2. Run the following command to connect to the server:

        nc <server_ip> <server_port>

   Replace `<server_ip>` with the IP address of the server where the script is running and `<server_port>` with the port number specified in the script (8000 in this case).

3. After connecting, you can interact with the script using the following commands:

   - **Admin**: To access the admin functionality, type `admin` and press Enter. You will be prompted to enter a password. Enter the password and press Enter. If the password is correct, you will see the message "Welcome Admin!!! Type 'shell' to begin". You can then proceed to use the shell functionality.

   - **Shell**: To access the shell functionality, type `shell` and press Enter. This will spawn a shell on the server, allowing you to execute commands. You can enter any valid shell command, and the output will be displayed on your `nc` session.

   - **Python Interactive**: To execute python commands on the server just send your python commands and it will be passed to the ``exec`` function.

Note: Make sure to replace `<server_ip>` with the actual IP address of the server running the script.

## Disclaimer

``The PyRAT CTF Rootkit is intended solely for educational purposes and authorized security assessments. Misuse of this tool for any malicious activities is strictly prohibited.
The developers and contributors of the PyRAT CTF Rootkit are not responsible for any misuse, damage, or illegal activities conducted using this tool.``

## Contributing

Contributions to the PyRAT CTF Rootkit project are welcome! If you have suggestions, bug reports, or feature requests, please open an issue on the GitHub repository.
Before contributing, please review the code of conduct and contribution guidelines for a smooth collaboration experience.

josemlwdf@github.com

## License

``The PyRAT CTF Rootkit is licensed under the MIT License. See the LICENSE file for more details. 
Feel free to modify and expand the README to provide more specific details, instructions, and guidelines according to your project requirements.``
    
