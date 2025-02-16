from django.contrib.auth.models import User

class UserChecking:
    @staticmethod
    def is_member_of_group(username, groupname):
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            return user.groups.filter(name=groupname).exists()
        else:
            return False