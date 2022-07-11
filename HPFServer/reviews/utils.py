from users.models import UserPreferences

import logging
logging.basicConfig(level=logging.DEBUG)


def can_post_reviews(parent_object, user):
    try:
        prefs = parent_object.creation_user.preferences

        if user.is_authenticated:
            if prefs.member_review_policy >= UserPreferences.ReviewPolicyChoices.WRITE_TEXT:
                return True
        elif user.is_anonymous:
            if prefs.anonymous_review_policy >= UserPreferences.ReviewPolicyChoices.WRITE_TEXT:
                return True

    except UserPreferences.DoesNotExist:
        logging.warning(f"Créateur de contenu sans préférences : {parent_object.creation_user.id}")
        return True


def can_see_reviews(parent_object, user):
    try:
        prefs = parent_object.creation_user.preferences

        if user.has_perm("view_reviews"):
            return True
        elif user.is_authenticated:
            if prefs.member_review_policy >= UserPreferences.ReviewPolicyChoices.SEE_TEXT:
                return True
        elif user.is_anonymous:
            if prefs.anonymous_review_policy >= UserPreferences.ReviewPolicyChoices.SEE_TEXT:
                return True

    except UserPreferences.DoesNotExist:
        logging.warning(f"Créateur de contenu sans préférences : {parent_object.creation_user.id}")
        return True

    return False