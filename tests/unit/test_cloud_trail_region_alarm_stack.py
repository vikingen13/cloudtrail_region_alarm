import aws_cdk as core
import aws_cdk.assertions as assertions

from cloud_trail_region_alarm.cloud_trail_region_alarm_stack import CloudTrailRegionAlarmStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cloud_trail_region_alarm/cloud_trail_region_alarm_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CloudTrailRegionAlarmStack(app, "cloud-trail-region-alarm")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
