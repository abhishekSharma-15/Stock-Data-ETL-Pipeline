from minio import Minio
from minio.versioningconfig import VersioningConfig

def configure_versioning(client: Minio) -> None:
    client.set_bucket_versioning(
        "stock-data-raw",
        VersioningConfig("Enabled")
    )