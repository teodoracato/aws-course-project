"""Reads information about the EC2 instance the code is running on.

Every EC2 instance can reach a special internal address, 169.254.169.254
(the Instance Metadata Service, IMDS). It answers questions such as
"which region and availability zone am I in?".

We use IMDSv2: first ask for a short-lived token, then send that token
with every question.
"""

import urllib.request

IMDS_URL = "http://169.254.169.254/latest"
TIMEOUT_SECONDS = 2


def _get_token():
    request = urllib.request.Request(
        IMDS_URL + "/api/token",
        method="PUT",
        headers={"X-aws-ec2-metadata-token-ttl-seconds": "300"},
    )
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        return response.read().decode()


def _get_metadata(path, token):
    request = urllib.request.Request(
        IMDS_URL + "/meta-data/" + path,
        headers={"X-aws-ec2-metadata-token": token},
    )
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        return response.read().decode()


def get_instance_info():
    """Returns region, availability zone and instance id.

    Outside of EC2 (for example on your own computer) the metadata service
    does not exist, so we return "unknown" instead of crashing.
    """
    try:
        token = _get_token()
        return {
            "region": _get_metadata("placement/region", token),
            "availability_zone": _get_metadata("placement/availability-zone", token),
            "instance_id": _get_metadata("instance-id", token),
        }
    except Exception:
        return {
            "region": "unknown (not running on EC2)",
            "availability_zone": "unknown (not running on EC2)",
            "instance_id": "unknown",
        }
