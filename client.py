import Pyro4

def main():
    # encontra o servidor do caixa do mercado
    ns = Pyro4.locateNS()
    uri = ns.lookup("example.market_cashier")
    cashier = Pyro4.Proxy(uri)

    # lista os produtos disponíveis
    print("Produtos disponíveis:")
    products = cashier.list_available_products()
    for item_id, item_info in products.items():
        print(f"ID: {item_id}, Produto: {item_info['product']}, Valor: R${item_info['value']:.2f}")

    # loop principal do cliente
    while True:
        print("\nDigite os IDs dos produtos comprados separados por vírgula (ou 'sair' para sair):")
        ids_input = input(">> ")
        if ids_input.lower() == "sair":
            break
        items_bought = [item.strip() for item in ids_input.split(',')]
        total_cost, products_bought = cashier.register_purchase(items_bought)
        print("\nNota Fiscal:")
        print("Produtos comprados:")
        for product in products_bought:
            print(f"- {product}")
        print(f"\nValor total da compra: R${total_cost:.2f}")

if __name__ == "__main__":
    main()
