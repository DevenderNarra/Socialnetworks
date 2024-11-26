
class InvalidUserException(Exception):
    def __init__(self, user_id):
        message=f'Invalid user id {user_id}'
        super().__init__(message)

class InvalidPostContent(Exception):
    def __init__(self, post_content):
        message=f'Invalid post content {post_content}'
        super().__init__(message)

class InvalidPostException(Exception):
    def __init__(self, post_id):
        message=f'Invalid post content {post_id}'
        super().__init__(message)

class InvalidCommentContent(Exception):
    def __init__(self, comment_content):
        message=f'Invalid post content {comment_content}'
        super().__init__(message)

class InvalidReplyContent(Exception):
    def __init__(self, reply_content):
        message=f'Invalid post content {reply_content}'
        super().__init__(message)
class InvalidReactionTypeException(Exception):
    def __init__(self, reaction_type):
        message=f'Invalid post content {reaction_type}'
        super().__init__(message)

class UserCannotDeletePostException(Exception):
    def __init__(self, user_id):
        message=f'User {user_id} cannot be deleted'
        super().__init__(message)


class InvalidCommentException(Exception):
    def __init__(self, comment_id):
        message=f'Invalid comment id {comment_id}'
        super().__init__(message)

class InvalidGroupNameException(Exception):
    def __init__(self, group_name):
        message=f'Invalid group name {group_name}'
        super().__init__(message)

class InvalidMemberException(Exception):
    def __init__(self, member_id):
        message=f'Invalid member id {member_id}'
        super().__init__(message)

class InvalidGroupNameException(Exception):
    def __init__(self, group_name):
        message=f'Invalid group name {group_name}'
        super().__init__(message)
class UserNotInGroupException(Exception):
    def __init__(self, user_id):
        message=f'User {user_id} not in group'
        super().__init__(message)

class InvalidOffSetValueException(Exception):
    def __init__(self, offset_value):
        message=f'Invalid offset value {offset_value}'
        super().__init__(message)
class InvalidLimitSetValueException(Exception):
    def __init__(self, limit_set_value):
        message=f'Invalid limit set value {limit_set_value}'
        super().__init__(message)