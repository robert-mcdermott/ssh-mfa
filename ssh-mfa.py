#!/home/rmcdermo/.local/bin/uv run
import pexpect
import getpass
import sys
import subprocess

def get_totp_code(namespace, servername):
    try:
        result = subprocess.run([
            "totp-cli", "generate", namespace, servername
        ], capture_output=True, text=True, input=getpass.getpass("TOTP Password: "))
        
        if result.returncode == 0:
            return result.stdout.strip().split("\n")[-1]  # Extract the last line (TOTP code)
        else:
            print("Failed to generate TOTP code.", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"Error generating TOTP: {e}", file=sys.stderr)
        sys.exit(1)

def ssh_with_totp(server, namespace):
    password = getpass.getpass("SSH Password: ")
    totp_code = get_totp_code(namespace, server)
    
    ssh_command = f"ssh {server}"
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
        print("Usage: python ssh_totp.py <server> <namespace>")
        sys.exit(1)
    
    server = sys.argv[1]
    namespace = sys.argv[2]
    
    ssh_with_totp(server, namespace)

