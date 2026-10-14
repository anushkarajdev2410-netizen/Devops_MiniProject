The application initializes its SQLite schema automatically when it starts.
The local database file is configured by the DATABASE environment variable.
The Kubernetes starter manifest uses a temporary database path inside each pod.
For durable shared production data, use a persistent volume or managed database;
the assignment deployment demonstrates application and DevOps orchestration.
