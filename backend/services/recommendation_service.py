
"""
Rule-based well-being suggestions for the MindWell prototype.

These rules provide general self-care suggestions only.
They are not clinically validated and do not diagnose,
screen for, or predict mental health conditions.
"""


def generate_recommendations(mood_rating, stress_rating, sleep_hours=None):
    """
    Generate general suggestions from one self-reported check-in.

    Ratings:
        mood_rating: integer from 1 (low) to 5 (high)
        stress_rating: integer from 1 (low) to 5 (high)
        sleep_hours: optional number from 0 to 24

    Returns:
        A list of supportive recommendation strings.
    """
    if not isinstance(mood_rating, int) or isinstance(mood_rating, bool):
        raise ValueError("Mood rating must be an integer from 1 to 5.")

    if not isinstance(stress_rating, int) or isinstance(stress_rating, bool):
        raise ValueError("Stress rating must be an integer from 1 to 5.")

    if not 1 <= mood_rating <= 5:
        raise ValueError("Mood rating must be between 1 and 5.")

    if not 1 <= stress_rating <= 5:
        raise ValueError("Stress rating must be between 1 and 5.")

    if sleep_hours is not None:
        if isinstance(sleep_hours, bool) or not isinstance(
            sleep_hours, (int, float)
        ):
            raise ValueError("Sleep hours must be a number from 0 to 24.")

        if not 0 <= sleep_hours <= 24:
            raise ValueError("Sleep hours must be between 0 and 24.")

    recommendations = []

    # Mood-based suggestions
    if mood_rating <= 2:
        recommendations.append(
            "Your mood rating is on the lower side today. "
            "Consider doing a small activity you enjoy and "
            "talking with someone you trust."
        )
    elif mood_rating == 3:
        recommendations.append(
            "Take a little time for yourself today. "
            "A relaxing activity or a short break may help."
        )
    else:
        recommendations.append(
            "Thanks for checking in. Consider continuing the "
            "healthy activities and routines that work for you."
        )

    # Stress-based suggestions
    if stress_rating >= 4:
        recommendations.append(
            "You reported higher stress today. Try taking a "
            "short break, breathing slowly and comfortably, "
            "or breaking a task into smaller steps."
        )

        recommendations.append(
            "If stress continues or feels difficult to manage, "
            "consider speaking with a trusted adult, school "
            "counsellor, or qualified professional."
        )
    elif stress_rating == 3:
        recommendations.append(
            "If things feel overwhelming, pause for a few minutes "
            "and focus on one manageable task at a time."
        )
    else:
        recommendations.append(
            "Keep making space for rest, enjoyable activities, "
            "and time with supportive people."
        )

    # Sleep-based suggestion
    if sleep_hours is not None:
        if sleep_hours < 7:
            recommendations.append(
                "You reported less than seven hours of sleep. "
                "If possible, try a consistent bedtime and a "
                "calming routine. Sleep needs vary by age."
            )
        elif sleep_hours > 12:
            recommendations.append(
                "You reported more than twelve hours of sleep. "
                "Sleep needs vary by age, so one check-in alone "
                "does not tell us whether this is a concern. "
                "If your sleep pattern worries you, talk with "
                "a trusted adult or healthcare professional."
            )
        else:
            recommendations.append(
                "Keep noticing how your sleep routine affects "
                "how you feel. Sleep needs vary with age."
            )

    recommendations.append(
        "These are general well-being suggestions, not a diagnosis "
        "or a substitute for professional support."
    )

    return recommendations
