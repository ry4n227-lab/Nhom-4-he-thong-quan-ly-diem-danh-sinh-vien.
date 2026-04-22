DROP DATABASE IF EXISTS attendance_db;
CREATE DATABASE attendance_db;
USE attendance_db;

-- =====================
-- Admin
-- =====================
CREATE TABLE Admin (
    admin_id VARCHAR(10) PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(20) NOT NULL,
    full_name VARCHAR(100)
);

-- =====================
-- Teachers
-- =====================
CREATE TABLE Teachers (
    teacher_id VARCHAR(10) PRIMARY KEY,
    full_name VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(20) DEFAULT '123456'
);

-- =====================
-- Classes
-- =====================
CREATE TABLE Classes (
    class_id INT AUTO_INCREMENT PRIMARY KEY,
    class_name VARCHAR(100),
    teacher_id VARCHAR(10),
    FOREIGN KEY (teacher_id) REFERENCES Teachers(teacher_id) ON DELETE CASCADE
);

-- =====================
-- Students
-- =====================
CREATE TABLE Students (
    student_id VARCHAR(10) PRIMARY KEY,
    full_name VARCHAR(100),
    email VARCHAR(100),
    class_id INT,
    password VARCHAR(20) DEFAULT '123456',
    FOREIGN KEY (class_id) REFERENCES Classes(class_id) ON DELETE SET NULL
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
    FOREIGN KEY (student_id) REFERENCES Students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES Classes(class_id) ON DELETE CASCADE
);

-- =====================
-- Bảng Sessions 
-- =====================
CREATE TABLE Sessions (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    class_id INT,
    date DATE,
    start_time TIME,
    end_time TIME,
    room VARCHAR(50),
    FOREIGN KEY (class_id) REFERENCES Classes(class_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS leave_requests (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(50) NOT NULL,
    reason TEXT NOT NULL,
    date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'Pending',
    FOREIGN KEY (student_id) REFERENCES students(student_id)
    
);

USE attendance_db;

-- =====================
-- ADMIN
-- =====================
INSERT INTO Admin VALUES ('A01', 'admin', '123456', 'System administrator');

-- =====================
-- TEACHERS
-- =====================
INSERT INTO Teachers (teacher_id, full_name, email, password) VALUES
('T01', 'Nguyen Van A', 'vana@gmail.com', '123456'),
('T02', 'Tran Thi B', 'thib@gmail.com', '123456');

-- =====================
-- CLASSES
-- =====================
INSERT INTO Classes (class_name, teacher_id) VALUES
('CNTT1', 'T01'),
('CNTT2', 'T02');

-- =====================
-- STUDENTS
-- =====================
INSERT INTO Students (student_id, full_name, email, class_id, password) VALUES
('SV01', 'Le Minh Hoang', 'hoang@gmail.com', 1, '123456'),
('SV02', 'Pham Thu Trang', 'trang@gmail.com', 1, '123456'),
('SV03', 'Nguyen Quang Huy', 'huy@gmail.com', 2, '123456'),
('SV04', 'Do Thi Lan', 'lan@gmail.com', 2, '123456');

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

INSERT INTO leave_requests (student_id, reason, date, status) 
VALUES ('SV01', 'Bị ốm nên xin nghỉ', '2026-04-26', 'Pending');
