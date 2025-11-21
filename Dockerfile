# 軽量な Python 3.11 イメージを使用
FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なライブラリを直接インストール
RUN pip install --no-cache-dir Flask==2.2.2 mysql-connector-python==8.0.31

# アプリケーションコードをコピー
COPY . .

# Flask のポートを公開
EXPOSE 5000

# アプリを起動
CMD ["python", "app.py"]