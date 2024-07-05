from bs4 import BeautifulSoup
import csv, os

def html_table_to_csv(html_string, csv_file):
    soup = BeautifulSoup(html_string, 'html.parser')
    table = soup.find('table')
    csv_writer = csv.writer(csv_file)

    for row in table.find_all('tr'):
        csv_row = []
        for cell in row.find_all(['th', 'td']):
            csv_row.append(cell.get_text(strip=True))
        csv_writer.writerow(csv_row)

if __name__ == "__main__":
    html_string = """
    <html>
    <body>
    <table>
        <tr><th>Name</th><th>Age</th><th>City</th></tr>
        <tr><td>John Doe</td><td>30</td><td>New York</td></tr>
        <tr><td>Jane Smith</td><td>25</td><td>San Francisco</td></tr>
        <tr><td>Bob Johnson</td><td>40</td><td>Chicago</td></tr>
    </table>
    </body>
    </html>
    """

    # Open a CSV file in write mode
    with open('data/out/table.csv', 'w', newline='') as csv_file:
        html_table_to_csv(html_string, csv_file)

    print("Conversion complete. CSV file created.")
