# How to create an read-only AWS access keyQ

This document was written in March 2014 as a step-by-step guide to create access keys with read-only permissions on Amazon AWS.

This is my no means a replacement of Amazon AWS documentation.  It's intended for users of Hawkeye to ensure they get the permissions they want to use Hawkeye effectively.

Also note:  This documentation may be slightly out of date with AWS, but we'll do our best to keep it current

## Step 1: Log into AWS

Log into your AWS instance as usual, and you will be presented with the following screen

![Log in to AWS](images/access_key-01-login.png)

* In the center of the screen find the section titled "Deployment & Management"
* Click on the link titled "IAM; Secure AWS Access Control"

## Step 2: Go to IAM

After clicking on IAM, you should be presented with the following (or similar) screen.  I am assuming you already have other users created.

![Go to IAM](images/access_key-02-IAM.png)

* Find the vertical menu on the left of the screen
* Click on the link titled "Users"

## Step 3: Go to Users 

Once you have clicked on Users you should see this screen

![Go to Users](images/access_key-03-Users.png)

* Find the action buttons located above the viewing tab
* Click the button "Create New Users" at the top of the screen

## Step 4: Create Users

After clicking on "Create New Users", you should be presented with this modal dialog to add new users

![Create Users](images/access_key-04-Create-User.png)

* Enter an easily identifyable username that meets your organizational policies
* Check the checkbox labeled "Generate an access key for each User
* Click the "Create" button.

## Step 5: Get Access Keys

After clicking the "Create" button, you should now see this modal dialog

![Get Access Keys](images/access_key-05-Success.png)

* Copy the Access Key ID and Secret Access Key to your Hawkeye configs
* (option) click on the button labled "Download Credentials"
* Click on the button labeled "Close Window"

## Step 6: If you didn't download credentials

If you did not download the credentials, you will see this dialog.  If you did not copy them either, this is your last chance to download the credentials locally.

If you did get a copy of the credentials, you can safely ignore this dialog

![If you didn't download credentials](images/access_key-06-DownloadCredentials.png)

* (optional) Click on the button labeled "Download Credentials"
* Click on the button labeled "Close Window"

## Step 7: Attach a policy to the keys

Once you have successfully created a user, your window should look similar to this, plus any existing users that may have already been there.

![Attach a policy to the keys](images/access_key-07-Attach-Policy.png)

* Find the user you just created
* Click on the user to select that user
* Locate the bottom payne of the window
* Click on the tab labeled "Permissions"
* Find the section titled "User Policies"
* Click on the button labeled "Attach User Policy"

## Step 8: Select a policy to use

After you click on "Attach User Policy" you should be presented with this modal dialog

![Select a policy to use](images/access_key-08-Select-Policy.png)

* Find the section labaled "Read Only Access"
* Click on the button titled "Select" in the "Read Only Access" section

## Step 9: Select the Read Only policy

Once you have selected "Read Only Access" you should be presented with the policy (in JSON format) within a modal dialog

![Select the Read Only policy](images/access_key-09-Read-Only.png)

* Click on the button titled "Access Policy"

## Step 10: Show the final policy used

In the lower payne under the permissions tab, the User Policies section should look similar to this window

![Show the final policy used](images/access_key-10-Show-Policy.png)

* Find the Policy titled "ReadOnlyAccess...."
* Click on the link titled "Show"

## Step 11: The final policy

Your final policy should be listed in a modal dialog.

![The final policy](images/access_key-11-The-Policy.png)

FIN!

# The Final Policy (JSON Format)

This is the final policy created by AWS at the time this document was written.  Unfortunately as Amazon changes services this policy may need to be changed over time.  I'd love to see a more universal read-only policy that doesn't need to be edited as services are added and removed.

In spite of supposedily having universal read-only access we will still receive access denied messages for certain API calls.  The Hawkeye developers are looking into this and will update the documentation to relect anything learned.

``` json "Example Read-Only Policy"
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "appstream:Get*",
        "autoscaling:Describe*",
        "cloudformation:DescribeStacks",
        "cloudformation:DescribeStackEvents",
        "cloudformation:DescribeStackResources",
        "cloudformation:GetTemplate",
        "cloudformation:List*",
        "cloudfront:Get*",
        "cloudfront:List*",
        "cloudtrail:DescribeTrails",
        "cloudtrail:GetTrailStatus",
        "cloudwatch:Describe*",
        "cloudwatch:Get*",
        "cloudwatch:List*",
        "directconnect:Describe*",
        "dynamodb:GetItem",
        "dynamodb:BatchGetItem",
        "dynamodb:Query",
        "dynamodb:Scan",
        "dynamodb:DescribeTable",
        "dynamodb:ListTables",
        "ec2:Describe*",
        "elasticache:Describe*",
        "elasticbeanstalk:Check*",
        "elasticbeanstalk:Describe*",
        "elasticbeanstalk:List*",
        "elasticbeanstalk:RequestEnvironmentInfo",
        "elasticbeanstalk:RetrieveEnvironmentInfo",
        "elasticloadbalancing:Describe*",
        "elastictranscoder:Read*",
        "elastictranscoder:List*",
        "iam:List*",
        "iam:Get*",
        "opsworks:Describe*",
        "opsworks:Get*",
        "route53:Get*",
        "route53:List*",
        "redshift:Describe*",
        "redshift:ViewQueriesInConsole",
        "rds:Describe*",
        "rds:ListTagsForResource",
        "s3:Get*",
        "s3:List*",
        "sdb:GetAttributes",
        "sdb:List*",
        "sdb:Select*",
        "ses:Get*",
        "ses:List*",
        "sns:Get*",
        "sns:List*",
        "sqs:GetQueueAttributes",
        "sqs:ListQueues",
        "sqs:ReceiveMessage",
        "storagegateway:List*",
        "storagegateway:Describe*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
```

