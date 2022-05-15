import datetime

import pytest

pytestmark = [pytest.mark.django_db]


@pytest.fixture(autouse=True)
def count_popug_with_negative_award(mixer):
    return mixer.blend('analytics.CountPopugWithNegativeAward', date=datetime.date(2020, 1, 1))


@pytest.mark.freeze_time('2020-01-01')
def test(manager_api_client, count_popug_with_negative_award):
    got = manager_api_client.get('/api/v1/analytics/popug-with-negative-award-count/')

    assert got.status_code == 200
    assert int(got.content) == count_popug_with_negative_award.award
