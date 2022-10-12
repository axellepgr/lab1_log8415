import boto3
import set_up_instances

class LoadBalancer:
    
    def __init__(self, security_group_id, subnet_id, target_group_arn):
        self.elbv2_client = boto3.client('elbv2')
        self.ec2_resource = boto3.resource('ec2')
        self.load_balancer_arn = None
        self.dns_name = None
        self.security_group_id = security_group_id
        self.subnet_id = subnet_id
        self.listener_arn = None
        self.rules_arn = None
        self.tg_arn = target_group_arn

    def setup(self):
        self.create_load_balancer()
        self.create_listener()
        return self.get_lb_dns()
        
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
        
    def get_lb_arn(self):
        return self.load_balancer_arn
    
    def get_lb_dns(self):
        return self.dns_name
        
    def create_listener(self):
        response = self.elbv2_client.create_listener(
            LoadBalancerArn=self.load_balancer_arn,
            Protocol='HTTP',
            Port=80,
            DefaultActions=[
                {
                    'Type': 'forward',
                    'ForwardConfig': {
                        'TargetGroups': [
                            {
                                'TargetGroupArn': str(self.tg_arn[0]),
                                'Weight': 2
                            },
                            {
                                'TargetGroupArn': str(self.tg_arn[1]),
                                'Weight': 1
                            }
                        ],
                    }
                },
            ],
            Tags=[
                {
                    'Key': 'string',
                    'Value': 'string'
                },
            ]
        )
        self.listener_arn = response['Listeners'][0]['ListenerArn']
        
    # def create_listener(self):
    #     response = self.elbv2_client.create_listener(
    #         LoadBalancerArn=self.load_balancer_arn,
    #         Protocol='HTTP',
    #         Port=80,
    #         DefaultActions=[
    #             {
    #                 'Type': 'fixed-response',
    #                 'FixedResponseConfig': { 'StatusCode': '404' },
    #             },
    #         ],
    #         Tags=[
    #             {
    #                 'Key': 'string',
    #                 'Value': 'string'
    #             },
    #         ]
    #     )
    #     self.listener_arn = response['Listeners'][0]['ListenerArn']
    
    # def add_rules(self):
    #     for i in range(len(self.tg_arn)):
    #         indice = i+1
    #         response = self.elbv2_client.create_rule(
    #             ListenerArn=self.listener_arn,
    #             Conditions=[
    #                 {
    #                     'Field': 'path-pattern',
    #                     'Values': [f'/cluster{indice}']
    #                 },
    #             ],
    #             Priority=indice,
    #             Actions=[
    #                 {
    #                     'Type': 'forward',
    #                     'TargetGroupArn': self.tg_arn[i],
    #                 },
    #             ]
    #         )
    #         #self.rules_arn.append( response['Rules'][0]['RuleArn'] )
        
    def delete_listener(self):
        self.elbv2_client.delete_listener(ListenerArn=self.listener_arn)
        self.listener_arn = None
        print('Listener deleted.')
        
    def get_listener_arn(self):
        return self.listener_arn
