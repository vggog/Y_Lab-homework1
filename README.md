# YLAB-homework

## Запуск проекта
Для запуска проекта необходим docker, docker-compose.
Также необходимо создать и заполнить файл
.env(в качестве примера - файл .env_example) в корневой директории проекта.
```commandline
docker-compose up --build
```

## Тесты
Для запуска тестов необходимо создать заполнить файл
.env_test(в качестве примера - файл .env_test_example) в корневой директории проекта.
```commandline
docker-compose -f docker-compose-test.yaml up --abort-on-container-exit --build
```

## Задания
### 2 урок
3-й вопрос<br>
Файл src/menu/model.py класс MenuModel, атрибуты submenus_count и dishes_count<br>
Файл src/submenu/model.py класс SubmenuModel, атрибут dishes_count

4-й вопрос<br>
Файл tests/test_count_of_dish_and_submenu.py

### 3 урок
6-й вопрос
Файл src/core/utils.py функция reverse()
