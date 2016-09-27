-- Seeding test data for testing 0.1
INSERT INTO users (phone_number, active_book_id, book_section)
VALUES
	('123-456-7890', 1, 1),
	('911-911-1234', 2, 1);

INSERT INTO books (title, author, language, difficulty_level, times_subscribed)
VALUES
	('You Should Use Rails', 'Paul', 'Ruby', 'medium', 1),
	('How to Code for Dummies', 'Andrew', 'Ingrish', 'hard', 2),
	('When to Use Rails', 'Aditya', 'English', 'easy', 3),
	('Always', 'Aman', 'Francais', 'easy', 4);

INSERT INTO snippets (book_id, section, content)
VALUES
	(1, 1, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus non porttitor leo. Etiam ut erat imperdiet, pulvinar neque non, molestie elit. Suspendisse sagittis euismod nisl ac porta. Nulla cursus augue rhoncus, pellentesque libero id, tincidunt augue. Suspendisse potenti. Mauris a lorem viverra, vehicula ipsum eu, porta ante. Curabitur sit amet ante eu velit gravida imperdiet. Phasellus arcu ante, semper tincidunt volutpat a, mattis non augue.' ),
    (1, 2, 'Part 2 of the greatest book ever'),
    (1, 3, 'The final chapter'),
    (2, 1, 'RANDOM'),
	(3, 1, 'Random and test data');
