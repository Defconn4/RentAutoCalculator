<!-- PROJECT SHIELDS -->

### Easy Links

<!-- [![Stars][stars-shield]][stars-url] -->

[![LinkedIn][linkedin-shield]][linkedin-url]

<div align="center">
  <h3 align="center">Automated Monthly Rent Calculator</h3>

  <p align="center">
    A simple AWS-powered service that automates the monthly calculation of rent for my apartment and sends an email report. This script can be run locally or deployed via AWS.
    <br /><br />
    I like to automate things and I had to find an excuse to use my AWS Cloud Practitioner knowledge lol.
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#the-story">The Story</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#what-i-learned">What I Learned</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

Every month, I used to manually enter rent details into a local Excel sheet and then send a group text to my roommates with the updated figures. This repetitive process was not only time-consuming but also error-prone.

After earning my AWS Cloud Practitioner Certification, I saw an opportunity to build a simple AWS service that automates this process. This project uses AWS Lambda (triggered by a monthly CRON schedule), CodeBuild, CodePipeline, and CodeDeploy to:

- Scrape my rent portal for the latest balance using Selenium.
- Calculate the rent share based on predefined parameters.
- Send an email with a detailed monthly rent calculation report.

### The Story

I embarked on this project to solve a practical problem in my everyday life. Managing rent and splitting costs among roommates is just kinda annoying. I love automating tedious tasks and figured this would be a good way to actually make use of my Cloud Practitioner knowledge, so I hammered some AWS services in here.

### Built With

- **AWS Lambda** – Serverless compute to run the monthly task.
- **AWS CodeBuild** – To package the project.
- **AWS CodePipeline** – To automate deployment from GitHub.
- **AWS CodeDeploy** – For updating the Lambda function.
- **Python 3.10** – The programming language used.
- **Selenium** – For web scraping the rent portal.
- **Boto3** – AWS SDK for Python.
- **AWS SES** – To send email reports.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

I will provide configuration steps on how to set up the project for deployment with AWS.

### Prerequisites

- AWS Account with access to Lambda, CodeBuild, CodePipeline, CodeDeploy, and SES.
- Python 3.10 installed locally.
- Git installed.
- Download the Chrome Labs Chromium Binary to run Selenium [here](https://googlechromelabs.github.io/chrome-for-testing/#stable).
  - If you don't want to peruse the versions, here is version [1.33.0.6943.53 for Win64](https://storage.googleapis.com/chrome-for-testing-public/133.0.6943.53/win64/chrome-win64.zip).
- [Selenium WebDriver](https://www.selenium.dev/) and appropriate binaries for headless Chrome (for local testing).
- AWS CLI configured with appropriate IAM permissions.

### Installation

1. **Clone the Repository**

   ```sh
   git clone https://github.com/your_github_username/Automated-Monthly-Rent-Calculator.git
   cd Automated-Monthly-Rent-Calculator
   ```

2. **Install Python Dependencies**

   ```sh
   pip install -r requirements.txt
   ```

3. **Refer to the `deployment.md` file for further instructions on AWS. I did not want to clutter this README with a vast amount of instructions.**

<p align="right">(<a href="#readme-top">back to top</a>)</p> <!-- USAGE -->

### Usage

This project runs as a monthly CRON job on AWS Lambda. Here’s how it works:

1. **Monthly Trigger**:

   - The Lambda function is scheduled to run once a month using an AWS CRON expression (via CloudWatch Events/EventBridge).

2. **Rent Data Collection**:

   - When triggered, the Lambda function calls the Selenium scraper (rent_scraper.py), which logs into the rent portal, scrapes the current balance, and returns the data.

3. **Calculation and Reporting**:

   - The main handler in lambda_function.py combines the scraped data with static rent calculations and creates an email report.

4. **Email Notification**:

   - The report is sent to the designated email address using AWS SES.

5. **CI/CD Pipeline**:

   - CodePipeline and CodeBuild automatically update the Lambda function whenever code is pushed to GitHub.

<p align="right">(<a href="#readme-top">back to top</a>)</p> <!-- WHAT I LEARNED -->

### What I Learned

1. **AWS Cloud Services Integration**:

   - I gained hands-on experience with AWS Lambda, CodeBuild, CodePipeline, CodeDeploy by automating deployments from GitHub.

2. **Serverless Architecture**:

   - I learned how to build and deploy a serverless application that handles scheduled tasks and integrates multiple AWS services.

3. **Selenium Web Scraping**:

   - I improved my skills with Selenium for automating browser interactions and scraping dynamic web pages.

4. **Problem Solving & Automation**:

   - I transformed a tedious, manual process into an automated solution, showcasing an entrepreneurial mindset and efficient problem solving.

<p align="right">(<a href="#readme-top">back to top</a>)</p> <!-- ROADMAP -->

### Roadmap

1. **Local Script Usage**:

   - [x] Add a separate directory with files to run this script locally instead of needing
         to rely on AWS, in the case of hitting free monthly usage limits like I currently have due to debugging.

2. **Basic Automation**:

   - [ ] Automate monthly rent calculation and email reporting using AWS Lambda, SES, and scheduled CRON jobs. I am currently waiting for my AWS monthly free usage limits to reset for AWS CodeBuild and AWS CodePipeline.

3. **Complete CI/CD Integration**:

   - [ ] Fully integrate CodePipeline and CodeBuild to automatically update the Lambda function.

4. **Secure Credential Management**:

   - [ ] Integrate AWS Secrets Manager for secure handling of login credentials.

5. **Enhanced Error Handling**:

   - [ ] Improve logging and error notifications for the Selenium scraper.

6. **Portfolio Documentation**:
   - [ ] Expand documentation and add examples to better showcase this project in my personal portfolio.

<p align="right">(<a href="#readme-top">back to top</a>)</p> <!-- CONTACT -->

## Contact

- Feel free to reach me at fcostant.business@gmail.com

- Project Link: [https://github.com/Defconn4/RentAutoCalculator](https://github.com/Defconn4/RentAutoCalculator)

- LinkedIn: [https://www.linkedin.com/in/frank-costantino-a4a61b133/](https://www.linkedin.com/in/frank-costantino-a4a61b133/)

<p align="right">(<a href="#readme-top">back to top</a>)</p> <!-- END -->

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

<!-- [stars-shield]: https://img.shields.io/github/stars/Defconn4/RentAutoCalculator
[stars-url]: https://github.com/Defconn4/RentAutoCalculator -->

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/frank-costantino-a4a61b133/
