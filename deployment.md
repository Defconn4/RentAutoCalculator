# AWS Deployment

- I personally had a lot of trouble navigating the AWS console to figure out how everything works together, so this is a separate document with more detailed instructions solely for the AWS Deployment.

1. **Navigating and Setting up AWS**

- **Prerequisites**:

  - Creation of an `buildspec.yml` file is required for AWS CodeBuild to run. The [format](https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html) of the file is very important in ensuring that CodeBuild understands what features are available in that file (i.e. version 0.2 [references specific changes made to the build specification format](https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html#build-spec-ref-versions)).

- **Some things to understand**:
  - AWS CodePipeline operates as a pipe: artifacts are defined in each stage, `Source`, `Build`, and `Deploy`. Outputs of a previous stage of the inputs of a subsequent stage. For example, the `Source` stage produces `SourceArtifact` that is used as the input to the `Build` stage to produce a `BuildArtifact`. Thus, it's pivotal that the artifact names match _exactly_ between stages. This is an issue I ran into many times before understanding the root cause of a typo.

2. **Configure AWS IAM Roles**

- AWS CodeBuild requires a service role to be created with the following permission policies. I don't exactly remember why these are needed, but I found that this is what has worked:

  - (1) **CodeBuildBasePolicy**
  - (2) **CodeBuildCloudWatchLogsPolicy**
  - (3) **CodeBuildSecretsManagerSourceCredentialsPolicy**

- AWS CodePipeline requires an `AWSCodePipelineServiceRole` with the following permission policy attached to the role:

  - (1) **AWSCodePipelineServiceRole**

- The AWS Lambda function requires that you create an IAM role that has 2 permission policies:

  - (1) **AmazonSESFullAccess** - this allows you to send emails using SES from the Lambda
  - (2) **AWSLambdaBasicExecutionRole** - this is required for execution of the Lambda (in the name duh).

- AWS CodeDeploy requires an IAM role for the `DeploymentGroup` you will create later with the following permission policies:
  - (1) **AmazonS3FullAccess** - For uploading the `deployment-package.zip` from the `buildspec.yml` after it is created to S3.
  - (2) **AWSCodeDeployRole** - It just needs this, idk.
  - (3) **AWSLambda_FullAccess** - For being able to execute your Lambda function, assumedly.

3. **Preparing for AWS Deployment**

- Ensure your `buildspec.yml` is correctly configured to package the project into a ZIP file, which it already is for this project's purpose.
- The project is integrated with AWS CodePipeline and CodeBuild for automated deployment which is part of the fuckery of set up and debugging.

- In the AWS Lambda function, set the following environment variables:

  - `EMAIL` - The email used to log into your rental portal.
  - `LOGIN_URL`- The URL of your rental management portal.
  - `ROOMMATE_1, ROOMMATE_2, ROOMMATE_3` - Your name and up to two other roommates, if you have less than 3 total occupants in the unit, you'll have to make adjustments to the `lambda_function.py` file to remove roommates from the `BEDROOMS` variable.
  - `SENDER_EMAIL` – Your verified sender email (I used my personal email for this).
  - `RECIPIENT_EMAIL` – The recipient email address (I used an alternative business email for this).

    - Having 2 separate Gmail accounts is FAR easier than trying to make your way out of the Sandbox for `AWS SNS`, which is not worth spending the time on IMO.

    > **NOTE**:
    > If you do not want to put the above information directly into the environment variables of your AWS Lambda function, you can leverage AWS Secrets Manager instead and pull the credentials from there. I did not do this because I don't care that much, I hope someone hacks me AND pays my rent for me bro.

    - You will need to download Linux-compatible `headless-chromium` and `chromedriver` for AWS and add a **Lambda Layer** to the Lambda function to ensure that Selenium works properly when operating inside of AWS.

      - After downloading the compatible binaries, create the folder structure (layer/bin) and copy the binaries into this folder.
      - ZIP the contents and create the Lambda Layer in the AWS Console, which should look like this:

        ```sh
        bin/
        headless-chromium
        chromedriver
        ```

      - Attach the newly created layer to your Lambda function.
      - Adjust your Lambda function’s timeout (e.g., set it to 60 seconds or more) to accommodate Selenium’s runtime.
      - Select a compatible runtime, in this case, we are using Python 3.10.
      - Now your Lambda function will have the binaries from your layer available under `/opt`. Specifically:

        - The headless Chromium binary will be at: `/opt/bin/headless-chromium`
        - The ChromeDriver binary will be at: `/opt/bin/chromedriver`

- **NOTE**: I'm unsure if the Lambda function needs to source the `deployment-package.zip` (`RentCalcDeploymentPackage` that is created from CodeBuild) that is kept inside of my S3 bucket to keep my code updated, but I did make this change at the time of writing this.

- In AWS EventBridge, a trigger needs to be created to ensure that the Lambda function runs at the end of every month:

  - Create a new rule, give it a name and description, such as `MonthlyRentCalculationRule` and "Triggers the Monthly Rent Calculator Lambda function at 23:59 on the 28th of every month; the Lambda checks if it is the last day."
  - Set the `Event Source` to **Schedule** and enter the following CRON expression:

  ```sh
  cron(59 23 28 * ? *)
  ```

  - **Breakdown of this expression**:

    - 59 → At minute 59

    - 23 → At hour 23 (11:59 PM UTC)

    - 28 → On the 28th day of the month

    - \* → Every month

    - ? → Any day of the week (not used)

    - \* → Every year

    > Note:
    > Although this will trigger on the 28th at 23:59 UTC, your Lambda’s code (using is_last_day_of_month()) will check if it’s really the last day of the month before sending the email. This is necessary because AWS does not support an “L” (last day) specifier.

    - Set the `Target` of the event to the name of the created Lambda function.

- I will briefly illuminate the rest of the required AWS services needed (lol good luck with this part):
  - (1) AWS CodeBuild needs to have a project created that has a GitHub source of the RentCalc repository to pull from. Ensure that **Environment** is set up to to use Ubuntu as the OS with standard runtime(s) and an `aws/codebuild/standard:7.0 image`. Make sure the Buildspec uses `buildspec.yml` in the root directory of the GitHub repository.
    - Artifacts created should be stored in S3. I recommend using the `codepipeline` bucket that already exists. Make sure that the `deployment-package.zip` or whatever you name the outputted artifact from the CodeBuild is properly named here and that build path is selected to be the root (`.`) directory. Finally, the **artifacts packaging** should be a Zip file.
    - I recommend creating a CloudWatch group for capturing CodeBuild logs, since you will be unable to access them otherwise.
    - Select your created IAM role for CodeBuild `codebuild-service-role` (e.g. `codebuild-RentCalc-service-role`).
    - (2) I'm not even sure if you need CodeDeploy for this honestly, but you will need to create a **DeploymentGroup** with the `Compute type` of `AWS Lambda` and a `CodeDeployServiceRole`, with the permissions stated above. I recommend keeping the default deployment configuration otherwise.
    - (3) Finally, you will need to create a CodePipeline, with the source stage coming from your GitHub to capture all updates from EventBridge (when new changes are pushed to your `master` or `main` branch) to ensure that a new build runs from CodeBuild and then the output of CodeBuild is sourced within your CodePipeline.

4. **Debugging (Where I Left Off)**

- To avoid paying past my monthly free usage limit for AWS CodeBuild and CodePipeline, I had t disable my `MonthlyRentCalculationRule` inside of Amazon EventBridge which is what triggers the MonthlyRentCalculator Lambda function at the end of each month. This event runs every time that I push code to my `master` branch on GitHub for my repository. This triggers the `Source` stage of AWS CodePipeline to run, which runs CodeBuild to actually create the `deployment-package.zip` artifact in the `my-lambda-layers-rent-calc` S3 bucket directory.
- AWS CodePipeline repeatedly complains about being unable to find the artifact of `deployment-package.zip` that is created by CodeBuild and then stored in my AWS S3 bucket. It expects to find the `deployment-package.zip` inside of the directory of my GitHub repository's source code, hence I keep seeing `CLIENT_ERROR Message: no matching artifact paths found`, every time my source artifact (my GitHub repository code) builds in the `Source` stage of CopePipeline. It's possible I just don't understand the workflow...

  - CodePipeline outputs the following errors inside of its logs:

  ```sh
  Container] 2025/02/13 20:40:29.926678 Running command echo "Building GitHub Pipeline"
  Building GitHub Pipeline
    [Container] 2025/02/13 20:40:29.933423 Phase complete: BUILD State: SUCCEEDED
    [Container] 2025/02/13 20:40:29.933436 Phase context status code: Message:
    [Container] 2025/02/13 20:40:29.982855 Entering phase POST_BUILD
    [Container] 2025/02/13 20:40:29.984603 Phase complete: POST_BUILD State: SUCCEEDED
    [Container] 2025/02/13 20:40:29.984615 Phase context status code: Message:
    [Container] 2025/02/13 20:40:30.091159 Expanding base directory path: .
    [Container] 2025/02/13 20:40:30.094575 Assembling file list
    [Container] 2025/02/13 20:40:30.094590 Expanding .
    [Container] 2025/02/13 20:40:30.097886 Expanding file paths for base directory .
    [Container] 2025/02/13 20:40:30.097899 Assembling file list
    [Container] 2025/02/13 20:40:30.097902 Expanding deployment-package.zip
    [Container] 2025/02/13 20:40:30.101057 Skipping invalid file path deployment-package.zip
    [Container] 2025/02/13 20:40:30.101447 Phase complete: UPLOAD_ARTIFACTS State: FAILED
    [Container] 2025/02/13 20:40:30.101459 Phase context status code: CLIENT_ERROR Message: no matching artifact paths found
  ```

  - I figured out by going through the AWS CloudWatch logs that the `Build` stage of CodePipeline is using some default CodeBuild `buildspec.yml`, which is why I am unable to properly produce my `deployment-package.zip` in the current directory of my source code, which would allow me to reach the `Deploy` stage of CodePipeline. It appears that this default is the `CODEBUILD_SRC_DIR`.

  ```sh
  [Container] 2025/02/13 21:11:02.822739 YAML location is /codebuild/readonly/buildspec.yml
  ```

  - I am still working on fixing this, it depends on if I care enough to come back to this lol.
