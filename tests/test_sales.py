from src.sales_analysis import calculate_results, read_csv
import pytest

@pytest.fixture
def sample_sales():
    test_data = [
        {"product": "Notebook", "quantity": "2", "unit_price": "15.50"},
        {"product": "Pen", "quantity": "5", "unit_price": "2.40"}
    ]
    return test_data

def test_sales_count(sample_sales):
    results = calculate_results(sample_sales)
    assert results["sales_count"] == 2
    
def test_total_revenue(sample_sales):
    results = calculate_results(sample_sales)
    assert results["total_revenue"] == 43.00

def test_revenue_by_product(sample_sales):
    results = calculate_results(sample_sales)
    assert results["revenue_by_product"]["Pen"] == 12.00
    assert results["revenue_by_product"]["Notebook"] == 31.00

def test_empty_sales():
    results = calculate_results([])
    assert results['sales_count'] == 0
    assert results['total_revenue'] == 0
    assert results['individual_sale_values'] == []
    assert results['revenue_by_product'] == {}

def test_extended_csv_processing():
    data = read_csv("data/sales_extended.csv")
    results = calculate_results(data)
    assert results['sales_count'] == 36
    assert results['total_revenue'] == pytest.approx(1175.70)
