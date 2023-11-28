"""Скрипт для заполнения данными таблиц в БД Postgres."""
import psycopg2
import os
import csv
from datetime import datetime

emp_data = os.path.join(os.path.dirname(__file__), "north_data", "employees_data.csv")
custom_data = os.path.join(os.path.dirname(__file__), "north_data", "customers_data.csv")
orders_data = os.path.join(os.path.dirname(__file__), "north_data", "orders_data.csv")


def load_data(filename):
    """Возвращает список словарей, полученный из csv-файла"""
    with open(filename, 'r', encoding='utf-8', newline='') as csv_file:
        csv_list = list(csv.DictReader(csv_file))
        return csv_list


def create_employees_entries(list_dict):
    """Возвращает список кортежей с данными для заполнения таблицы employees"""
    list_emp = []
    for row in list_dict:
        list_emp.append((
            int(row['employee_id']),
            row['first_name'],
            row['last_name'],
            row['title'],
            datetime.strptime(row['birth_date'], '%Y-%m-%d').date(),
            row['notes']
        ))
    return list_emp


def create_customers_entries(list_dict):
    """Возвращает список кортежей с данными для заполнения таблицы customers"""
    list_cust = []
    for row in list_dict:
        list_cust.append((
            row['customer_id'],
            row['company_name'],
            row['contact_name']
        ))
    return list_cust


def create_orders_entries(list_dict):
    """Возвращает список кортежей с данными для заполнения таблицы orders"""
    list_orders = []
    for row in list_dict:
        list_orders.append((
            int(row['order_id']),
            row['customer_id'],
            int(row['employee_id']),
            datetime.strptime(row['order_date'], '%Y-%m-%d').date(),
            row['ship_city']
        ))
    return list_orders


def insert_to_database(query, vars_list):
    """Подключается к БД north и записывает данные в таблицу"""
    conn = psycopg2.connect(
        host="localhost",
        database="north",
        user="postgres",
        password="12345"
    )
    try:
        with conn:
            with conn.cursor() as cur:
                cur.executemany(query=query, vars_list=vars_list)
    finally:
        conn.close()


def main():
    employees = load_data(emp_data)
    emp_list = create_employees_entries(employees)
    insert_to_database(query="INSERT INTO employees VALUES (%s, %s, %s, %s, %s, %s)", vars_list=emp_list)

    customers = load_data(custom_data)
    cus_list = create_customers_entries(customers)
    insert_to_database(query="INSERT INTO customers VALUES (%s, %s, %s)", vars_list=cus_list)

    orders = load_data(orders_data)
    ord_list = create_orders_entries(orders)
    insert_to_database(query="INSERT INTO orders VALUES (%s, %s, %s, %s, %s)", vars_list=ord_list)


if __name__ == "__main__":
    main()
