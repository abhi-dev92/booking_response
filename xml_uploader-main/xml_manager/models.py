# xml_manager/models.py
from django.db import models


class XMLFile(models.Model):
    """
    Model representing an uploaded XML file.

    Follows best practices:
    - Uses auto-incremented integer as primary key
    - Adds timestamps for tracking
    - Includes file name for better file management
    - Provides a descriptive string representation
    """
    id = models.AutoField(primary_key=True)

    content = models.TextField(help_text="XML file content stored as text")

    file_name = models.CharField(
        max_length=255,
        help_text="Original name of the uploaded XML file",
        blank=True,
        null=True
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String representation of the XML file.
        Truncates content for readability.
        """
        return f"XML File {self.file_name or self.id} - uploaded at {self.uploaded_at}"

    class Meta:
        """
        Meta options for the model.
        Ensures consistent ordering and provides a meaningful table name.
        """
        ordering = ['-uploaded_at']
        verbose_name = 'XML File'
        verbose_name_plural = 'XML Files'
        db_table = 'xml_file'  # Matches the specified database table name