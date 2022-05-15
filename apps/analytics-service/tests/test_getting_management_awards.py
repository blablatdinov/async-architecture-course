import datetime

import pytest

pytestmark = [pytest.mark.django_db]


@pytest.fixture(autouse=True)
def management_award(mixer):
    return mixer.blend('analytics.ManagementAward', date=datetime.date(2020, 1, 1))


@pytest.mark.freeze_time('2020-01-01')
def test(manager_api_client, management_award):
    got = manager_api_client.get('/api/v1/analytics/management-award/')

    assert got.status_code == 200
    assert int(got.content) == management_award.award
