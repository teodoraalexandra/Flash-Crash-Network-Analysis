FROM python:3.11-slim-bullseye

# Install OpenJDK 11 (JDK includes javac) and bash
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-11-jdk \
    bash \
 && rm -rf /var/lib/apt/lists/*

# Detect JAVA_HOME dynamically
ENV JAVA_HOME=/usr/lib/jvm/default-java
RUN if command -v javac >/dev/null 2>&1; then \
      export JBIN="$(readlink -f $(command -v javac))"; \
      export JHOME="$(dirname "$(dirname "$JBIN" )")"; \
      echo "Detected JAVA_HOME: $JHOME"; \
      ln -sfn "$JHOME" "$JAVA_HOME"; \
    else \
      echo "javac not found after install!" && exit 1; \
    fi
ENV PATH="${JAVA_HOME}/bin:${PATH}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential python3-dev bash \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app/

RUN python -m pip install --upgrade pip setuptools wheel \
 && python -m pip install --no-cache-dir "numpy==1.23.4" cython \
 && pip install --no-cache-dir -r requirements.txt --verbose

COPY . /app/
RUN chmod +x script.sh
