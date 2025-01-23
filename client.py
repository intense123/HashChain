from hashchain import ServerController
import random

class HashChainClient:
    def __init__(self, mod=145321, initial_servers=3):
        """Initialize the client with a ServerController instance"""
        self.controller = ServerController(mod, initial_servers)
        
    def add_data(self, data):
        """Add data to the hash chain"""
        try:
            hash_value = data % self.controller.mod  # Calculate hash
            print(f"\nData: {data}")
            print(f"Hash value: {hash_value}")
            print(f"Available servers: {self.controller.servers}")
            
            self.controller.insert_data(data)
            server = self.controller.get_server_by_data(data)
            print(f"Data was stored in server: {server}")
        except Exception as e:
            print(f"Error adding data: {e}")
            
    def remove_data(self, data):
        """Remove data from the hash chain"""
        success = self.controller.delete_data(data)
        return success
    
    def find_data(self, data):
        """Find which server contains the data"""
        return self.controller.get_server_by_data(data)
    
    def add_server(self):
        """Add a new server to the network"""
        try:
            self.controller.insert_a_new_server()
            print("Successfully added a new server")
        except Exception as e:
            print(f"Error adding server: {e}")
    
    def remove_server(self, server_index):
        """Remove a server from the network"""
        success = self.controller.delete_a_server(server_index)
        return success
    
    def display_network_state(self):
        """Display the current state of all servers and their data"""
        print("\nCurrent Network State:")
        print("-" * 50)
        self.controller.print_servers_and_data()
        
    def bulk_add_random_data(self, count, max_value=10**15):
        """Add multiple random data points to the network"""
        print(f"\nAdding {count} random data points...")
        for _ in range(count):
            self.add_data(random.randint(0, max_value))

def main():
    # Create a client instance
    print("Initializing Hash Chain Client...")
    client = HashChainClient()
    
    # Demonstrate client operations
    print("\n1. Adding some specific data")
    client.add_data(24566565356352)
    client.add_data(1234567890)
    
    print("\n2. Adding bulk random data")
    client.bulk_add_random_data(5)
    
    print("\n3. Displaying current network state")
    client.display_network_state()
    
    print("\n4. Finding specific data")
    client.find_data(24566565356352)
    client.find_data(9999)  # Non-existent data
    
    print("\n5. Adding a new server")
    client.add_server()
    client.display_network_state()
    
    print("\n6. Removing data")
    client.remove_data(24566565356352)
    
    print("\n7. Removing a server")
    client.remove_server(1)
    client.display_network_state()

if __name__ == "__main__":
    main() 