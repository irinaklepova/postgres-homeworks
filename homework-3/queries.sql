-- Напишите запросы, которые выводят следующую информацию:
-- 1. Название компании заказчика (company_name из табл. customers) и ФИО сотрудника, работающего над заказом этой
--компании (см таблицу employees),
-- когда и заказчик и сотрудник зарегистрированы в городе London, а доставку заказа ведет компания United Package
--(company_name в табл shippers)
SELECT c.company_name, CONCAT(e.last_name,' ', e.first_name) AS employer_name
FROM orders o
INNER JOIN customers c USING(customer_id)
INNER JOIN employees e USING(employee_id)
INNER JOIN shippers s ON s.shipper_id=o.ship_via
WHERE c.city='London' AND e.city='London' AND s.company_name='United Package'

-- 2. Наименование продукта, количество товара (product_name и units_in_stock в табл products),
-- имя поставщика и его телефон (contact_name и phone в табл suppliers) для таких продуктов,
-- которые не сняты с продажи (поле discontinued) и которых меньше 25 и которые в категориях Dairy Products и Condiments.
-- Отсортировать результат по возрастанию количества оставшегося товара.
SELECT p.product_name, p.units_in_stock, s.contact_name, s.phone
FROM products p
INNER JOIN suppliers s USING(supplier_id)
INNER JOIN categories c USING(category_id)
WHERE p.discontinued = 0 AND c.category_name IN ('Dairy Products', 'Condiments') AND p.units_in_stock < 25
ORDER BY p.units_in_stock

-- 3. Список компаний заказчиков (company_name из табл customers), не сделавших ни одного заказа
SELECT c.company_name FROM customers c
LEFT JOIN orders o USING(customer_id)
WHERE o.order_id IS NULL
ORDER BY c.company_name

-- 4. уникальные названия продуктов, которых заказано ровно 10 единиц (количество заказанных единиц см в колонке quantity
--табл order_details)
-- Этот запрос написать именно с использованием подзапроса.
SELECT product_name FROM products
WHERE product_id IN(SELECT product_id FROM order_details WHERE quantity=10)