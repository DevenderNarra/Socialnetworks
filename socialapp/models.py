from django.db import models
from .constants import ReactionType

class User(models.Model):
    name = models.CharField(max_length=100)
    profile_pic = models.URLField()


class Post(models.Model):
    content = models.TextField(max_length=1000)
    posted_at = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")


class Comment(models.Model):
    content = models.TextField(max_length=1000)
    commented_at = models.DateTimeField(auto_now_add=True)
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    parent_comment = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies")


class Reaction(models.Model):
    reaction = models.CharField(max_length=100, choices=[(tag.name, tag.value) for tag in ReactionType])
    reacted_at = models.DateTimeField(auto_now_add=True)
    reacted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reactions")
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE, related_name="reactions")
    comment = models.ForeignKey(Comment,null=True, blank=True, on_delete=models.CASCADE, related_name="reactions")

class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    members = models.ManyToManyField(
        User,
        through='Membership',
        related_name='groups'
    )

class Membership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

    class Meta:
        unique_together = ('group', 'member')