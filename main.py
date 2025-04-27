"""Student Grade Tracker - Main Application

This is the main entry point for the Student Grade Tracker application.
It provides a command-line interface for managing student records with options to:
- Add new students
- Update student scores
- View average scores
- Save data to file

The application uses the StudentManager class to handle all data operations.
"""

from student import StudentManager

student = StudentManager()

while True:
    print(' ------ Welcome to Student Grade Tracker ------')
    print('''
    -- Select the operation: 
    1 for add student, 
    2 for update scores, 
    3 for average scores,
    0 for exit
    ''')
    user_input = input('Main Menu - Enter the number of the operation: ')
    
    if user_input == '1':
        student_id = input('Enter the student ID: ')
        if not student.search_id_file(student_id):
            user = student.add_student({
                "ID": student_id,
                "Name": input('Enter the student name: '),
                "Courses": input('Enter the courses (comma-separated): ').split(','),
                "Scores": [],
                "Attendance": {},
                "Remarks": []
            })
            user_id = student.save_students_to_file(user['ID'])
            print(f'Data saved successfully to student/{user_id}.json')
        else:
            print(f'Student ID {student_id} already exists')
            
    elif user_input == '2':
        try:
            student_id = input('Enter the student ID: ')
            # First check if student exists by searching the file
            student_data = student.search_id_file(student_id)
            
            if student_data:
                try:
                    scores_input = input('Enter scores (comma-separated): ')
                    scores = [int(s.strip()) for s in scores_input.split(',')]
                    updated_scores = student.update_scores(student_data, scores)
                    print('\nCurrent scores:', updated_scores)
                except ValueError:
                    print('\nError: Score must be a number')
                    
            else:
                print(f'No student found with ID {student_id}')
                
        except ValueError:
            print('\nError: Score must be a number')
            
        except Exception as e:
            print(f'\nError updating scores: {e}')
            
    elif user_input == '3':
        try:
            student_id = input('Enter the student ID: ')
            if not student.search_id_file(student_id):
                print(f'No student found with ID {student_id}')             
            else: 
                print(f'Average score for student {student_id} is {student.get_average_scores(student_id)}')
        
        except Exception as e:
            print(f'\nError getting average scores: {e}')
    
    elif user_input == '0':
        exit()

    else:
        print('Invalid input, please try again.')