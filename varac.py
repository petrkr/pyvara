import curses
import socket
import threading

# Function to parse the received data
def parse_message(data_buffer):
    messages = []
    while True:
        if ' ' not in data_buffer:
            break  # We don't have enough data to determine the message length

        # Find the space to determine the number of characters in the message
        space_index = data_buffer.find(' ')
        try:
            num_chars = int(data_buffer[:space_index])
        except ValueError:
            break  # Invalid data; wait for more data to arrive

        message_end = space_index + 1 + num_chars
        if len(data_buffer) < message_end:
            break  # We don't have the full message yet

        message = data_buffer[space_index + 1:message_end]
        messages.append(message)

        # Remove the processed message from the buffer
        data_buffer = data_buffer[message_end:]

    return messages, data_buffer


# Function to format and send a message
def format_message(msg):
    num_chars = len(msg)
    return f"{num_chars} {msg}"


# Function to handle receiving messages with chunked stream support
def receive_messages(sock, chat_window):
    data_buffer = ""
    while True:
        try:
            received_data = sock.recv(1024).decode('utf-8')
            if not received_data:
                break
            data_buffer += received_data

            # Parse messages from the data buffer
            messages, data_buffer = parse_message(data_buffer)
            for msg in messages:
                chat_window.addstr(f"\nReceived: {msg}")
                chat_window.refresh()
        except Exception as e:
            chat_window.addstr(f"\nError receiving data: {e}")
            chat_window.refresh()
            break

def start_client(stdscr, host, port):
    # Set up socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to the server
        client_socket.connect((host, port))

        # Setting up the curses window layout
        curses.curs_set(1)
        height, width = stdscr.getmaxyx()
        chat_window = curses.newwin(height - 3, width, 0, 0)
        input_window = curses.newwin(3, width, height - 3, 0)

        chat_window.scrollok(True)
        input_window.scrollok(True)

        # Create a thread for receiving messages
        recv_thread = threading.Thread(target=receive_messages, args=(client_socket, chat_window))
        recv_thread.daemon = True
        recv_thread.start()

        input_text = ""
        
        while True:
            input_window.clear()
            input_window.addstr("> " + input_text)
            input_window.refresh()

            key = stdscr.getch()
            
            # Handle backspace
            if key == curses.KEY_BACKSPACE or key == 127:
                input_text = input_text[:-1]
            # Handle Enter key to send message
            elif key == ord('\n'):
                if input_text.lower() == 'quit':
                    break

                # Format and send the message
                formatted_message = format_message(input_text)
                client_socket.sendall(formatted_message.encode('utf-8'))

                # Display the sent message in the chat window
                chat_window.addstr(f"\nYou: {input_text}")
                chat_window.refresh()

                # Clear input_text after sending
                input_text = ""
            else:
                input_text += chr(key)

    except Exception as e:
        chat_window.addstr(f"\nError: {e}")
        chat_window.refresh()
    finally:
        client_socket.close()
        curses.endwin()

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 8301
    curses.wrapper(start_client, host, port)
