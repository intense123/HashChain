import random

class ServerController:
    def __init__(self, mod, numberOfServer):
        self.mod = mod
        self.servers = set()
        self.dataStorage = {}
        for i in range(numberOfServer):
            randomNumber = random.randint(0, self.mod - 1)
            self.servers.add(randomNumber)
            self.dataStorage[randomNumber] = []
            
        self.servers = sorted(self.servers)
        print("The servers are:", self.servers, '\n')
    
    def get_previous_server(self, hash_value):
        for i in range(len(self.servers) - 1, -1, -1):
            if self.servers[i] <= hash_value:
                return self.servers[i]
        return self.servers[-1]  # Wrap around to the last server if no smaller server exists
    
    def insert_data(self, data):
        hash_value = self.hash(data)
        # print(f"The hash value of data '{data}' is {hash_value}")
        server = self.get_previous_server(hash_value)
        self.dataStorage[server].append(data)
        # print(f"Data '{data}' stored in server {server}\n")
    
    def delete_data(self, data):
        hash_value = self.hash(data)
        server = self.get_previous_server(hash_value)
        if data in self.dataStorage[server]:
            self.dataStorage[server].remove(data)
            print(f"Data '{data}' deleted from server {server}\n")
            return True
        print(f"Data '{data}' not found in any server\n")
        return False
    
    def get_server_by_data(self, data):
        hash_value = self.hash(data)
        server = self.get_previous_server(hash_value)
        if data in self.dataStorage[server]:
            print(f"Data {data} is at server {server}\n")
            return server
        print(f"No data found with value {data}\n")
        return None

    def insert_a_new_server(self):
        new_server = random.randint(0, self.mod - 1)
        while new_server in self.servers:
            new_server = random.randint(0, self.mod - 1)
        
        self.servers.append(new_server)
        self.servers = sorted(self.servers)
        self.dataStorage[new_server] = []
        
        print(f"New server {new_server} added.\n")
        
        # Rebalance data
        all_data = []
        for server in self.servers:
            all_data.extend(self.dataStorage[server])
            self.dataStorage[server] = []
        
        for data in all_data:
            self.insert_data(data)
    
    def delete_a_server(self, server_index_pos):
        if server_index_pos < 0 or server_index_pos >= len(self.servers):
            print(f"Server index {server_index_pos} is out of range.\n")
            return False
        
        server_to_delete = self.servers[server_index_pos]
        data_to_rebalance = self.dataStorage[server_to_delete]
        
        del self.dataStorage[server_to_delete]
        self.servers.remove(server_to_delete)
        
        print(f"Server {server_to_delete} deleted.\n")
        
        # Track data movement
        data_movement = []
        for data in data_to_rebalance:
            hash_value = self.hash(data)
            new_server = self.get_previous_server(hash_value)
            data_movement.append({
                'data': data,
                'from_server': server_to_delete,
                'to_server': new_server,
                'hash_value': hash_value
            })
            self.dataStorage[new_server].append(data)
        
        return {
            'success': True,
            'deleted_server': server_to_delete,
            'data_movement': data_movement
        }
    
    def print_servers_and_data(self):
        for server in self.servers:
            print(f"Server {server}: {self.dataStorage[server]}")
        print()
    
    def hash(self, value):
        return value % self.mod


