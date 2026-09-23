from minio import Minio
from minio.versioningconfig import VersioningConfig

def configure_versioning(
    client: Minio,
    bucket: str
) -> None:
    
    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)
        
    client.set_bucket_versioning(
        bucket,
        VersioningConfig("Enabled")
    )