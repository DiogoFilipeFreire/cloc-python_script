import platform
import subprocess
import smtplib
import getpass
from email.mime.text import MIMEText

def is_app_installed(app_name):
    try:
        subprocess.run([app_name, "--version"], capture_output=True, text=True, check=True)
        print(f"{app_name} installed.")
        return True
    except subprocess.CalledProcessError:
        print(f"{app_name} not installed.")
        return False
    except FileNotFoundError:
        print(f"{app_name} not found.")
    except Exception as e:
        print(f"Error for checking {app_name}: {e}")

def yn_user_input(string):
    choice = input(string +  "(y/n): ").strip().lower()
    
    while choice not in ["y", "n"]:
        print("Invalid choice. Please enter 'y' or 'n'.")
        choice = input(string +  "(y/n): ").strip().lower()
    
    return choice == "y"

def package_manager_configuration():
    if platform.system() == "Darwin":  # macOS
        try:
            subprocess.run(["which", "brew"], capture_output=True, check=True)
            print("Homebrew installed.")
        except subprocess.CalledProcessError:
            print("Homebrew not installed.")
            if yn_user_input("Do you want to install Homebrew?"):
                subprocess.run(['/bin/bash', '-c', 
                            '"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'])
            print("Homebrew installation completed.")
    elif platform.system() == "Windows":  # Windows
        try:
            subprocess.run(["winget", "--version"], capture_output=True, check=True)
            print("Windows Package Manager (winget) installed.")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Windows Package Manager (winget) not installed.")
            if yn_user_input("Do you want to install Windows Package Manager (winget)?"):
                subprocess.run(['powershell', '-Command', 
                            '$progressPreference = \'silentlyContinue\'; '
                            'Invoke-WebRequest -Uri https://aka.ms/getwinget -OutFile Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle; '
                            'Invoke-WebRequest -Uri https://aka.ms/Microsoft.VCLibs.x64.14.00.Desktop.appx -OutFile Microsoft.VCLibs.x64.14.00.Desktop.appx; '
                            'Invoke-WebRequest -Uri https://github.com/microsoft/microsoft-ui-xaml/releases/download/v2.7.3/Microsoft.UI.Xaml.2.7.x64.appx -OutFile Microsoft.UI.Xaml.2.7.x64.appx;'])
            subprocess.run(['powershell', '-Command', 
                            'Add-AppxPackage Microsoft.VCLibs.x64.14.00.Desktop.appx; '
                            'Add-AppxPackage Microsoft.UI.Xaml.2.7.x64.appx; '
                            'Add-AppxPackage Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle;'])
            print("Windows Package Manager (winget) installation completed.")
    elif platform.system() == "Linux":  # Linux with apt
        try:
            subprocess.run(["apt", "--version"], capture_output=True, check=True)
            print("APT installed.")
        except subprocess.CalledProcessError:
            print("APT not installed. Please install APT to use this script.")
    else:
        print("Unsupported OS")
    return

def package_install(package_name):
    if package_name == "git":
        if platform.system() == "Darwin":
            command = ["brew", "install", package_name]
        elif platform.system() == "Windows":
            command = ["winget", "install", "-e", "--id", "Git.Git"]
        elif platform.system() == "Linux":
            command = ["sudo", "apt", "install", "-y", package_name]
        else:
            print("Unsupported OS")
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError:
            print(f"Failed to install {package_name}.")
    else:
        if platform.system() == "Darwin":
            command = ["brew", "install", package_name]
        elif platform.system() == "Windows":
            command = ["winget", "install", "-e", "--id", package_name]
        elif platform.system() == "Linux":
            command = ["sudo", "apt", "install", "-y", package_name]
        else:
            print("Unsupported OS")
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError:
            print(f"Failed to install {package_name}.")

def git_processing(repo_link):
    def clone_repo(link):
        try:
            subprocess.run(["git", "clone", link, "new_custom_directory"], capture_output=True, text=True)
            print("repo cloned")
        except subprocess.CalledProcessError:
            print("error cloning repo")
    
    if is_app_installed("git"):
        clone_repo(repo_link)
    else:
        if yn_user_input("Do you want to install Git?: "):
            package_install("git")
            clone_repo(repo_link)

def cloc_processing():
    def run_cloc():
        if platform.system() == "Windows":
            cloc_path = input("Enter cloc executable path:")
            try:
                result = subprocess.run([cloc_path, "new_custom_directory"], capture_output=True, text=True, check=True)
                return result.stdout
            except subprocess.CalledProcessError as e:
                print(f"Error running CLOC: {e}")
        else: 
            try:
                result = subprocess.run(["cloc", "new_custom_directory"], capture_output=True, text=True, check=True)
                return result.stdout
            except subprocess.CalledProcessError as e:
                print(f"Error running CLOC: {e}")
                return None
    if platform.system() == "Windows":
        cloc_result = run_cloc()
    elif platform.system() != "Windows" and is_app_installed("cloc"):
        cloc_result = run_cloc()
    else:
        if yn_user_input("Do you want to install CLOC?:"):
            package_install("cloc")
            cloc_result = run_cloc()
    return cloc_result

def send_email(body):
    if yn_user_input("Do you want to send the results via email?"):
        gmail_address = input("Enter your gmail address: ")
        gmail_password = getpass.getpass("Enter your password: ")
        email_subject = input("Enter the subject of the email: ")
        to_email = input("Enter email address destination: ")
        

        msg = MIMEText(body)
        msg['From'] = gmail_address
        msg['To'] = to_email
        msg['Subject'] = email_subject

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            try:
                smtp_server.ehlo()
                smtp_server.login(gmail_address, gmail_password)
                smtp_server.sendmail(gmail_address, to_email, msg.as_string())
                print('Email sent!')
            except Exception as e:
                print(f'Error sending email: {e}')        

if __name__ == "__main__":
    print(platform.system())
    package_manager_configuration()
    repo_link = input("Enter repository ink: ")
    git_processing(repo_link)
    cloc_result_on_git = cloc_processing()
    email_body = "CLOC's results for repository " + repo_link + " :\n" + cloc_result_on_git
    print(email_body)
    send_email(email_body)