# Create EC2 instances using Python BOTO3
import boto3
"""
def create_key_pair():
    ec2_client = boto3.client("ec2", region_name="us-east-1")
    key_pair = ec2_client.create_key_pair(KeyName="ec2-key-pair")

    private_key = key_pair["KeyMaterial"]

    # write private key to file with 400 permissions
    with os.fdopen(os.open("/tmp/aws_ec2_key.pem", os.O_WRONLY | os.O_CREAT, 0o400), "w+") as handle:
        handle.write(private_key)
create_key_pair()

def create_instance():
    ec2_client = boto3.client("ec2", region_name="us-east-1")
    instances = ec2_client.run_instances(
        ImageId="ami-0b0154d3d8011b0cd",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.large",
        KeyName="vockey"
    )

    print(instances["Instances"][0]["InstanceId"])
create_instance()
"""

def create_ec2_instance():
   
    #MaxCount=1, # Keep the max count to 1, unless you have a requirement to increase it
    #InstanceType="t2.micro", # Change it as per your need, But use the Free tier one
    #KeyName="ec2-key" # Change it to the name of the key you have.
    #return Creates the EC2 instance
    
    try:
        print ("Creating EC2 instance")
        resource_ec2 = boto3.client('ec2')
        resource_ec2.run_instances(
            ImageId="ami-00399ec92321828f5",
            MinCount=1,
            MaxCount=5,
            InstanceType="t2.large",
            KeyName="vockey"
        )
    except Exception as e:
        print(e)

create_ec2_instance()


PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP