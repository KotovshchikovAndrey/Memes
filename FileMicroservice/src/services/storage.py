import aioboto3
import httpx

from config.settings import settings


async def get_image_url(image_name: str) -> str:
    session = aioboto3.Session()
    async with session.client(
        "s3",
        endpoint_url=f"http://{settings.s3_host}:{settings.s3_port}",
        aws_access_key_id=settings.s3_access_key,
        aws_secret_access_key=settings.s3_secret_key,
        use_ssl=False,
    ) as s3_client:
        url = await s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.s3_bucket, "Key": image_name},
            ExpiresIn=3600,  # 1 hour
        )

        return url


async def upload_image(image_name: str) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=f"{settings.api_service_url}/api/v1/memes/images/{image_name}"
        )

        if response.status_code == 404:
            return

    session = aioboto3.Session()
    async with session.client(
        "s3",
        endpoint_url=f"http://{settings.s3_host}:{settings.s3_port}",
        aws_access_key_id=settings.s3_access_key,
        aws_secret_access_key=settings.s3_secret_key,
        use_ssl=False,
    ) as s3_client:
        await s3_client.put_object(
            Bucket=settings.s3_bucket,
            Key=image_name,
            Body=await response.aread(),
            ACL="public-read",
        )

    async with httpx.AsyncClient() as client:
        await client.delete(
            url=f"{settings.api_service_url}/api/v1/memes/images/{image_name}"
        )
