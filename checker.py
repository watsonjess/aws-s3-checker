import boto3

def list_buckets(s3):
    response = s3.list_buckets()
    buckets = response["Buckets"]
    print("Buckets:")
    for bucket in buckets:
        print(f"  - {bucket['Name']}")


if __name__ == "__main__":
    s3 = boto3.client("s3")
    list_buckets(s3)
