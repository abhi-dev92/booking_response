from rest_framework import serializers
from .models import XMLFile
import xml.etree.ElementTree as ET


class XMLFileSerializer(serializers.ModelSerializer):
    """
    Serializer for XMLFile model.

    Best practices:
    - Supports both JSON and file upload
    - Provides XML content validation
    - Handles file name extraction
    - Dynamically handles content generation
    """
    file = serializers.FileField(write_only=True, required=True)

    class Meta:
        model = XMLFile
        fields = ['id', 'content', 'file_name', 'uploaded_at', 'file']
        extra_kwargs = {
            'content': {'required': False},
            'uploaded_at': {'read_only': True},
            'id': {'read_only': True}
        }

    def validate_file(self, file):
        """
        Validate the uploaded file.

        Args:
            file: Uploaded file object

        Returns:
            file: Validated file object

        Raises:
            serializers.ValidationError: If file is invalid
        """
        # Check file size (optional, example limit of 10MB)
        if file.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("File size should not exceed 10MB")

        # Validate file extension (optional)
        if not file.name.lower().endswith('.xml'):
            raise serializers.ValidationError("Only XML files are allowed")

        return file

    def validate(self, data):
        """
        Validate input data.

        Args:
            data (dict): Input data to validate

        Returns:
            dict: Validated data

        Raises:
            serializers.ValidationError: If XML is invalid
        """
        file = data.get('file')

        if not file:
            raise serializers.ValidationError("File is required")

        try:
            # Read file content
            content = file.read().decode('utf-8')

            # Validate XML content
            try:
                ET.fromstring(content)
            except ET.ParseError as e:
                raise serializers.ValidationError(f"Invalid XML format: {str(e)}")

            # Set content and file name
            data['content'] = content
            data['file_name'] = data.get('file_name', file.name)
        except UnicodeDecodeError:
            raise serializers.ValidationError("Unable to decode file content")
        except Exception as e:
            raise serializers.ValidationError(f"Error processing file: {str(e)}")

        return data

    def create(self, validated_data):
        """
        Custom create method to handle XML file upload.

        Args:
            validated_data (dict): Validated data for XMLFile creation

        Returns:
            XMLFile: Created XMLFile instance
        """
        # Remove file field before creating the model instance
        validated_data.pop('file', None)
        return XMLFile.objects.create(**validated_data)