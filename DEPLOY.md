# Deployment Guide - WhatsApp AI Agent

This project is fully dockerized and ready for deployment on any server (Ubuntu/Debian recommended) with Docker installed.

## Prerequisites on Server
1.  **Docker**: `sudo apt install docker.io`
2.  **Docker Compose**: `sudo apt install docker-compose`
3.  **Git**: `sudo apt install git`

## Deployment Steps

### Option 1: Git-Based Deployment (Recommended)
This method builds the images directly on your server, ensuring the latest code is always running.

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/balacot/whatai.git
    cd whatai
    ```

2.  **Configure Environment**:
    Create the `.env` file in `backend/.env` with your production keys:
    ```bash
    nano backend/.env
    # Paste your GOOGLE_API_KEY, WHATSAPP credentials, etc.
    ```

3.  **Start the Application**:
    ```bash
    docker-compose up --build -d
    ```
    - `--build`: Rebuilds images to include latest code.
    - `-d`: Runs in detached mode (background).

### Option 2: Docker Hub Deployment
If you prefer to build locally and push to Docker Hub.

1.  **Build and Push (Local Machine)**:
    ```bash
    docker-compose build
    docker push balacotes/whatai:backend
    docker push balacotes/whatai:frontend
    ```

2.  **Pull and Run (Server)**:
    ```bash
    # Copy docker-compose.yml to server
    docker-compose pull
    docker-compose up -d
    ```

## Updating the App
To deploy changes:
1.  **Push changes** to git from your local machine.
2.  **On the server**:
    ```bash
    git pull
    docker-compose up --build -d
    ```
