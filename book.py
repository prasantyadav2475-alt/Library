import mysql.connector
from datetime import date
conn=mysql.connector.connect(
    host="localhost",
    user="root",
    password="140416",
    database="library"
)  
cursor=conn.cursor()
def add_book():
    print("""-------||Welcome Young Guy!!!||------
You can add books in the shelf to increase knowledge.
    """)
    book_id=int(input("Enter the book id: "))
    title=input("Enter Title to the book: ")
    author=input("Enter the author name: ")
    quantity=int(input("Enter the quantity of books: "))
    query="insert into books(book_id,title,author,quantity)values(%s,%s,%s,%s)"
    values=(book_id,title,author,quantity)
    cursor.execute(query,values)
    conn.commit()
    print("Book Submitted👍")
    with open("book.txt","a") as file:
        file.write("-"*40+"\n")
        file.write(f"Book id       : {book_id}\n")
        file.write(f"Title         : {title}\n")
        file.write(f"Author        : {author}\n")
        file.write(f"quantity      : {quantity}\n")
        file.write("-"*40+"\n")
#issue book 
def issue_book():
    book_id=int(input("Enter the book ID: "))
    student_name=input("Enter the name of the student: ")
    cursor.execute("SELECT quantity FROM books where book_id=%s",(book_id,))
    book=cursor.fetchone()
    if book and book[0]>0:
        cursor.execute("""
        INSERT INTO issueing_book(issued_id,book_id,student_name,issue_date)
        values(%s,%s,%s,%s)
        """,(0,book_id,student_name,date.today())
        )
        is_id=cursor.lastrowid
        cursor.execute("UPDATE books set quantity = quantity - 1 where book_id=%s",(book_id,))
        conn.commit()
        print("Book Issued😉")
        with open("Issue.txt","a") as file:
            file.write("-"*40+"\n")
            file.write(f"Issued ID        : {is_id}\n")
            file.write(f"Book ID          : {book_id}\n")
            file.write(f"Student Name     : {student_name}\n")
            file.write(f"Issue Date       : {date.today()}\n")
            file.write("-"*40+"\n")
    else:
        print("Better luck next time🥲") 
#return book
def return_book():
    book_id=int(input("Enter the book id: "))
    student_name=input("Enter student name: ")
    cursor.execute("select issue_date from issueing_book where book_id=%s and student_name=%s and return_date is NULL",(book_id,student_name))
    record=cursor.fetchone()
    if record:
        issue_date=record[0]
        days=(date.today() - issue_date).days
        fine=max(0,(days-7) * 5)
        cursor.execute("update issueing_book set return_date=%s,fine=%s where book_id=%s and student_name=%s and return_date is null",(date.today(),fine,book_id,student_name))    
        cursor.execute("update books set quantity=quantity + 1 where book_id=%s",(book_id,))
        conn.commit()
        print(f"Book Returned | fine=₹{fine}\n")
    else:
        print(" | No Issue Record Found |")
def view_book():
    query="select book_id,title,author,quantity from books"
    cursor.execute(query)
    views=cursor.fetchall()
    if views:
        for view in views:
         print("-"*40+"\n")
         print(f"Book ID      : {view[0]}\n")
         print(f"Title        : {view[1]}\n")
         print(f"Author       : {view[2]}\n") 
         print(f"Quantity     : {view[3]}\n")
         print("-"*40+"\n")
    else:
        print("Not Available❌")
# main menu
while True:
    print("""
     ------------| Welcome To Library |-------------
    Choose Options:
    1.Add Book
    2.Issue Book
    3.Return Book
    4.View all books     
    5.Exit      
    """)
    choice=int(input("Enter your choice:"))
    if choice==1:
        add_book()
    elif choice==2:
        issue_book()
    elif choice==3:
        return_book()
    elif choice==4:
        view_book()    
    elif choice==5:
        print("Thanks for Visiting🙏")
        break
    else :
        print("Invalid Choice Selected❌")     