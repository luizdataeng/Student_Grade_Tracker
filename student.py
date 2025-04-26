"""Student Grade Tracker - Student Management Module

This module provides functionality for managing student records, including:
- Adding new students
- Updating student scores
- Calculating average scores
- Saving student data to JSON files

The module uses a dictionary-based storage system for maintaining student records
with support for courses, scores, attendance, and remarks.
"""

import decimal


class StudentManager:
    """Manages student records and operations.
    
    This class handles all operations related to student data management,
    including adding students, updating scores, and calculating averages.
    """
    
    def __init__(self):
        self.students = {}
    
    def add_student(self, student: dict) -> dict:
        """Add a new student to the system.
        
        Args:
            student (dict): Dictionary containing student information with
                           ID, Name, and Courses fields.
        
        Returns:
            dict: The complete student record with all fields initialized.
        """
        new_student = {
            "ID": student["ID"],
            "Name": student["Name"],
            "Courses": student["Courses"],
            "Scores": {},
            "Attendance": {},
            "Remarks": []
        }
        self.students[student["ID"]] = new_student
        return new_student

    def update_scores(self, student_data: dict, scores: list) -> list:
        """Update scores for all courses in student data.
        
        Args:
            student_data (dict): Student data dictionary with courses
            scores (list): List of scores to add
            
        Returns:
            list: Updated scores list
        """
        import os
        import json
        
        # Overwrite the scores list with new scores
        student_data["Scores"] = scores
            
        # Save updated data back to file
        try:
            filepath = os.path.join(os.path.dirname(__file__), f'student/{student_data["ID"]}.json')
            with open(filepath, 'w') as f:
                json.dump(student_data, f, indent=4)
            print(f'Scores saved successfully to {filepath}')
        except Exception as e:
            print(f'Error saving scores: {e}')
            
        return student_data['Scores']

    def get_average_scores(self, id: str) -> decimal.Decimal:
        """Calculate average score for a student.
        
        Args:
            id (str): Student ID
        
        Returns:
            decimal.Decimal: Average score with 2 decimal places
        """
        import os
        import json
        
        try:
            with open(os.path.join(os.path.dirname(__file__), f'student/{id}.json'), 'r') as f:
                student_data = json.load(f)
                scores = student_data["Scores"]
                if not scores:
                    return decimal.Decimal('0.00')
                total = sum(scores)
                avg = decimal.Decimal(str(total)) / decimal.Decimal(str(len(scores)))
                return avg.quantize(decimal.Decimal('0.00'))
        except FileNotFoundError:
            print(f'No student found with ID {id}')
            return decimal.Decimal('0.00')
        except Exception as e:
            print(f'Error calculating average: {e}')
            return decimal.Decimal('0.00')

    def save_students_to_file(self, user_id: str) -> None:
        """Save student data to a JSON file.
        
        Args:
            user_id (str): The ID of the student to save
        
        The data is saved to 'student/<user_id>.json'.
        Creates the student directory if it doesn't exist.
        """
        import json
        import os
        
        # Create student directory if it doesn't exist
        os.makedirs('student', exist_ok=True)
        
        try:
            filepath = os.path.join('student', f'{user_id}.json')
            with open(filepath, 'w') as f:
                # Only save the specific student's data
                if user_id in self.students:
                    json.dump(self.students[user_id], f, indent=4)
                    print(f'Data saved successfully to {filepath}')
                else:
                    print(f'Student ID {user_id} not found')
        except Exception as e:
            print(f'Error saving data: {e}')

    def search_id_file(self, search_id: str) -> dict:
        """Search for a student file by ID in the student folder.
        
        Args:
            search_id (str): The ID to search for
            
        Returns:
            dict: Student data if found, None if not found
        """
        import os
        import json
        
        filepath = os.path.join('student', f'{search_id}.json')
        
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    student_data = json.load(f)
                    print(student_data)
                    return student_data
            else:
                # No data found for student ID {search_id}
                return None
        except Exception as e:
            print(f'Error reading student file: {e}')
            return None
