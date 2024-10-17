from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os

# Example file path (adjust as needed)
FILE_DIRECTORY = '/path/to/save/files/'

@api_view(['POST'])
def create_file(request):
    file_name = request.data.get('file_name')
    
    if not file_name:
        return Response({'error': 'File name is required'}, status=status.HTTP_400_BAD_REQUEST)

    file_path = os.path.join(FILE_DIRECTORY, file_name)

    # Create the file
    try:
        with open(file_path, 'w') as new_file:
            new_file.write('')  # Creates an empty file
        return Response({'message': 'File created successfully!'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)