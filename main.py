from tkinter import *
from tkinter import filedialog    
from IPython.display import display
import pandas as pd
import matplotlib.pyplot as plt  

columns = ['Text','Credit/Debit Amount', 'Balance','Category','Booked At','Month','Year']
options = ["Necessities", "Transport", "Groceries", "Treats", "Investment", "Business", "Shopping/Entertainment", "Selfcare", "Travel", "Other"] # Necessities = Rent, Insurance, Phone
def convert(with_overview=False, categorize = True):
    
    #Create a hidden Tkinter window which is always on top (so that filedialog doesn't open behind the active window)
    root = Tk() 
    root.withdraw()  # Hide the main Tkinter window
    root.attributes("-topmost", True)  # Ensure the dialog is on top
    
    file_path = filedialog.askopenfilename(
        title="Select a csv file",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    
    df = pd.read_csv(file_path, encoding='ISO-8859-1', sep=";")
    
    root.destroy()  # Destroy the root window after the dialog closes
        
    month = input("Which month is this from? ")
    year = input("And which year? ")
    
    #CLEAN UP
    df["Booked At"] = df["Booked At"].str.split().str[0] # .str[0] selects the first element of each list. splits each string in the column into a list of words.
    df['Month'] = month
    df['Year'] = year
    df['Category'] = ""

    
    # Cleanup 'Text' column 
    keywords = ['Einkauf', 'Bancomat']
    for index, row in df.iterrows():
        if any(keyword in row['Text'] for keyword in keywords):
            # Split the string by commas
            parts = row['Text'].split(',')
            # Take the first part and remove the last 11 characters
            updated_text = parts[0][:-11]
            # Update the 'Text' column with the modified value
            df.at[index, 'Text'] = updated_text
    
    df = df.sort_values('Booked At',ascending=True).reset_index()
   
    
    df = df.filter(items=columns) #only keep the columns interesting to us
    df.to_csv(f'csv_database/{year}_{month}.csv',encoding='ISO-8859-1', sep=";",index=False)
    
    # Do you want to plot the monthly overview graph?
    if with_overview:
        display(df)
        plt.plot(df.index, df.Balance)
        plt.title("Bank Transfers " + month + year)
        plt.xlabel('Transaction Nr.')  
        plt.ylabel('Bank Balance')  
        plt.show()
    
    return df
        
        
        
        
        
def create_new_database():
    df = pd.DataFrame(columns=columns)
    df.to_csv("csv_database/database.csv", encoding='ISO-8859-1', sep=";", index=False)

    print(f"CSV file saved as database.csv")





def add_to_database():
    root = Tk() 
    root.withdraw()  # Hide the main Tkinter window
    root.attributes("-topmost", True)  # Ensure the dialog is on top
    file_path = filedialog.askopenfilename(
        title="Select a csv file to add to your database",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    root.destroy()
    
    df = pd.read_csv(file_path, encoding='ISO-8859-1', sep=";")
    df = df.reset_index(drop=True)
    
    #df.to_csv("csv_database/df.csv", encoding='ISO-8859-1', sep=";", index=False)

    database = pd.read_csv("csv_database/database.csv", encoding='ISO-8859-1', sep=";")
    database = database.reset_index(drop=True)

    
    database = pd.concat([database,df],ignore_index=True)

    if 'Unnamed: 0' in database.columns:
        database = database.drop(['Unnamed: 0'],axis=1)
    display(database)
    database.to_csv("csv_database/database.csv", encoding='ISO-8859-1', sep=";",index=False)
    print(f"Selected file has been added to database")
    
    





#needs to be worked on
def categorization_process():
    # If df is not already loaded by the function
    root = Tk() 
    root.withdraw()  # Hide the main Tkinter window
    root.attributes("-topmost", True)  # Ensure the dialog is on top
    
    file_path = filedialog.askopenfilename(
        title="Select a csv file to categorize",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    df = pd.read_csv(file_path, encoding='ISO-8859-1', sep=";")

    display(df)
    print("Would you like to categorize all entries? \n 1. Yes \n 2. No (just a selection)")
    d = int(input())
    if d == 1:
        print("Alright, let's get it over with..")
        print("For each transaction choose one of the following categories:")
        for n, option in enumerate(options):
            if n+1 == 10:
                print(f"0. {option}")    
            else:
                print(f"{n+1}. {option}")    
            
        for index, row in df.rowiter():
            print("\nWere looking at: ")
            print(row['Text'], row['Booked At'])
            n = int(input())
            if n == 0:
                choice = 9
            else:
                choice = n-1
            df.at[index, 'Category'] = options[choice]
    
    else: 
        print("Do you know the Index of the entry you want to categorize? \n 1. Yes \n 2. No")
        q1 = input() 
        if q1 in ['2','2.','No','N','Niggativ']:
            print("Then GTFO!")
            
        elif q1 in ['1','1.', "Yes", "Y",'Positive']:
            while True:
                print("Do you wanna tell me? \n 1. Yes \n 2. No, fuck off.")
                q3 = int(input())

                if q3 == 1:
                    count = 0
                    while True:
                        if count == 0:
                            print("Which one is it?")
                            q2 = input("Enter the ID")
                        else:
                            q2 = input("Next ID! ")
                        q2 = int(q2)
                        print("\nWe are looking at: ")
                        print(df.loc[q2, 'Text'], df.loc[q2, 'Booked At'])
                        print("\nYour options are: ")
                        for n, option in enumerate(options):
                            if n+1 == 10:
                                print(f"0. {option}")    
                            else:
                                print(f"{n+1}. {option}")    
                        
                        cat = int(input("Choose a category: "))
                        if cat == 0:
                            choice = 9
                        else:
                            choice = cat-1
                            
                        df.at[q2, 'Category'] = options[choice]
                        break
                
                else: 
                    print("Man, you're wasting energy")
                    break
            df.to_csv("csv_database/database.csv", encoding='ISO-8859-1', sep=";")               
                
            
        

def summarize_by_category():
    df_payments_shrink = df_payments.filter(items=['Category', 'Credit/Debit Amount'])
    print(df_payments_shrink.groupby('Category')['Credit/Debit Amount'].sum().abs().sort_values(ascending=False))

def edit_entry():
    if 'Category' not in df.columns:
        print(f"The following columns are missing: Category")
    else:
        database = pd.read_csv("csv_database/database.csv", encoding='ISO-8859-1', sep=";")
        #database = database.reset_index(drop=True)
        display(database)
        print(database.iloc[0])
        
        print("Whicht entry do you want to change? Gimme the ID.")


convert()

""" 
# Data Wrangling
df["Booked At"] = df["Booked At"].str.split().str[0] # .str[0] selects the first element of each list. splits each string in the column into a list of words.
df = df.sort_values('Booked At',ascending=True).reset_index()
df = df.filter(items=columns)
# alternativ drop: df = df.drop(columns=['Valuta Date','index','IBAN'])
df['Month'] = month
df['Year'] = year
df_deposits = df.loc[df['Credit/Debit Amount'] > 0] #money earned
df_payments = df.loc[df['Credit/Debit Amount'] < 0]
total_transfers = len(df)
#df.describe()

        

################# OVERVIEW SECTION ###################
display(df)     
    # Display the first few rows of the DataFrame
#print(df.head())

# show general trajectory of bank balance
plt.plot(df.index, df.Balance)
plt.xlabel('Transaction Nr.')  
plt.ylabel('Bank Balance')  
plt.show()


top10_expenses = df_payments.sort_values('Credit/Debit Amount').head(10) # the 10 highest expenditures of the month
 """
#Zeitliche Auflistung Anzahl Bank Transfers
#df['Booked At'].value_counts()
#payments.plot.hist()
#kf = df.groupby(by='Booked At')


#alternative vectorized method for selection of rows for value replacement   
#top10_expenses['Leech'] = [input("Gimme something: ") for _ in range(len(top10_expenses))]


#How to address the 50th entry of the dataframe:
#df.iloc[[50]]


#summarize by Category
#groceries = df.loc[df['Lebensmittel']=="x", ["Credit/Debit Amount","Text"]]

#Making a Dict with every df entry as element
#df_dict = {index: row.tolist() for index, row in df.iterrows()}


#things to do:
# 1. plot spendings summed up by day
# 2. sum up spending per category and also plot

# 3. System for iterating through the data frame and adding categories
#Treat Salary indipendently
#Iterating: for index, row in df.iterrows()
#next(df.iterrows())[1]

# Prompt user for input
#user_input = input("Enter your name: ")

# Print the entered input
#print(f"Hello, {user_input}!")

# 4. Keep a list of subscriptions

# 5. Possibility to edit single entries