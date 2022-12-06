from .google.service import create_service
from googleapiclient.errors import HttpError
from django.core.files import File
from googleapiclient.http import MediaFileUpload

# Drive Quota: https://developers.google.com/drive/api/guides/limits


def get_folder_id_by_user_id(service, user_id):
    # docs: https://developers.google.com/drive/api/v3/reference/files/list
    try:
        # create drive api client
        page_token = None
        query = f"mimeType='application/vnd.google-apps.folder' and name='{user_id}' and trashed=false"
        while True:
            # pylint: disable=maybe-no-member
            response = service.files().list(q=query,
                                            spaces='drive',
                                            fields='nextPageToken, '
                                            'files(id, name)',
                                            pageToken=page_token).execute()
            results = response.get('files', [])

            file = first(results, lambda f: f.get("name") == str(user_id))
            if file is not None:
                return file.get('id')

            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
    except HttpError as error:
        print(F'An error occurred: {error}')
        return None


def create_folder_by_user_id(service, user_id):
    # docs: https://developers.google.com/drive/api/v3/reference/files/create
    try:
        file_metadata = {
            'name': user_id,
            'mimeType': 'application/vnd.google-apps.folder'
        }

        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, fields='id'
                                      ).execute()
        return file.get('id')
    except HttpError as error:
        print(F'An error occurred: {error}')
        return None


def upload_file_to_folder(service, file_data,  folder_id):
    # docs: https://developers.google.com/drive/api/guides/manage-uploads
    try:
        file_metadata = {
            'name': file_data['name'],
            'parents': [folder_id]
        }
        media = MediaFileUpload(file_data['path'],
                                mimetype=file_data['mimetype'], resumable=True)
        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, media_body=media,
                                      fields='id').execute()
        print(F'File ID: "{file.get("id")}".')
        return file.get('id')
    except HttpError as error:
        print(F'An error occurred: {error}')
        return None


def upload_file(user_id, file_data):
    try:
        # create drive api client
        service = create_service('drive')
        user_folder_id = get_folder_id_by_user_id(service, user_id)
        if user_folder_id is None:
            user_folder_id = create_folder_by_user_id(service, user_id)

        upload_file_to_folder(service, file_data, user_folder_id)

    except HttpError as error:
        print(F'An error occurred: {error}')
        return None


def first(ls, filterFn):
    filteredList = list(filter(filterFn, ls))
    return filteredList[0] if len(
        filteredList) > 0 else None
