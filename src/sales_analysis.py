import csv

def read_csv():
    with open("data/sales.csv",'r',encoding='utf-8') as file:
        data = []
        for row in csv.DictReader(file):
            data.append(row)
    return data

def validate_csv():
    pass

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
    print(f"Total Revenue: R$:{results['total_revenue']:.2f}\n")
    print("Revenue by product:")
    for product, revenue in results['revenue_by_product'].items():
        print(f"- {product} R$:{revenue:.2f}")


if __name__ == "__main__": 
    data = read_csv()
    sales = calculate_results(data)
    display_report(sales)
    