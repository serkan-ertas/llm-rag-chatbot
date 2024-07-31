CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message TEXT NOT NULL,
    user_id INT NOT NULL,
    chat_id INT NOT NULL,
    date DATETIME NOT NULL,
    sender BOOLEAN NOT NULL
);