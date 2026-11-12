from src.sales_analysis import calculate_results

def test_sales_count():
    test_data = [
        {"product": "Notebook", "quantity": "2", "unit_price": "15.50"},
        {"product": "Pen", "quantity": "5", "unit_price": "2.40"}
    ]

    results = calculate_results(test_data)

    assert results["sales_count"] == 2
    assert results["total_revenue"] == 43.00
    assert results["revenue_by_product"]["Pen"] == 12.00
    assert results["revenue_by_product"]["Notebook"] == 31.00