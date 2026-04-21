CREATE DATABASE attendance_db;
USE attendance_db;

-- =====================
-- Students
-- =====================
CREATE TABLE Students (
    student_id VARCHAR(10) PRIMARY KEY,
    full_name VARCHAR(100),
    email VARCHAR(100),
    class_id INT
);

-- =====================
-- Teachers
-- =====================
CREATE TABLE Teachers (
    teacher_id VARCHAR(10) PRIMARY KEY,
    full_name VARCHAR(100),
    email VARCHAR(100)
);

-- =====================
-- Classes
-- =====================
CREATE TABLE Classes (
    class_id INT AUTO_INCREMENT PRIMARY KEY,
    class_name VARCHAR(100),
    teacher_id VARCHAR(10),
    FOREIGN KEY (teacher_id) REFERENCES Teachers(teacher_id)
);

-- =====================
-- Attendance
-- =====================
CREATE TABLE Attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(10),
    class_id INT,
    date DATE,
    status VARCHAR(20),
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (class_id) REFERENCES Classes(class_id)
);
USE attendance_db;

-- =====================
-- TEACHERS
-- =====================
INSERT INTO Teachers VALUES
('T01', 'Nguyen Van A', 'vana@gmail.com'),
('T02', 'Tran Thi B', 'thib@gmail.com');

-- =====================
-- CLASSES
-- =====================
INSERT INTO Classes (class_name, teacher_id) VALUES
('CNTT1', 'T01'),
('CNTT2', 'T02');

-- =====================
-- STUDENTS
-- =====================
INSERT INTO Students VALUES
('SV01', 'Le Minh Hoang', 'hoang@gmail.com', 1),
('SV02', 'Pham Thu Trang', 'trang@gmail.com', 1),
('SV03', 'Nguyen Quang Huy', 'huy@gmail.com', 2),
('SV04', 'Do Thi Lan', 'lan@gmail.com', 2);

-- =====================
-- ATTENDANCE
-- =====================
INSERT INTO Attendance (student_id, class_id, date, status) VALUES
('SV01', 1, '2026-04-20', 'Present'),
('SV02', 1, '2026-04-20', 'Absent'),
('SV03', 2, '2026-04-20', 'Late'),
('SV04', 2, '2026-04-20', 'Present'),

('SV01', 1, '2026-04-21', 'Present'),
('SV02', 1, '2026-04-21', 'Present'),
('SV03', 2, '2026-04-21', 'Absent'),
('SV04', 2, '2026-04-21', 'Late');