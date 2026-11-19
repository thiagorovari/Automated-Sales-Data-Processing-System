import csv
from decimal import Decimal, InvalidOperation
from datetime import datetime
def read_csv(path):
    with open(path,'r',encoding='utf-8') as file:
        data = []
        for row in csv.DictReader(file):
            data.append(row)
    return data

def validate_csv(data):
    
    valid =[]
    invalid = []
    seen_ids = []
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

        try:
            price = Decimal(copy['unit_price'])
            if not price.is_finite():
                copy["errors"].append("Unit price must be a finite, non-negative number")
            elif price < 0.00:
                copy["errors"].append("Unit price must be a finite, non-negative number")
        except InvalidOperation:
            copy["errors"].append("Unit price must be a finite, non-negative number")

        try:
            parsed_date = datetime.strptime(copy["date"], "%Y-%m-%d")
            if(copy["date"] != parsed_date.date().isoformat()):
                copy["errors"].append("Sales date must be in format YYYY-MM-DD")

        except ValueError:
            copy["errors"].append("Sales date must be in format YYYY-MM-DD")

        try:
            id_check = int(copy["sale_id"])
            if id_check <= 0 or id_check in seen_ids:
                copy["errors"].append("Invalid id")
            elif(copy["errors"] == []):
                seen_ids.append(id_check)
        except ValueError:
            copy["errors"].append("Invalid id")


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
        row_revenue = int(row['quantity']) * Decimal(row['unit_price'])
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
    # Reject this row for its price, but don't reserve ID 1001.
    {"sale_id": "1001", "product": "Backpack", "quantity": "1", "unit_price": "abc", "date": "2026-11-18"},

    # Accept Notebook, then reject Stapler because "01001" also converts to 1001.
    {"sale_id": "1001", "product": "Notebook", "quantity": "2", "unit_price": "15.50", "date": "2026-11-18"},
    {"sale_id": "01001", "product": "Stapler", "quantity": "1", "unit_price": "24.90", "date": "2026-11-18"},

    # Keep the original date cases.
    {"sale_id": "1002", "product": "Pencil", "quantity": "5", "unit_price": "1.50", "date": "2024-02-29"},
    {"sale_id": "1003", "product": "Pen", "quantity": "3", "unit_price": "2.40", "date": "2026-02-30"},
    {"sale_id": "1004", "product": "Folder", "quantity": "1", "unit_price": "4.50", "date": "2026-1-5"},
    {"sale_id": "1005", "product": "Eraser", "quantity": "2", "unit_price": "3.20", "date": ""},
    {"sale_id": "1006", "product": "Marker", "quantity": "abc", "unit_price": "7.90", "date": "2025-02-29"},

    # All other fields are valid, so these rows should fail only on sale_id.
    {"sale_id": "0", "product": "Binder", "quantity": "1", "unit_price": "8.00", "date": "2026-11-18"},
    {"sale_id": "abc", "product": "Ruler", "quantity": "1", "unit_price": "3.00", "date": "2026-11-18"},
]
    data = test_data
    valid_data, invalid = validate_csv(data)
    sales = calculate_results(valid_data)
    display_report(sales)
    print('Invalid data:\n')

    for row in invalid:
        print(f"{row}\n")


    