import jwt
from datetime import datetime, timedelta

... # Define your payload variables

# Encode JWT
encoded_jwt = jwt.encode({
                          "user_id": 1,
                          "exp": datetime.now()+timedelta(minutes=5)
                          },
                          'secret',
                          algorithm='HS256')

# Decode JWT
decoded_jwt = jwt.decode(encoded_jwt, 'secret', algorithms=['HS256'])

print(encoded_jwt, decoded_jwt, sep="\n")
print(decoded_jwt['user_id'])
