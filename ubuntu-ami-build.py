import boto3
import time

# Initialize the Boto3 client for EC2
ec2_client = boto3.client('ec2', region_name='us-west-2')  # Change region as needed

# Step 1: Launch an EC2 instance with a base Ubuntu AMI
def launch_instance():
    response = ec2_client.run_instances(
        ImageId='ami-0c55b159cbfafe1f0',  
        InstanceType='t2.micro',
        KeyName='your-key-pair',  
        MinCount=1,
        MaxCount=1,
        SecurityGroupIds=['sg-xxxxxxxx'], 
        SubnetId='subnet-xxxxxxxx'  
    )
    instance_id = response['Instances'][0]['InstanceId']
    print(f'Launched instance with ID: {instance_id}')
    return instance_id

# Step 2: Wait for the instance to be in a running state
def wait_for_instance(instance_id):
    print('Waiting for instance to be in running state...')
    waiter = ec2_client.get_waiter('instance_running')
    waiter.wait(InstanceIds=[instance_id])
    print('Instance is running.')

# Step 3: Customize the instance (installing updates and required software)
def customize_instance(instance_id):
    ssm_client = boto3.client('ssm', region_name='us-west-2')
    
    commands = [
        'sudo apt-get update -y',
        'sudo apt-get upgrade -y',
        'sudo apt-get install -y nginx git python3 python3-pip npm docker.io',
        'sudo systemctl enable nginx',
        'sudo systemctl start nginx',
        'sudo systemctl enable docker',
        'sudo systemctl start docker'
    ]
    
    response = ssm_client.send_command(
        InstanceIds=[instance_id],
        DocumentName='AWS-RunShellScript',
        Parameters={'commands': commands}
    )
    
    command_id = response['Command']['CommandId']
    print(f'Sent command with ID: {command_id}')

    # Wait for the command to complete
    time.sleep(30)
    output = ssm_client.get_command_invocation(CommandId=command_id, InstanceId=instance_id)
    print(f'Command status: {output["Status"]}')

# Step 4: Create an AMI from the instance
def create_ami(instance_id):
    image_name = 'my-custom-ubuntu-ami'
    response = ec2_client.create_image(
        InstanceId=instance_id,
        Name=image_name,
        Description='A custom Ubuntu AMI with NGINX, Git, Python, NPM, and Docker',
        NoReboot=True
    )
    ami_id = response['ImageId']
    print(f'Created AMI with ID: {ami_id}')
    return ami_id

# Step 5: Clean up (terminate the instance)
def terminate_instance(instance_id):
    ec2_client.terminate_instances(InstanceIds=[instance_id])
    print(f'Terminated instance with ID: {instance_id}')

if __name__ == '__main__':
    instance_id = launch_instance()
    wait_for_instance(instance_id)
    customize_instance(instance_id)
    ami_id = create_ami(instance_id)
    terminate_instance(instance_id)
    print(f'Custom AMI created successfully: {ami_id}')
