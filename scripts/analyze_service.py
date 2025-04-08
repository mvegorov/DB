import os
import psycopg2
import statistics
import re
from datetime import datetime


def execute_explain_analyze(cursor, query):
    try:
        cursor.execute(f"EXPLAIN ANALYZE {query}")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error executing query: {query}. Error: {e}")
        return []


def parse(result):
    cost_pattern = re.compile(r' * \(cost=\d+\.\d+..(\d+\.\d+) rows=\d+ width=\d+\)')
    time_pattern = re.compile(r' * \(actual time=\d+\.\d+..(\d+\.\d+) rows=\d+ loops=\d+\)')

    cost_match = cost_pattern.search(str(result))
    time_match = time_pattern.search(str(result))

    cost_end = float(cost_match.group(1)) if cost_match else None
    time_end = float(time_match.group(1)) if time_match else None

    return {'cost': cost_end, 'time': time_end}


def log_results(query, cost, times, file_path):
    best = min(times)
    worst = max(times)
    avg = statistics.mean(times)

    with open(file_path, 'a') as file:
        file.write(f"Query: {query}\n")
        file.write(f"Cost: {cost}\n")
        file.write(f"Best Time: {best}\n")
        file.write(f"Worst Time: {worst}\n")
        file.write(f"Average Time: {avg}\n")
        file.write("=" * 40 + "\n")


def main():
    num_attempts = int(os.getenv("NUM_ATTEMPTS", 5))
    queries = [
        "SELECT * FROM \"User\";",
        "SELECT * FROM users_verified;",
        "SELECT * FROM \"Word\" WHERE subcategory_id = 1;"
    ]

    log_dir = "../logs"
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"{log_dir}/query_performance_{timestamp}.log"

    try:
        with psycopg2.connect(
            dbname=os.getenv("DB"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            host="db",
            port="5432"
        ) as connection:
            with connection.cursor() as cursor:
                for query in queries:
                    cost = None
                    times = []
                    for _ in range(num_attempts):
                        result = execute_explain_analyze(cursor, query)
                        parsed_result = parse(result)
                        if parsed_result['time'] is not None:
                            times.append(parsed_result['time'])
                        if parsed_result['cost'] is not None:
                            cost = parsed_result['cost']

                    if cost:
                        log_results(query, cost, times, log_file)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
