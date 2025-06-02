# Email_Scanner

A command-line email monitoring tool that connects to IMAP servers, detects phishing using AI, scans embedded links with third-party tools, and checks sender reputation — perfect for automated, real-time inbox security.
![Image description](https://github.com/sam99235/PHISHING_DETECTOR_AI/blob/917e70c3a8017694100d36538c43fd61b717782d/Picture1.png)
## Features

- Connect to popular IMAP servers (Gmail, Outlook, Yahoo, etc.)
- Add custom IMAP servers with custom configurations
- Run as a background service that starts automatically at system logon
- Secure credential management
- Verbose mode for detailed logging
- Simple command-line interface

## Installation

```cmd
# Clone the repository
git clone https://github.com/sam99235/PHISHING_DETECTOR_AI
cd PHISHING_DETECTOR_AI

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Commands

```cmd
# Display help information
python main.py -h

# Configure with a predefined IMAP server
python main.py -is gmail -e your.email@gmail.com --app_password

# Start the scanner in verbose mode
python main.py -ss

# Run the scanner in the background
python main.py -ssbg

# Configure the scanner to run at system startup
python main.py -runbg

# Remove the scanner from background startup
python main.py -rmvbg

# Remove saved credentials
python main.py -rmvc
```

### Adding Custom IMAP Servers

```cmd
# Add a custom IMAP server
python main.py add_new -cn MyServer -is imap.myserver.com -iport 993
```

## Command Reference

| Command | Description |
|---------|-------------|
| `-is`, `--imap_server` | Choose your IMAP service from available options |
| `-e`, `--email` | Specify your email address |
| `--user_password` | Use your account password for authentication |
| `--app_password` | Use an application-specific password (recommended for services with 2FA) |
| `-ss`, `--start_scanner` | Launch email scanner in verbose mode |
| `-ssbg`, `--start_scanner_bg` | Launch email scanner in the background |
| `-runbg`, `--run_in_background` | Configure the scanner to run at system startup |
| `-rmvbg`, `--remove_background` | Remove the scanner from startup configuration |
| `-rmvc`, `--remove_creds` | Remove saved credentials |
| `-v`, `--verbose` | Enable verbose output |

### Custom IMAP Server Commands

| Command | Description |
|---------|-------------|
| `add_new` | Add a new custom IMAP server |
| `-cn`, `--costume_name` | Specify a name for the custom server |
| `-is`, `--imap_server` | Specify the IMAP server address |
| `-iport`, `--imap_port` | Specify the IMAP server port |

## Security Notes

- The application stores your credentials securely using system keyring
- Using application-specific passwords is recommended over account passwords
- No credentials are stored in plain text

## Example Workflows

### Setting up with Gmail

```cmd
# Configure with Gmail
python main.py -is gmail -e your.email@gmail.com --app_password
# Enter your app password when prompted

# Start scanning
python main.py -ss
```

### Setting up with a Custom Server

```cmd
# Add your custom server
python main.py add_new -cn MyWork -is imap.myworkserver.com -iport 993

# Configure with your custom server
python main.py -is MyWork -e your.email@work.com --user_password
# Enter your password when prompted

# Start scanning in the background
python main.py -ssbg
```

### Configuring as a Background Service

```cmd
# First set up your credentials
python main.py -is outlook -e your.email@outlook.com --app_password

# Configure to run at startup
python main.py -runbg

# Remove from startup if needed
python main.py -rmvbg
```
## 🔐 Third-Party API Integration

To enhance phishing detection, this tool can integrate with third-party APIs to scan URLs and evaluate sender reputation.

You need to obtain API keys from the following providers:

* [VirusTotal](https://www.virustotal.com/)
* [IPQualityScore](https://www.ipqualityscore.com/)

Once you have your API keys, set them securely using environment variables or a configuration file.

### Example: Setting API keys via environment variables

**For Windows**

```cmd
set URL_SCANNER_API_KEY=your_virustotal_api_key
set EMAIL_SCANNER_API_KEY=your_ipqualityscore_api_key
```


## Prerequisites

- Python 3.6+
- Access to an email account with IMAP enabled
- For Gmail, Yahoo, and some other providers, you'll need to create an application-specific password

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
