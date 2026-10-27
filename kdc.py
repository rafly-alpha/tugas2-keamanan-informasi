import socket
import random
import string
import sys
import threading

from manual_des import encrypt_text, decrypt_text
from config import KDC_IP, KDC_PORT, KA, KB


def generate_session_key() -> str:
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=16))


def handle_request(conn, addr):
    try:
        data = conn.recv(8192)
        if not data:
            return

        request = data.decode("ascii").strip()
        print(f"\n[KDC] Request dari {addr}: {request[:100]}{'...' if len(request) > 100 else ''}")

        # UBAH_KEY|<Alice|Bob>|<key_8char>
        if request.startswith("UBAH_KEY|"):
            parts = request.split("|")
            if len(parts) != 3:
                conn.sendall(b"ERR|Format salah")
                return

            _, who, new_key = parts
            if len(new_key) != 8:
                conn.sendall(b"ERR|Key harus 8 char")
                return

            if who == "Alice":
                old = handle_request.KA_current
                handle_request.KA_current = new_key
                print(f"[KDC] KA diubah: {old!r} -> {new_key!r}")
                conn.sendall(b"OK")
            elif who == "Bob":
                old = handle_request.KB_current
                handle_request.KB_current = new_key
                print(f"[KDC] KB diubah: {old!r} -> {new_key!r}")
                conn.sendall(b"OK")
            else:
                conn.sendall(b"ERR|Identitas tidak dikenal")
            return

        # REQ|Alice|Bob|N1_hex
        parts = request.split("|")
        if len(parts) != 4 or parts[0] != "REQ":
            print("[KDC] Format request tidak valid")
            conn.sendall(b"ERR|Format tidak valid")
            return

        _, alice_id, bob_id, n1_hex = parts
        n1 = bytes.fromhex(n1_hex)

        KA_latest = handle_request.KA_current
        KB_latest = handle_request.KB_current

        Ks = generate_session_key()
        print(f"[KDC] Ks            : {Ks!r}")
        print(f"[KDC] Pakai KA      : {KA_latest!r}")
        print(f"[KDC] Pakai KB      : {KB_latest!r}")

        tiket_plain = Ks + "|Alice"
        tiket_hex = encrypt_text(tiket_plain, KB_latest)
        print(f"[KDC] Tiket (Hex)   : {tiket_hex}")

        payload = n1.hex().upper() + Ks + "|Bob|" + tiket_hex
        response_hex = encrypt_text(payload, KA_latest)
        print(f"[KDC] Response (Hex): {response_hex[:80]}...")

        conn.sendall(response_hex.encode("ascii"))

    except Exception as e:
        print(f"[KDC] Error: {type(e).__name__}: {e}")
        try:
            conn.sendall(b"ERR")
        except Exception:
            pass
    finally:
        conn.close()


def accept_loop(server):
    while True:
        try:
            conn, addr = server.accept()
            threading.Thread(target=handle_request, args=(conn, addr), daemon=True).start()
        except OSError:
            break
        except Exception as e:
            print(f"[KDC] Accept error: {e}")


def main():
    handle_request.KA_current = KA
    handle_request.KB_current = KB

    print("=" * 60)
    print("KDC - Key Distribution Center")
    print("=" * 60)
    print(f"  Listening : {KDC_IP}:{KDC_PORT}")
    print(f"  KA (DES)  : {KA!r}")
    print(f"  KB (DES)  : {KB!r}")
    print("=" * 60)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((KDC_IP, KDC_PORT))
    server.listen(10)

    print("[KDC] Menunggu koneksi... (Ctrl+C untuk stop)\n")

    threading.Thread(target=accept_loop, args=(server,), daemon=True).start()

    try:
        while True:
            threading.Event().wait(1)
    except KeyboardInterrupt:
        print("\n[KDC] Shutdown.")
        server.close()
        sys.exit(0)


if __name__ == "__main__":
    main()