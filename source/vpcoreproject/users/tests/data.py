from django.contrib.auth import get_user_model

User = get_user_model()


class UserGenerator:
    data = [
        ("test_user1", "test1@gmail.com", "temporary"),
        ("test_user2", "test2@gmail.com", "temporary"),
        ("test_user3", "test3@gmail.com", "temporary"),
        ("test_user4", "test4@gmail.com", "temporary"),
        ("test_user5", "test5@gmail.com", "temporary"),
        ("test_user6", "test6@gmail.com", "temporary"),
    ]

    def __init__(self):
        self.users = []

    def generate_users(self):
        users = User.objects.all()
        if users.count():
            self.users = users
            return self.users
        for user_data in UserGenerator.data:
            user = User.objects.create_user(*user_data)
            user.password = user_data[2]
            self.users.append(user)
        return self.users
