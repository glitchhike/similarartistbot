import dataset
from similar import check_album
from config import db_address

def insert_suggestion(message):
    # connecting to a SQLite database
    db = dataset.connect(db_address)

    table = db['user']
    
    # split message into Artist and Album
    s = message.text[9:].split(' - ', 2)

    # search lstfm for artist and album
    found = check_album(s[0], s[1])
    
    # insertin database
    table.insert(dict(#sender=message.from_user, 
                      sender_id=message.from_user.id, 
                      message_id=message.message_id,
                      timestamp=message.date,
                      suggested_artist=s[0],
                      suggested_album=s[1],
                      found_on_lastfm=found))
