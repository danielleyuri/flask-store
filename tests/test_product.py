def test_it_returns_status_code_200_on_product_route(client):
     response = client.get("/app/products")
     assert response.status_code == 200