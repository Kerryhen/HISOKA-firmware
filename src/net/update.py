import net.ugit

def update_firmware():
    try:
        ugit.update_all()
        print("Atualização concluída.")
        return True
    except Exception as e:
        print("Erro na atualização:", e)
        return False
