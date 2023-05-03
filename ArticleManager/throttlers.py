from rest_framework.throttling import UserRateThrottle, ScopedRateThrottle

class LoginRateThrottle(UserRateThrottle):
    scope = 'login'

class PublicationUserRateThrottle(UserRateThrottle):
    scope = 'publication'

class PublicationAllRateThrottle(ScopedRateThrottle):
    scope = 'publicationAll'

class TextRateThrottle(UserRateThrottle):
    scope = 'text'

class ProjectRateThrottle(UserRateThrottle):
    scope = 'project'

class CommentRateThrottle(UserRateThrottle):
    scope = 'comment'
