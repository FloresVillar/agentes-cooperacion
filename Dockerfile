FROM ros:jazzy
RUN apt-get update && apt-get install -y python3-pip bc curl && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r  requirements.txt --break-system-packages
COPY ./app ./app
COPY ./agentes_cooperacion ./agentes_cooperacion
RUN . /opt/ros/jazzy/setup.sh && \
    cd /app/agentes_cooperacion && \
    chmod +x src/agente_pkg/agente_pkg/mover_agente.py && \
    colcon build --packages-select agente_pkg
RUN echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc && \
    echo "source /app/agentes_cooperacion/install/setup.bash" >> ~/.bashrc
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
CMD ["bash", "-c", "source /opt/ros/jazzy/setup.bash && python3 -m app.main"]
