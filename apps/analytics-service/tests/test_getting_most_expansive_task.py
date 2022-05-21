from collections import namedtuple

import pytest

pytestmark = [pytest.mark.django_db]


@pytest.fixture(autouse=True)
def most_expansive_task_statistic(mixer):
    return namedtuple('MostExpansiveTaskStatistic', 'month,week,day')(
        month=mixer.blend('analytics.MostExpensiveTask', time_range='month'),
        week=mixer.blend('analytics.MostExpensiveTask', time_range='week'),
        day=mixer.blend('analytics.MostExpensiveTask', time_range='day'),
    )


@pytest.mark.freeze_time('2020-01-01')
def test(manager_api_client, most_expansive_task_statistic):
    got = manager_api_client.get('/api/v1/analytics/most-expansive-task/')

    assert got.status_code == 200
    assert got.json()['month'] == most_expansive_task_statistic.month.award
    assert got.json()['week'] == most_expansive_task_statistic.week.award
    assert got.json()['day'] == most_expansive_task_statistic.day.award
