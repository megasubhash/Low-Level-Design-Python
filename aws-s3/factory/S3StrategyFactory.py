from ..strategies.StandardS3Strategy import StandardS3Strategy
from ..strategies.MultipartS3Strategy import MultipartS3Strategy

class S3StrategyFactory:
    @staticmethod
    def create_strategy(strategy_type="standard", **kwargs):
        """
        Create an S3 strategy based on the specified type.
        
        Args:
            strategy_type: The type of S3 strategy to create ('standard' or 'multipart')
            **kwargs: Additional parameters for the strategy
                - aws_access_key: AWS access key ID
                - aws_secret_key: AWS secret access key
                - region_name: AWS region name
                - part_size_mb: Size of each part in MB for multipart operations
            
        Returns:
            IS3Strategy: An instance of the requested S3 strategy
        """
        aws_access_key = kwargs.get('aws_access_key')
        aws_secret_key = kwargs.get('aws_secret_key')
        region_name = kwargs.get('region_name')
        
        if strategy_type.lower() == "multipart":
            part_size_mb = kwargs.get('part_size_mb', 5)
            return MultipartS3Strategy(
                aws_access_key=aws_access_key,
                aws_secret_key=aws_secret_key,
                region_name=region_name,
                part_size_mb=part_size_mb
            )
        else:
            # Default to standard strategy
            return StandardS3Strategy(
                aws_access_key=aws_access_key,
                aws_secret_key=aws_secret_key,
                region_name=region_name
            )
