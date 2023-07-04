# get_metrics_from_pagespeed_API
DAG for getting Metrics by PageSpeed Insights API

Пример ![DAG](https://github.com/hustler1984/get_metrics_from_pagespeed_API/blob/main/site_metrics_dag.py) файла для Airflow, который собирает метрики TBT и LCP и кладёт их в ClickHouse, а также
![DDL](https://github.com/hustler1984/get_metrics_from_pagespeed_API/blob/main/DDL.txt) для создания в ClickHouse таблицы, хранящей значение метрик. 

![Подробнее о PageSpeed Insights API](https://developers.google.com/speed/docs/insights/v5/get-started?hl=ru)

1. Largest Contentful Paint (LCP) — как быстро загружается основной контент интернет-ресурса. Пользователь чувствует себя комфортно, если загрузка контента происходит за 2,5 секунды или быстрее.
   
2. Метрика Total Blocking Time (TBT) измеряет общее количество времени между FCP (Первой отрисовкой контента) и TTI (Временем до интерактивности). В данный период времени основной поток блокируется и не реагирует на действия пользователя.

Подробнее о метриках по ссылке: (https://vc.ru/seo/317853-core-web-vitals-polnoe-rukovodstvo-glava-1-perevod-knigi).

Использовались библиотеки:

**requests версии 2.27.1**

**pandas версии 1.5.3.**

**clickhouse_driver версии 0.2.6**

В планах добавить докер контейнер.
