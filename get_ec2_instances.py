import boto3

def get_instances():
    ec2 = boto3.client('ec2', region_name="us-east-1")

    ris = get_reserved_instances(ec2)
    ins = get_running_instances(ec2)
    print ins

    for ri, count in ris.items():
        ins[ri] -= count

    return ins

def get_reserved_instances(client):
    resp = {}
    ris = client.describe_reserved_instances(
        Filters=[{'Name': 'state', 'Values': ['active', ]}])

    for ri in ris['ReservedInstances']:
        k = ri['InstanceType']
        try:
            resp[k] += ri['InstanceCount']
        except:
            resp[k] = ri['InstanceCount']

    return resp


def get_running_instances(client):
    ins = {}
    nt = None
    _args = {
        "Filters": [{'Name': 'instance-state-name', 'Values': ['running']}]
    }

    while True:
        if nt:
            _args['NextToken'] = nt

        resp = client.describe_instances(**_args)

        for r in resp['Reservations']:
            for i in r['Instances']:
                if 'SpotInstanceRequestId' in i:
                    continue

                try:
                    ins[i['InstanceType']] += 1
                except:
                    ins[i['InstanceType']] = 1

        try:
            nt = resp['NextToken']
        except:
            break

    return ins
