import heapq
import pickle
import os
from django.conf import settings  # Import Django settings

class HuffmanCoding:
    def __init__(self):
        self.huffman_codes = {}  # Dictionary to store Huffman codes for each character
        self.reverse_huffman_codes = {}  # Reverse dictionary for decoding

    class HuffmanNode:
        def __init__(self, char=None, freq=0):
            self.char = char  # The character stored in the node (None for internal nodes)
            self.freq = freq  # Frequency of the character or sum of frequencies for internal nodes
            self.left = None  # Left child (None for leaf nodes)
            self.right = None  # Right child (None for leaf nodes)

        def __lt__(self, other):
            # To compare nodes based on frequency for the priority queue (heap)
            return self.freq < other.freq

    def build_frequency_table(self, text):
        frequency = {}
        for char in text:
            frequency[char] = frequency.get(char, 0) + 1
        return frequency

    def build_huffman_tree(self, frequency):
        priority_queue = [self.HuffmanNode(char, freq) for char, freq in frequency.items()]
        heapq.heapify(priority_queue)

        while len(priority_queue) > 1:
            left = heapq.heappop(priority_queue)
            right = heapq.heappop(priority_queue)
            merged = self.HuffmanNode(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            heapq.heappush(priority_queue, merged)

        return priority_queue[0]

    def build_codes(self, root, current_code):
        if root is None:
            return
        if root.char is not None:
            self.huffman_codes[root.char] = current_code
            self.reverse_huffman_codes[current_code] = root.char
            return
        self.build_codes(root.left, current_code + "0")
        self.build_codes(root.right, current_code + "1")

    def encode_text(self, text):
        return ''.join([self.huffman_codes[char] for char in text])

    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        encoded_text += "0" * extra_padding
        padded_info = "{0:08b}".format(extra_padding)
        return padded_info + encoded_text

    def to_byte_array(self, padded_encoded_text):
        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i + 8]
            b.append(int(byte, 2))
        return b

    def compress(self, input_file, output_file):
    # Ensure the input file exists
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"The file {input_file} was not found!")

        # Read the input file
        with open(input_file, 'r') as file:
            text = file.read()

        # Build the Huffman Tree and codes
        frequency = self.build_frequency_table(text)
        huffman_tree_root = self.build_huffman_tree(frequency)
        self.build_codes(huffman_tree_root, "")

        # Encode the text
        encoded_text = self.encode_text(text)
        padded_encoded_text = self.pad_encoded_text(encoded_text)
        byte_array = self.to_byte_array(padded_encoded_text)

        # Define the output path
        output_path = os.path.join(settings.MEDIA_ROOT, "downloads", output_file)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Ensure directory exists

        # Save the compressed file
        with open(output_path, 'wb') as output:
            pickle.dump((huffman_tree_root, byte_array), output)

        print(f"File compressed and saved to: {output_path}")

    def decompress(self, input_file, output_file):
        with open(input_file, 'rb') as file:
            huffman_tree_root, byte_array = pickle.load(file)

        bit_string = ""
        for byte in byte_array:
            bits = bin(byte)[2:].rjust(8, '0')
            bit_string += bits

        padded_info = bit_string[:8]
        extra_padding = int(padded_info, 2)
        encoded_text = bit_string[8:-extra_padding]
        decoded_text = self.decode_text(encoded_text, huffman_tree_root)

        os.makedirs("downloads", exist_ok=True)  # Ensure the downloads directory exists
        output_path = os.path.join("downloads", output_file)
        with open(output_path, 'w') as output:
            output.write(decoded_text)

        print(f"File decompressed and saved to: {output_path}")

    def decode_text(self, encoded_text, root):
        decoded_text = ""
        current_node = root
        for bit in encoded_text:
            current_node = current_node.left if bit == "0" else current_node.right
            if current_node.left is None and current_node.right is None:
                decoded_text += current_node.char
                current_node = root
        return decoded_text


# Main Program
def main(input_file):
    compressed_file = "compressed.huff"
    decompressed_file = "decompressed.txt"

    huffman = HuffmanCoding()
    huffman.compress(input_file, compressed_file)
    huffman.decompress(f"downloads/{compressed_file}", decompressed_file)
