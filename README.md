# hseforms

Описание: 
Наша цель - создать собственный аналог Google Forms со своими фичами (веб-приложение с простой регистрацией, где пользователи могут создавать опросы)

Набор функционала: 
Создание собственной учетной записи на сайте (через уникальный логин и пароль) и вход в неё
В личном кабинете можно:
 а) создать опрос/викторину 
 б) просмотреть/изменить уже существующие опросы/викторины 
 в) просмотреть статистику по текущим опросам 
 г) просмотреть пройденные опросы и правильные ответы по ним 

Каким образом пользователь будет пользоваться проектом: 
Пользователь будет заходить на веб-сайт и через взаимодействие с интерфейсом создавать или проходить опросы 

Примерное представление как это будет работать
Регистрация на сайте: пользователь нажимает кнопку “регистрация” - вводит логин и пароль - мы делаем запрос в базу данных: 
    - если такой логин уже есть в базе данных, то выводим пользователю сообщение об ошибке и просим изменить логин или вернуться назад и нажать на кнопку “вход” 
   - если такого логина в БД нет, то добавляем в БД новую запись, а пользователю выводим сообщение об успешной регистрации 

Вход на сайт: пользователь нажимает кнопку “войти” - вводит логин и пароль - мы делаем запрос в базу данных 
    - если такого логина в БД нет, то выводим пользователю ошибку и просим проверить правильность введенного логина или вернуться назад и нажать на кнопку “регистрация” 
   - если такой логин есть в БД, но введенный пользователем пароль не совпадает с паролем, записанным в БД, то выводим пользователю ошибку и просим проверить правильность введенного пароля 
   - если логин и пароль, введенные пользователем, совпадают с записью в БД, то перенаправляем пользователя в личный кабинет 

Создание/прохождение/просмотр опроса/викторины: мы создаем соответствующие модели, пользователь делает запросы через соответствующие кнопки сайта 

Прохождение опроса: пользователь вводит свои ответы в соответствующие поля на сайт - мы записываем ответы пользователя в уникальную для каждого опроса Базу Данных 

Результаты опросов и продвинутая аналитика: пользователь нажимает на конкретный опрос - мы делаем запрос в БД данного опроса - на основе информации из БД строим необходимые диаграммы и считаем статистические параметры - выводим их пользователю 

Функционал: 
регистрация и авторизация пользователя
создание опроса
прохождение опроса
сбор статистики по опросу

Технический стек: Django/FastAPI/Flask, html, SQL

Распределение людей в команде:
2 django разработчика: 
– реализация основной логики создания опросов
– регистрация и авторизация пользователя
– реализация основной логики прохождения опросов
– интегрирование БД в проект
Верстка html + дизайн

Части проекта:
Реализация регистрации и авторизации пользователя
Инициализация проекта, реализация страницы конструктора опросов
реализация страницы взаимодействия пользователя с подготовленными другими пользователями опросами
Интеграция проекта с БД 
Создание html шаблонов

Гитхаб проекта:
https://github.com/davletbaevtr/hseforms


