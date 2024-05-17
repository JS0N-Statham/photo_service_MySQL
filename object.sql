-- Удаление существующей базы данных, если она существует
--DROP DATABASE IF EXISTS object;

-- Создание базы данных, если она еще не существует
CREATE DATABASE IF NOT EXISTS object;
USE object4;

-- Создание таблицы пользователей, где вся информация хранится в JSON
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  data JSON
);

-- Вставка данных в таблицу пользователей в формате JSON
INSERT INTO users (data) VALUES 
(JSON_OBJECT('username', 'ADMIN', 'password', '3axoduM_B_xaTy')),
(JSON_OBJECT('username', 'Aleksandr', 'password', 'zxcv1q2fdsw3e4r')),
(JSON_OBJECT('username', 'Misha', 'password', 'CEPBEP_yMeP')),
(JSON_OBJECT('username', 'Alesha', 'password', 'AHTOH1987')),
(JSON_OBJECT('username', 'Nikitos', 'password', 'LOL2019www'));

-- Создание таблицы фотографий, где информация о фотографии хранится в JSON
CREATE TABLE photos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    details JSON,
    image_data LONGTEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

	