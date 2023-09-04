class Contato:
    def __init__(self, nome, telefone):
        self.nome = nome
        self.telefone = telefone
        self.proximo = None

class AgendaHeroes:
    def __init__(self):
        self.tabela_hash = [None] * 26
        self.importar_contatos('agenda.csv')

    def calcular_indice(self, nome):
        primeira_letra = nome[0].upper()
        indice = ord(primeira_letra) - ord('A')
        return indice

    def adicionar_contato(self, nome, telefone):
        if not self.contato_existe(nome):
            indice = self.calcular_indice(nome)
            novo_contato = Contato(nome, telefone)
            
            if self.tabela_hash[indice] is None:
                self.tabela_hash[indice] = novo_contato
            else:
                atual = self.tabela_hash[indice]
                while atual.proximo:
                    atual = atual.proximo
                atual.proximo = novo_contato
            
            with open('agenda.csv', 'a') as f:
                f.write(f"{nome},{telefone}\n")
                print("Contato adicionado com sucesso!")

    def contato_existe(self, nome):
        try:
            with open('agenda.csv', 'r') as f:
                for linha in f:
                    nome_contato, _ = linha.strip().split(',')
                    if nome_contato == nome:
                        return True
        except FileNotFoundError:
            pass 

        return False

    def buscar_contato(self, nome):
        indice = self.calcular_indice(nome)
        atual = self.tabela_hash[indice]
        
        while atual:
            if atual.nome == nome:
                return atual
            atual = atual.proximo
        
        return None

    def listar_contatos_por_letra(self, letra):
        letra = letra.upper()
        contatos = []

        # Verifica a tabela hash
        indice = ord(letra) - ord('A')
        atual = self.tabela_hash[indice]
        while atual:
            contatos.append((atual.nome, atual.telefone))
            atual = atual.proximo

        try:
            with open('agenda.csv', 'r') as f:
                for linha in f:
                    nome, telefone = linha.strip().split(',')
                    if nome[0].upper() == letra:
                        contatos.append((nome, telefone))
        except FileNotFoundError:
            pass

        return contatos

    def remover_contato(self, nome):
        indice = self.calcular_indice(nome)
        atual = self.tabela_hash[indice]
        anterior = None

        while atual:
            if atual.nome == nome:
                if anterior:
                    anterior.proximo = atual.proximo
                else:
                    self.tabela_hash[indice] = atual.proximo
                return True
            anterior = atual
            atual = atual.proximo
        
        return False

    def importar_contatos(self, arquivo):
        try:
            with open(arquivo, 'r') as f:
                for linha in f:
                    nome, telefone = linha.strip().split(',')
                    self.adicionar_contato(nome, telefone)
            print("Contatos importados com sucesso!")
        except FileNotFoundError:
            print("O arquivo 'agenda.csv' não foi encontrado.")

    def menu_interativo(self):
        while True:
            print("\nMenu:")
            print("1. Adicionar Contato")
            print("2. Buscar Contato por Nome")
            print("3. Listar Contatos por Letra")
            print("4. Remover Contato")
            print("5. Sair")

            escolha = input("Escolha uma opção: ")

            if escolha == '1':
                nome = input("Nome: ")
                telefone = input("Telefone: ")
                self.adicionar_contato(nome, telefone)
            elif escolha == '2':
                nome = input("Nome a ser buscado: ")
                contato = self.buscar_contato(nome)
                if contato:
                    print(f"Nome: {contato.nome}")
                    print(f"Telefone: {contato.telefone}")
                else:
                    print("Contato não encontrado.")
            elif escolha == '3':
                letra = input("Digite a letra: ")
                contatos = self.listar_contatos_por_letra(letra)
                if contatos:
                    for contato in contatos:
                        print(f"Nome: {contato[0]}, Telefone: {contato[1]}")
                else:
                    print("Nenhum contato encontrado com essa letra.")
            elif escolha == '4':
                nome = input("Nome a ser removido: ")
                if self.remover_contato(nome):
                    print(f"Contato {nome} removido com sucesso!")
                else:
                    print("Contato não encontrado.")
            elif escolha == '5':
                break
            else:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    agenda = AgendaHeroes()
    agenda.menu_interativo()