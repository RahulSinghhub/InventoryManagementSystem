Capstone Project: Inventory Management System with Predictive Restocking Using Python

Team Members
Ansharah Laraib  , Fatima , Gokul Vijay Shankar P , Jayanth Dixit , Rahul Singh
Objective:

To build an Inventory Management System using Python that tracks products, manages stock levels, and integrates machine learning to predict when items need to be restocked based on historical sales data.

Key Features: 
●	Inventory Tracking: The system will store product details (e.g., name, category, stock quantity, price) in a database (MySQL).
   - Example: A store manager can add new products or update existing product quantities through a command-line or web interface.

●	 Low Stock Alerts:  Alerts will be triggered when stock levels drop below a predefined threshold, notifying the user to reorder.
   - Example: The system sends a notification when a particular product’s stock falls below 10 units.

●	Machine Learning for Predictive Restocking:The system will use a machine learning model (e.g., linear regression) to predict when products need to be restocked based on historical sales data and trends.
   - Example: Based on past sales, the system predicts that a certain item will need to be restocked in 5 days and notifies the user.

●	 Sales Reporting: The system will generate sales reports, tracking inventory movement over time, and providing insights into high-selling products.
   - Example: A weekly report shows the top 5 best-selling products and their current stock levels.

Action Items
1.	 Python Source Code: Includes inventory management functionality and machine learning integration for predictive restocking.
2.	 Machine Learning Model: A trained model that predicts when products need to be reordered.
3.	 Database Setup: Instructions on setting up and configuring the product database.
4.	 Demo: A working inventory system where users can manage stock, view reports, and receive restocking recommendations based on predictions.

Technologies Used:
- Python: Core programming for managing inventory, database connections, and machine learning integration.
- SQLite/MySQL: To store product data and transaction history.
- scikit-learn: To build predictive models for stock replenishment based on sales trends.
- Tkinter-package for GUI.
- Matplotlib: To visualize sales trends and stock levels in reports.


Referred Data Sets :
1. [Walmart Sales Forecasting](https://www.kaggle.com/c/walmart-recruiting-store-sales-forecasting/data) (Kaggle):
   - Contains sales data for various departments within Walmart stores. You can adapt this dataset for inventory and sales trends.

2. [Rossmann Store Sales](https://www.kaggle.com/c/rossmann-store-sales/data) (Kaggle):
   - Features sales data from a German pharmacy chain, which can be used for inventory predictions and management.

3. [Online Retail II Dataset](https://www.kaggle.com/mashlyn/online-retail-ii-uci) (Kaggle):
   - Transaction data from an online retail store, ideal for simulating product sales and stock levels in an inventory system.

4. [Wholesale Customers Data](https://archive.ics.uci.edu/ml/datasets/Wholesale+customers) (UCI Machine Learning Repository):
   - Annual spending data of wholesale customers across different categories, useful for restocking predictions based on consumption patterns.

5. [Mockaroo](https://www.mockaroo.com/):
   - A tool to generate custom datasets. You can generate realistic sales and inventory data by specifying product categories, sales quantities, and time ranges.

6. [Retailrocket Dataset](https://www.kaggle.com/retailrocket/ecommerce-dataset) (Kaggle):
   - Contains real-time customer interaction data, including product sales and stock information, suitable for machine learning model training.

7. [Superstore Sales Dataset](https://www.kaggle.com/datasets/rohitsahoo/sales-forecasting) (Kaggle):
   - A fictional retail chain dataset covering categories like furniture, office supplies, and technology, often used for sales and inventory analysis.






