# Monitoring the creation of AWS ressources with AWS Cloudtrail and Amazon Cloudwatch

This sample demonstrate the use of AWS Cloudtrail and Amazon Cloudwatch to be alerted if ressources are created outside of an allowed region. After deploying this solution in your AWS account, you will receive an e-mail notification each time a "write event" outside an allowed region will be logged by AWS Cloudtrail.

Please note that global service events are logged as occurring in US East 1 region. This means that if the allowed region is not US East 1, user might be alerted in case of the creation of global resources like IAM users.

## Solution architecture

![Architecture overview](images/architecture.png)

## Quick deployment

Please run the following commands in your local shell or in AWS CloudShell.

### **1. Deploy the CDK stack**

``` shell
# Clone the repository 
git clone https://github.com/vikingen13/cloudtrail_region_alarm
cd cloudtrail_region_alarm
# Set up and activate virtual environment
python3 -m venv .env
source .env/bin/activate 
# Install AWS CDK and neccessary CDK libraries
npm install -g aws-cdk
pip3 install -r requirements.txt   
# If first time running CDK deployment in this account / region, run CDK bootstap
# This is a one-time activity per account/region, e.g. 
# cdk bootstrap aws://123456789/us-east-1
cdk bootstrap aws://<Account Id>/<Region name>
# Deploy the stack. Ensure to replace <E-Mail> with the E-Mail adresss to send notifications to and <AWSREGION> by the region where you want to allow the ressource creation. You will be alerted when ressources are created OUTSIDE <AWSREGION>
cdk deploy --parameters email=<EMAIL> --parameters awsregion=<AWSREGION>
```

### **2. Confirm the SNS e-mail subscription**  

Please check your mailbox for an e-mail message with subject "AWS Notification - Subscription Confirmation" and confirm the subscription.

### **3. Test the solution** 

Create a ressource outside the allowed region. You should receive a notification on your email.

### **4.Remove the stack**

``` 
cd cloudtrail_region_alarm
cdk destroy
```

**Note**
This architecture makes an opinionated use of AWS services. Other solutions such as the use of AWS event bridge are possible.
## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

