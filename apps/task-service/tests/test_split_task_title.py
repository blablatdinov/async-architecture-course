from tasks.views import split_jira_topic_and_task_title


def test():
    jira_id, task_title = split_jira_topic_and_task_title('[UBERPOP-42] Поменять оттенок зелёного на кнопке')

    assert jira_id == 'UBERPOP-42'
    assert task_title == 'Поменять оттенок зелёного на кнопке'
