# LPL-Demo

A demonstration project showcasing integrations between JIRA, MySQL, Docker, and Model Context Protocol (MCP).

## Project Structure

```
LPL-Demo/
├── docker-compose.yaml        # Multi-service Docker setup (JIRA, MySQL, Postgres)
├── requirements.txt           # Python dependencies
├── package.json               # Node.js dependencies
├── env.example                # Example environment variables
├── README.md                  # This file
└── ...                        # Other project files
```

## Getting Started

### Prerequisites

- Python (v3.11)
- Docker
- Access to a JIRA instance (local or cloud)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/vsusheel/LPL-Demo.git
   cd LPL-Demo
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

### Running with Docker Compose

Start JIRA, MySQL, and Postgres services:
```bash
docker-compose up -d
```

### JIRA & MySQL Integration Workflow

- **Query JIRA ticket status using MCP**
- **Sync ticket data to MySQL**
- **Update or query tickets from MySQL**

#### Example: Sync JIRA Ticket to MySQL

1. Query JIRA ticket status (using MCP or API)
2. Insert or update the ticket in MySQL:
   ```sql
   INSERT INTO jira_table (issue_key, summary, description, priority, status, assignee, reporter, created, updated)
   VALUES ('DEMO-1', 'Demo Ticket', 'Created via UI', 'Medium', 'In Progress', 'Unassigned', 'user@email.com', '2025-07-13 23:01:05', '2025-07-13 23:04:31')
   ON DUPLICATE KEY UPDATE summary=VALUES(summary), description=VALUES(description), priority=VALUES(priority), status=VALUES(status), assignee=VALUES(assignee), reporter=VALUES(reporter), created=VALUES(created), updated=VALUES(updated);
   ```

#### Query Tickets from MySQL
```bash
docker run -it --rm mysql:8.0 mysql -h<mysql_host> -P3306 -u<user> -p<password> mydb -e "SELECT * FROM jira_table;"
```

## Inventory API

### Endpoints

#### `GET /inventory`
- **Description:** Search inventory items.
- **Query Parameters:**
  - `searchString` (optional, string): Search by name.
  - `skip` (optional, int): Pagination offset.
  - `limit` (optional, int, max 50): Pagination limit.
- **Response:**
  - `200 OK`: List of inventory items (see schema below).

#### `POST /inventory`
- **Description:** Add a new inventory item.
- **Request Body:**
  - JSON object matching the `InventoryItem` schema (see below).
- **Responses:**
  - `201 Created`: Item added successfully.
  - `409 Conflict`: Item with the same `id` already exists.

### InventoryItem Schema
```json
{
  "id": "d290f1ee-6c54-4b01-90e6-d701748f0851", // string, uuid, required
  "name": "Widget Adapter",                  // string, required
  "releaseDate": "2016-08-29T09:12:33.001Z", // string, date-time, required
  "manufacturer": {                           // Manufacturer object, required
    "name": "ACME Corporation",              // string, required
    "homePage": "https://www.acme-corp.com", // string, url, optional
    "phone": "408-867-5309"                  // string, optional
  }
}
```

### Example Usage

**Add an item:**
```bash
curl -X POST "http://localhost:8000/inventory" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
    "name": "Widget Adapter",
    "releaseDate": "2016-08-29T09:12:33.001Z",
    "manufacturer": {
      "name": "ACME Corporation",
      "homePage": "https://www.acme-corp.com",
      "phone": "408-867-5309"
    }
  }'
```

**Get all items:**
```bash
curl "http://localhost:8000/inventory"
```

## User Management API

### Endpoints

#### `POST /useradd`
- **Description:** Add a new user.
- **Request Body:**
  - JSON object with:
    - `username` (string, required)
    - `password` (string, required)
    - `email` (string, optional)
- **Responses:**
  - `201 Created`: User created successfully.
  - `400 Bad Request`: User already exists.

**Example:**
```json
{
  "username": "alice",
  "password": "secret",
  "email": "alice@example.com"
}
```

#### `DELETE /useradd`
- **Description:** Delete a user by username.
- **Query Parameter:**
  - `username` (string, required)
- **Responses:**
  - `204 No Content`: User deleted successfully.
  - `404 Not Found`: User not found.

---

**Note:** User storage is in-memory and resets on app restart. For production, integrate with a persistent database.

## Docker Compose Services

- `webservice`: Runs the FastAPI app on port 8000.
- `test-eval`: Runs all tests using pytest for live feedback.

## Features

- [x] JIRA ticket status query via MCP
- [x] Sync JIRA tickets to MySQL
- [x] Docker Compose for multi-service orchestration
- [ ] Automated ticket sync scripts
- [ ] Web dashboard (coming soon)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

- Project Link: [https://github.com/vsusheel/LPL-Demo](https://github.com/vsusheel/LPL-Demo) 

## Testing & CI/CD

### Running Tests Locally

- **Python tests:**
  ```bash
  pytest
  ```

### CI/CD Process

- On every push or pull request, GitHub Actions will:
  1. Set up Python environment
  2. Install dependencies
  3. Run `pytest`
  4. Report test results in the PR/build logs

You can add your test files in the `tests/` directory. 

Would you like me to run this command for you now?