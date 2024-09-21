# teleblock
This script automatically blocks users that message you on telegram if they are not added to your contacts. At this moment, the script is static, so the criteria for a user getting blocked is as follows:

- the number is not in your contacts
- the last **20** messages in the chat are from the number
- the chat is a direct message

The script also adds a logging message to the self chat. To avoid accidental bans however, it is recommended to add the number to your contacts.

To obtain credentials, please consider https://core.telegram.org/api/obtaining_api_id and add the values to your config.json
