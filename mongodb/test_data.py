import uuid
import bcrypt

def get_test_users():
    test = {
        "users": [
            {
                "u_id": uuid.uuid4(),
                "u_name": "Mike",
                "u_surname": "Tyson",
                "u_username": "miketheking",
                "u_mail": "mike_tyson@gmail.com",
                "u_password": bcrypt.hashpw(b"123456789", bcrypt.gensalt())
            },
            {
                "u_id": uuid.uuid4(),
                "u_name": "John",
                "u_surname": "Wick",
                "u_username": "bangbang",
                "u_mail": "jonathan_wick@gmail.com",
                "u_password": bcrypt.hashpw(b"dontkillmypuppyb1tch", bcrypt.gensalt())
            },
            {
                "u_id": uuid.uuid4(),
                "u_name": "Daenerys",
                "u_surname": "Targaryen",
                "u_username": "khaalesi",
                "u_mail": "dany@gmail.com",
                "u_password": bcrypt.hashpw(b"dracarys99", bcrypt.gensalt())

            }
        ]
    }

    return test