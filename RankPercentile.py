from tkinter import *
import mysql.connector

class RankPercentile:
    def __init__(self, root):
        self.root = root
        self.root.title("Rank-Based Percentile Calculator")
        self.root.geometry("700x500")

        # Labels and Entry fields for adding student data
        self.add_student_label = Label(self.root, text="Add Student Data", font=("Arial", 14))
        self.add_student_label.grid(row=0, column=1, columnspan=5)

        self.name_label = Label(self.root, text="Student Name")
        self.name_label.grid(row=1, column=1, padx=10)

        self.marks_label = Label(self.root, text="Marks")
        self.marks_label.grid(row=1, column=3, padx=10)

        self.rank_label = Label(self.root, text="Rank")
        self.rank_label.grid(row=1, column=5, padx=10)

        self.name_entry = Entry(self.root)
        self.name_entry.grid(row=2, column=1)

        self.marks_entry = Entry(self.root)
        self.marks_entry.grid(row=2, column=3)

        self.rank_entry = Entry(self.root)
        self.rank_entry.grid(row=2, column=5)

        self.add_button = Button(self.root, text="Add Student", command=self.add_student)
        self.add_button.grid(row=2, column=6)

        # Labels and Entry fields for deleting student data
        self.delete_student_label = Label(self.root, text="Delete Student Data", font=("Arial", 14))
        self.delete_student_label.grid(row=3, column=1, columnspan=5)

        self.delete_name_label = Label(self.root, text="Student Name")
        self.delete_name_label.grid(row=4, column=1, padx=10)

        self.delete_name_entry = Entry(self.root)
        self.delete_name_entry.grid(row=5, column=1)

        self.delete_button = Button(self.root, text="Delete Student", command=self.delete_student)
        self.delete_button.grid(row=5, column=6)

        # Labels and Entry fields for calculating percentile
        self.calculate_label = Label(self.root, text="Calculate Percentile", font=("Arial", 14))
        self.calculate_label.grid(row=6, column=1, columnspan=5)

        self.rank_heading_label = Label(self.root, text="Enter Rank for Percentile Calculation", font=("Arial", 12))
        self.rank_heading_label.grid(row=7, column=1, columnspan=5)

        self.rank_input_label = Label(self.root, text="Rank")
        self.rank_input_label.grid(row=8, column=1, padx=10)

        self.total_participant_entry = Entry(self.root)
        self.total_participant_entry.grid(row=8, column=2)

        self.percentile_entry = Entry(self.root)
        self.percentile_entry.grid(row=9, column=4)

        self.student_name_entry = Entry(self.root)
        self.student_name_entry.grid(row=10, column=4)

        self.student_marks_entry = Entry(self.root)
        self.student_marks_entry.grid(row=11, column=4)

        self.find_button = Button(self.root, text="Find Percentile", command=self.find_percentile)
        self.find_button.grid(row=9, column=5)

        self.clear_button = Button(self.root, text="Clear", command=self.clear)
        self.clear_button.grid(row=12, column=4)

        # Output Labels
        self.output_label = Label(self.root, text="", font=("Arial", 12), fg="green")
        self.output_label.grid(row=13, column=1, columnspan=5)

    def add_student(self):
        try:
            # Connect to MySQL database
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="student_data"
            )
            cursor = conn.cursor()

            # Fetch data from entry fields
            name = self.name_entry.get()
            marks = int(self.marks_entry.get())
            rank = int(self.rank_entry.get())  # Get rank from the new entry field

            # Insert student data into the database
            cursor.execute("INSERT INTO students (name, marks, student_rank) VALUES (%s, %s, %s)", (name, marks, rank))
            conn.commit()

            # Clear entry fields after adding
            self.name_entry.delete(0, END)
            self.marks_entry.delete(0, END)
            self.rank_entry.delete(0, END)

            # Display success message
            self.output_label.config(text=f"Student '{name}' added successfully.")

            # Close the database connection
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            self.output_label.config(text=f"Database error: {err}", fg="red")
        except ValueError:
            self.output_label.config(text="Please enter valid marks and rank.", fg="red")
        except Exception as e:
            self.output_label.config(text=f"Unexpected error: {e}", fg="red")

    def delete_student(self):
        try:
            # Connect to MySQL database
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="student_data"
            )
            cursor = conn.cursor()

            # Fetch data from entry field
            name = self.delete_name_entry.get()

            # Delete student data from the database
            cursor.execute("DELETE FROM students WHERE name = %s", (name,))
            conn.commit()

            # Clear entry field after deleting
            self.delete_name_entry.delete(0, END)

            # Display success message
            self.output_label.config(text=f"Student '{name}' deleted successfully.")

            # Close the database connection
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            self.output_label.config(text=f"Database error: {err}", fg="red")
        except Exception as e:
            self.output_label.config(text=f"Unexpected error: {e}", fg="red")

    def find_percentile(self):
        try:
            # Connect to MySQL database
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="student_data"
            )
            cursor = conn.cursor()

            # Fetch the total number of participants
            cursor.execute("SELECT COUNT(*) FROM students")
            students_count = cursor.fetchone()[0]

            # Fetch the rank from user input
            student_rank = int(self.total_participant_entry.get())

            # Fetch the student name and marks based on student_rank
            cursor.execute("SELECT name, marks FROM students WHERE student_rank = %s", (student_rank,))
            student_data = cursor.fetchone()

            if student_data:
                student_name, student_marks = student_data
                self.student_name_entry.delete(0, END)
                self.student_name_entry.insert(0, student_name)

                self.student_marks_entry.delete(0, END)
                self.student_marks_entry.insert(0, student_marks)

                # Calculate percentile
                result = round((students_count - student_rank) / students_count * 100, 3)
                self.percentile_entry.delete(0, END)
                self.percentile_entry.insert(0, str(result))

                # Display success message
                self.output_label.config(text=f"Percentile for '{student_name}' (Rank {student_rank}): {result}%")
            else:
                self.student_name_entry.delete(0, END)
                self.student_marks_entry.delete(0, END)
                self.percentile_entry.delete(0, END)
                self.output_label.config(text="No student found with the given rank.", fg="red")

            # Close the database connection
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            self.output_label.config(text=f"Database error: {err}", fg="red")
        except ValueError:
            self.output_label.config(text="Please enter a valid rank.", fg="red")
        except Exception as e:
            self.output_label.config(text=f"Unexpected error: {e}", fg="red")

    def clear(self):
        self.name_entry.delete(0, END)
        self.marks_entry.delete(0, END)
        self.rank_entry.delete(0, END)
        self.delete_name_entry.delete(0, END)
        self.total_participant_entry.delete(0, END)
        self.percentile_entry.delete(0, END)
        self.student_name_entry.delete(0, END)
        self.student_marks_entry.delete(0, END)
        self.output_label.config(text="")  # Clear output message

if __name__ == "__main__":
    root = Tk()
    app = RankPercentile(root)
    root.mainloop()
