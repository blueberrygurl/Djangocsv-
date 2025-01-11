# Aya's Data Analysis and Visualization Project

## Overview
This project is a web application built using Django that allows users to analyze and visualize data from CSV files. It provides an intuitive interface for file upload, data processing, statistical analysis, and interactive data visualization.



## Features
1. **File Upload and Processing**
   - Upload CSV files and manage their content.
   - Automatic detection and handling of numeric and textual columns.

2. **Indexing and Data Access**
   - Specify row and column indices to view selected data.
   - User-friendly interface to navigate data.

3. **Statistical Analysis**
   - Perform statistical operations on selected rows or columns.
   - Display clear and concise analysis results.

4. **Data Visualization**
   - Create interactive plots using Matplotlib and Seaborn.
   - Support for various chart types (e.g., bar charts, line graphs, histograms).

5. **Web Interface**
   - Built with Django for a seamless and interactive experience.
   - Views for all major functionalities, ensuring a smooth user workflow.



## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/blueberrygurl/Djangocsv-.git
   cd Djangocsv-
   ```

2. **Create and Activate a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

6. **Access the Application**
   Open your browser and navigate to: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)



## Usage

1. **Upload a CSV File**
   - Navigate to the file upload page.
   - Select a CSV file and upload it.

2. **View and Process Data**
   - Use the interface to access specific rows and columns.
   - Perform operations like sorting, filtering, and indexing.

3. **Perform Statistical Analysis**
   - Select data columns and apply statistical functions (mean, median, etc.).

4. **Visualize Data**
   - Create custom plots to visualize trends and distributions.
   - Save or export plots as needed.



## Project Structure
```
project_root/
├── manage.py
├── project_name/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── app_name/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── views.py
│   ├── models.py
│   ├── urls.py
│   └── admin.py
└── requirements.txt
```


## Technologies Used

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, Bootstrap
- **Data Visualization:** Matplotlib, Seaborn
- **Database:** SQLite (default Django configuration)



## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch.
3. Make your changes and commit them.
4. Push your changes to your fork.
5. Open a pull request.



PS: you can find somme csv files among the project feel free to use them while testing the project or for personal use <3 



## Contact
For any inquiries or support, please contact:
- **Name:** Mohhi Aya
- **Email:** mohhiaya3@gmail.com
- **GitHub:** [blueberrygurl](https://github.com/blueberrygurl)
```
