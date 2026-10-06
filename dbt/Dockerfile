FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 DBT_PROFILES_DIR=/usr/app/dbt
WORKDIR /usr/app/dbt
RUN apt-get update && apt-get install -y --no-install-recommends gcc g++ build-essential curl ca-certificates krb5-user libkrb5-dev inotify-tools && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir "dbt-core==1.3.8" "dbt-spark-livy==1.3.1"
COPY dbt-dev-entrypoint.sh /usr/local/bin/dbt-dev-entrypoint.sh
RUN chmod +x /usr/local/bin/dbt-dev-entrypoint.sh
COPY . /usr/app/dbt
ENTRYPOINT ["dbt"]
