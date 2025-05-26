# Mixify - Spotify Playlist Manager

Mixify is a Flask-based web application that generates personalized Spotify playlists by leveraging the Spotify Web API through the Spotipy library. Designed to enhance your music experience, Mixify allows users to create dynamic playlists based on their listening habits.

## Features
- **Spotify Integration**: Authenticate users via Spotify's OAuth and access their listening data.

- **List User Playlists**: View all playlists associated with your Spotify account.
- **Create Playlists**: Easily create new playlists and add songs to them.
- **Generate Daily Mixes**: Automatically generate daily mixes based on your listening history and preferences.

## Technologies Used
- Backend: Python, Flask
- API Integration: Spotipy (Spotify Web API)
- Deployment: GitLab CI/CD (docker compose, helm)
- Containerization: Docker (optional)


# Deployment methods
- Python flask app
- Docker compose
- Helm chart

## Python flask app
### Prerequisites

- Python 3.6 or higher
- Spotify Developer Account (for API credentials)

### Steps

1. Clone the repository:

    ```bash
    git clone https://gitlab.timych.ru/timych/mixify.git
    cd mixify/services/web
    ```
2. Create a Virtual Environment:
     ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Set Environment Variables:

   Create a .env file(or copy from .env.example) with the following content:
   ```ini
    SPOTIPY_CLIENT_ID=your_spotify_client_id
    SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
    SPOTIPY_REDIRECT_URI=http://localhost:5000/callback
    FLASK_APP=app.py
    FLASK_ENV=development
    FLASK_RUN_HOST=0.0.0.0
   ```

5. Run the application:

    ```
    flask run
    ```

6. Access the application at [http://localhost:5000](http://localhost:5000) in your web browser.


## Docker compose
### Prerequisites
- Docker installed on host
- Spotify Developer Account (for API credentials)

### Steps

1. Clone the repository:

    ```bash
    git clone https://gitlab.timych.ru/timych/mixify.git
    cd mixify
    ```
2. Set Environment Variables:

   Edit a mixify.env file(oput your API credentials) with the following content:
   ```ini
    SPOTIPY_CLIENT_ID=your_spotify_client_id
    SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
    SPOTIPY_REDIRECT_URI=http://localhost:5000/callback
   ```
3. Modify docker-compose.yaml if needed(i.g. port, nginx config)
3. Run the application:

    ```
    docker compose up
    ```

6. Access the application at [http://localhost:8080](http://localhost:8080) in your web browser.


## Helm
### Prerequisites
- Access to K8S cluster
- Spotify Developer Account (for API credentials)

### Steps

1. Add Helm repository:

    ```bash
    helm repo add mixify https://pages.timych.ru/timych/mixify
    helm repo update mixify
    ```
2. Set values for chart:

   Edit a mixify.env file(put your API credentials) with the following content:
   ```yaml
    replicaCount: 1

    mixifyImage:
      repository: timych84/mixify
      tag: "latest"
      pullPolicy: IfNotPresent

    mixifySpec:
      targetPort: 5000
      clientid: default_client_id
      clientsecret: default_client_secret
      redirecturi: 'http://your-spotify-redirect.url'
      url: your-spotify-redirect.url


    service:
      name: multitool-service
      type: ClusterIP
      httpPort: 9002
      httpsPort: 9443
   ```

3. Install the application:
    ```
    helm upgrade --install  mixify-test mixify/mixify -f charts/mixify/values.yaml --namespace mixify --create-namespace
    ```

6. Access the application by mixifySpec.url(from values.yaml) in your web browser.

helm upgrade  --install  -f charts/mixify/values.yaml  mixify-local ./charts/mixify --namespace mixify-test --create-namespace

## Usage

1. Log in with your Spotify account credentials.
2. Explore your existing playlists or create new ones.
3. Generate daily mixes based on your listening history.
4. Enjoy your personalized playlists!

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

Special thanks to the [Spotify API](https://developer.spotify.com/documentation/web-api/) for providing the tools to interact with the Spotify platform.
