## Tecnhologies
`Python` `Django`  `Docker` `Gunicorn` `NGINX` `PostgreSQL`  

# **_welbex_test_**
Приложение в котором на данном этапе доступен 
- Создание нового груза (характеристики локаций pick-up, delivery определяются по введенному zip-коду);
- Получение списка грузов (локации pick-up, delivery, количество ближайших машин до груза ( =< 450 миль));
- Получение информации о конкретном грузе по ID (локации pick-up, delivery, вес, описание, список номеров ВСЕХ машин с расстоянием до выбранного груза);
- Редактирование машины по ID (локация (определяется по введенному zip-коду));
- Редактирование груза по ID (вес, описание);
- Удаление груза по ID.

### Локальный запуск проекта:

**_Склонировать репозиторий к себе_**
```
git@github.com:aksdr53/weblex_test.git
```


*_Установить Docker, Docker Compose:_**
```
sudo apt install curl                                   - установка утилиты для скачивания файлов
curl -fsSL https://get.docker.com -o get-docker.sh      - скачать скрипт для установки
sh get-docker.sh                                        - запуск скрипта
sudo apt-get install docker-compose-plugin              - последняя версия docker compose
```

**_Создать и запустить контейнеры Docker**_

```
sudo docker compose up -d
```