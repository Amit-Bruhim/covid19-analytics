from fileinput import filename
import mysql.connector
import os
from tabulate import tabulate
from decimal import Decimal

# ANSI color codes for terminal
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

# Database connection configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "covid_db",
    "port": 3307
}

# Map query numbers to filenames
queries = {
    "1": "q1.py",
    "2": "q2.py",
    "3": "q3.py",
    "4": "q4.py",
    "5": "q5.py",
    "6": "q6.py",
    "7": "q7.py",
    "8": "q8.py"
}

def run_query_file(filename, cursor):
    """Run a query from a Python file that defines a variable 'query'."""
    file_path = os.path.join(os.path.dirname(__file__), "queries", filename)
    namespace = {}
    with open(file_path, "r") as f:
        code = f.read()
        exec(code, namespace)
    if "query" in namespace:
        cursor.execute(namespace["query"])
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        if results:
            # Format numbers to 2 decimal places, avoid scientific notation
            formatted_results = []
            for row in results:
                new_row = []
                for val in row:
                    if isinstance(val, (int, float)):
                        new_row.append(f"{val:.2f}")
                    elif isinstance(val, Decimal):
                        new_row.append(f"{float(val):,.2f}")
                    else:
                        new_row.append(val)
                formatted_results.append(new_row)

            # Print header in green
            print(GREEN + f"\nResults saved to output.txt (total {len(results)} rows)\n" + RESET)
            
            # Write full table to file
            with open("output.txt", "w", encoding="utf-8") as f:
                f.write(tabulate(formatted_results, headers=columns, tablefmt="grid"))
        else:
            print(GREEN + "No results returned" + RESET)
    else:
        print(RED + f"No 'query' variable found in {filename}" + RESET)


def main():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    while True:
        print(GREEN + "\nSelect a query to run (1-8) or 0 to exit:" + RESET)
        choice = input("> ").strip()
        
        if choice == "0":
            print(GREEN + "Exiting..." + RESET)
            break
        elif choice in queries:
            try:
                run_query_file(queries[choice], cursor)
            except Exception as e:
                print(RED + f"Error running query: {e}" + RESET)
        else:
            print(RED + "Invalid input" + RESET)

    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()
