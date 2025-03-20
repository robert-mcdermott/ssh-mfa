#!/home/rmcdermo/.local/bin/uv run
import pexpect
import getpass
import sys
import subprocess
import os

def get_totp_code(namespace, server_identifier):
    totp_password = os.getenv("TOTP_PASS")

    if not totp_password:
        totp_password = getpass.getpass("TOTP Password: ")
        os.environ["TOTP_PASS"] = totp_password  # Set it for subsequent use

    try:
        result = subprocess.run([
            "totp-cli", "generate", namespace, server_identifier
        ], capture_output=True, text=True, input=totp_password)

        if result.returncode == 0:
            return result.stdout.strip().split("\n")[-1]  # Extract the last line (TOTP code)
        else:
            print("Failed to generate TOTP code.", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"Error generating TOTP: {e}", file=sys.stderr)
        sys.exit(1)

def ssh_with_totp(server_identifier, namespace):
    password = getpass.getpass("SSH Password: ")
    totp_code = get_totp_code(namespace, server_identifier)

    ssh_command = f"ssh {server_identifier}"
    child = pexpect.spawn(ssh_command, encoding='utf-8', timeout=10)

    try:
        child.expect("Password:")
        child.sendline(password)

        child.expect("Verification code:")
        child.sendline(totp_code)

        child.interact()  # Hand over control to the user
    except pexpect.exceptions.EOF:
        print("Connection closed unexpectedly.")
    except pexpect.exceptions.TIMEOUT:
        print("Timeout waiting for SSH response.")
    finally:
        child.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python ssh-mfa.py <user@server> <namespace>")
        sys.exit(1)

    server_identifier = sys.argv[1]  # Can be either "server" or "user@server"
    namespace = sys.argv[2]

    ssh_with_totp(server_identifier, namespace)

