import boto3
import os

profile = os.environ['AWS_PROFILE']
print "Inventory profile: " + profile

rds_count = 0
ec2_count = 0
lambda_count = 0
regions = ["us-east-1", "us-east-2", "us-west-1", "ap-northeast-1", "ap-northeast-2", "ap-southeast-1", "ap-southeast-2", "ap-south-1", "ca-central-1", "eu-central-1", "eu-west-1", "eu-west-2", "eu-west-3", "eu-north-1", "sa-east-1"]

for region in regions:
    print "[EC2] checking region " + region
    ec2 = boto3.client('ec2', region_name=region)
    ins = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for r in ins['Reservations']:
        for i in r['Instances']:
            if 'SpotInstanceRequestId' in i:
                continue
            else:
                ec2_count += 1

for region in regions:
    print "[RDS] checking region " + region
    rds = boto3.client('rds', region_name=region)
    ins = rds.describe_db_instances()
    rds_count += len(ins['DBInstances'])

for region in regions:
    print "[Lambda] checking region " + region
    lamb = boto3.client('lambda', region_name=region)
    ins = lamb.list_functions()
    lambda_count += len(ins['Functions'])

print "EC2 count is: " + str(ec2_count)
print "RDS count is: " + str(rds_count)
print "Lambda count is: " + str(lambda_count)

f = open(profile + ".txt", "a")
f.write("EC2 count is : " + str(ec2_count) + "\n")
f.write("RDS count is: " + str(rds_count) + "\n")
f.write("Lambda count is: " + str(lambda_count) + "\n")
f.close()

print "Done!"
