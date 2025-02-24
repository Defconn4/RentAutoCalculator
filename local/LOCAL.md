<a id="readme-top"></a>

# Local Script Execution Tutorial

This guide explains how to run the rent calculation and notification scripts locally from the `./local` directory in this repository. The scripts are designed to simulate the AWS Lambda functionality on your local machine, including sending an email using AWS SES via the AWS CLI and the `boto3` library.

> **Note:**  
> Before running the scripts, ensure that you have set up your credentials `login_info.py` located in the parent directory. This file must contain your AWS SES email settings, your login credentials for the web portal, roommate names, etc.

---

## Prerequisites

- **Python 3.10**  
  Ensure Python 3.10 (or later) is installed on your machine.

  - **Windows:** [Download Python for Windows](https://www.python.org/downloads/windows/)
  - **Mac:** [Download Python for macOS](https://www.python.org/downloads/macos/)

- **PIP**  
  PIP should be installed along with Python. You can verify by running:

  ```sh
  pip --version
  ```

- **AWS CLI & Selenium**
  Install and configure the AWS CLI to enable the boto3 library to interact with AWS SES. To do this, simply install the local `requirements.txt`:

  ```sh
   pip install -r requirements.txt
  ```

- Installation:
  Follow the [AWS CLI Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).

- Configuration:
  Run the following command and provide your AWS Access Key, Secret Key, and region:
  ```sh
  aws configure
  ```

## Directory Structure

```sh
    /project-root
    │
    ├── local/
    │ ├── lambda_function_local.py
    | ├── rent_scraper_local.py
    | ├── requirements.txt  # This file
    │ └── LOCAL.md
    │
    ├── login_info.py       # Contains your rental login credentials and other metadata.
    └── other files...
```

## Running the Script Locally

1. Run the main script (lambda_function_local.py), which will:
   - Call the Selenium scraper (in rent_scraper_local.py) to retrieve the latest rent information.
   - Calculate the rent and utilities.
   - Attempt to send an email using AWS SES via the AWS CLI and boto3.
2. Run the script using Python:

```sh
python lambda_function_local.py
```

> **Tip for Windows Users**:
> If you have multiple versions of Python installed, you might need to use `python3` instead of `python`.

3. Verify the Output

- Once executed, you should see the following printed to your terminal:
  - Confirmation messages from each step (e.g., navigating to the login page, entering credentials, etc.).
  - **A summary report to your recipient email that includes**:
    - Current rent balance.
    - Total base rent.
    - Total utilities cost.
    - Calculated rent for each roommate.
    - A message indicating that the email was sent (or an error message if something went wrong).

## Troubleshooting

- **Missing `login_info.py`**:

  - Ensure that login_info.py exists in the parent directory with the required constants. The script will raise an exception if it's not found.

- **AWS SES Email Issues**:

  - Verify that your AWS CLI is configured correctly and that your AWS SES settings (verified emails, region, etc.) are properly set up in login_info.py.

## Additional Notes

- **Local Testing Only**:

  - This script is for local, non-AWS execution and is meant for development and testing purposes. For production, the same logic is intended to run on AWS Lambda triggered via a scheduled event (CRON job) integrated into AWS CodeBuild and CodePipeline.

- **Debugging**:

  - If you experience issues, check the printed logs in the terminal for detailed error messages. Consider adding more print statements for further debugging as needed.

Happy coding, and enjoy automating your rent calculation process!

<p align="right">(<a href="#readme-top">back to top</a>)</p>
