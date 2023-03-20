-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 01, 2022 at 01:25 AM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 7.3.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sb`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `admin_id` int(11) NOT NULL,
  `admin_name` varchar(20) NOT NULL,
  `admin_email` varchar(20) DEFAULT NULL,
  `admin_department` varchar(20) DEFAULT NULL,
  `admin_designation` varchar(20) DEFAULT NULL,
  `admin_password` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`admin_id`, `admin_name`, `admin_email`, `admin_department`, `admin_designation`, `admin_password`) VALUES
(1, 'Ashmal', 'ashmal@gmail.com', 'Finance', 'CEO', 'ashmal'),
(3, 'Ibrahim Ali Asghar', 'ibrahim@gmail.com', 'Accounts', 'CFO', 'ibrahim');

-- --------------------------------------------------------

--
-- Table structure for table `answer_recorded`
--

CREATE TABLE `answer_recorded` (
  `answer_id` int(11) NOT NULL,
  `test_no` int(11) DEFAULT NULL,
  `question_no` int(11) DEFAULT NULL,
  `emp_id` int(11) DEFAULT NULL,
  `scenario_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `answer_recorded`
--

INSERT INTO `answer_recorded` (`answer_id`, `test_no`, `question_no`, `emp_id`, `scenario_id`) VALUES
(1, 49, 1, 15, 1),
(2, 49, 2, 15, 1),
(3, 58, 1, 15, 1),
(4, 58, 1, 16, 1),
(5, 58, 2, 15, 2),
(6, 58, 2, 16, 2),
(7, 58, 1, 17, 1),
(8, 58, 2, 17, 3),
(9, 67, 1, 18, 1),
(10, 67, 2, 18, 1),
(11, 67, 3, 18, 2),
(12, 68, 1, 19, 1),
(13, 68, 2, 19, 2),
(14, 68, 1, 19, 1),
(15, 68, 2, 19, 2),
(16, 68, 1, 20, 2),
(17, 68, 2, 20, 2),
(26, 68, 2, 39, 1),
(27, 68, 3, 39, 2),
(28, 68, 5, 39, 1),
(31, 68, 2, 41, NULL),
(32, 68, 3, 41, 1),
(33, 68, 5, 41, 1),
(34, 68, 2, 43, 1),
(35, 68, 3, 43, 2),
(36, 68, 5, 43, 1);

-- --------------------------------------------------------

--
-- Table structure for table `employees`
--

CREATE TABLE `employees` (
  `emp_id` int(11) NOT NULL,
  `emp_name` varchar(20) NOT NULL,
  `emp_designation` varchar(20) NOT NULL,
  `emp_department` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `employees`
--

INSERT INTO `employees` (`emp_id`, `emp_name`, `emp_designation`, `emp_department`) VALUES
(15, 'Ibrahim', 'Doctor', 'Pharmacy'),
(16, 'Husnain', 'NURSE', 'EE'),
(17, 'Ashmal', 'Teacher', 'Mathematics'),
(18, 'samar', 'manager', 'accounts'),
(19, 'Asad ', 'CEO', 'CS'),
(20, 'Kiran', 'Worker', 'Accounts'),
(38, 'alizna', 'developer', 'Accounts'),
(39, 'ali', 'manager', 'Accounts'),
(41, 'alizain', 'manager', 'accounts'),
(43, 'khurram', 'developer', 'Accounts');

-- --------------------------------------------------------

--
-- Table structure for table `questiondepartments`
--

CREATE TABLE `questiondepartments` (
  `test_no` int(11) NOT NULL,
  `question_no` int(11) NOT NULL,
  `department_name` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `questiondepartments`
--

INSERT INTO `questiondepartments` (`test_no`, `question_no`, `department_name`) VALUES
(65, 2, 'Accounts'),
(59, 3, 'Accounts'),
(67, 1, 'AI'),
(55, 5, 'B'),
(55, 3, 'BBA'),
(55, 4, 'BBA'),
(55, 7, 'BBA'),
(49, 1, 'CS'),
(59, 1, 'CS'),
(65, 1, 'CS'),
(66, 1, 'CS'),
(67, 1, 'CS'),
(68, 1, 'CS'),
(49, 2, 'CS'),
(67, 2, 'CS'),
(67, 3, 'CS'),
(59, 4, 'CS'),
(55, 8, 'CS'),
(55, 9, 'CS'),
(65, 2, 'Dance'),
(67, 2, 'DS'),
(49, 1, 'EE'),
(65, 1, 'EE'),
(67, 1, 'EE'),
(68, 1, 'EE'),
(59, 2, 'EE'),
(67, 2, 'EE'),
(67, 3, 'EE'),
(68, 4, 'EE'),
(58, 2, 'English'),
(49, 1, 'IT'),
(65, 1, 'IT'),
(66, 1, 'IT'),
(65, 2, 'IT'),
(58, 1, 'Physics'),
(55, 2, 'SDA');

-- --------------------------------------------------------

--
-- Table structure for table `questions`
--

CREATE TABLE `questions` (
  `question_no` int(11) NOT NULL,
  `test_no` int(11) NOT NULL,
  `question_text` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `questions`
--

INSERT INTO `questions` (`question_no`, `test_no`, `question_text`) VALUES
(1, 49, 'Haste kese hain'),
(2, 49, 'Haste kese hain'),
(3, 49, 'Hasne ke baad kiya hota hai'),
(4, 49, 'Hasne ke baad kiya hota hai'),
(1, 52, 'xaxa'),
(2, 52, 'aca'),
(3, 52, 'aca'),
(4, 52, 'aca'),
(5, 52, 'aca'),
(6, 52, 'aca'),
(7, 52, 'aca'),
(8, 52, 'aca'),
(9, 52, 'aca'),
(10, 52, 'aca'),
(11, 52, 'aca'),
(12, 52, 'aca'),
(13, 52, 'aca'),
(14, 52, 'aca'),
(15, 52, 'aca'),
(16, 52, 'aca'),
(17, 52, 'aca'),
(18, 52, 'aca'),
(19, 52, 'aca'),
(20, 52, 'aca'),
(21, 52, 'aca'),
(22, 52, 'aca'),
(23, 52, 'aca'),
(24, 52, 'aca'),
(25, 52, 'aca'),
(26, 52, 'aca'),
(27, 52, 'aca'),
(28, 52, 'aca'),
(29, 52, 'aca'),
(30, 52, 'aca'),
(1, 55, 'axxxxpqr'),
(2, 55, 'sxs'),
(3, 55, 'Yeh hai naya question'),
(4, 55, 'Yeh hai naya question'),
(5, 55, 'zcz'),
(6, 55, 'zcz'),
(7, 55, 'csck'),
(8, 55, 'csc'),
(9, 55, 'Never Mind'),
(1, 58, 'How is perfection measured'),
(2, 58, 'How is my name spelled?'),
(1, 59, 'Pehla sawaal aapke kitnay bachhe hain'),
(2, 59, 'Doosra Sawaal'),
(3, 59, 'xs'),
(4, 59, 'Yeh Chautha Sawaal hai'),
(5, 59, 'what\'s your fav programming language'),
(1, 65, 'Favourite Dancer?'),
(2, 65, 'Favourite Dance?'),
(1, 66, 'Which song you like?'),
(1, 67, 'Do you guys have events at fast?'),
(2, 67, 'Is your Management cooperative?'),
(3, 67, 'What\'s your gpa at fast?'),
(1, 68, 'What personality do you have?'),
(2, 68, 'Are you good in studies?'),
(3, 68, 'Do you sleep early at night?'),
(4, 68, 'Do you like coal?'),
(5, 68, 'How\'s sir rafi?');

-- --------------------------------------------------------

--
-- Table structure for table `scenario`
--

CREATE TABLE `scenario` (
  `scenario_id` int(11) NOT NULL,
  `test_no` int(11) NOT NULL,
  `question_no` int(11) NOT NULL,
  `scenario_options` varchar(200) DEFAULT NULL,
  `deduction` varchar(200) DEFAULT NULL,
  `Show_In_Sort_By` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `scenario`
--

INSERT INTO `scenario` (`scenario_id`, `test_no`, `question_no`, `scenario_options`, `deduction`, `Show_In_Sort_By`) VALUES
(1, 49, 1, 'Moon say', 'Namoona', 0),
(1, 52, 1, 'sc', 'sc', 0),
(1, 55, 1, 'css', 'scs', 0),
(1, 58, 1, 'Inches', 'Vulnerable Risky', 1),
(1, 59, 1, 'Kesa hai', 'Vulnerable Risky', 1),
(1, 65, 1, 'Raghav', 'Vulnerable Risky', 1),
(1, 66, 1, 'Raabta', 'Vulnerable Risky', 1),
(1, 67, 1, 'Yes', 'Safe', 1),
(1, 68, 1, 'Introvert', 'Vulnerable Risky', 1),
(1, 49, 2, 'Moon say', 'Namoona', 0),
(1, 52, 2, 'caaca', 'ac', 0),
(1, 55, 2, 'sx', 'x', 0),
(1, 58, 2, 'ebrahim', 'Not sure', 0),
(1, 59, 2, 'Tu kon hai?', 'Namoona', 0),
(1, 65, 2, 'Salsa', 'Vulnerable Risky', 1),
(1, 67, 2, 'YES', 'Safe', 1),
(1, 68, 2, 'Yes', 'Safe', 1),
(1, 49, 3, 'Kuch nahi', 'Kese', 0),
(1, 52, 3, 'caaca', 'ac', 0),
(1, 55, 3, 'sda', 'sc', 0),
(1, 59, 3, 'xa', 'Safe', 1),
(1, 67, 3, 'above 3', 'Safe', 1),
(1, 68, 3, 'YES', 'Vulnerable Risky', 1),
(1, 49, 4, 'Kuch nahi', 'Kese', 0),
(1, 52, 4, 'caaca', 'ac', 0),
(1, 55, 4, 'sda', 'sc', 0),
(1, 59, 4, 'Tu kiya kar raha hai yahan', 'TAfreeh', 0),
(1, 68, 4, 'Alot', 'Safe', 1),
(1, 52, 5, 'caaca', 'ac', 0),
(1, 55, 5, 'sfs', 'cs', 0),
(1, 68, 5, 'Cheetay hain bhae woh to', 'Safe', 1),
(1, 52, 6, 'caaca', 'ac', 0),
(1, 55, 6, 'sfs', 'cs', 0),
(1, 52, 7, 'caaca', 'ac', 0),
(1, 55, 7, 'sjxv', 'scsssx', 0),
(1, 52, 8, 'caaca', 'ac', 0),
(1, 55, 8, 'd', 'd', 0),
(1, 52, 9, 'caaca', 'ac', 0),
(1, 55, 9, 'as', 'd', 0),
(1, 52, 10, 'caaca', 'ac', 0),
(1, 52, 11, 'caaca', 'ac', 0),
(1, 52, 12, 'caaca', 'ac', 0),
(1, 52, 13, 'caaca', 'ac', 0),
(1, 52, 14, 'caaca', 'ac', 0),
(1, 52, 15, 'caaca', 'ac', 0),
(1, 52, 16, 'caaca', 'ac', 0),
(1, 52, 17, 'caaca', 'ac', 0),
(1, 52, 18, 'caaca', 'ac', 0),
(1, 52, 19, 'caaca', 'ac', 0),
(1, 52, 20, 'caaca', 'ac', 0),
(1, 52, 21, 'caaca', 'ac', 0),
(1, 52, 22, 'caaca', 'ac', 0),
(1, 52, 23, 'caaca', 'ac', 0),
(1, 52, 24, 'caaca', 'ac', 0),
(1, 52, 25, 'caaca', 'ac', 0),
(1, 52, 26, 'caaca', 'ac', 0),
(1, 52, 27, 'caaca', 'ac', 0),
(1, 52, 28, 'caaca', 'ac', 0),
(1, 52, 29, 'caaca', 'ac', 0),
(1, 52, 30, 'caaca', 'ac', 0),
(2, 49, 1, 'hch', 'uufu', 0),
(2, 52, 1, 'sc', 'sc', 0),
(2, 55, 1, 'css', 'scsssx', 0),
(2, 58, 1, 'Love', 'Safe', 1),
(2, 59, 1, 'Kesa nahi hai', 'Lassan', 0),
(2, 65, 1, 'Dharmesh', 'Safe', 1),
(2, 66, 1, 'Perfect', 'Safe', 1),
(2, 67, 1, 'No', 'Vulnerable Risky', 1),
(2, 68, 1, 'Extrovert', 'Safe', 1),
(2, 52, 2, 'cac', 'aca', 0),
(2, 55, 2, 'x ', ' x ', 0),
(2, 58, 2, 'Ibrahim', 'Safe', 1),
(2, 59, 2, 'Tu HAi ke nahi', 'SCS', 0),
(2, 65, 2, 'Arial', 'Safe', 1),
(2, 67, 2, 'No', 'Vulnerable Risky', 1),
(2, 68, 2, 'No', 'Vulnerable Risky', 1),
(2, 52, 3, 'cac', 'aca', 0),
(2, 55, 3, 'css', 'css', 0),
(2, 59, 3, 'VAlee', 'Vulnerable Risky', 1),
(2, 67, 3, 'below 2', 'Vulnerable Risky', 1),
(2, 68, 3, 'NO', 'Safe', 1),
(2, 52, 4, 'cac', 'aca', 0),
(2, 55, 4, 'css', 'css', 0),
(2, 59, 4, 'Kiyun', 'Safe', 1),
(2, 68, 4, 'Eww', 'Vulnerable Risky', 1),
(2, 52, 5, 'cac', 'aca', 0),
(2, 55, 5, 'cs', 'svd', 0),
(2, 68, 5, 'Bekar Marking hai unki', 'Vulnerable Risky', 1),
(2, 52, 6, 'cac', 'aca', 0),
(2, 55, 6, 'cs', 'svd', 0),
(2, 52, 7, 'cac', 'aca', 0),
(2, 55, 7, 'ada', 'sscs', 0),
(2, 52, 8, 'cac', 'aca', 0),
(2, 55, 8, 's', 'h', 0),
(2, 52, 9, 'cac', 'aca', 0),
(2, 55, 9, 'sc', 'ac', 0),
(2, 52, 10, 'cac', 'aca', 0),
(2, 52, 11, 'cac', 'aca', 0),
(2, 52, 12, 'cac', 'aca', 0),
(2, 52, 13, 'cac', 'aca', 0),
(2, 52, 14, 'cac', 'aca', 0),
(2, 52, 15, 'cac', 'aca', 0),
(2, 52, 16, 'cac', 'aca', 0),
(2, 52, 17, 'cac', 'aca', 0),
(2, 52, 18, 'cac', 'aca', 0),
(2, 52, 19, 'cac', 'aca', 0),
(2, 52, 20, 'cac', 'aca', 0),
(2, 52, 21, 'cac', 'aca', 0),
(2, 52, 22, 'cac', 'aca', 0),
(2, 52, 23, 'cac', 'aca', 0),
(2, 52, 24, 'cac', 'aca', 0),
(2, 52, 25, 'cac', 'aca', 0),
(2, 52, 26, 'cac', 'aca', 0),
(2, 52, 27, 'cac', 'aca', 0),
(2, 52, 28, 'cac', 'aca', 0),
(2, 52, 29, 'cac', 'aca', 0),
(2, 52, 30, 'cac', 'aca', 0),
(3, 52, 1, 'sccs', 'ax', 0),
(3, 55, 1, 'sxxsxssxssxs', 'sxxsxaxaxxsss', 0),
(3, 58, 1, 'Humanity', 'Good', 0),
(3, 58, 2, 'Obrahim', 'Vulnerable Risky', 1),
(3, 68, 4, 'Zabardast course hai', 'Safe', 1),
(4, 58, 1, 'Other', 'Not sure', 0),
(4, 58, 2, 'abraham', 'Good', 0);

-- --------------------------------------------------------

--
-- Table structure for table `superadmin`
--

CREATE TABLE `superadmin` (
  `super_admin_id` int(11) NOT NULL,
  `super_admin_name` varchar(20) NOT NULL,
  `super_admin_email` varchar(20) NOT NULL,
  `super_admin_password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `superadmin`
--

INSERT INTO `superadmin` (`super_admin_id`, `super_admin_name`, `super_admin_email`, `super_admin_password`) VALUES
(2, 'ashmal', 'ashmalanis@gmail.com', 'ashmal'),
(4, 'kamran', 'kamran@gmail.com', 'kamran');

-- --------------------------------------------------------

--
-- Table structure for table `temperory_questiondepartments`
--

CREATE TABLE `temperory_questiondepartments` (
  `test_no` int(11) NOT NULL,
  `question_no` int(11) NOT NULL,
  `department_name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `temperory_questiondepartments`
--

INSERT INTO `temperory_questiondepartments` (`test_no`, `question_no`, `department_name`) VALUES
(1, 1, 'CS'),
(1, 1, 'EE'),
(1, 1, 'IT');

-- --------------------------------------------------------

--
-- Table structure for table `temperory_questions`
--

CREATE TABLE `temperory_questions` (
  `question_no` int(11) NOT NULL,
  `test_no` int(11) NOT NULL,
  `question_text` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `temperory_questions`
--

INSERT INTO `temperory_questions` (`question_no`, `test_no`, `question_text`) VALUES
(1, 1, 'Programming Language?');

-- --------------------------------------------------------

--
-- Table structure for table `temperory_scenario`
--

CREATE TABLE `temperory_scenario` (
  `scenario_id` int(11) NOT NULL,
  `test_no` int(11) NOT NULL,
  `question_no` int(11) NOT NULL,
  `scenario_options` varchar(200) DEFAULT NULL,
  `deduction` varchar(200) DEFAULT NULL,
  `Show_In_Sort_By` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `temperory_scenario`
--

INSERT INTO `temperory_scenario` (`scenario_id`, `test_no`, `question_no`, `scenario_options`, `deduction`, `Show_In_Sort_By`) VALUES
(1, 1, 1, 'C++', 'Vulnerable Risky', 1),
(2, 1, 1, 'Java', 'Safe', 1);

-- --------------------------------------------------------

--
-- Table structure for table `temperory_tests`
--

CREATE TABLE `temperory_tests` (
  `test_no` int(11) NOT NULL,
  `test_subject` varchar(40) NOT NULL,
  `admin_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `temperory_tests`
--

INSERT INTO `temperory_tests` (`test_no`, `test_subject`, `admin_id`) VALUES
(1, 'Programming', 1);

-- --------------------------------------------------------

--
-- Table structure for table `tests`
--

CREATE TABLE `tests` (
  `test_no` int(11) NOT NULL,
  `test_subject` varchar(40) NOT NULL,
  `admin_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tests`
--

INSERT INTO `tests` (`test_no`, `test_subject`, `admin_id`) VALUES
(49, 'Hahatest', 3),
(52, 'HARD TEST', 3),
(55, 'Naya', 3),
(56, 'Word', 3),
(57, 'dvdv', 3),
(58, 'Perfect', 3),
(59, 'VEryImportant Test', 3),
(65, 'Dance Groups', 1),
(66, 'Songs', 1),
(67, 'How\'s life at FAST NUCES?', 1),
(68, 'How\'s life in general?', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`admin_id`),
  ADD UNIQUE KEY `admin_email` (`admin_email`);

--
-- Indexes for table `answer_recorded`
--
ALTER TABLE `answer_recorded`
  ADD PRIMARY KEY (`answer_id`),
  ADD KEY `test_no` (`test_no`,`question_no`,`scenario_id`),
  ADD KEY `emp_id` (`emp_id`);

--
-- Indexes for table `employees`
--
ALTER TABLE `employees`
  ADD PRIMARY KEY (`emp_id`),
  ADD UNIQUE KEY `emp_name` (`emp_name`,`emp_designation`);

--
-- Indexes for table `questiondepartments`
--
ALTER TABLE `questiondepartments`
  ADD PRIMARY KEY (`department_name`,`question_no`,`test_no`),
  ADD KEY `test_no` (`test_no`,`question_no`);

--
-- Indexes for table `questions`
--
ALTER TABLE `questions`
  ADD PRIMARY KEY (`test_no`,`question_no`);

--
-- Indexes for table `scenario`
--
ALTER TABLE `scenario`
  ADD PRIMARY KEY (`scenario_id`,`question_no`,`test_no`),
  ADD KEY `test_no` (`test_no`,`question_no`);

--
-- Indexes for table `superadmin`
--
ALTER TABLE `superadmin`
  ADD PRIMARY KEY (`super_admin_id`);

--
-- Indexes for table `temperory_questiondepartments`
--
ALTER TABLE `temperory_questiondepartments`
  ADD PRIMARY KEY (`department_name`,`question_no`,`test_no`),
  ADD KEY `test_no` (`test_no`,`question_no`);

--
-- Indexes for table `temperory_questions`
--
ALTER TABLE `temperory_questions`
  ADD PRIMARY KEY (`test_no`,`question_no`);

--
-- Indexes for table `temperory_scenario`
--
ALTER TABLE `temperory_scenario`
  ADD PRIMARY KEY (`scenario_id`,`question_no`,`test_no`),
  ADD KEY `test_no` (`test_no`,`question_no`);

--
-- Indexes for table `temperory_tests`
--
ALTER TABLE `temperory_tests`
  ADD PRIMARY KEY (`test_no`),
  ADD KEY `admin_id` (`admin_id`);

--
-- Indexes for table `tests`
--
ALTER TABLE `tests`
  ADD PRIMARY KEY (`test_no`),
  ADD KEY `admin_id` (`admin_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `admin_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `answer_recorded`
--
ALTER TABLE `answer_recorded`
  MODIFY `answer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT for table `employees`
--
ALTER TABLE `employees`
  MODIFY `emp_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;

--
-- AUTO_INCREMENT for table `superadmin`
--
ALTER TABLE `superadmin`
  MODIFY `super_admin_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `temperory_tests`
--
ALTER TABLE `temperory_tests`
  MODIFY `test_no` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `tests`
--
ALTER TABLE `tests`
  MODIFY `test_no` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=69;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `answer_recorded`
--
ALTER TABLE `answer_recorded`
  ADD CONSTRAINT `answer_recorded_ibfk_1` FOREIGN KEY (`test_no`,`question_no`,`scenario_id`) REFERENCES `scenario` (`test_no`, `question_no`, `scenario_id`),
  ADD CONSTRAINT `answer_recorded_ibfk_2` FOREIGN KEY (`emp_id`) REFERENCES `employees` (`emp_id`);

--
-- Constraints for table `questiondepartments`
--
ALTER TABLE `questiondepartments`
  ADD CONSTRAINT `questiondepartments_ibfk_1` FOREIGN KEY (`test_no`,`question_no`) REFERENCES `questions` (`test_no`, `question_no`);

--
-- Constraints for table `questions`
--
ALTER TABLE `questions`
  ADD CONSTRAINT `questions_ibfk_1` FOREIGN KEY (`test_no`) REFERENCES `tests` (`test_no`);

--
-- Constraints for table `scenario`
--
ALTER TABLE `scenario`
  ADD CONSTRAINT `scenario_ibfk_1` FOREIGN KEY (`test_no`,`question_no`) REFERENCES `questions` (`test_no`, `question_no`);

--
-- Constraints for table `temperory_questiondepartments`
--
ALTER TABLE `temperory_questiondepartments`
  ADD CONSTRAINT `temperory_questiondepartments_ibfk_1` FOREIGN KEY (`test_no`,`question_no`) REFERENCES `temperory_questions` (`test_no`, `question_no`);

--
-- Constraints for table `temperory_questions`
--
ALTER TABLE `temperory_questions`
  ADD CONSTRAINT `temperory_questions_ibfk_1` FOREIGN KEY (`test_no`) REFERENCES `temperory_tests` (`test_no`);

--
-- Constraints for table `temperory_scenario`
--
ALTER TABLE `temperory_scenario`
  ADD CONSTRAINT `temperory_scenario_ibfk_1` FOREIGN KEY (`test_no`,`question_no`) REFERENCES `temperory_questions` (`test_no`, `question_no`);

--
-- Constraints for table `temperory_tests`
--
ALTER TABLE `temperory_tests`
  ADD CONSTRAINT `temperory_tests_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`admin_id`);

--
-- Constraints for table `tests`
--
ALTER TABLE `tests`
  ADD CONSTRAINT `tests_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`admin_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
