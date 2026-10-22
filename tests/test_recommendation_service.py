
import pytest

from backend.services.recommendation_service import (
    generate_recommendations,
)


def test_low_mood_returns_supportive_suggestion():
    result = generate_recommendations(
        mood_rating=1,
        stress_rating=2,
        sleep_hours=8,
    )

    assert any("lower side" in item for item in result)
    assert any("not a diagnosis" in item for item in result)


def test_high_stress_recommends_support():
    result = generate_recommendations(
        mood_rating=3,
        stress_rating=5,
        sleep_hours=8,
    )

    assert any("higher stress" in item for item in result)
    assert any("trusted adult" in item for item in result)


def test_low_sleep_returns_sleep_suggestion():
    result = generate_recommendations(
        mood_rating=4,
        stress_rating=2,
        sleep_hours=5,
    )

    assert any("less than seven hours" in item for item in result)


def test_sleep_is_optional():
    result = generate_recommendations(
        mood_rating=4,
        stress_rating=2,
    )

    assert len(result) > 0


@pytest.mark.parametrize(
    "mood, stress",
    [
        (0, 3),
        (6, 3),
        (3, 0),
        (3, 6),
    ],
)
def test_invalid_ratings_raise_error(mood, stress):
    with pytest.raises(ValueError):
        generate_recommendations(mood, stress)


@pytest.mark.parametrize("sleep", [-1, 25])
def test_invalid_sleep_raises_error(sleep):
    with pytest.raises(ValueError):
        generate_recommendations(3, 3, sleep)
