# Practical 10: Docker Containerization of the Iris ML Application

## 1. Objective

To containerize the Iris machine learning application using Docker, package a trained model, expose HTTP endpoints for predictions, and verify the application using health checks.

## 2. Tools and Technologies

- Docker Engine with Linux container engine
- Python 3.11
- Scikit-learn
- Pandas
- NumPy
- Joblib
- Python HTTP Server
- Git and GitHub

## 3. Implementation

The application uses a multi-stage Dockerfile.

### Builder Stage

- Installs the pinned Python dependencies.
- Reads the `data/processed/iris_features.csv` dataset.
- Trains a Random Forest classifier.
- Saves the trained model and label encoder.

### Runtime Stage

- Copies the installed Python packages and trained model from the builder stage.
- Copies `src/serve.py`.
- Exposes port 8000.
- Configures a Docker health check using the `/health` endpoint.

## 4. HTTP Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /health | Checks application health |
| POST | /predict | Predicts an Iris species |

The prediction request contains four original Iris measurements and three engineered numeric features: `sepal_area`, `petal_area`, and `sepal_to_petal_length_ratio`.

## 5. Build and Run

### Build Docker Image

```bash
sudo docker build -t iris-classifier:v1 .
```

### Start Container

```bash
sudo docker run -d --name iris-classifier-container -p 8000:8000 iris-classifier:v1
```

### Check Container Status

```bash
sudo docker ps
```

## 6. Testing and Results

### Health Check

Request:

```bash
curl http://localhost:8000/health
```

Observed response:

```json
{"status": "healthy"}
```

### Valid Prediction

For the sample Iris measurements, the application returned:

```json
{"prediction": "setosa", "probabilities": [1.0, 0.0, 0.0]}
```

### Invalid Request

A request missing required features returned HTTP 400 Bad Request and identified the missing fields.

### Docker Image Inspection

The Docker image was successfully created with the tag `iris-classifier:v1`.

The reported Docker disk usage was approximately 680 MB, with a content size of 155 MB.

The Docker history command confirmed the multi-stage runtime image layers.

### Health Status

The container health inspection returned:

```text
healthy
```

## 7. Conclusion

The Iris ML application was successfully containerized using a multi-stage Docker build. The model was trained during the image build, the HTTP server returned a valid prediction, and invalid input was handled with an appropriate client error. The health endpoint responded successfully.

## 8. Cleanup

Stop the running container:

```bash
sudo docker stop iris-classifier-container
```

Remove the container:

```bash
sudo docker rm iris-classifier-container
```

The Docker image can be retained locally for future use.