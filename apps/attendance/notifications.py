"""
	This module contains notifications methods such as sending notification, receiving notifications,
	or deleting notifications.

"""


def delete_not_object(obj, id1):
    ''' Makes the particular object of notifications as read '''
    for i in obj:
        if i.id == id1:
            i.mark_as_read()


def not_object(obj, id1):
    ''' This function filter the particular object of notification ''' 
    for i in obj:
        if i.id == id1:
            mydata = {'des':i.description, 'verb': i.verb, 'actor': i.actor, 'recipient': i.recipient,
                        'id': i.id, 'recipient_id': i.recipient_id, 'action_object': i.action_object,
                        'timestamp': i.timestamp}    
    return mydata
