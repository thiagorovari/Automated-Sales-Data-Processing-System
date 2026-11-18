import csv

def read_csv(path):
    with open(path,'r',encoding='utf-8') as file:
        data = []
        for row in csv.DictReader(file):
            data.append(row)
    return data

def validate_csv(data):
    
    valid =[]
    invalid = []
    for row in data:
        
        try:
            copy = row.copy()
            copy['errors'] = []
            if(int(copy['quantity'])<=0):
                copy["errors"].append("Quantity must be a positive integer")
        except ValueError:
                    copy["errors"].append("Quantity must be a positive integer")

        if not copy["product"].strip():
            copy["errors"].append("Product name is empty")
        

        if(copy['errors'] == []):
            valid.append(copy)
        else:
            invalid.append(copy)
    return valid, invalid
            


def calculate_results(data):
    results = {}
    sale_values = []
    revenue_by_product = {}
    
    for row in data:
        row_revenue = int(row['quantity']) * float(row['unit_price'])
        sale_values.append(row_revenue)
        product = row['product']

        if product in revenue_by_product:
            revenue_by_product[product] += row_revenue

        else:
            revenue_by_product[product] = row_revenue
    
    revenue = sum(sale_values)
    sale_count = len(data)

    results['individual_sale_values'] = sale_values
    results['total_revenue'] = revenue
    results['revenue_by_product'] = revenue_by_product
    results['sales_count'] = sale_count
    
    return results

def display_report(results):
    print('====== SALES REPORT ======\n')
    print(f"Total sales processed: {results['sales_count']}")
    print(f"Total Revenue: R${results['total_revenue']:.2f}\n")
    print("Revenue by product:")
    for product, revenue in results['revenue_by_product'].items():
        print(f"- {product}: R$ {revenue:.2f}")


if __name__ == "__main__": 
    test_data = [
    {"product": "Notebook", "quantity": "2", "unit_price": "15.50"},
    {"product": "Pen", "quantity": "-3", "unit_price": "2.40"},
    {"product": "", "quantity": "abc", "unit_price": "89.90"},
    {"product": "Pencil", "quantity": "5", "unit_price": "1.50"}
    ]
    data = test_data
    valid_data, invalid = validate_csv(data)
    sales = calculate_results(valid_data)
    display_report(sales)
    print('Invalid data:\n')
    print(invalid)


    