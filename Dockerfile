# Use a lightweight Python base image
FROM python:3.12-slim

# Prevent Python from writing pyc files and keep stdout unbuffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install uv (using pip is fine here, or you can copy the binary from astral's image)
RUN pip install --no-cache-dir uv

# Copy ONLY the dependency files first.
# This takes advantage of Docker's layer caching so you don't reinstall
# dependencies every time you change a line of code in your Python scripts.
COPY pyproject.toml uv.lock ./

# Install the dependencies into the system environment.
# Since containers are already isolated environments, we use --system
# to bypass the creation of a virtual environment.
RUN uv pip install --system -r pyproject.toml

# Copy the rest of your application code
# (assets, data, models, src, main.py)
COPY . .

# Specify the command to run your application
CMD ["python", "main.py"]
