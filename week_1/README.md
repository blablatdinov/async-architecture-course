### Бизнес цепочки:

1) Создание задачи:

```
Создание таска
```

2) Выполнение задачи:

```
Задачу отмечают выполненной |-> Пересчет аудита
                            |-> Начисляются деньги
```

3) Назначение исполнителей

```
Нажата кнопка для назначения исполнителей |-> Пересчет аудита
                                          |-> Списываются деньги
```

### Требования:

1) Создание таска:

```
Actor: Account
Command: CreateTask
Data: Task
Event: Task.Created
```

2) Заасайнить  задачи

```
Actor: Account (manager or admin only)
Command: AssignTasks
Data: ???
Event: Task.Assigned
```

3) Пересчитать аудит  TODO может быть несколько акторов

```
Actor: "Task.Assigned" event
Command: UpdateAnalytics
Data: Task
Event: Accounting.AuditUpdated
```

4) Списать деньги

```
Actor: "Task.Assigned" event
Command: WriteOff
Data: popugId, taskId
Event: Accounting.WriteOff
```

5) Отметить задачу выполненной

```
Actor: Popug
Command: DoneTask
Data: TaskId, PopugId
Event: Task.Finished
```

6) Начислить деньги:

```
Actor: "Task.Finished" event
Commnad: AccrueAward
Data: TaskId, PopugId
Event: Accounting.AwardAccrued
```

Домены:

<img width="50%" alt="Accounting domain" src="img/Accounting domain.png">
<img width="50%" alt="Analytics domain" src="img/Analytics domain.png">
<img width="50%" alt="Task domain" src="img/Task domain.png">
<img width="50%" alt="Service schema" src="img/service schema.png">
