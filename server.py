import Pyro4
import csv

# classe que representa o servidor do caixa do mercado
class MarketCashier(object):
    def __init__(self):
        self.items = self.load_items_from_csv("items.csv")

    def load_items_from_csv(self, filename):
        items = {}
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                items[row['id']] = {'product': row['product'], 'value': float(row['value'])}
        return items

    @Pyro4.expose
    # metodo para listar os produtos disponíveis
    def list_available_products(self):
        return self.items

    @Pyro4.expose
    # metodo para registrar uma compra
    def register_purchase(self, items_bought):
        total_cost = 0
        products_bought = []
        for item_id in items_bought:
            if item_id in self.items:
                total_cost += self.items[item_id]['value']
                products_bought.append(self.items[item_id]['product'])
            else:
                print(f"Item com ID {item_id} não encontrado.")
        return total_cost, products_bought


def main():
    daemon = Pyro4.Daemon()  # cria um daemon para aguardar as chamadas dos clientes

    ns_uri = "PYRO:Pyro.NameServer@127.0.0.1:9090"

    # cria uma instância do servidor do caixa do mercado
    cashier = MarketCashier()
    # registra o servidor com o Pyro
    uri = daemon.register(cashier)

    with Pyro4.Proxy(ns_uri) as ns:
        ns.register("example.market_cashier", uri)

    print("Servidor do caixa do mercado pronto.")
    daemon.requestLoop()    # Aguarda as chamadas dos clientes

if __name__ == "__main__":
    main()
