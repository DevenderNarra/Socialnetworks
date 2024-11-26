
from .models import User, Post, Comment,Reaction,Membership,Group
from .exceptions import (InvalidUserException,InvalidPostException,InvalidPostContent,InvalidCommentContent,
                         InvalidReplyContent,InvalidReactionTypeException,UserCannotDeletePostException,InvalidCommentException,
                         InvalidMemberException,InvalidGroupNameException,UserNotInGroupException,InvalidOffSetValueException,InvalidLimitSetValueException)
from .constants import ReactionType
from django.db.models import Q,Count,F
from datetime import datetime

def create_post(user_id, post_content):
      try:
          user=User.objects.get(id=user_id)
      except User.DoesNotExist:
          raise InvalidUserException(user_id)

      if not post_content or len(post_content)<1000:
          raise InvalidPostContent(post_content)

      post=Post.objects.create(content=post_content,posted_by=user)
      return post.id

def create_comment(user_id, post_id, comment_content):
    try:
          user=User.objects.get(id=user_id)
          post=Post.objects.get(id=post_id)
    except User.DoesNotExist:
        raise InvalidUserException(user_id)
    except Post.DoesNotExist:
        raise InvalidPostException(post_id)

    if not comment_content or len(comment_content)<1000:
        raise InvalidCommentContent(comment_content)
    comment=Comment.objects.create(content=comment_content,commenter=user,post=post)
    return comment.id

def reply_to_comment(user_id, comment_id, reply_content):
     try:
         user=User.objects.get(id=user_id)
         comment=Comment.objects.get(id=comment_id)
     except Comment.DoesNotExist:
         raise InvalidCommentContent(comment_id)
     except User.DoesNotExist:
         raise InvalidUserException(user_id)

     if not reply_content or len(reply_content)<1000:
         raise InvalidReplyContent(reply_content)

     reply=Reaction.objects.create(reaction=reply_content,reacted_by=user,comment=comment)
     return reply.id
def react_to_post(user_id, post_id, reaction_type):
    try:
          user=User.objects.get(id=user_id)
          post=Post.objects.get(id=post_id)

          existing_reaction = Reaction.objects.filter(
              Q(post=post) & Q(reacted_by=user)
          ).first()

          if not existing_reaction:
              Reaction.objects.create(
                  post=post,
                  reaction=reaction_type,
                  reacted_by=user,
                  reacted_at=datetime.now()
              )
              return "Reaction created successfully."


    except User.DoesNotExist:
        raise InvalidUserException(user_id)
    except Post.DoesNotExist:
        raise InvalidPostContent(post_id)

    if reaction_type not in ReactionType:
        raise InvalidReactionTypeException(reaction_type)

    reaction=Reaction.objects.create(reaction_type=reaction_type,reacted_by=user,post=post)
    return reaction.id

def react_to_comment(user_id, comment_id, reaction_type):
    try:
          user=User.objects.get(id=user_id)
          comment=Comment.objects.get(id=comment_id)

          existing_reaction = Reaction.objects.filter(
              Q(comment=comment) & Q(reacted_by=user)
          ).first()

          if not existing_reaction:
              Reaction.objects.create(
                  comment=comment,
                  reaction=reaction_type,
                  reacted_by=user,
                  reacted_at=datetime.now()
              )
              return "Reaction created successfully."

          elif existing_reaction.reaction == reaction_type:
              existing_reaction.delete()
              return "Reaction deleted successfully."
          else:
              existing_reaction.reaction = reaction_type
              existing_reaction.reacted_at = datetime.now()
              existing_reaction.save()
              return "Reaction updated successfully."

    except Comment.DoesNotExist:
        raise InvalidCommentContent(comment_id)

    except User.DoesNotExist:
        raise InvalidUserException(user_id)



def get_total_reaction_count():
    reaction_count = Reaction.objects.count()
    return reaction_count


def get_reaction_metrics(post_id):
    try:
            reactions = Reaction.objects.filter(post_id=post_id).values('reaction').annotate(count=Count('reaction'))
            return reactions

    except Post.DoesNotExist:
        raise InvalidPostContent(post_id)

def delete_post(user_id, post_id):
    try:
        get_post=Post.objects.get(id=post_id)
        get_post.delete()
        posted_by=User.objects.get(id=user_id)
    except Post.DoesNotExist:
        raise InvalidPostContent(post_id)
    except User.DoesNotExist:
        raise InvalidUserException(user_id)

    users=User.objects.all()
    if user_id in users.all():
        posted_by.delete()
    else:
        raise UserCannotDeletePostException(user_id)

def get_posts_with_more_positive_reactions():
    posts=list(Reaction.objects.filter(reaction__in =["THUMBS-UP", "LIT", "LOVE", "HAHA", "WOW"]).select_related('reaction'))
    return posts

def get_posts_reacted_by_user(user_id):
    posts = Post.objects.filter(reactions__reacted_by=user_id).distinct()
    return list(posts)


def get_reactions_to_post(post_id):
    try:
        reactions = list(Reaction.objects.filter(post_id=post_id))
        return reactions
    except Post.DoesNotExist:
        raise InvalidPostException(post_id)

def get_post(post_id):
    try:
        post=Post.objects.get(id=post_id)
        return post
    except Post.DoesNotExist:
        raise InvalidPostException(post_id)

def get_user_posts(user_id):
    try:
        user_post=Post.objects.get(id=user_id)
        return user_post
    except User.DoesNotExist:
        raise InvalidUserException(user_id)


def get_replies_for_comment(comment_id):
    try:
        replies = Comment.objects.filter(parent_comment_id=comment_id)
        return list(replies)
    except Comment.DoesNotExist:
        return InvalidCommentException(comment_id)

def create_group(user_id, name, member_ids):
     try:
         user=User.objects.get(id=user_id)
         user.is_admin = True
         members=Group.objects.create(name=name, members=member_ids)
         user.save()
         return members
     except User.DoesNotExist:
         raise InvalidUserException(user_id)
     except Membership.DoesNotExist:
         raise InvalidMemberException(member_ids)
     except Group.DoesNotExist:
         raise InvalidGroupNameException(name)

def add_member_to_group(user_id, new_member_id, group_id):
    try:
        user=User.objects.get(id=user_id)
        group=Group.objects.get(id=group_id)
        if user_id not in group:
            Membership.objects.create(user=user,group=group,member_id=new_member_id)
        else:
            raise UserNotInGroupException(user_id)
    except User.DoesNotExist:
        raise InvalidUserException(user_id)
    except Membership.DoesNotExist:
        raise InvalidMemberException(new_member_id)
    except Group.DoesNotExist:
        raise InvalidGroupNameException(group_id)

    if user_id not in group.members.all():
        raise UserNotInGroupException(user_id)

def remove_member_from_group(user_id, member_id, group_id):
    try:
        group=Group.objects.get(id=group_id)
        group.members.remove(member_id)
    except User.DoesNotExist:
        raise InvalidUserException(user_id)
    except Group.DoesNotExist:
        raise InvalidGroupNameException(group_id)

    except Membership.DoesNotExist:
        raise InvalidMemberException(member_id)

    if member_id not in group.members.all() or user_id not in group.members.all():
        raise UserNotInGroupException(user_id)

def make_member_as_admin(user_id, member_id, group_id):
    try:
        member=Membership.objects.get(id=member_id)
        if not member.is_admin:
            member.is_admin = True
    except Membership.DoesNotExist:
        raise InvalidMemberException(member_id)
    except Group.DoesNotExist:
        raise InvalidGroupNameException(group_id)
    except Membership.MultipleObjectsReturned:
        raise InvalidMemberException(member_id)
    except Group.DoesNotExist:
        raise InvalidGroupNameException(group_id)
    except Membership.DoesNotExist:
        raise InvalidMemberException(member_id)

def get_group_feed(user_id, group_id, offset, limit):
    try:
        group = Group.objects.get(id=group_id, members__id=user_id)

        posts = (
            Post.objects.filter(group_id=group_id)
            .select_related('posted_by')
            .order_by('-created_at')[offset: offset + limit]
        )

        return list(posts)
    except Group.DoesNotExist:
        raise InvalidGroupNameException(group_id)
    except User.DoesNotExist:
        raise InvalidUserException(user_id)
    if user_id not in group.members:
        raise UserNotInGroupException(user_id)

    if offset<0:
        raise InvalidOffSetValueException(offset)
    if limit<=0:
        raise InvalidLimitSetValueException(limit)

def get_posts_with_more_comments_than_reactions():
    posts = (
        Post.objects.annotate(
            comment_count=Count('comments'),
            reaction_count=Count('reactions')
        )
        .filter(comment_count__gt=F('reaction_count'))
    )
    return posts


def get_user_posts(user_id):
    try:
        posts = Post.objects.filter(posted_by_id=user_id).select_related('group', 'posted_by')

        user_posts = []
        for post in posts:
            group_details = None
            if post.group:
                group_details = {
                    "group_id": post.group.id,
                    "name": post.group.name
                }

            post_details = {
                "post_id": post.id,
                "group": group_details,
                "posted_by": {
                    "name": post.posted_by.name,
                    "user_id": post.posted_by.id,
                    "profile_pic": post.posted_by.profile_pic_url,
                },
                "posted_at": post.posted_at.isoformat(),
                "post_content": post.content,
                "reactions": {
                    "count": post.reactions.count(),
                    "type": list(post.reactions.values_list('reaction_type', flat=True).distinct())
                }
            }

            user_posts.append(post_details)

        return user_posts
    except User.DoesNotExist:
        raise InvalidUserException(user_id)


def get_silent_group_members(group_id):
    try:
        group = Group.objects.get(id=group_id)
        silent_members = group.members.annotate(post_count=Count('posts')).filter(post_count=0)
        return silent_members
    except Group.DoesNotExist:
        raise InvalidGroupNameException(group_id)

