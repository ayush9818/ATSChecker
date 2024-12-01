FROM --platform=linux/x86-64 python:3.11-slim
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application source code
COPY . .

EXPOSE 8001

# Set the command to run the main script
CMD ["streamlit", "run", "main.py", "--server.fileWatcherType=none", "--server.port=8001", "--server.address", "0.0.0.0"]
