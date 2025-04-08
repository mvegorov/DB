import os
import subprocess
import time
from datetime import datetime


BACKUP_DIR = os.getenv("BACKUP_DIR")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
N_HOURS = int(os.getenv("N_HOURS"))
M_BACKUPS = int(os.getenv("M_BACKUPS"))


def create_backup():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"/backups/MyEnglishVocabulary_backup_{timestamp}.sql"

    command = [
        "pg_dump",
        "-h", DB_HOST,
        "-U", DB_USER,
        "-d", DB_NAME,
        "-f", backup_file
    ]

    # Запускаем pg_dump с передачей пароля через env
    result = subprocess.run(command, env={"PGPASSWORD": os.getenv("PGPASSWORD")}, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"Бекап успешно создан: {backup_file}")
    else:
        print(f"Ошибка при создании бекапа: {result.stderr}")


def delete_old_backups():
    backups = sorted(
        [f for f in os.listdir(f"/{BACKUP_DIR}") if f.startswith(f"{DB_NAME}_backup_")],
        reverse=True
    )

    # Если количество бэкапов больше чем M_BACKUPS, удаляем старые
    if len(backups) > M_BACKUPS:
        for old_backup in backups[M_BACKUPS:]:
            os.remove(f"/{BACKUP_DIR}/{old_backup}")
            print(f"Удалён старый бэкап: {old_backup}")


def main():
    while True:
        try:
            create_backup()

            delete_old_backups()

            print(f"Ожидание {N_HOURS} часов до следующего бэкапа...")
            time.sleep(N_HOURS * 3600)
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            break


if __name__ == "__main__":
    main()
