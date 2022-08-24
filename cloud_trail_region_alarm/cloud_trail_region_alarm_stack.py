from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_cloudtrail as cloudtrail,
    aws_logs as logs,
    aws_cloudwatch_actions as actions,
    CfnParameter
)
from constructs import Construct

class CloudTrailRegionAlarmStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        email_address = CfnParameter(self, "email")
        aws_region = CfnParameter(self, "aws-region")

        #first we create a trail activated in all regions and sending info to Cloudwatch
        myTrail = cloudtrail.Trail(self, "myCloudTrail",
            send_to_cloud_watch_logs=True,
            management_events=cloudtrail.ReadWriteType.WRITE_ONLY
        )

       #second we create an SNS topic with a subscription
        mySNSTopic = sns.Topic(self, "CloudTrailAlarmsTopic")
        mySNSTopic.add_subscription(subscriptions.EmailSubscription(email_address.value_as_string))

        #then we create a filter in the cloudwatch log group
        myLogGroup = myTrail.log_group

        myMetricFilter = myLogGroup.add_metric_filter("RegionsNotAllowed",
            metric_namespace=self.stack_name,
            metric_name="RegionsNotAllowed",
            filter_pattern=logs.FilterPattern.all(
                logs.FilterPattern.string_value("$.awsRegion","!=",aws_region.value_as_string),
                logs.FilterPattern.string_value("$.eventSource","!=","sts.amazonaws.com")
            ),
            metric_value="1",
            default_value=0
        )

        #At last, we create an alarm that publish on the SNS topic
        myAlarm = myMetricFilter.metric(statistic="sum").create_alarm(self, "Alarm",
            threshold=1,
            evaluation_periods=1,
            datapoints_to_alarm=1
        )

        myAlarm.add_alarm_action(actions.SnsAction(mySNSTopic))

 

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "CloudTrailRegionAlarmQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
