import boto3
import set_up_instances

class TargetGroup:
    
    def __init__(self, number, vpc_id, instance_id):
        self.elbv2_client = boto3.client('elbv2')
        self.tg_number = number
        self.vpc_id = vpc_id
        self.instance_id = instance_id
        self.target_group_arn = None
    
    def create_target_group(self):
        print('Creating target group ' + str(self.tg_number) + '...')
        response = self.elbv2_client.create_target_group(
            Name=f'target-group-{self.tg_number}',
            Protocol='HTTP',
            ProtocolVersion='HTTP1',
            Port=80,
            VpcId=self.vpc_id,
            HealthCheckEnabled=True,
            HealthCheckPath='/',
            HealthCheckIntervalSeconds=30,
            HealthCheckTimeoutSeconds=6,
            HealthyThresholdCount=5,
            UnhealthyThresholdCount=2,
            TargetType='instance',
            Tags=[
                {
                    'Key': 'string',
                    'Value': 'string'
                },
            ],
            IpAddressType='ipv4'
        )
        self.target_group_arn = response['TargetGroups'][0]['TargetGroupArn']
        print('Target group ' + str(self.tg_number) + ' created.')
        
    def delete_target_groupr(self):
        self.elbv2_client.delete_target_group(TargetGroupArn=self.target_group_arn)
        self.target_group_arn = None
        print('Target group deleted.')
        
    def register_target(self):
        self.elbv2_client.register_targets(
            TargetGroupArn=self.target_group_arn,
            Targets=[
                {
                    'Id': id,
                    'Port': 80
                } for id in self.instance_id
            ]
        )
        print('Instance targets ' + str(self.instance_id) + ' are registered in target group number ' + str(self.tg_number) + '.')
        
    def get_tg_arn(self):
        return self.target_group_arn