from __future__ import print_function
import re
import pprint
import base64
from django.core.files.base import ContentFile
from googleapiclient.errors import HttpError
from .receipts import get_receipt_info_from_file
from .google.service import create_service

# Gmail quota: https://developers.google.com/gmail/api/reference/quota
# Quickstar: https://developers.google.com/gmail/api/quickstart/python


def get_messages(service):
    """
    https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/gmail_v1.users.messages.html#list
    """
    results = service.users().messages().list(userId='me').execute()
    messages = results.get('messages', [])
    return messages


def get_attachment(service, message_id, attachment_id):
    """
    https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/gmail_v1.users.messages.attachments.html#get
    """
    attachment = service.users().messages().attachments().get(
        userId='me', messageId=message_id, id=attachment_id).execute()
    return attachment


def get_message_by_id(service, id):
    """
    https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/gmail_v1.users.messages.html#get
    """
    message = service.users().messages().get(
        userId='me', id=id).execute()
    return message


def trash_message_by_id(service, id):
    """
    https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/gmail_v1.users.messages.html#trash
    """
    message = service.users().messages().trash(
        userId='me', id=id).execute()
    return message


def decode_attachment_data(data):
    return base64.urlsafe_b64decode(data)


def save_attachment(attachment, filename, user):
    from .models import Receipt

    try:
        file = ContentFile(decode_attachment_data(
            attachment['data']), name=filename)

        receipt_info = get_receipt_info_from_file(file)
        new_receipt = Receipt()
        new_receipt.file = file
        new_receipt.filename = filename
        new_receipt.type = receipt_info['type']
        new_receipt.business_name = receipt_info['business_name']
        new_receipt.date = receipt_info['date']
        new_receipt.total = receipt_info['total']
        new_receipt.text = receipt_info['text']
        new_receipt.user = user
        new_receipt.save()
    except Exception as err:
        pprint.pprint(err)


def fetch_gmail_receipts():
    from .models import User
    try:
        # Call the Gmail API
        service = create_service('gmail')
        messages = get_messages(service)
        messages_to_delete = []

        if not messages:
            print('No messages found.')
            return

        for message in messages:
            print('-------------- Processing message ',
                  message['id'], '-------------')
            message_object = get_message_by_id(service, message['id'])

            payload = message_object['payload']
            mimetype = payload['mimeType']
            if mimetype != 'multipart/mixed':
                messages_to_delete.append(message['id'])
                continue

            from_header = first(payload['headers'],
                                lambda h: h['name'] == 'From')['value']
            from_email = re.search("<(\S+)>", from_header).group(1)

            parts = payload.get('parts', [])
            attachment_parts = list(
                filter(lambda p: p['filename'] != '', parts))

            if len(attachment_parts) == 0:
                continue

            users = User.objects.filter(email=from_email)
            if len(users) == 0:
                continue
            user = users[0]

            for attachment_part in attachment_parts:
                attachment = get_attachment(
                    service, message['id'], attachment_part['body']['attachmentId'])
                save_attachment(attachment, attachment_part['filename'], user)

            messages_to_delete.append(message['id'])

        for message_id in messages_to_delete:
            print('Moving', message_id, 'to trash...')
            trash_message_by_id(service, message_id)
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


def first(ls, filterFn):
    filteredList = list(filter(filterFn, ls))
    return filteredList[0] if len(
        filteredList) > 0 else None
