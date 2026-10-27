import socket
import threading
import os
import sys
import time

from manual_des import encrypt_text, decrypt_text
from manual_aes import encrypt_text as aes_encrypt_text, decrypt_text as aes_decrypt_text
from config import (
    KDC_IP, KDC_PORT, ALICE_IP, ALICE_PORT, BOB_IP, BOB_PORT,
    KA, KB,
)


class NodeState:
    def __init__(self):
        self.identity = None
        self.my_ip = None
        self.my_port = None
        self.peer_ip = None
        self.peer_port = None
        self.master_key_ascii = None
        self.session_key = None
        self.n2 = None
        self.tiket = None
        self.handshake_done = False

    def is_ready(self) -> bool:
        return self.session_key is not None and self.handshake_done


state = NodeState()


# ============================================================
# LISTENER (background thread)
# ============================================================
def listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((state.my_ip, state.my_port))
    sock.listen(5)
    print(f"[{state.identity}] Listener aktif di {state.my_ip}:{state.my_port}")

    while True:
        try:
            conn, addr = sock.accept()
            data = conn.recv(8192).decode("ascii").strip()
            conn.close()
            handle_incoming(data, addr)
        except Exception as e:
            print(f"[{state.identity}] Listener error: {e}")
            break


# ============================================================
# HANDLE PESAN MASUK
# ============================================================
def handle_incoming(data: str, addr):
    print(f"\n[{state.identity}] Pesan masuk dari {addr}: {data[:80]}{'...' if len(data) > 80 else ''}")

    # HANDLE RESET — reset state, siap terima Tiket baru
    if data == "RESET":
        print(f"[{state.identity}] Terima RESET dari peer — reset state")
        state.session_key = None
        state.n2 = None
        state.tiket = None
        state.handshake_done = False
        try:
            send_to_peer("RESET_OK")
            print(f"[{state.identity}] Kirim RESET_OK")
        except Exception as e:
            print(f"[{state.identity}] Gagal kirim RESET_OK: {e}")
        return

    # HANDLE RESET_OK — konfirmasi
    if data == "RESET_OK":
        print(f"[{state.identity}] Peer konfirmasi RESET_OK")
        return

    # ============ ALICE ============
    if state.identity == "Alice":
        # FASE 1: sudah punya Ks, handshake belum selesai -> tunggu N2 dari Bob
        if state.session_key and not state.handshake_done:
            try:
                n2_hex_str = aes_decrypt_text(data, state.session_key)
                print(f"[Alice] Terima N2_hex = {n2_hex_str}")

                n2_bytes = bytes.fromhex(n2_hex_str)
                n2_min_1 = bytes([(b - 1) % 256 for b in n2_bytes])
                n2_min_1_hex_str = n2_min_1.hex().upper()
                print(f"[Alice] Kirim N2_hex - 1 = {n2_min_1_hex_str}")

                reply = aes_encrypt_text(n2_min_1_hex_str, state.session_key)
                send_to_peer(reply)
                state.handshake_done = True
                print("[Alice] Langkah 5 selesai - siap komunikasi AES dua arah")
            except Exception as e:
                print(f"[Alice] Abaikan pesan (bukan N2): {e}")

        # FASE 2: handshake selesai -> chat AES
        elif state.handshake_done:
            try:
                plaintext = aes_decrypt_text(data, state.session_key)
                print(f"[Alice] Pesan dari Bob: {plaintext!r}")
            except Exception as e:
                print(f"[Alice] Gagal decrypt pesan: {e}")

        else:
            print("[Alice] Abaikan pesan (session key belum siap)")

    # ============ BOB ============
    elif state.identity == "Bob":
        # FASE 1: belum punya Ks -> tunggu Tiket DES dari Alice
        if state.session_key is None:
            try:
                tiket_plain = decrypt_text(data, state.master_key_ascii)
                Ks = tiket_plain[:16]
                sender = tiket_plain[17:]
                state.session_key = Ks
                print(f"[Bob] Terima Tiket dari {sender}")
                print(f"[Bob] Ks = {Ks!r}")

                state.n2 = os.urandom(8)
                n2_hex_str = state.n2.hex().upper()
                print(f"[Bob] Bangkitkan N2 = {n2_hex_str}")
                n2_encrypted = aes_encrypt_text(n2_hex_str, Ks)
                send_to_peer(n2_encrypted)
                print("[Bob] Kirim AES_Ks(N2_hex) ke Alice")
            except Exception as e:
                print(f"[Bob] Gagal proses Tiket: {e}")

        # FASE 2: sudah punya Ks, handshake belum selesai -> tunggu N2-1
        elif not state.handshake_done:
            try:
                received_hex_str = aes_decrypt_text(data, state.session_key)
                print(f"[Bob] Terima N2_hex - 1 = {received_hex_str}")

                expected_bytes = bytes([(b - 1) % 256 for b in state.n2])
                expected_hex_str = expected_bytes.hex().upper()

                if received_hex_str == expected_hex_str:
                    print("[Bob] Verifikasi N2-1 OK - siap komunikasi AES dua arah")
                    state.handshake_done = True
                    state.n2 = None
                else:
                    print("[Bob] Verifikasi GAGAL")
                    print(f"        Expected: {expected_hex_str}")
                    print(f"        Received: {received_hex_str}")
            except Exception as e:
                print(f"[Bob] Abaikan pesan (bukan N2-1): {e}")

        # FASE 3: handshake selesai -> chat AES
        else:
            try:
                plaintext = aes_decrypt_text(data, state.session_key)
                print(f"[Bob] Pesan dari Alice: {plaintext!r}")
            except Exception as e:
                print(f"[Bob] Gagal decrypt pesan: {e}")


# ============================================================
# SEND HELPERS
# ============================================================
def send_to_peer(message: str):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((state.peer_ip, state.peer_port))
    sock.sendall(message.encode("ascii"))
    sock.close()


def sync_key_to_kdc(new_key: str) -> bool:
    """Kirim UBAH_KEY ke KDC. Return True kalau KDC setuju."""
    msg = f"UBAH_KEY|{state.identity}|{new_key}"
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((KDC_IP, KDC_PORT))
        sock.sendall(msg.encode("ascii"))
        response = sock.recv(1024).decode("ascii").strip()
        sock.close()
        return response == "OK"
    except Exception as e:
        print(f"[{state.identity}] Gagal hubungi KDC: {e}")
        return False


# ============================================================
# ALUR LANGKAH 1-3 (ALICE)
# ============================================================
def alice_request_session_key():
    print(f"\n[Alice] Minta session key ke KDC {KDC_IP}:{KDC_PORT}...")

    n1 = os.urandom(8)
    request = f"REQ|Alice|Bob|{n1.hex().upper()}"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((KDC_IP, KDC_PORT))
    sock.sendall(request.encode("ascii"))
    response_hex = sock.recv(8192).decode("ascii").strip()
    sock.close()

    print(f"[Alice] Response dari KDC (Hex): {response_hex[:80]}...")

    payload = decrypt_text(response_hex, state.master_key_ascii)
    n1_received = payload[:16]
    Ks = payload[16:32]
    tiket_hex = payload[37:]

    if n1_received != n1.hex().upper():
        print("[Alice] Nonce N1 tidak cocok!")
        return None

    state.session_key = Ks
    state.tiket = tiket_hex
    state.handshake_done = False
    print("[Alice] N1 cocok")
    print(f"[Alice] Ks = {Ks!r}")
    print(f"[Alice] Tiket = {tiket_hex}")
    return tiket_hex


def alice_send_tiket_to_bob(tiket_hex: str):
    """RESET Bob dulu, lalu kirim Tiket baru."""
    print(f"\n[Alice] Kirim RESET ke Bob {state.peer_ip}:{state.peer_port}...")
    send_to_peer("RESET")
    print("[Alice] RESET terkirim — beri waktu Bob reset...")
    time.sleep(0.5)

    print(f"[Alice] Kirim Tiket ke Bob...")
    send_to_peer(tiket_hex)
    print("[Alice] Tiket terkirim — menunggu N2 dari Bob...")


# ============================================================
# MENU
# ============================================================
def print_menu():
    print("\n" + "=" * 60)
    print(f"  MENU - {state.identity}")
    print(f"  Master Key: {state.master_key_ascii!r}")
    if state.session_key:
        status = "handshake OK" if state.handshake_done else "handshake..."
        print(f"  Session Key: {state.session_key!r}  ({status})")
    else:
        print(f"  Session Key: (belum ada)")
    print("=" * 60)
    if state.identity == "Alice":
        print("  [1] Minta Session Key ke KDC")
        print("  [2] Kirim Tiket ke Bob (RESET otomatis)")
    print("  [3] Kirim Pesan AES ke peer")
    print("  [4] Tampilkan Session Key saat ini")
    print("  [5] Ubah Master Key (otomatis sinkron ke KDC)")
    print("  [6] Keluar")
    print("=" * 60)


def menu_loop():
    while True:
        print_menu()
        choice = input("Pilih: ").strip()

        if choice == "1" and state.identity == "Alice":
            if state.session_key is not None:
                print("[Alice] Session key sudah ada. Restart kalau mau minta baru.")
                continue
            tiket = alice_request_session_key()
            if tiket:
                print("[Alice] Tiket tersimpan - pilih menu [2] untuk kirim ke Bob")

        elif choice == "2" and state.identity == "Alice":
            if state.session_key is None:
                print("[Alice] Minta session key dulu (menu [1])")
                continue
            if not state.tiket:
                print("[Alice] Tiket tidak ditemukan - minta ulang (menu [1])")
                continue
            alice_send_tiket_to_bob(state.tiket)

        elif choice == "3":
            if not state.is_ready():
                print(f"[{state.identity}] Belum siap. Selesaikan handshake dulu.")
                continue
            msg = input("Pesan: ").strip()
            if not msg:
                continue
            try:
                ct_hex = aes_encrypt_text(msg, state.session_key)
                print(f"[{state.identity}] Ciphertext AES: {ct_hex}")
                send_to_peer(ct_hex)
                print(f"[{state.identity}] Terkirim")
            except Exception as e:
                print(f"[{state.identity}] Gagal kirim: {e}")

        elif choice == "4":
            if state.session_key:
                print(f"Session Key (ASCII): {state.session_key!r}")
                print(f"Session Key (Hex)  : {state.session_key.encode().hex().upper()}")
                print(f"Handshake          : {'selesai' if state.handshake_done else 'belum'}")
            else:
                print("Belum ada session key.")

        elif choice == "5":
            new_key = input(f"Master key baru (8 char ASCII, sekarang {state.master_key_ascii!r}): ").strip()
            if len(new_key) != 8:
                print("Harus tepat 8 karakter.")
                continue

            old_key = state.master_key_ascii
            state.master_key_ascii = new_key
            print(f"Master key lokal diubah: {old_key!r} -> {new_key!r}")
            print(f"[{state.identity}] Sinkronisasi ke KDC...")

            if sync_key_to_kdc(new_key):
                print(f"[{state.identity}] KDC sudah update key")
                state.session_key = None
                state.tiket = None
                state.n2 = None
                state.handshake_done = False
                print(f"[{state.identity}] Session lama di-reset. Minta session baru (menu [1] untuk Alice)")
            else:
                state.master_key_ascii = old_key
                print(f"[{state.identity}] Gagal sinkron - key dikembalikan ke {old_key!r}")

        elif choice == "6":
            print(f"[{state.identity}] Keluar.")
            sys.exit(0)

        else:
            print("Pilihan tidak valid.")


# ============================================================
# MAIN
# ============================================================
def main():
    if len(sys.argv) < 2 or sys.argv[1].lower() not in ("alice", "bob"):
        print("Usage: python node.py [alice|bob]")
        sys.exit(1)

    identity = sys.argv[1].capitalize()
    state.identity = identity

    if identity == "Alice":
        state.my_ip = ALICE_IP
        state.my_port = ALICE_PORT
        state.peer_ip = BOB_IP
        state.peer_port = BOB_PORT
        state.master_key_ascii = KA
    else:
        state.my_ip = BOB_IP
        state.my_port = BOB_PORT
        state.peer_ip = ALICE_IP
        state.peer_port = ALICE_PORT
        state.master_key_ascii = KB

    print("=" * 60)
    print(f"  NODE - {identity}")
    print("=" * 60)
    print(f"  My IP     : {state.my_ip}:{state.my_port}")
    print(f"  Peer IP   : {state.peer_ip}:{state.peer_port}")
    print(f"  Master Key: {state.master_key_ascii!r}")
    print("=" * 60)

    threading.Thread(target=listener, daemon=True).start()

    try:
        menu_loop()
    except KeyboardInterrupt:
        print(f"\n[{identity}] Shutdown.")
        sys.exit(0)


if __name__ == "__main__":
    main()