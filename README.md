# SSH MFA (TOTP) Wrapper Utility

This utility is a Python wrapper script that automates SSH login for servers protected with multi-factor authentication (MFA). It securely provides both the SSH password and the TOTP verification code using the `totp-cli` tool.

## Prerequisites

### Install `pexpect`
The script requires the `pexpect` Python module for handling interactive SSH sessions. Install it using:
```sh
pip install pexpect # or uv sync if you are using uv and cloned this repo
```

### Install `totp-cli`
The script uses [`totp-cli`](https://github.com/yitsushi/totp-cli) to generate TOTP codes. Install it followign the instructions for your enviroment, or go to the releases page and download the appropriate version for your enviroment
```

Ensure that your SSH servers are already configured with `totp-cli` for generating codes.

## Usage
Run the script using the following command:
```sh
python ssh_mfa.py <user@server> <namespace>
```
Where:
- `<user@server>` is the remote SSH server with optional username (e.g., `user2@example.com` or just `example.com`).
- `<namespace>` is the namespace used in `totp-cli` to generate the correct TOTP code.

### TOTP Profile Setup
When using the user@server format, make sure to create your TOTP profile with the same identifier:
```sh
totp-cli new <namespace> user@server
```

## Environment Variables (Optional)
The script can use an environment variable `TOTP_PASS` to store the password required for `totp-cli` to decrypt the stored credentials.

### Setting the Environment Variable
You can export the password before running the script to avoid being prompted:
```sh
export TOTP_PASS=<your_totp_password>
python ssh_mfa.py <user@server> <namespace>
```
Alternatively, if `TOTP_PASS` is not set, the script will prompt for it during execution.

## How It Works
1. The script checks if the `TOTP_PASS` environment variable is set:
   - If set, it uses it directly.
   - If not set, it prompts the user to enter the password and stores it for subsequent use.
2. The script logs in to the SSH server:
   - It first prompts for and enters the SSH password.
   - It then generates a TOTP code using `totp-cli` and enters it when prompted.
3. Once authenticated, the SSH session is handed over to the user.

## Notes
- Ensure that `totp-cli` is installed and configured correctly with your accounts before using this script.
- The script only automates login and does not store any credentials persistently.
- When using different usernames for SSH, be sure to set up your TOTP profiles using the full `user@server` format.
