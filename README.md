# ec2-watcher-lambda

Watch your EC2 instances with Lambda.

When EC2 state changes, send notification to [BearyChat](https://bearychat.com/) channel of your choice.

## IAM Permissions

Attach **AmazonEC2ReadOnlyAccess** policy to the IAM role under which the lambda function runs.

## Notification Examples

- EC2 (cn-north-1) **running**: [i-08cfa289619d660eb](https://console.amazonaws.cn/ec2/v2/home?region=cn-north-1#Instances:instanceId=i-08cfa289619d660eb) (prometheus-trial)
- EC2 (cn-north-1) **stopped**: [i-08cfa289619d660eb](https://console.amazonaws.cn/ec2/v2/home?region=cn-north-1#Instances:instanceId=i-08cfa289619d660eb) (prometheus-trial)
- EC2 (cn-north-1) **terminated**: [i-08cfa289619d660eb](https://console.amazonaws.cn/ec2/v2/home?region=cn-north-1#Instances:instanceId=i-08cfa289619d660eb) (prometheus-trial)