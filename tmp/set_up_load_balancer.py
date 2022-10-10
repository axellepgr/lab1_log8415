import boto3
import set_up_instances

class LoadBalancer:
    
    def __init__(self, security_group_id, subnet_id):
        self.elbv2_client = boto3.client('elbv2')
        self.ec2_resource = boto3.resource('ec2')
        self.load_balancer_arn = None
        self.dns_name = None
        self.security_group_id = security_group_id
        self.subnet_id = subnet_id

    def create_load_balancer(self):
        print('Creating load balancer...')
        response = self.elbv2_client.create_load_balancer(
        Name='Load-balancer-1',
        Subnets=self.subnet_id,
        SecurityGroups=[self.security_group_id],
        Scheme='internet-facing',
        #Tags=[
        #    {
        #        'Key': 'string',
        #        'Value': 'string'
        #    },
        #],
        Type='application',
        IpAddressType='ipv4',
        )
        self.dns_name = response['LoadBalancers'][0]['DNSName']
        self.load_balancer_arn = response['LoadBalancers'][0]['LoadBalancerArn']
        print('Load balancer created at : ' + self.dns_name)

        
    def delete_load_balancer(self):
        self.elbv2_client.delete_load_balancer(LoadBalancerArn=self.load_balancer_arn)
        self.load_balancer_arn = None
        print('Load balancer deleted.')
