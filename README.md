# GitHub CLOC script

This script aims to automate the cloning of a GitHub repository, to count the lines of code (LOC) and propose the possibility of send the results via email. It verifies the availability of the needed elements (a package manager, git and CLOC) and, if one of those components is missing, it propose to install those package according to the OS.

### Requirements

- Python 3.x
- Supported platforms: MacOS, Windows, Linux(via `apt`)
- On windows Git must be installde and a Cloc executable must be available. More info about cloc on [https://cloc.sourceforge.net/](https://cloc.sourceforge.net/)

### Usage

Run the script using:

```
python pyrepocloc.py
```

Then, in the terminal, if needed confirm the installation of the needed package, insert the link of the repository to clone.

You have the possibility to send the results via email. The script is currently configured to do it via gmail, which requires an "App Password"" for this use case. However, you can easily configure a different STMP server within the function `send_email()`

By accepting to send an email, you will be prompt to insert your email address, password, the subject of the email and the destination email address

### Contribution & Feedback

If you encounter any issues or have feedback, please open an issue on GitHub.
