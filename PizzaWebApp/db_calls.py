from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import pyodbc

key_vault_url = 'https://adjp-pizza-co-key-vault.vault.azure.net/'
credential = DefaultAzureCredential()
client = SecretClient(vault_url=key_vault_url,credential=credential)
db_connection_string = client.get_secret('adjp-pizza-co-db-connection-string') #currently set to JP's local db, need to update to azure sql when ready


def connection():
    cstr = db_connection_string.value
    conn = pyodbc.connect(cstr)
    return(conn)

class db_read: 
    def basket_count(order_id): 
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("""SELECT CASE WHEN COUNT(*) IS NULL THEN 0 ELSE COUNT(*) END AS pizza_count
        FROM [order].[pizzas] AS op
        WHERE op.order_id = ?""",order_id)
        basket_count = cursor.fetchone()
        conn.close()
        return basket_count.pizza_count

    def check_open_orders(user_id): 
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT order_id FROM [order].[details] WHERE customer_id = ? AND status_id = 1",user_id)
        order_id = cursor.fetchone()
        conn.close()
        if order_id:
            return order_id.order_id
        else:
            return

    def get_pizza_toppings():
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT topping_id,topping_name,topping_category,cost FROM pizza.toppings")
        topping_info = cursor.fetchall()
        conn.close()
        return topping_info

    def get_order_statuses():
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT status_id FROM [order].[status]")
        status_info = cursor.fetchall()
        conn.close()
        return status_info

    def get_pizza_sizes():
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT size_id,external_name,inches,cm,cost FROM pizza.sizes")
        size_id = cursor.fetchall()
        conn.close()
        return size_id

    def get_user_id(user_name):
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT customer_id FROM customer.details WHERE email = ?",user_name)
        user_id = cursor.fetchone()
        conn.close()
        if user_id:
            return user_id.customer_id

    def get_user_info(user_id):
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT customer_id, email, full_name, password_hash FROM customer.details WHERE customer_id = ?",user_id)
        user = cursor.fetchone()
        conn.close()
        return user

    def get_basket(user_id, order_id):
        conn = connection()
        cursor = conn.cursor()
        cursor.execute(f"EXEC [order].[basket] {order_id},{user_id}")
        basket = cursor.fetchone()
        conn.close()
        return basket

    def get_basket_items(user_id, order_id):
        conn = connection()
        cursor = conn.cursor()
        cursor.execute(f"EXEC [order].[basket_items] {order_id},{user_id}")
        basket_items = cursor.fetchall()
        conn.close()
        return basket_items

class db_write: 
    def populate_toppings():
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO pizza.toppings 
    VALUES 
     ('Mozzarella','Cheese',1)
    ,('Parmesan','Cheese',1)
    ,('Romano','Cheese',1)
    ,('Fontina','Cheese',1)
    ,('Gruyere','Cheese',1)
    ,('Gorgonzola','Cheese',1)
    ,('Blue cheese','Cheese',1)
    ,('Goat cheese','Cheese',1)
    ,('Pepperoni','Meat',2.5)
    ,('Sausage','Meat',2.5)
    ,('Ham','Meat',2.5)
    ,('Bacon','Meat',2.5)
    ,('Chicken','Meat',2.5)
    ,('Ground beef','Meat',2.5)
    ,('Shrimp','Meat',2.5)
    ,('Anchovies','Meat',2.5)
    ,('Mushrooms','Vegetables',2)
    ,('Onions','Vegetables',2)
    ,('Bell peppers','Vegetables',2)
    ,('Green peppers','Vegetables',2)
    ,('Red peppers','Vegetables',2)
    ,('Jalepenios','Vegetables',2)
    ,('Gerkhins','Vegetables',2)
    ,('Black olives','Vegetables',2)
    ,('Green olives','Vegetables',2)
    ,('Artichoke hearts','Vegetables',2)
    ,('Spinach','Vegetables',2)
    ,('Zucchini','Vegetables',2)
    ,('Eggplant','Vegetables',2)
    ,('Pineapple','Vegetables',2)
    ,('chilli flakes','misc',1.5)
    ,('burger sauce','misc',1.5);
""")
        conn.commit()
        conn.close()
        return

    def populate_sizes():
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO pizza.sizes
    VALUES 
     (1,'Small',6,15,7)
    ,(2,'Medium',9,23,12)
    ,(3,'Large',12,30,16)
    ,(4,'MEGA',15,38,20);""")
        conn.commit()
        conn.close()
        return

    def populate_order_status():
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO [order].[status]
    VALUES 
     (1,'In Basket')
    ,(2,'Order Placed')
    ,(3,'Delivered');""")
        conn.commit()
        conn.close()
        return


    def add_new_customer(data,pw_hash):
        email = data.get('email')
        full_name = data.get('full_name')
        phone_num = data.get('phone_num')
        street_address = data.get('street_address')
        city = data.get('city')
        postcode = data.get('postcode')
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO customer.details
        VALUES(?,?,?,?,?,?,?)
        """,email,full_name,phone_num,street_address,city,postcode,pw_hash
        )
        conn.commit()
        conn.close()
        return

    def start_new_order(user_id):
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO [order].details(customer_id,created_date,total_cost,status_id)
        VALUES(?,GETUTCDATE(),0,1 )
        """,user_id)
        conn.commit()
        conn.close()
        return

    def new_custom_pizza(order_id, order_details):
        pizza_size = order_details.get('selected_size')
        pizza_toppings = order_details.getlist('selected_topping')
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO [order].pizzas(order_id,pizza_size_id,is_custom)
        VALUES(?,?,1)
        """,order_id,pizza_size)
        conn.commit()
        cursor.execute("SELECT TOP (1) order_pizza_id FROM [order].pizzas WHERE order_id = ? ORDER BY order_pizza_id DESC",order_id)
        pizza_id = cursor.fetchone()
        print(pizza_id[0])
        for topping in pizza_toppings:
            cursor.execute("INSERT INTO [order].pizza_toppings(order_pizza_id,topping_id) VALUES(?,?)",pizza_id.order_pizza_id,topping)
        conn.commit()
        cursor.execute(f"""
        SELECT ps.cost + SUM(pt.cost) AS add_cost
        FROM [order].[details] AS od 
        INNER JOIN [order].[pizzas] AS op
            ON op.order_id = od.order_id
        INNER JOIN pizza.sizes AS ps 
            ON ps.size_id = op.pizza_size_id
        INNER JOIN  [order].[pizza_toppings] AS opt 
            ON opt.order_pizza_id = op.order_pizza_id
        INNER JOIN pizza.toppings AS pt 
            ON pt.topping_id = opt.topping_id
        WHERE op.order_pizza_id = {pizza_id[0]}
        GROUP BY ps.cost;
        """)
        add_cost = cursor.fetchone()
        cursor.execute(f"""
        UPDATE od
        SET od.total_cost = od.total_cost + {add_cost[0]}
        FROM [order].[details] AS od 
        INNER JOIN [order].[pizzas] AS op
            ON op.order_id = od.order_id
        WHERE op.order_pizza_id = {pizza_id[0]}
        """)
        conn.commit()
        conn.close()
        return

    def order_the_pizza(order_id):
        conn = connection()
        cursor = conn.cursor()
        cursor.execute(""" UPDATE od
        SET od.status_id = 2
        FROM [order].[details] AS od 
        WHERE od.order_id = ?
        """,order_id)
        conn.commit()
        conn.close()
        return