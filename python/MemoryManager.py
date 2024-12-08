import random

class MemoryManager:
    def __init__(self, memory_size):
        self.memory = [0] * memory_size
        self.last_alloc_index = 0  # Usado pelo Next Fit

    def display_memory(self):
        print("Estado atual da memória:", self.memory)

    def calculate_fragmentation(self):
        free_blocks = ''.join(map(str, self.memory)).split('1')
        fragmentation = sum(1 for block in free_blocks if len(block) > 0 and len(block) < min_process_size)
        print(f"Fragmentação externa: {fragmentation}")

    def allocate(self, process_id, process_size, strategy):
        allocation_index = strategy(process_size)
        if allocation_index is not None:
            for i in range(allocation_index, allocation_index + process_size):
                self.memory[i] = process_id
            print(f"Processo {process_id} ({process_size} blocos) alocado no índice {allocation_index}.")
        else:
            print(f"Erro: Processo {process_id} ({process_size} blocos) não pôde ser alocado.")

    def deallocate(self, process_id):
        deallocated = False
        for i in range(len(self.memory)):
            if self.memory[i] == process_id:
                self.memory[i] = 0
                deallocated = True
        if deallocated:
            print(f"Processo {process_id} desalocado.")
        else:
            print(f"Erro: Processo {process_id} não encontrado para desalocar.")

    def first_fit(self, process_size):
        for i in range(len(self.memory) - process_size + 1):
            if all(block == 0 for block in self.memory[i:i + process_size]):
                return i
        return None

    def next_fit(self, process_size):
        n = len(self.memory)
        start_index = self.last_alloc_index
        for i in range(n):
            index = (start_index + i) % n
            if all(self.memory[(index + j) % n] == 0 for j in range(process_size)):
                self.last_alloc_index = (index + process_size) % n
                return index
        return None

    def best_fit(self, process_size):
        best_index = None
        best_size = float('inf')
        i = 0
        while i < len(self.memory):
            if self.memory[i] == 0:
                start = i
                while i < len(self.memory) and self.memory[i] == 0:
                    i += 1
                size = i - start
                if process_size <= size < best_size:
                    best_index, best_size = start, size
            i += 1
        return best_index

    def worst_fit(self, process_size):
        worst_index = None
        worst_size = -1
        i = 0
        while i < len(self.memory):
            if self.memory[i] == 0:
                start = i
                while i < len(self.memory) and self.memory[i] == 0:
                    i += 1
                size = i - start
                if size >= process_size and size > worst_size:
                    worst_index, worst_size = start, size
            i += 1
        return worst_index

    def quick_fit(self, process_size):
        # Quick Fit utiliza um pré-processamento de blocos livres por tamanho
        blocks = {}
        i = 0
        while i < len(self.memory):
            if self.memory[i] == 0:
                start = i
                while i < len(self.memory) and self.memory[i] == 0:
                    i += 1
                size = i - start
                if size not in blocks:
                    blocks[size] = []
                blocks[size].append(start)
            i += 1
        for size, start_indices in sorted(blocks.items()):
            if size >= process_size:
                return start_indices[0]
        return None

# Configurações
memory_size = 32
processes = [
    (1, 5), (2, 4), (3, 2), (4, 5), (5, 8),
    (6, 3), (7, 5), (8, 8), (9, 2), (10, 6)
]
min_process_size = min(p[1] for p in processes)
operations = 30

# Gerenciamento
memory_manager = MemoryManager(memory_size)

strategies = {
    "First Fit": memory_manager.first_fit,
    "Next Fit": memory_manager.next_fit,
    "Best Fit": memory_manager.best_fit,
    "Worst Fit": memory_manager.worst_fit,
    "Quick Fit": memory_manager.quick_fit
}

# Executando operações sorteadas
for strategy_name, strategy in strategies.items():
    print(f"\n== Estratégia: {strategy_name} ==")
    memory_manager = MemoryManager(memory_size)  # Reiniciar memória
    for _ in range(operations):
        process_id, process_size = random.choice(processes)
        if process_id in memory_manager.memory:
            memory_manager.deallocate(process_id)
        else:
            memory_manager.allocate(process_id, process_size, strategy)
        memory_manager.display_memory()
        memory_manager.calculate_fragmentation()
