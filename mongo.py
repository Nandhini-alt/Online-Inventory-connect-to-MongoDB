from pymongo import MongoClient


class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def get_quantity(self):
        return self.quantity

    def set_name(self, name):
        self.name = name

    def set_price(self, price):
        self.price = price

    def set_quantity(self, quantity):
        self.quantity = quantity


class DiscountedProduct(Product):
    def __init__(self, name, price, quantity, discount_percentage):
        super().__init__(name, price, quantity)
        self.discount_percentage = discount_percentage

    def get_discount_percentage(self):
        return self.discount_percentage

    def get_price(self):
        discount = self.price * (self.discount_percentage / 100)
        discounted_price = self.price - discount
        return discounted_price


def add_product(collection, product):
    if 'discount' in product:

        discounted_product = DiscountedProduct(
            product['name'], product['price'], product['quantity'], product['discount']
        )
        discounted_price = discounted_product.get_price()  # Calculate the discounted price
        product_data = {
            'name': product['name'],
            'price': discounted_price,
            'quantity': product['quantity'],
            'discount_percentage': product['discount']
        }
        collection.insert_one(product_data)
    else:
        product_data = {
            'name': product['name'],
            'price': product['price'],
            'quantity': product['quantity']
        }
        collection.insert_one(product_data)
    print("Product added successfully!!!")


def update_product(collection, product_name):
    product_data = collection.find_one({'name': product_name})
    if product_data:
        new_name = input("Enter new product name: ")
        new_price = get_float_input("Enter new product price: ")
        new_quantity = get_int_input("Enter new product quantity: ")

        if 'discount_percentage' in product_data:
            new_discount = get_int_input("Enter new product discount: ")
            updated_product = DiscountedProduct(new_name, new_price, new_quantity, new_discount)
        else:
            updated_product = Product(new_name, new_price, new_quantity)

        update_data = {
            'name': updated_product.get_name(),
            'price': updated_product.get_price(),
            'quantity': updated_product.get_quantity()
        }

        if isinstance(updated_product, DiscountedProduct):
            update_data['discount_percentage'] = updated_product.get_discount_percentage()

        collection.update_one({'name': product_name}, {'$set': update_data})
        print("Product updated successfully!!!")
    else:
        print("Product not found in the inventory.")


def remove_product(collection, product_name):
    product_data = collection.find_one({'name': product_name})
    if product_data:
        collection.delete_one({'name': product_name})
        print("Product removed successfully!!!")
    else:
        print("Product not found in the inventory.")


def search_product(collection, search_query):
    query = {'name': {'$regex': search_query, '$options': 'i'}}
    found_products = list(collection.find(query))

    if found_products:
        print("Matching products:")
        display_products(found_products)
    else:
        print("No matching products found.")


def display_products(products):
    for product in products:
        print("---------------------------------------------------------------------------")
        if 'discount_percentage' in product:
            discount = product['price'] * (product['discount_percentage'] / 100)
            discounted_price = product['price'] - discount
            print(
                f"ID:Name: {product['name']}, Price: ${discounted_price:.2f}, "
                f"Quantity: {product['quantity']}, Discount: {product['discount_percentage']}%"
            )
        else:
            print(
                f"ID:Name: {product['name']}, Price: ${product['price']:.2f}, "
                f"Quantity: {product['quantity']}, Discount: 0%"
            )
        print("---------------------------------------------------------------------------")


def get_float_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_int_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter an integer.")


def display_inventory(collection):
    products = list(collection.find())
    if products:
        print("Current inventory:")
        display_products(products)
    else:
        print("Inventory is empty.")


def main():
    # Connect to MongoDB
    client = MongoClient("mongodb://127.0.0.1:27017")
    database = client['ProductsDB']
    collection = database['Products']

    while True:
        print("--------------------------------------------")
        print("======= Inventory Management System =======")
        print("1. Add Product")
        print("2. Update Product")
        print("3. Remove Product")
        print("4. Search Product")
        print("5. Display Inventory")
        print("6. Exit")
        print("--------------------------------------------")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            print("**** ADD PRODUCT: ****")
            name = input("Enter product name: ")
            price = get_float_input("Enter product price: ")
            quantity = get_int_input("Enter product quantity: ")
            discount = get_int_input("Enter discount %: ")

            product = {'name': name, 'price': price, 'quantity': quantity, 'discount': discount}
            add_product(collection, product)

        elif choice == '2':
            try:
                print("**** UPDATE PRODUCT: ****")
                product_name = input("Enter product name: ")
                if product_name:
                    update_product(collection, product_name)
                else:
                    print("Invalid product name.")
            except ValueError:
                print("Invalid input. Please enter a valid product name.")

        elif choice == '3':
            print("**** REMOVE PRODUCT: ****")
            product_name = input("Enter product name: ")
            remove_product(collection, product_name)

        elif choice == '4':
            print("**** SEARCH QUERY: ****")
            search_query = input("Enter search query: ")
            search_product(collection, search_query)

        elif choice == '5':
            print("**** DISPLAY PRODUCT: ****")
            display_inventory(collection)

        elif choice == '6':
            print("Exiting the program...")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


if __name__ == '__main__':
    main()
