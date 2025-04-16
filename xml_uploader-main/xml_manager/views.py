# xml_manager/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import XMLFile
from .serializers import XMLFileSerializer


class XMLFileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling XML file operations.

    Implements RESTful best practices:
    - Supports multiple upload methods
    - Provides comprehensive file handling
    - Handles file name extraction
    """
    queryset = XMLFile.objects.all()
    serializer_class = XMLFileSerializer

    def list(self, request):
        """
        List all uploaded XML files.

        Returns:
            Response: Serialized list of XML files
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Handle XML file upload.
        Supports both multipart/form-data and raw XML content.

        Args:
            request (Request): HTTP request with XML file or content

        Returns:
            Response: Serialized uploaded XML file or error details
        """
        # Check if it's a multipart file upload
        if 'file' in request.FILES:
            file = request.FILES['file']
            serializer = self.get_serializer(data={
                'file': file,
                'file_name': file.name
            })
        # Check if it's a raw XML content upload
        elif request.content_type in ['application/xml', 'text/xml']:
            try:
                # Read raw XML content
                content = request.body.decode('utf-8')
                serializer = self.get_serializer(data={
                    'content': content,
                    'file_name': request.headers.get('X-Filename', 'unnamed.xml')
                })
            except Exception as e:
                return Response(
                    {'error': f'Error reading XML content: {str(e)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            # Fallback to standard serializer validation
            serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """
        Retrieve a specific XML file by its primary key.

        Args:
            request (Request): HTTP request
            pk (str): Primary key of the XML file

        Returns:
            Response: Serialized XML file or 404 error
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)