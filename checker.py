import boto3


def list_buckets(s3):
    response = s3.list_buckets()
    buckets = response["Buckets"]
    print("Buckets:")
    for bucket in buckets:
        print(f"  - {bucket['Name']}")


def check_public_access_blocked(s3, bucket_name):
    try:
        response = s3.get_public_access_block(Bucket=bucket_name)
        public_access_block = response["PublicAccessBlockConfiguration"]
        settings = [
            "BlockPublicAcls",
            "IgnorePublicAcls",
            "BlockPublicPolicy",
            "RestrictPublicBuckets",
        ]

        print(f"Public access block settings for '{bucket_name}':")
        for setting in settings:
            private = public_access_block.get(setting, False)
            status = "PRIVATE" if private else "PUBLIC"
            print(f"  - {setting}: {status}")

        if all(public_access_block.get(setting, False) for setting in settings):
            print(f"Bucket '{bucket_name}' has public access fully blocked.")
        else:
            print(f"Bucket '{bucket_name}' does NOT have public access fully blocked.")
    except s3.exceptions.NoSuchPublicAccessBlockConfiguration:
        print(
            f"Bucket '{bucket_name}' does NOT have a public access block configuration set up."
        )


if __name__ == "__main__":
    s3 = boto3.client("s3")
    response = s3.list_buckets()
    buckets = response["Buckets"]

    list_buckets(s3)

    print("\nPublic access review:")
    for bucket in buckets:
        check_public_access_blocked(s3, bucket["Name"])
